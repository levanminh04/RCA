# -*- coding: utf-8 -*-
"""T-072 — sinh file provisioning luật cảnh báo Grafana từ bieu-thuc.json + nguong.json.

  py -3 results/T-072/sinh_luat_grafana.py --nguong results/T-072/nguong.json --webhook http://<ip>:<cổng>/t072 --ra <file.yaml>

Bước 5 (sau E2) ghi vào worktree lab: observability/grafana/provisioning/alerting/t072-luat.yaml.
Định tuyến thông báo đặt ở từng luật (notification_settings, "simplified routing"), không sửa cây chính sách thông báo
hiện có của Grafana. Mọi luật mang nhãn t072_uid và annotation t072_* để bản ghi I1 (i1-schema.json) đọc được.
"""
import argparse, hashlib, json, pathlib, yaml

GOC = pathlib.Path(__file__).parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--nguong', required=True)
    ap.add_argument('--webhook', required=True)
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    bt = json.loads((GOC / 'bieu-thuc.json').read_text(encoding='utf-8'))
    raw = pathlib.Path(a.nguong).read_bytes()
    ng = json.loads(raw.decode('utf-8'))['nguong']
    ng_ver = hashlib.sha256(raw).hexdigest()[:12]
    g = bt['grafana']
    rules = []
    for L in bt['luat']:
        n = L['dieu_kien']['nguong']
        th = float(n) if isinstance(n, (int, float)) else float(ng[n])
        loai = {'>': 'gt', '<': 'lt'}[L['dieu_kien']['phep']]
        rules.append({
            'uid': L['uid'], 'title': L['uid'], 'condition': 'C',
            'data': [
                {'refId': 'A', 'relativeTimeRange': g['truy_van']['relativeTimeRange'], 'datasourceUid': g['datasource_uid'],
                 'model': {'refId': 'A', 'expr': L['promql'], 'instant': True, 'range': False, 'intervalMs': 10000,
                           'maxDataPoints': 43200}},
                {'refId': 'C', 'relativeTimeRange': {'from': 0, 'to': 0}, 'datasourceUid': '__expr__',
                 'model': {'refId': 'C', 'type': 'threshold', 'expression': 'A', 'datasource': {'type': '__expr__', 'uid': '__expr__'},
                           'conditions': [{'evaluator': {'type': loai, 'params': [th]}}]}},
            ],
            'noDataState': L['no_data_state'], 'execErrState': L['exec_err_state'], 'for': f"{L['for_s']}s",
            'isPaused': False,
            'labels': dict(L['nhan'], t072_uid=L['uid']),
            'annotations': {'summary': L['tieu_de'], 't072_eval_interval_s': str(g['eval_interval_s']), 't072_for_s': str(L['for_s']),
                            't072_nguong': repr(th), 't072_nguong_phien_ban': ng_ver, 't072_bieu_thuc': bt['phien_ban']},
            'notification_settings': {'receiver': 't072-bo-nhan-nhe', 'group_by': ['...'], 'group_wait': '0s',
                                      'group_interval': '10s', 'repeat_interval': '4h'},
        })
    doc = {
        'apiVersion': 1,
        'contactPoints': [{'orgId': 1, 'name': 't072-bo-nhan-nhe', 'receivers': [
            {'uid': 't072-webhook', 'type': 'webhook', 'disableResolveMessage': False,
             'settings': {'url': a.webhook, 'httpMethod': 'POST'}}]}],
        'groups': [{'orgId': 1, 'name': g['nhom_luat'], 'folder': g['thu_muc'], 'interval': f"{g['eval_interval_s']}s", 'rules': rules}],
    }
    hdr = (f"# Sinh bởi results/T-072/sinh_luat_grafana.py (repo RCA) từ {bt['phien_ban']} và nguong.json {ng_ver}. Không sửa tay.\n")
    pathlib.Path(a.ra).write_text(hdr + yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=100000), encoding='utf-8', newline='\n')
    print(a.ra, len(rules))


main()
