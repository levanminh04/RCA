"""T-034: hàm dùng chung cho việc dựng gói G2. Mọi con số trong văn bản đi qua `Facts`: (file JSON, con trỏ JSON) → giá trị.

Con trỏ theo RFC 6901: `/a/b/0`; trong tên khóa, `~1` là dấu `/`, `~0` là dấu `~`.
Phép biến đổi được phép (ghi trong trường `op`): không có; `len` (số phần tử); `count_true`; `sum`.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
_cache = {}


def load(rel):
    if rel not in _cache:
        _cache[rel] = json.loads((ROOT / rel).read_text(encoding="utf-8"))
    return _cache[rel]


def sha(rel):
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def resolve(doc, pointer):
    cur = doc
    if pointer in ("", "/"):
        return cur
    for raw in pointer.lstrip("/").split("/"):
        key = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(cur, list):
            cur = cur[int(key)]
        else:
            cur = cur[key]
    return cur


def apply(value, op):
    if op is None:
        return value
    if op == "len":
        return len(value)
    if op == "count_true":
        return sum(bool(v) for v in value)
    if op == "sum":
        return sum(value)
    raise ValueError(op)


class Facts:
    def __init__(self):
        self.items = {}

    def add(self, fid, path, pointer, op=None, note=None):
        assert fid not in self.items, fid
        value = apply(resolve(load(path), pointer), op)
        assert isinstance(value, (int, float, str, bool)) or value is None, (fid, type(value))
        self.items[fid] = {"value": value, "path": path, "pointer": pointer, "op": op, "note": note}
        return fid

    def value(self, fid):
        return self.items[fid]["value"]

    def ref(self, path, pointer, spec="", op=None):
        """Đăng ký một số không đặt tên (dùng trong bảng sinh tự động) và trả về chỗ giữ `{{mã:định dạng}}`."""
        key = (path, pointer, op)
        if not hasattr(self, "_anon"):
            self._anon = {}
        if key not in self._anon:
            fid = f"a{len(self._anon) + 1:04d}"
            self.add(fid, path, pointer, op)
            self._anon[key] = fid
        return "{{" + self._anon[key] + (":" + spec if spec else "") + "}}"


def fmt(value, spec=""):
    """Định dạng kiểu Việt: dấu phẩy thập phân. spec: '' (số nguyên hoặc float gọn), '.Nf', 'pctN' (nhân 100), 'x' (chuỗi nguyên trạng)."""
    if spec == "x" or isinstance(value, str):
        return str(value)
    if value is None:
        return "N/A"
    if spec.startswith("pct"):
        n = int(spec[3:] or 0)
        return f"{value * 100:.{n}f}".replace(".", ",") + "%"
    if spec.startswith("."):
        return format(value, spec).replace(".", ",")
    if spec == "e":
        return f"{value:.1e}".replace(".", ",")
    if isinstance(value, bool):
        return "có" if value else "không"
    if isinstance(value, int):
        return f"{value:,}".replace(",", ".") if abs(value) >= 1000 else str(value)
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.4g}".replace(".", ",")
