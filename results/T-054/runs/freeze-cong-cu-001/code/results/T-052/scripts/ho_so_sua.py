"""Sinh bản giao thức/hồ sơ ứng viên sau phản biện. Không đọc dữ liệu test."""
import copy
import subprocess
from pathlib import Path

from common import OUT, ROOT, digest, pin, read, save
from m1 import runner as m1runner
from p3 import runner
from p7_entry_v2 import fingerprint


def ref(path):
    return {'path': str(path), 'sha256': digest(path), 'bytes': (ROOT / path).stat().st_size}


def configurations(base):
    out = {}
    for arm, changes in [('M1', {}), ('bo-E1', {'E1': 'tat'}), ('bo-E2', {'E2': 'tat'}),
                         ('bo-E5', {'E5': False}), ('C-a0', {'E1': 'tat', 'E2': 'tat', 'E5': False}),
                         ('C-a1', {'E2': 'tat', 'E5': False}), ('T12-on', {'T12': True})]:
        conf = dict(copy.deepcopy(base), config_id=arm)
        conf['bat_tat'].update(changes)
        if arm in ('C-a0', 'C-a1'):
            conf.update(chay_M1=True, doi_chung=arm)
        m1runner._params(conf, {})
        out[arm] = {'config': conf, 'sha256': fingerprint(conf)}
    return out


def environment_refs():
    environments = {}
    for name, executable in runner.ENVS.items():
        package_names = ('numpy', 'scipy', 'pandas', 'networkx', 'pyarrow', 'psutil', 'drain3')
        command = ('import sys,json,importlib.metadata as m; '
                   'ds={d.metadata.get("Name", "").lower():d.version for d in m.distributions()}; '
                   f'print(json.dumps([sys.version, {{n:ds.get(n) for n in {package_names!r}}}]))')
        import json
        interpreter, packages = json.loads(subprocess.check_output([executable, '-B', '-c', command], text=True))
        environments[name] = {'python_executable': executable, 'python': interpreter, 'packages': packages,
                              'PYTHONPATH': runner.PYTHONPATH[name], 'PYTHONHASHSEED': 0}
    external = {}
    for source in sorted(set(runner.PYTHONPATH['main']) - {str(ROOT / 'src')}):
        p = Path(source)
        git = subprocess.run(['git', '-C', source, 'rev-parse', '--show-toplevel', 'HEAD'], capture_output=True, text=True)
        if git.returncode == 0 and Path(git.stdout.splitlines()[0]).resolve() == p.resolve():
            diff = subprocess.check_output(['git', '-C', source, 'status', '--porcelain', '--untracked-files=no'], text=True)
            external[source] = {'revision': git.stdout.splitlines()[-1], 'tracked_dirty': bool(diff.strip())}
        else:
            external[source] = {'status': 'PINNED_FILES_REVISION_OPEN',
                                'py_files': {x.relative_to(p).as_posix(): digest(x) for x in sorted(p.rglob('*.py'))}}
    return {'environments': environments, 'external_code': external}


