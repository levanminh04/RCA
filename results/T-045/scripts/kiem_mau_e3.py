"""T-045 phiên 2 — A8 (REVIEW.md T-045 lượt 1, mục C5): nội dung các dòng log mà E3 xếp vào ô "mẫu mới", và tên
mẫu Drain của thực thể vượt lên trên root khi bật E3. Chỉ để tìm nguyên nhân và thiết kế E3 cho chặng sau; không dùng
để chọn lại E3 trên dev. Không chạy lại chuỗi M1: chỉ dựng lại bước Drain của E3 (`m1.e3.hoc_va_dem`, cách khớp (a)
`hoan_toan`, sim_th 0,4, độ sâu 4 như cấu hình K-E3) trên log của ca được chọn, rồi **kiểm tái lập** với bản ghi
K-E3 đã băm (`extra.thong_ke_log.cap_drain` n_N, n_A và `mau_moi` theo thực thể). Ca không tái lập thì không dùng.

Luật khai trước (ghi trước khi xem nội dung; theo C5 của REVIEW.md):
1. Chọn ca: mọi ca có RR của root ở K-E3 thấp hơn ở K-R0 (cặp (R0, E3); nhãn đọc ở pha 2), cộng cửa sổ giả
   (t − 300) của các ca RE2-TT trong số đó.
2. Thực thể xét: (i) cửa sổ thật: thực thể đứng trước hẳn root ở K-E3 mà không đứng trước ở K-R0 ("vượt mới"), kênh
   mạnh nhất thuộc nhóm log; (ii) mọi thực thể có kênh "mẫu mới" có cờ ở P, cả cửa sổ thật và cửa sổ giả.
3. Mỗi dòng A rơi vào "mẫu mới" được phân loại, theo thứ tự:
   (d) hỏng: nội dung rỗng hoặc dưới 3 token sau khi che;
   (a) có tên lỗi rõ: dòng lớp lỗi theo quy tắc của dataset (RE2-TT: bộ từ khóa SimpleRCA; Nezha-OB: severity),
       hoặc có tên ngoại lệ `…Exception`/`…Error`, hoặc mã HTTP 4xx/5xx sau "HTTP"/"status"/"code", hoặc
       "timeout"/"timed out"/"refused";
   (c) khác số token: không mẫu đã biết nào (học từ N) của thực thể có cùng số token với dòng; với cách khớp (a),
       Drain chỉ so mẫu cùng số token nên dòng này không thể khớp;
   (b) còn lại: có mẫu cùng số token nhưng nội dung khác ("dòng bình thường nhưng hiếm" theo C5).
   Báo kèm: tỷ lệ dòng có tiền tố ngày-giờ (RE2-TT) hoặc `TraceID:` (Nezha-OB).
4. So tỷ lệ bốn loại giữa cửa sổ thật và cửa sổ giả; ở cửa sổ thật tách bên gọi root (có cạnh quan sát e → root
   trong `extra.canh`) với thực thể khác.
Đầu ra: tỷ lệ theo loại; 10 dạng đã che nhiều dòng nhất mỗi (dataset, loại cửa sổ, loại), mỗi dạng 3 dòng gốc cắt
300 ký tự; tên mẫu Drain (khuôn) của thực thể vượt mới có kênh mạnh nhất là mẫu Drain.
Thêm sau khi xem lượt `a8-mau-e3-001` (chỉ mô tả, không đổi luật 1–4): tách root khỏi nhóm "khác"; đếm dòng khung ngăn
xếp (`at …(`, `Caused by:`, `... N more`), vì lượt 001 cho thấy ngoại lệ Java nhiều dòng bị tách thành từng dòng log.
Chạy: $PY -B results/T-045/scripts/kiem_mau_e3.py --luot results/T-045/runs/a8-mau-e3-001 --ra results/T-045/e3-noi-dung-mau.json
"""
import argparse
import collections
import json
import re
import sys
import time
from pathlib import Path

import psutil

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from drain3.drain import Drain  # noqa: E402
from m1 import e3, runner  # noqa: E402
from m1.chuoi import NS, _alias, _he_so_ns  # noqa: E402
from m1_danh_gia import rr  # noqa: E402
import chay_pha1 as cp  # noqa: E402
import co_che_khoi_k as ck  # noqa: E402
import pha2_khoi_k as pk  # noqa: E402
from p3 import nhan as p3nhan  # noqa: E402

