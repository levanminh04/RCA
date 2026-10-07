"""Selector ca dev (§3, §11.1). Chỉ runner gọi; phương pháp không thấy gì ở đây."""
import hashlib
import json
import os
import re
from pathlib import Path, PurePosixPath

MA_MO = re.compile(r'^dev-[0-9a-f]{10}$')
THU_MUC_DU_LIEU = PurePosixPath('data/rcaeval')
CAM = ('data/locked',)


class LoiRunner(Exception):
    """Lỗi dữ liệu hoặc runner (§8.3): không phải trạng thái phương pháp."""


def sha256_file(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(chunk), b''):
            h.update(block)
    return h.hexdigest()


def nap_allowlist(path):
    with open(path, encoding='utf-8') as f:
        doc = json.load(f)
    cases = doc.get('cases')
    if not isinstance(cases, list) or doc.get('so_ca') != len(cases):
        raise LoiRunner('allowlist: so_ca không khớp danh sách')
    out = {}
    for c in cases:
        oid = c.get('opaque_id')
        if not isinstance(oid, str) or not MA_MO.match(oid):
            raise LoiRunner(f'allowlist: mã mờ sai dạng: {oid!r}')
        if oid in out:
            raise LoiRunner(f'allowlist: mã mờ trùng: {oid}')
        out[oid] = c
    return out


def _kiem_duong_dan(rel):
    if not isinstance(rel, str) or not rel:
        raise LoiRunner('đường dẫn rỗng')
    if '\\' in rel or rel.startswith('/') or re.match(r'^[A-Za-z]:', rel):
        raise LoiRunner(f'đường dẫn phải tương đối kiểu POSIX: {rel}')
    p = PurePosixPath(rel)
    if any(part in ('..', '.') for part in p.parts):
        raise LoiRunner(f'path traversal: {rel}')
    low = rel.lower()
    if any(low == c or low.startswith(c + '/') or ('/' + c + '/') in ('/' + low) for c in CAM):
        raise LoiRunner(f'đường dẫn bị cấm (data/locked): {rel}')
    if p.parts[:2] != THU_MUC_DU_LIEU.parts:
        raise LoiRunner(f'đường dẫn ngoài {THU_MUC_DU_LIEU}: {rel}')
    return p


def chon_ca(allowlist, opaque_id, repo_root, kiem_hash=True, tep=None):
    """Trả {tên tệp: đường dẫn tuyệt đối} của một ca trong allowlist.

    Từ chối: mã sai dạng, ca ngoài allowlist, đường dẫn cấm/traversal/ngoài data/rcaeval,
    tệp vắng, SHA-256 sai. `tep` giới hạn các tệp cần (mặc định mọi tệp của ca).
    """
    if not isinstance(opaque_id, str) or not MA_MO.match(opaque_id):
        raise LoiRunner(f'mã mờ sai dạng: {opaque_id!r}')
    if opaque_id not in allowlist:
        raise LoiRunner(f'ca ngoài allowlist: {opaque_id}')
    root = Path(repo_root).resolve()
    goc = (root / Path(*THU_MUC_DU_LIEU.parts)).resolve()
    files = allowlist[opaque_id]['files']
    out = {}
    for name, meta in files.items():
        if tep is not None and name not in tep:
            continue
        if meta is None:  # allowlist ghi tệp vắng của ca (ca không có logs.parquet); tep đòi tệp này thì báo thiếu
            continue
        p = _kiem_duong_dan(meta['path'])
        full = (root / Path(*p.parts)).resolve()
        if os.path.commonpath([str(full), str(goc)]) != str(goc):
            raise LoiRunner(f'đường dẫn thoát khỏi data/rcaeval sau resolve: {meta["path"]}')
        if not full.is_file():
            raise LoiRunner(f'tệp vắng: {meta["path"]}')
        if kiem_hash and sha256_file(full) != meta['sha256']:
            raise LoiRunner(f'SHA-256 sai: {opaque_id}/{name}')
        out[name] = str(full)
    if tep is not None and set(tep) - set(out):
        raise LoiRunner(f'ca thiếu tệp: {sorted(set(tep) - set(out))}')
    return out
