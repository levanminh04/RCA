"""Hợp đồng vào/ra của M1: bộ kiểm trường cấm đệ quy, chặn rò nhãn ở mức giá trị, kiểm params.

- Tên cấm = `hop-dong.json#/cam/ten_cam` = CAM của src/p3/ban_ghi.py cộng FORBIDDEN_LABEL_KEYS của src/p3/nezha.py.
- Bộ kiểm duyệt đệ quy qua dict, list và tuple (đặc tả v1 §1; fixture 74). Không dùng `ban_ghi.kiem`
  (không duyệt list/tuple; SPEC T-043 dòng 157).
- Chặn rò ở mức giá trị (dinh-chinh-cai-dat.md CĐ12): mã mờ hay case_dir không được nằm trong giá trị
  (kể cả chuỗi con) hay khóa của params, aliases, inventory.
"""
from p3 import ban_ghi, nezha

TEN_CAM = frozenset(ban_ghi.CAM) | frozenset(nezha.FORBIDDEN_LABEL_KEYS)


class LoiTruongCam(ValueError):
    """Bản ghi chứa trường nhãn."""


def vi_pham_truong_cam(obj, duong=''):
    """Danh sách đường dẫn có khóa cấm ở bất kỳ mức nào của dict/list/tuple."""
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f'{duong}.{k}' if duong else str(k)
            if k in TEN_CAM:
                out.append(p)
            out += vi_pham_truong_cam(v, p)
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            out += vi_pham_truong_cam(v, f'{duong}[{i}]')
    return out


def kiem_ban_ghi(rec):
    """Từ chối bản ghi có trường cấm. Khóa `opaque_id` ở mức ngoài cùng là của runner (ban_ghi.tao), bỏ qua."""
    vp = vi_pham_truong_cam({k: v for k, v in rec.items() if k != 'opaque_id'})
    if vp:
        raise LoiTruongCam(f'bản ghi chứa trường nhãn: {vp}')
    return rec


def _chuoi(obj):
    """Mọi chuỗi (giá trị và khóa) trong dict/list/tuple lồng nhau."""
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str):
                yield k
            yield from _chuoi(v)
    elif isinstance(obj, (list, tuple, set, frozenset)):
        for v in obj:
            yield from _chuoi(v)


def vi_pham_gia_tri(params, aliases, inventory, chuoi_cam):
    """CĐ12: danh sách (nơi, chuỗi cấm) khi một chuỗi cấm là chuỗi con của một chuỗi trong đầu vào."""
    cam = [c for c in chuoi_cam if c]
    out = []
    for ten, obj in (('params', params), ('aliases', aliases), ('inventory', inventory)):
        for s in _chuoi(obj):
            for c in cam:
                if c in s:
                    out.append((ten, c))
    return out
