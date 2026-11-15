# -*- coding: utf-8 -*-
"""Đầu vào bổ sung của M1-FT (không phải nhãn): thông tin phụ của span đọc từ trace thô, cùng cửa sổ và cùng chuẩn hóa ID
với `m1.adapter_flashticket.normalize_spans` (ID hex chữ thường, span trong [t−300, t+300) theo start/end ns).

`span_phu(trace_documents, t)` → {"<traceID>|<spanID>": {"luong", "scope", "kind", "db", "db_ten", "dich", "message", "route"}}
Chỉ giữ thuộc tính kỹ thuật (luồng, thư viện đo, loại span, hệ DB, đích lời gọi, tên queue, route). Không đọc tên ca/nhãn.
"""
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
from m1.adapter_flashticket import attributes, hex_id  # noqa: E402

NS = 10 ** 9


def span_phu(trace_documents, t):
    lo, hi = (int(t) - 300) * NS, (int(t) + 300) * NS
    out = {}
    for document in trace_documents:
        for rs in document.get('resourceSpans', document.get('batches', [])):
            for group in rs.get('scopeSpans', rs.get('instrumentationLibrarySpans', [])):
                scope = (group.get('scope') or group.get('instrumentationLibrary') or {}).get('name', '')
                for raw in group.get('spans', []):
                    st, en = int(raw['startTimeUnixNano']), int(raw['endTimeUnixNano'])
                    if st < lo or en >= hi:
                        continue
                    a = attributes(raw.get('attributes', []))
                    k = f"{hex_id(raw['traceId'], 32)}|{hex_id(raw['spanId'], 16)}"
                    out[k] = {'luong': a.get('thread.name'), 'scope': scope, 'kind': int(raw.get('kind', 0) or 0),
                              'db': a.get('db.system') or a.get('db.system.name'),
                              'db_ten': a.get('db.namespace') or a.get('db.name'),
                              'dich': a.get('server.address') or a.get('net.peer.name'),
                              'message': a.get('messaging.destination.name'),
                              'route': a.get('http.route')}
    return out


def log_phu(log_documents, t):
    """Trường kết cục nghiệp vụ (B16: `outcome`, `reasonCode`, `eventName`) của từng bản ghi log trong [t−300, t+300),
    cùng cách đọc với `m1.adapter_flashticket.normalize_logs` (mốc, chủ sở hữu, thân JSON, severity) để ghép 1–1 với dòng
    log đầu vào M1 theo khóa (timestamp, entity, message, severity_raw). Không đọc nhãn/tên ca.
    → danh sách {"timestamp", "entity", "message", "severity_raw", "outcome", "reasonCode", "eventName"} (mọi bản ghi
    trong cửa sổ, kể cả không có outcome — outcome None)."""
    import json as _json
    import re as _re
    from m1.adapter_flashticket import otlp_value
    lo, hi = (int(t) - 300) * NS, (int(t) + 300) * NS
    out = []
    for document in log_documents:
        for resource_logs in document.get('resourceLogs', []):
            owner = attributes(resource_logs.get('resource', {}).get('attributes', [])).get('service.name')
            for group in resource_logs.get('scopeLogs', []):
                for record in group.get('logRecords', []):
                    when = int(record.get('timeUnixNano') or record.get('observedTimeUnixNano'))
                    if not lo <= when < hi:
                        continue
                    body = otlp_value(record.get('body', {}))
                    parsed = {}
                    if isinstance(body, str):
                        try:
                            parsed = _json.loads(body)
                            parsed = parsed if isinstance(parsed, dict) else {}
                        except ValueError:
                            pass
                    elif isinstance(body, dict):
                        parsed = body
                    severity = parsed.get('severity') or parsed.get('level') or record.get('severityText')
                    if not severity and isinstance(body, str):
                        match = _re.search(r'\b(TRACE|DEBUG|INFO|WARN|WARNING|ERROR|FATAL)\b', body)
                        severity = match[1] if match else None
                    message = parsed.get('message') if parsed else body
                    out.append({'timestamp': when, 'entity': owner, 'message': '' if message is None else str(message),
                                'severity_raw': severity, 'outcome': parsed.get('outcome'),
                                'reasonCode': parsed.get('reasonCode'), 'eventName': parsed.get('eventName')})
    return out