TS_E3 = dict(runner.TS_E3, khop='hoan_toan')  # cấu hình K-E3 (D17 Q-d giữ cách khớp (a))
EXC = re.compile(r'[A-Za-z_][\w.$]*(?:Exception|Error)\b')
HTTP = re.compile(r'\b(?:HTTP|status|code)\D{0,12}[45]\d\d\b', re.IGNORECASE)
KW = re.compile(r'time[d]?\s?out|refused', re.IGNORECASE)
TIEN_TO = {'RE2-TT': re.compile(r'^\s*\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}'), 'Nezha-OB': re.compile(r'^\s*TraceID:')}
NGAN_XEP = re.compile(r'^\s*(?:at\s+[\w.$<>]+\(|Caused by:|\.\.\.\s*\d+\s+more)')


def dong_log(ca, t):
    """Như chuoi._chay: dòng log trong [t − 300, t + 300), thực thể qua alias; chia N (< t) và A."""
    p = ca['params_ca']
    he_l = _he_so_ns(p['don_vi_thoi_gian']['logs.timestamp'])
    t_ns = int(round(t * NS))
    lo, hi = t_ns - 300 * NS, t_ns + 300 * NS
    dong = []
    for r in ca['logs']:
        m = r['timestamp'] * he_l
        if lo <= m < hi:
            dong.append({'moc': int(m), 'thuc_the': _alias(ca['aliases'], r['entity']), 'noi_dung': r.get('message') or '',
                         'severity_raw': r.get('severity_raw'), 'lop': None})
    return [d for d in dong if d['moc'] < t_ns], [d for d in dong if d['moc'] >= t_ns], p['ho_so_nguon']['quy_tac_log']


def drain_co_dong(dong_N, dong_A, quy_tac):
    """Bản sao vòng học và khớp của e3.hoc_va_dem, giữ thêm dòng rơi vào mẫu mới và số token các mẫu đã biết."""
    drain = Drain(depth=int(TS_E3['do_sau']), sim_th=float(TS_E3['sim_th']), max_children=100, max_clusters=None,
                  extra_delimiters=(), parametrize_numeric_tokens=True)
    biet, n = {}, collections.Counter()
    for d in sorted(dong_N, key=lambda x: (x['moc'], x['thuc_the'], x['noi_dung'])):
        cl, _ = drain.add_log_message(e3.che_token(d['noi_dung']))
        biet.setdefault(d['thuc_the'], set()).add(cl.cluster_id)
        n[(d['thuc_the'], cl.cluster_id, 'N')] += 1
    moi = collections.defaultdict(list)
    for d in sorted(dong_A, key=lambda x: (x['moc'], x['thuc_the'], x['noi_dung'])):
        e = d['thuc_the']
        tokens = drain.get_content_as_tokens(e3.che_token(d['noi_dung']))
        cl = e3._khop(drain, tokens, set(biet.get(e, set())), 'hoan_toan', float(TS_E3['sim_th']))
        if cl is None:
            moi[e].append((d, tokens))
        else:
            n[(e, cl.cluster_id, 'A')] += 1
    dai = {cl.cluster_id: len(cl.log_template_tokens) for cl in drain.clusters}
    khuon = {cl.cluster_id: cl.get_template() for cl in drain.clusters}
    return {'biet': biet, 'n': n, 'moi': moi, 'dai': dai, 'khuon': khuon, 'quy_tac': quy_tac}


def tai_lap(kq, rec):
    tk = rec['extra']['thong_ke_log']
    for c in tk['cap_drain'] or []:
        if kq['n'][(c['thuc_the'], c['mau'], 'N')] != c['n_N'] or kq['n'][(c['thuc_the'], c['mau'], 'A')] != c['n_A']:
            return False
    so_cap = sum(1 for k in kq['n'] if k[2] == 'N')
    mm = {e: len(v) for e, v in kq['moi'].items()}
    return so_cap == len(tk['cap_drain'] or []) and all(mm.get(e, 0) == v for e, v in (tk['mau_moi'] or {}).items()) \
        and all(e in (tk['mau_moi'] or {}) for e in mm)


