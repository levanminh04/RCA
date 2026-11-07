"""Worker OB nhận đúng ca đã chọn và cắt theo adapter T-026."""
import json
import sys
from pathlib import Path

from p3 import nezha
from p3.adapters.nezha import UNSUPPORTED, chay
from p3.nezha_worker import _json_default


def main(job_path, result_path):
    job = json.loads(Path(job_path).read_bytes())
    method, selection = job['method'], job['selection']
    if method in UNSUPPORTED:
        t = selection['t_ns']
        window = {'t_ns': t, 'N_ns': [t - 300 * nezha.NS, t], 'A_ns': [t, t + 300 * nezha.NS], 'trace_guard_s': 0}
        payload = None
    else:
        payload = nezha.doc_cua_so(selection, trace_guard_s=0)
        window = payload['window']
    output = {'window': window, 'ket_qua_nhieu': chay(method, payload, trace_guard_s=0),
              'input_sha256': {p: m['sha256'] for p, m in selection['files'].items()}}
    with Path(result_path).open('x', encoding='utf-8') as stream:
        json.dump(output, stream, ensure_ascii=False, allow_nan=False, default=_json_default)


if __name__ == '__main__':
    main(*sys.argv[1:])
