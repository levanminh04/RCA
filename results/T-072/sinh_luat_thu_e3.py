# -*- coding: utf-8 -*-
"""T-072 — sinh luật THỬ cho E3 (Minh duyệt (a), LOG T-070 lượt 4) và file GỠ chúng.

  py -3 results/T-072/sinh_luat_thu_e3.py nap --ra <worktree>/observability/grafana/provisioning/alerting/t072-thu-e3.yaml
  py -3 results/T-072/sinh_luat_thu_e3.py go  --ra <worktree>/observability/grafana/provisioning/alerting/t072-thu-e3-go.yaml
  py -3 results/T-072/sinh_luat_thu_e3.py hoan-tac --ra <worktree>/observability/grafana/provisioning/alerting/t072-hoan-tac-n.yaml
  (hoan-tac: gỡ MỌI đối tượng commit N tạo — 11 luật thật, 4 luật thử, contact point t072-webhook — khi N nạp lỗi/một phần)

Luật thử = bản sao bốn luật p95 trong bieu-thuc.json (cùng PromQL, cùng chặn ≥ 30 request, cùng for 60 s, nhịp 10 s),
ngưỡng thử 0,005 s (mốc bucket nhỏ nhất; p95 khỏe ×1 đã thấy 0,02–0,16 s), nên cháy khi có tải ×1 và về Normal khi hết
tải (chặn → NoData → OK) → có cả tin firing và resolved. uid `t072-thu-*`, nhãn `t072_loai = thu` (không phải
he-thong/quan-sat: không vào bất kỳ phép đếm W4 nào, không chạy RCA), thư mục và nhóm riêng. Gửi tới contact point
`t072-bo-nhan-nhe` (định nghĩa trong t072-luat.yaml do sinh_luat_grafana.py sinh). Đây KHÔNG là bằng chứng dương thật
cho luật p95 nào (7 luật chưa có dương thật giữ nguyên trạng thái).
File gỡ dùng `deleteRules` của provisioning: xóa file luật khỏi thư mục KHÔNG xóa luật đã nạp trong DB của Grafana.
"""
import argparse, json, pathlib, yaml

GOC = pathlib.Path(__file__).parent
NGUONG_THU = 0.005


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('lenh', choices=['nap', 'go', 'hoan-tac'])
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    bt = json.loads((GOC / 'bieu-thuc.json').read_text(encoding='utf-8'))
    g = bt['grafana']
    p95 = [L for L in bt['luat'] if L['nhan'].get('t072_tin_hieu') == 'p95']
    uids = ['t072-thu-' + L['uid'][len('t072-'):] for L in p95]
    if a.lenh == 'hoan-tac':
        that = [L['uid'] for L in bt['luat']]
        doc = {'apiVersion': 1, 'deleteRules': [{'orgId': 1, 'uid': u} for u in that + uids],
               'deleteContactPoints': [{'orgId': 1, 'uid': 't072-webhook'}]}
        hdr = ('# T-072 E3: HOÀN TÁC commit N (gỡ 11 luật thật, 4 luật thử, contact point t072-webhook). Chỉ dùng khi N nạp\n'
               '# lỗi hoặc một phần. Thư mục Grafana do provisioning tạo không bị xóa (ghi lại, gỡ bằng tay nếu Minh muốn).\n'
               '# Sinh bởi results/T-072/sinh_luat_thu_e3.py hoan-tac. Không sửa tay.\n')
    elif a.lenh == 'go':
        doc = {'apiVersion': 1, 'deleteRules': [{'orgId': 1, 'uid': u} for u in uids]}
        hdr = '# T-072 E3: gỡ luật thử (deleteRules). Sinh bởi results/T-072/sinh_luat_thu_e3.py go. Không sửa tay.\n'
    else:
        rules = []
        for L, u in zip(p95, uids):
            rules.append({
                'uid': u, 'title': u, 'condition': 'C',
                'data': [
                    {'refId': 'A', 'relativeTimeRange': g['truy_van']['relativeTimeRange'], 'datasourceUid': g['datasource_uid'],
                     'model': {'refId': 'A', 'expr': L['promql'], 'instant': True, 'range': False, 'intervalMs': 10000,
                               'maxDataPoints': 43200}},
                    {'refId': 'C', 'relativeTimeRange': {'from': 0, 'to': 0}, 'datasourceUid': '__expr__',
                     'model': {'refId': 'C', 'type': 'threshold', 'expression': 'A',
                               'datasource': {'type': '__expr__', 'uid': '__expr__'},
                               'conditions': [{'evaluator': {'type': 'gt', 'params': [NGUONG_THU]}}]}},
                ],
                'noDataState': 'OK', 'execErrState': 'Error', 'for': f"{L['for_s']}s", 'isPaused': False,
                'labels': {'t072_loai': 'thu', 't072_tin_hieu': 'p95-thu', 't072_uid': u, 'http_route': L['nhan']['http_route'],
                           'service_name': 'api-gateway'},
                'annotations': {'summary': f"THỬ E3 — bản sao {L['uid']}, ngưỡng thử {NGUONG_THU} s",
                                't072_eval_interval_s': str(g['eval_interval_s']), 't072_for_s': str(L['for_s']),
                                't072_nguong': repr(NGUONG_THU), 't072_nguong_phien_ban': 'thu-e3', 't072_bieu_thuc': bt['phien_ban']},
                'notification_settings': {'receiver': 't072-bo-nhan-nhe', 'group_by': ['...'], 'group_wait': '0s',
                                          'group_interval': '10s', 'repeat_interval': '4h'},
            })
        doc = {'apiVersion': 1, 'groups': [{'orgId': 1, 'name': 't072-e3-thu', 'folder': 'T-072 E3 thử (gỡ trước E4)',
                                             'interval': f"{g['eval_interval_s']}s", 'rules': rules}]}
        hdr = ('# T-072 E3: luật THỬ (bản sao p95, ngưỡng 0,005 s). Phải gỡ bằng t072-thu-e3-go.yaml (commit G) trước giờ hiệu lực E4.\n'
               '# Sinh bởi results/T-072/sinh_luat_thu_e3.py nap. Không sửa tay.\n')
    pathlib.Path(a.ra).write_text(hdr + yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=100000), encoding='utf-8', newline='\n')
    print(a.ra, len(uids))


main()
