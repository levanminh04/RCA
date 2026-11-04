"""Driver T-047: chỉ pha 1, từng ca; giữ lượt, thời gian/RAM từ đầu.

Tối đa ba worker cộng một điều phối. Không đọc nhãn dùng chấm.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import shutil
from datetime import datetime, timezone, timedelta
from pathlib import Path

import psutil

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'results/T-047/scripts'),
                str(ROOT / 'results/T-045/scripts')]
import adapter_t047 as ad
import chay_pha1 as old
import soi_ban_ghi
import d5_t047
import tep_pha1
from m1 import runner
from m1_danh_gia import pha2
from p3 import nhan


def now():
    return datetime.now(timezone(timedelta(hours=7))).isoformat(timespec='seconds')


def emit(f, **kw):
    f.write(json.dumps(dict(time=now(), **kw), ensure_ascii=False) + '\n')
    f.flush()


def configs(group):
    mt = json.loads((ROOT / 'results/T-043/ma-tran-thu.json').read_text(encoding='utf-8'))
    return ad.cau_hinh(mt, group)


def worker(a):
    try:
        path = ad.duong_ra(a.run)
    except ValueError:
        print(json.dumps(dict(event='path_guard_diagnostic', raw_run=a.run,
            resolved_run=str(Path(a.run).resolve()), adapter_module=ad.__file__,
            adapter_root=str(ad.ROOT), adapter_out=str(ad.OUT), resolved_out=str(ad.OUT.resolve()),
            cwd=str(Path.cwd()), argv=sys.argv, sys_path=sys.path)),file=sys.stderr,flush=True)
        raise
    path.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    old.tat_ha_toc()
    with (path / 'worker-progress.jsonl').open('x', encoding='utf-8') as f:
        emit(f, event='start_load', dataset=a.dataset, oid=a.oid, rss=psutil.Process().memory_info().rss)
        _, re, nz = old.danh_sach_ca('all', None, 0, False)
        hd = json.loads((ROOT / 'results/T-043/hop-dong.json').read_text(encoding='utf-8'))
        U = json.loads((ROOT / 'results/T-022/mappings/universe-re2tt-dev.json').read_text(encoding='utf-8'))['U']
        moc = nhan.nap_moc(ROOT / 'results/T-022/nhan-dev.json')
        case, t = old.nap_ca(a.dataset, a.oid, re, nz, moc, a.fake, hd, U)
        if a.shuffle is not None:
            old.xao(case, a.shuffle)
        loaded = time.monotonic()
        emit(f, event='loaded', seconds=loaded-start, rss=psutil.Process().memory_info().rss,
             spans=len(case['spans']), metrics=len(case.get('metrics') or []), logs=len(case.get('logs') or []))
        meta = ad.pha1([case], {a.oid: t}, configs(a.group), path / 'phase1')
        _, records = pha2.doc(path / 'phase1', meta['sha256'])
        qt = [soi_ban_ghi.soi(r, False) for r in records]
        ad.ghi(path / 'qt5.json', qt)
        if a.group == 'T1':
            ad.ghi(path / 'd5.json', d5_t047.tinh(case, t, records[0], configs('T1')[0]))
        mi = psutil.Process().memory_info()
        summary = dict(dataset=a.dataset, oid=a.oid, seed=os.getenv('PYTHONHASHSEED'), fake=a.fake,
                       shuffle=a.shuffle, seconds=time.monotonic()-start, load_seconds=loaded-start,
                       phase_seconds=time.monotonic()-loaded, rss=mi.rss, peak_rss=getattr(mi, 'peak_wset', mi.rss),
                       adapter=case.get('chan_doan_adapter'), records=len(records), meta=meta)
        ad.ghi(path / 'summary.json', summary)
        emit(f, event='done', seconds=summary['seconds'], peak_rss=summary['peak_rss'])
    print(json.dumps({k: v for k, v in summary.items() if k not in ('adapter', 'meta')}), flush=True)


def merge(path, jobs, ch):
    # Đọc từng cấu hình để tránh giữ 832 bản ghi lớn cùng lúc.
    source = {}
    for ds, oid in jobs:
        p = path / 'cases' / oid / 'phase1'
        source[oid] = (p, tep_pha1.kiem(p))
    h, count = hashlib.sha256(), 0
    with (path/'ban-ghi.jsonl').open('xb') as out:
        for cid in sorted(c['config_id'] for c in ch):
            for oid in sorted(source):
                p, meta = source[oid]
                found = []
                with (p/meta['tep']).open('rb') as f:
                    for b in f:
                        r = json.loads(b)
                        if r['config_id'] == cid:
                            found.append(runner._json(r).encode()+b'\n')
                if len(found) != 1:
                    raise ValueError('ghép thiếu/trùng bản ghi')
                out.write(found[0]); h.update(found[0]); count += 1
    m = dict(tep='ban-ghi.jsonl', sha256=h.hexdigest(), so_ban_ghi=count,
             so_ca=len(jobs), cau_hinh=sorted(c['config_id'] for c in ch),
             phien_ban=ad.chuoi.PHIEN_BAN_CHE_DO, che_do=ad.MODE)
    ad.ghi(path / 'pha1.json', m)
    tep_pha1.kiem(path)
    return m


def stop_tree(p):
    try:
        root = psutil.Process(p.pid)
        tree = root.children(recursive=True)+[root]
        for proc in reversed(tree):
            try:
                proc.terminate()
            except psutil.NoSuchProcess:
                pass
        _, alive = psutil.wait_procs(tree, timeout=5)
        for proc in alive:
            try:
                proc.kill()
            except psutil.NoSuchProcess:
                pass
    except psutil.NoSuchProcess:
        pass


def control(a):
    path = ad.duong_ra(a.run)
    path.mkdir(parents=True, exist_ok=False)
    jobs, _, _ = old.danh_sach_ca(a.dataset, None, 1 if a.stage == 'pilot' else 0, a.fake)
    ch = configs(a.group)
    reused = []
    reuse_path = getattr(a,'reuse',None)
    if reuse_path:
        source = ad.duong_ra(reuse_path)
        for ds,oid in jobs:
            src = source/'cases'/oid
            if not (src/'summary.json').is_file():
                continue
            m = tep_pha1.kiem(src/'phase1')
            diag = json.loads((src/'summary.json').read_text(encoding='utf-8'))
            requested = json.loads((src/'phase1/tham-so.json').read_text(encoding='utf-8'))['configs']
            if (requested != ch or diag['seed'] != os.getenv('PYTHONHASHSEED') or diag['fake'] != a.fake
                or diag['shuffle'] != a.shuffle or m['so_ca'] != 1 or m['so_ban_ghi'] != len(ch)):
                raise ValueError('không được dùng lại ca khác cấu hình/seed/chế độ')
            dst=path/'cases'/oid
            dst.parent.mkdir(exist_ok=True)
            shutil.copytree(src,dst)
            reused.append((ds,oid))
        ad.ghi(path/'reuse.json',dict(from_run=str(source.relative_to(ROOT)),cases=reused))
    start = time.monotonic()
    budget_path = ad.OUT / 'runs/ngan-sach.json'
    if budget_path.exists():
        budget = json.loads(budget_path.read_text(encoding='utf-8'))
    else:
        # Lượt test cũ và helper 001/002: thời gian thật từ kết quả đã giữ.
        tests = json.loads((ad.OUT / 'runs/ra-soat-003/tests.json').read_text(encoding='utf-8'))
        k = json.loads((ad.OUT / 'kiem-helper.json').read_text(encoding='utf-8'))
        prior = sum(x['seconds'] for x in tests)+sum(x['seconds'] for x in k['new_regression']['attempts'])
        budget = dict(start_epoch=time.time(), prior_seconds=prior, cap_seconds=7*3600,
                      note='Tính bảo thủ mọi thời gian thực kể từ pilot, gồm khoảng chuẩn bị giữa lượt; cộng test bước 0 đã lưu.')
        ad.ghi(budget_path, budget)
    ad.ghi(path / 'command.json', dict(argv=sys.argv, start=now(), seed=os.getenv('PYTHONHASHSEED'),
                                      workers=a.workers, configs=ch, jobs=jobs, budget=budget,
                                      source_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                                     for p in Path(__file__).parent.glob('*.py')}))
    for source_path in Path(__file__).parent.glob('*.py'):
        dst = path/'source'/source_path.name
        dst.parent.mkdir(exist_ok=True)
        dst.write_bytes(source_path.read_bytes())
    all_jobs=list(jobs)
    jobs=[x for x in jobs if x not in reused]
    active, done, failed, i = {}, list(reused), [], 0
    with (path / 'monitor.jsonl').open('x', encoding='utf-8') as f:
        while i < len(jobs) or active:
            used = budget['prior_seconds'] + time.time()-budget['start_epoch']
            if used >= budget['cap_seconds']-15:  # dư cho kết thúc cây, vẫn trong trần thời gian thực
                failed.append(dict(error='budget_cap', seconds=used))
                for p, handles, job in active.values():
                    stop_tree(p)
            while not failed and i < len(jobs) and len(active) < a.workers:
                ds, oid = jobs[i]; i += 1
                pth = path / 'cases' / oid
                (path / 'logs').mkdir(exist_ok=True)
                out = (path / 'logs' / (oid+'.stdout')).open('xb')
                err = (path / 'logs' / (oid+'.stderr')).open('xb')
                cmd = [sys.executable, '-B', str(Path(__file__)), '--worker', '--run', str(pth),
                       '--dataset', ds, '--oid', oid, '--group', a.group]
                if a.fake:
                    cmd.append('--fake')
                if a.shuffle is not None:
                    cmd += ['--shuffle', str(a.shuffle)]
                p = subprocess.Popen(cmd, cwd=ROOT, stdout=out, stderr=err)
                active[oid] = (p, (out, err), (ds, oid))
                emit(f, event='launch', oid=oid, dataset=ds, pid=p.pid, budget_seconds=used)
            rss = {}
            for oid, (p, handles, job) in list(active.items()):
                code = p.poll()
                if code is None:
                    try:
                        proc = psutil.Process(p.pid)
                        # Virtualenv Windows có thể có launcher nhỏ và Python con.
                        tree = [proc] + proc.children(recursive=True)
                        rss[oid] = sum(x.memory_info().rss for x in tree if x.is_running())
                    except psutil.Error:
                        pass
                    continue
                for h in handles:
                    h.close()
                active.pop(oid)
                emit(f, event='finished', oid=oid, exit_code=code, seconds=time.monotonic()-start)
                if code:
                    failed.append(dict(oid=oid, exit_code=code))
                else:
                    done.append(job)
                    print(f'{len(done)}/{len(jobs)} {job[0]} {oid} {time.monotonic()-start:.1f}s', flush=True)
            emit(f, event='sample', rss=rss, rss_total=sum(rss.values()), free_ram=psutil.virtual_memory().available,
                 seconds=time.monotonic()-start, budget_seconds=used)
            if failed and not active:
                break
            if active:
                time.sleep(2)
        result = dict(done=len(done), planned=len(all_jobs), reused=len(reused), failed=failed, seconds=time.monotonic()-start,
                      budget_seconds=budget['prior_seconds']+time.time()-budget['start_epoch'])
        if not failed and len(done) == len(all_jobs):
            result['phase1'] = merge(path, all_jobs, ch)
        ad.ghi(path / 'result.json', result)
        emit(f, event='done', **result)
    if failed:
        raise SystemExit('STOP lỗi worker hoặc ngân sách; giữ mọi lượt')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--run', required=True)
    p.add_argument('--worker', action='store_true')
    p.add_argument('--stage', choices=['pilot', 'full'], default='full')
    p.add_argument('--dataset', default='all')
    p.add_argument('--oid')
    p.add_argument('--group', choices=['T1', 'K'], default='T1')
    p.add_argument('--workers', type=int, choices=[1, 2, 3], default=3)
    p.add_argument('--fake', action='store_true')
    p.add_argument('--shuffle', type=int)
    p.add_argument('--reuse')
    args = p.parse_args()
    worker(args) if args.worker else control(args)