def main():
    old = read(OUT / 'giao-thuc-p7-a.json')
    cohort_path = 'results/T-052/ke-hoach-tap-test.json'
    cohort = read(cohort_path)
    protocol = dict(old, status='CANDIDATE_FOR_G3_REVIEW_NOT_LOCKED')
    protocol['cohorts_source'] = ref(cohort_path)
    protocol['configurations'] = configurations(old['effective_config'])
    protocol['entrypoint'] = 'results/T-052/scripts/p7_entry_v2.py'
    protocol['hypotheses'] = {
        'TT_primary': 'MRR M1−TORAI B: biên không thua 0,05, 60 ca theo E-04.',
        'OB_secondary': 'Hit@5 kỳ vọng M1−SimpleRCA M4 trên 34 ca, kiểm có điều kiện về hoán đổi dấu theo ô.',
        'others': 'Cỡ chênh/CI theo bộ và vế; không chọn lại nền theo test.'}
    protocol['interpretation'] = [
        {'when': 'TT CI toàn trên 0', 'report': 'Hơn TORAI B theo CI danh nghĩa, kèm giả định và số ô.'},
        {'when': 'TT CI toàn dưới 0 nhưng lo > −0,05', 'report': 'Đạt E-04 theo công thức dù kém TORAI B theo CI.'},
        {'when': 'TT CI chứa 0', 'report': 'Chưa phân biệt hơn/kém; đọc E-04 riêng theo cận dưới.'},
        {'when': 'TT lo ≤ −0,05', 'report': protocol['A4']['failure_statement']},
        {'when': 'TT CI suy biến', 'report': 'Ghi trong cùng câu và số đếm; giữ mức OB 0,025.'},
        {'when': 'OB p vượt mức, chênh dương', 'report': 'Chưa phân xử; báo cỡ chênh/CI, ô hữu hiệu và giới hạn M4.'},
        {'when': 'M1 hơn baseline nhưng thua C-a hoặc C-d2', 'report': 'Giới hạn theo cặp, không khẳng định lợi ích quan hệ chung.'},
        {'when': 'Khác dấu theo nhóm/world', 'report': 'Báo tách và điều kiện, chỉ P quyết A4.'}]
    protocol['exposure'] = {'source': ref('results/T-021/goi-g1.md'),
        'counts': {k: {x: row[x] for x in ('n', 'TX', 'symptom_probe_metadata')} for k, row in cohort['cohorts'].items()},
        'limits': 'TT và OB test TX1. OB 34/34 từng dò triệu chứng; ca dev/test liền kề, file có thể dùng chung, chỉ cắt đoạn đã khai. RE3 TX0 là chưa tìm thấy nguồn tiếp xúc; cùng hệ OB với Nezha và cùng bộ công cụ với RE2-TT.'}
    protocol['position_N'] = {'code': ref('results/T-052/scripts/vung_ce.py'),
        'definition': 'Dùng K-R0 giữ span bọc; tập owner từ operation có n_N>0, cạnh G_N, cùng alias và end<t. Phân nhóm vắng/bậc 0/nguồn/lá/giữa/hub theo Q-60; p75 tổng bậc toàn nút, p90 độ nhạy. Ghép root sau seal, không dùng A.'}
    t12_plan = 'results/T-051/t12-001/plan.json'
    m51 = read('results/T-051/manifest.json')
    pin(t12_plan, m51['outputs'][t12_plan])
    protocol['snapshots'] = {k: pin(path, {'sha256': sha}) for k, (path, sha) in read(t12_plan)['source_static'].items()}
    protocol['C_e'] = {'dataset': 'RE2-TT', 'arm': 'M1', 'max_cases': 60,
        'window': 't′=t−300, cần N′ tới t−600. Dùng chứng nhận hỗ trợ lịch sử/A0 từ quản lý dữ liệu trước chấm.',
        'if_history_unsupported': 'INSUFFICIENT_EVIDENCE riêng, báo ở mẫu số khai; không chuyển thành V0 NO_CAUSE hoặc điểm 0 trong bảng miền hỗ trợ.',
        'if_provenance_unknown': 'Dừng vế C-e trước chấm, phân loại/ghi lý do.',
        'metrics': 'top mass/hòa/returned/O/U/V0/N1 và RR root tương lai ghép sau; báo cặp hợp lệ. Ngoài A4.'}
    protocol['A4'].update({'driver': 'results/T-052/scripts/a4_v2.py',
        'TT_sign_at_zero': 'Chỉ độ nhạy, đảo dấu theo ô quanh 0. Không thay cận dưới bootstrap của E-04.',
        'case_permutation': {'status': 'CANDIDATE_NOT_LOCKED', 'rule': 'Hai phía, đổi dấu từng ca, 10000 mẫu, seed 20261005, cộng 1; hạn chế phụ thuộc cùng ô.'},
        'error_excluded': {'required_by': ['Q-211(6)', 'WHY-06'], 'status': 'IMPLEMENTATION_CANDIDATE_NOT_LOCKED',
            'proposed': 'ERROR/TIMEOUT phương pháp ở bất kỳ vế/seed nào loại nguyên cặp trong bản nhạy. Giữ NO_EVIDENCE/UNSUPPORTED. Giữ đủ seed hoặc bỏ cả cặp; bảng chính vẫn đủ mẫu và lỗi trượt.'}})
    protocol['test_access_log'] = {'required_by': ['Q-211(7)', 'WHY-06'],
        'rule': 'Ghi mỗi lần xem test trước mở ở LOG task P7: người/quyền, UTC, cohort/mục đích/manifest, bước và có dùng để thiết kế không; sau lượt thêm kết quả và vùng đã xem. Tách đã xem và đã dùng để thiết kế.'}
    protocol['runtime_metadata'] = {'protocol_and_runtime_sha256': 'Từ hai biên nhận khóa/cấp quyền độc lập, không từ file tự khai.',
        'member_check': 'Toàn bộ test-<10 hex> và member hash khớp chính xác cohort ngoài manifest runtime; U theo kế hoạch G1.',
        'roots': {'RE2-TT': 'data/locked/rcaeval-re2tt-60', 'Nezha-OB': 'data/ngoai-rcaeval/nezha/online-boutique/rca_data'},
        'private_map': 'Chốt trong SPEC P7; ràng buộc t/t_ns, file, byte/hash và trạng thái hỗ trợ C-e từng ca trước cấp biên nhận runtime. Runner quản lý locator, adapter khoa học nhận cửa sổ đã cắt.'}
    protocol['fixture'] = 'results/T-052/runs/trien-khai-001/kiem-sua-002/summary.json'
    protocol['open_before_execution'] += [
        'F3 chạy một ca dev TT và một ca dev OB qua đúng v2, khớp input/window/status/nhóm hòa với nguồn đã ghim.',
        'Minh chốt công thức bản nhạy loại lỗi và phép hoán vị ca ứng viên cùng giao thức.',
        'Chốt môi trường và toàn bộ revision, driver P7, xác nhận nhánh T12/C-e cùng ngân sách; fixture không là parity khoa học.' ]
    folders = ['src/m1', 'src/m1_danh_gia', 'src/p3', 'src/torai', 'src/simplerca', 'src/microrank',
               'src/circa_kien_truc', 'results/T-052/scripts']
    protocol['source_code'] = {p.relative_to(ROOT).as_posix(): digest(p) for folder in folders
                               for p in sorted((ROOT / folder).rglob('*.py'))}
    protocol['runtime_dependencies'] = environment_refs()
    save(OUT / 'giao-thuc-p7-a-002.json', protocol)


if __name__ == '__main__':
    main()