def loai_dong(d, tokens, e, kq):
    if not d['noi_dung'].strip() or len(tokens) < 3:
        return 'd'
    s = d['noi_dung']
    if e3._lop_dong(d, kq['quy_tac']) == e3.LOI or EXC.search(s) or HTTP.search(s) or KW.search(s):
        return 'a'
    if not any(kq['dai'][c] == len(tokens) for c in kq['biet'].get(e, ())):
        return 'c'
    return 'b'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--luot', required=True)
    ap.add_argument('--ra', required=True)
    ap.add_argument('--dau', type=int, default=0, help='chỉ chạy N ca đầu của danh sách (thử script)')
    a = ap.parse_args()
    thu = Path(a.luot)
    thu.mkdir(parents=True, exist_ok=True)
    prog = open(thu / 'progress.jsonl', 'a', encoding='utf-8')

    def ghi(**x):
        x.update(thoi_diem=time.strftime('%Y-%m-%dT%H:%M:%S%z'), rss_gib=round(psutil.Process().memory_info().rss / 2 ** 30, 2))
        prog.write(json.dumps(x, ensure_ascii=False) + '\n')
        prog.flush()

    t0 = time.time()
    nhan = pk.nap_nhan(False)
    # bước 1: chọn ca theo cặp (R0, E3)
    chon, vuot = [], {}
    for L in pk.LUOT_THAT:
        r0, r3 = pk.doc_ban_ghi(L, 'K-R0'), pk.doc_ban_ghi(L, 'K-E3')
        for o in sorted(r3):
            root = nhan[o]['root']
            if rr.rr_ca(r3[o]['blocks'] or [], root) < rr.rr_ca(r0[o]['blocks'] or [], root):
                v0, v3 = ck.vi_tri(r0[o]['blocks']), ck.vi_tri(r3[o]['blocks'])
                truoc0 = {e for e in v0 if root in v0 and ck.truoc(v0[e], v0[root])}
                truoc3 = {e for e in v3 if root in v3 and ck.truoc(v3[e], v3[root])}
                vuot[o] = {e: ck.kenh_manh(r3[o], e) for e in sorted(truoc3 - truoc0)}
                chon.append((nhan[o]['dataset'], o, False))
    chon += [('RE2-TT', o, True) for ds, o, _ in list(chon) if ds == 'RE2-TT']
    if a.dau:
        chon = [x for x in chon if x[0] == 'RE2-TT'][:a.dau] + [x for x in chon if x[0] == 'Nezha-OB'][:a.dau]
    ghi(su_kien='chon_ca', so_ca_that=sum(1 for x in chon if not x[2]), so_cua_so_gia=sum(1 for x in chon if x[2]))
    hop_dong = json.loads((ROOT / 'results/T-043/hop-dong.json').read_text(encoding='utf-8'))
    U_re = json.loads((ROOT / 'results/T-022/mappings/universe-re2tt-dev.json').read_text(encoding='utf-8'))['U']
    moc_re = p3nhan.nap_moc(ROOT / 'results/T-022/nhan-dev.json')
    _, re_al, nz_al = cp.danh_sach_ca('all', None, None, False)
    rec3 = {**pk.doc_ban_ghi(pk.LUOT_THAT[0], 'K-E3'), **pk.doc_ban_ghi(pk.LUOT_THAT[1], 'K-E3')}
    rec3_mg = pk.doc_ban_ghi(pk.LUOT_MG, 'K-E3')
    dem = collections.defaultdict(collections.Counter)  # (dataset, cửa sổ, nhóm thực thể) -> loại -> số dòng
    tien_to = collections.defaultdict(collections.Counter)
    ngan_xep = collections.defaultdict(collections.Counter)  # (nhóm) -> loại -> số dòng khung ngăn xếp
    dang =collections.defaultdict(lambda: collections.defaultdict(lambda: {'so_dong': 0, 'vi_du': []}))
    khuon_vuot, khong_tai_lap = [], []
    for ds, o, gia in chon:
        t1 = time.time()
        ca, t = cp.nap_ca(ds, o, re_al, nz_al, moc_re, gia, hop_dong, U_re)
        dN, dA, qt = dong_log(ca, t)
        del ca
        kq = drain_co_dong(dN, dA, qt)
        rec = (rec3_mg if gia else rec3)[o]
        ok = tai_lap(kq, rec)
        ghi(su_kien='ca', ca=o, dataset=ds, cua_so_gia=gia, tai_lap=ok, dong_N=len(dN), dong_A=len(dA),
            giay=round(time.time() - t1, 1))
        if not ok:
            khong_tai_lap.append([o, gia])
            continue
        cua_so = 'gia' if gia else 'that'
        co_mau_moi = {k['thuc_the'] for k in rec['extra']['kenh_co'] if k['don_vi'].endswith('|mau_moi')}
        root = nhan[o]['root']
        ben_goi = {x for x, y in (tuple(c) for c in rec['extra']['canh']) if y == root and x != root}
        nhom_tt = {}
        for e in co_mau_moi:
            nhom_tt.setdefault(e, []).append('co_co_mau_moi' + ('' if gia else (
                '|root' if e == root else ('|ben_goi_root' if e in ben_goi else '|khac'))))
        if not gia:
            for e, k in vuot[o].items():
                if k and k['nhom'].startswith('log|mau_moi'):
                    nhom_tt.setdefault(e, []).append('vuot_moi_mau_moi')
                elif k and k['nhom'].startswith('log|mau'):
                    ma = [x for x in rec['extra']['kenh_co'] if x['thuc_the'] == e and x['s'] == k['s']
                          and x['don_vi'].startswith('log|')]
                    for x in ma:
                        cid = x['don_vi'].split('mau:', 1)[-1]
                        cap = next((c for c in rec['extra']['thong_ke_log']['cap_drain'] if c['thuc_the'] == e
                                    and str(c['mau']) == cid), None)
                        khuon_vuot.append({'ca': o, 'dataset': ds, 'thuc_the': e, 'huong': x['huong'],
                                           'ben_goi_root': e in ben_goi, 'khuon': cap['khuon'] if cap else None,
                                           'lop': cap['lop'] if cap else None,
                                           'n_N': cap['n_N'] if cap else None, 'n_A': cap['n_A'] if cap else None})
        for e, nhom_list in nhom_tt.items():
            for d, tokens in kq['moi'].get(e, []):
                lo = loai_dong(d, tokens, e, kq)
                for g in nhom_list:
                    dem[f'{ds}|{cua_so}|{g}'][lo] += 1
                    tien_to[f'{ds}|{cua_so}|{g}'][bool(TIEN_TO[ds].search(d['noi_dung']))] += 1
                    ngan_xep[f'{ds}|{cua_so}|{g}'][lo] += int(bool(NGAN_XEP.search(d['noi_dung'])))
                if any(g.startswith('co_co_mau_moi') for g in nhom_list):
                    x = dang[f'{ds}|{cua_so}|{lo}'][' '.join(tokens)]
                    x['so_dong'] += 1
                    if len(x['vi_du']) < 3:
                        x['vi_du'].append(d['noi_dung'][:300])
    ti_le = {k: {'so_dong': sum(v.values()), **{lo: round(v[lo] / sum(v.values()), 4) for lo in 'abcd'}}
             for k, v in sorted(dem.items()) if sum(v.values())}
    out = {'nguon': 'REVIEW.md T-045 lượt 1, C5 (A8); chỉ để tìm nguyên nhân, không dùng để chọn',
           'tham_so_E3': TS_E3, 'so_ca': {'that': sum(1 for x in chon if not x[2]), 'gia': sum(1 for x in chon if x[2])},
           'khong_tai_lap': khong_tai_lap,
           'dem_theo_loai': {k: dict(v) for k, v in sorted(dem.items())}, 'ti_le_theo_loai': ti_le,
           'tien_to': {k: {'co': v[True], 'khong': v[False]} for k, v in sorted(tien_to.items())},
           'khung_ngan_xep_theo_loai': {k: {**dict(v), 'tong': sum(v.values()), 'tren_so_dong': sum(dem[k].values())}
                                        for k, v in sorted(ngan_xep.items())},
           'dang_nhieu_nhat': {k: sorted(({'dang': s, **x} for s, x in v.items()), key=lambda y: -y['so_dong'])[:10]
                               for k, v in sorted(dang.items())},
           'khuon_thuc_the_vuot_moi': khuon_vuot, 'giay': round(time.time() - t0, 1)}
    Path(a.ra).write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    ghi(su_kien='xong', giay=out['giay'], khong_tai_lap=len(khong_tai_lap))
    print(json.dumps({k: out[k] for k in ('so_ca', 'khong_tai_lap', 'ti_le_theo_loai', 'tien_to', 'khung_ngan_xep_theo_loai',
                                          'giay')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
