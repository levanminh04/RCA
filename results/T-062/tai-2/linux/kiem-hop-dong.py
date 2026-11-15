"""Offline checks for controller error/launch contracts; no traffic or secret reads."""
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import tai_linux as ctl


class Contract(unittest.TestCase):
    def launch(self, step=0, multiplier=1, remaining=1800):
        args = type('Args', (), dict(tag='contract-only', seconds=180, buoc_tai=step, multiplier=multiplier))()
        commands, scripts, pools = [], [], []

        def ssh(machine, command, data=None, **kwargs):
            commands.append((machine, command, data))
            return b'test-container-id\n'

        def preflight(count, force):
            pools.append((count, force))
            return {'tokens': {'minRefreshRemaining': remaining}}

        with patch.object(ctl, 'guard'), patch.object(ctl, 'assert_idle'), patch.object(ctl, 'ssh', ssh), \
                patch.object(ctl, 'remote_python', side_effect=lambda machine, code, **kw: scripts.append(code)), \
                patch.object(ctl, 'preflight', preflight):
            value = ctl.start(args, {})
        for code in scripts:
            compile(code, 'remote-prepare', 'exec')
        return commands, scripts, pools, value

    def test_normal_pool_and_multiplier(self):
        commands, scripts, pools, result = self.launch(multiplier=3)
        self.assertEqual(pools, [(20, True)])
        self.assertEqual(result['run']['stepSeconds'], 0)
        self.assertIn('FT_LOAD_MULTIPLIER=3', commands[-1][2].decode())
        self.assertIn('FT_LOAD_STEP_SECONDS=0', commands[-1][2].decode())

    def test_step_pool_and_exact_docker_arguments(self):
        commands, scripts, pools, result = self.launch(step=90, multiplier=3)
        self.assertEqual(pools, [(40, True)])
        text = commands[-1][2].decode()
        for expected in ('--network host', 'FT_LOAD_SECONDS=180', 'FT_LOAD_STEP_SECONDS=90',
                         'FT_LOAD_MULTIPLIER=3', 'FT_JOURNEY_RATE=12',
                         'FT_MOCK_TRANSPORT_URL=http://127.0.0.1:19091',
                         '--out json=/out/raw.json', '--out csv=/out/raw.csv',
                         '--summary-export /out/summary.json', '/scripts/hanh-trinh.js'):
            self.assertIn(expected, text)

    def test_idle_seed_expiry_boundary(self):
        with self.assertRaises(ctl.Failure):
            self.launch(step=90, multiplier=3, remaining=150)
        self.launch(step=90, multiplier=3, remaining=151)

    def test_running_container_refuses_receive(self):
        with patch.object(ctl, 'get', return_value={'Running': True}), patch.object(ctl, 'ssh') as ssh:
            with self.assertRaises(ctl.Failure):
                ctl.receive('contract-only')
            ssh.assert_not_called()

    def test_subprocess_error_never_discloses_output(self):
        result = subprocess.CompletedProcess([], 37, b'PRIVATE_TEST_SENTINEL', b'PRIVATE_TEST_SENTINEL')
        with patch.object(subprocess, 'run', return_value=result):
            with self.assertRaises(ctl.Failure) as cm:
                ctl.run(['false'], label='controlled operation')
        self.assertNotIn('PRIVATE_TEST_SENTINEL', str(cm.exception))
        self.assertIn('37', str(cm.exception))

    def test_stop_flag_blocks_remote_calls(self):
        with patch.object(ctl, 'ROOT') as root, patch.object(ctl, 'run') as run:
            (root / 'STOP').exists.return_value = True
            with self.assertRaises(ctl.Failure):
                ctl.ssh('tai', 'true')
            run.assert_not_called()

    def test_emergency_stop_bypasses_stop_flag(self):
        with patch.object(ctl, 'ssh', return_value=b'') as ssh:
            result = ctl.stop('contract-only')
        self.assertEqual(result['stopped'], [])
        self.assertTrue(ssh.call_args.kwargs['ignore_stop'])

    def test_source_hash_mismatch_fails_before_ssh(self):
        with patch.object(ctl, 'digest', return_value='0' * 64), patch.object(ctl, 'ssh') as ssh:
            with self.assertRaisesRegex(ctl.Failure, 'Source hash mismatch'):
                ctl.verify_sources()
            ssh.assert_not_called()

    def test_receive_hash_mismatch_is_an_error(self):
        with patch.object(ctl, 'ROOT') as root, patch.object(ctl, 'get', return_value={'Running': False}), \
                patch.object(ctl, 'ssh', return_value=b''), patch.object(ctl, 'run', return_value=b''), \
                patch.object(ctl, 'options', return_value=[]), patch.object(ctl, 'digest', return_value='0' * 64):
            destination = root / 'tai-out' / 'contract-only'
            (destination / 'outputs.sha256').read_text.return_value = '1' * 64 + '  raw.json\n'
            (destination / 'raw.json').is_symlink.return_value = False
            (destination / 'raw.json').is_file.return_value = True
            with self.assertRaisesRegex(ctl.Failure, 'Output hash mismatch'):
                ctl.receive('contract-only')

    def test_export_manifest_commits_only_after_all_hashes_succeed(self):
        captured = []

        def capture(machine, command, data=None, **kwargs):
            captured.append(data.decode())
            raise ctl.Failure('captured without SSH')

        with patch.object(ctl, 'get', return_value={'Running': False}), patch.object(ctl, 'ssh', capture):
            with self.assertRaisesRegex(ctl.Failure, 'captured'):
                ctl.receive('contract-only')
        fixture = Path(tempfile.mkdtemp(prefix='atomic-', dir=ctl.ROOT / 'linux-check'))
        for name in ('raw.json', 'hanh-trinh.js', 'inputs.sha256'):
            (fixture / name).write_text('fixture\n')
        script = captured[0].replace('/opt/rca-tai/out/contract-only', str(fixture))
        script = "sudo() { printf '%s\\n' '{}'; }\n" + script
        failed = subprocess.run(['bash', '-s'], input=script.encode(), capture_output=True)
        self.assertNotEqual(failed.returncode, 0)
        self.assertFalse((fixture / 'outputs.sha256').exists())
        self.assertTrue((fixture / 'outputs.sha256.partial').exists())
        (fixture / 'raw.csv').write_text('fixture\n')
        passed = subprocess.run(['bash', '-s'], input=script.encode(), capture_output=True)
        self.assertEqual(passed.returncode, 0)
        self.assertTrue((fixture / 'outputs.sha256').exists())
        self.assertFalse((fixture / 'outputs.sha256.partial').exists())
        before = (fixture / 'outputs.sha256').read_bytes()
        again = subprocess.run(['bash', '-s'], input=script.encode(), capture_output=True)
        self.assertEqual(again.returncode, 0)
        self.assertEqual(before, (fixture / 'outputs.sha256').read_bytes())

    def test_nested_command_leaves_callers_stdin_intact(self):
        code = ("import json,sys,tai_linux as c; got=c.run(['cat']); "
                "remaining=sys.stdin.buffer.read(); print(json.dumps({'got':got.decode(),'remaining':remaining.decode()}))")
        p = subprocess.run([sys.executable, '-c', code], input=b'next caller command\n',
                           cwd=ctl.ROOT, capture_output=True)
        self.assertEqual(p.returncode, 0)
        self.assertEqual(json.loads(p.stdout), {'got': '', 'remaining': 'next caller command\n'})


if __name__ == '__main__':
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream).run(unittest.defaultTestLoader.loadTestsFromTestCase(Contract))
    print(json.dumps({'ok': result.wasSuccessful(), 'tests': result.testsRun,
                      'failures': len(result.failures), 'errors': len(result.errors), 'details': stream.getvalue()}))
    sys.exit(0 if result.wasSuccessful() else 1)
