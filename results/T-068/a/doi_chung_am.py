#!/usr/bin/env python3
"""T-068 A: đối chứng âm cho bộ kiểm độc lập và kiểm chéo của bộ dựng (chỉ ghi trong thư mục tạm của scratchpad/arg).

Dùng: py -3 -I doi_chung_am.py <thư mục tạm> <repo lab>
1-4: sửa bản sao một đồ thị (sai số, cạnh ngoài classes, link trên cạnh, sai p95) → dem_doc_lap.py phải báo lệch.
5: kỳ vọng tính trên cửa sổ dịch 1000 ms (--lech-cua-so-ms) → phải báo lệch.
6: bộ dựng với file ca có cửa sổ dịch 1000 ms → kiểm chéo canh_thao_tac phải dừng (TraceError), không ghi đồ thị.
"""
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys

R = pathlib.Path('D:/RCA-flashticket')
DU = R / 'results/T-065/may-l11/du-lieu'
SG = R / 'results/T-068/a/service-graph'
NT = R / 'results/T-068/a/nguon-trace.json'
KIEM = R / 'results/T-068/kiem/dem_doc_lap.py'
BAN, CA = 'V082-V066+H8a', 'eb48d6b3'


def chay(dt, extra=()):
    r = subprocess.run([sys.executable, '-I', str(KIEM), '--du-lieu', str(DU), '--do-thi', str(dt), '--nguon-trace',
                        str(NT), '--cap', f'{BAN}/{CA}', *extra], capture_output=True, text=True, encoding='utf-8')
    return r.returncode, json.loads(r.stdout)['loi']


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    tmp, lab = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    ket = {}
    goc = json.loads((SG / BAN / f'{CA}.json').read_text(encoding='utf-8'))

    def sua(ten, f):
        g = json.loads(json.dumps(goc))
        f(g)
        d = tmp / ten / BAN
        d.mkdir(parents=True, exist_ok=True)
        (d / f'{CA}.json').write_text(json.dumps(g, ensure_ascii=False), encoding='utf-8')
        ket[ten] = chay(tmp / ten)

    ket['0_goc'] = chay(SG)
    sua('1_sai_so', lambda g: g['canh'][0].update(detail__so_A=g['canh'][0]['detail__so_A'] + 1))
    sua('2_ngoai_classes', lambda g: g['canh'].append({**g['canh'][0], 'id': 'x', 'target': 'khong-co',
                                                        'detail__loai': 'db'}))
    sua('3_link_canh', lambda g: g['canh'][0].update(detail__url='/d/x'))
    sua('4_sai_p95', lambda g: g['canh'][1].update(detail__p95_A_ms=(g['canh'][1]['detail__p95_A_ms'] or 0) + 0.001))
    ket['5_sai_cua_so'] = chay(SG, ['--lech-cua-so-ms', '1000'])
    # 6: bộ dựng với cửa sổ sai.
    spec = importlib.util.spec_from_file_location('sg', lab / 'campaigns/g1/service_graph.py')
    sg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sg)
    d6 = tmp / '6_du_lieu' / BAN
    d6.mkdir(parents=True, exist_ok=True)
    ca = json.loads((DU / BAN / f'{CA}.json').read_text(encoding='utf-8'))
    ca['cua_so_ms'] = [x + 1000 for x in ca['cua_so_ms']]
    (d6 / f'{CA}.json').write_text(json.dumps(ca, ensure_ascii=False), encoding='utf-8')
    nt = json.loads(NT.read_text(encoding='utf-8'))[CA]
    try:
        sg.build_case(tmp / '6_du_lieu', [BAN], CA, nt['goi'], nt['sha_ngoai'], tmp / '6_ra')
        ket['6_bo_dung_sai_cua_so'] = 'KHONG DUNG (lỗi)'
    except sg.TraceError as e:
        ket['6_bo_dung_sai_cua_so'] = ['dừng: ' + str(e)[:200], 'có ghi file' if (tmp / '6_ra').exists() else 'không ghi file']
    print(json.dumps(ket, ensure_ascii=False, indent=1))
    ok = ket['0_goc'][0] == 0 and all(ket[k][0] == 1 and ket[k][1] for k in ket if k[0] in '12345') \
        and ket['6_bo_dung_sai_cua_so'][-1] == 'không ghi file'
    print('DAT' if ok else 'KHONG DAT')


if __name__ == '__main__':
    main()
