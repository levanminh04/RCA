r"""T-006 L4 ⑥ (loại C, không có mốc số): chạy GDN như `run.sh cpu msl` của repo GDN 9853899, dữ liệu MSL mẫu trong repo.

Không sửa code GDN. Chỉ một chỗ phải xử lý vì Windows: `Main.get_save_path` đặt tên file theo `'%m|%d-%H:%M:%S'`,
ký tự `|` và `:` không hợp lệ trong tên file Windows. Script nạp `main.py` như một module, thay tên `datetime` trong
module đó (chỉ `get_save_path` dùng, `main.py:182`) bằng lớp con có `strftime` đổi `|` -> `_`, `:` -> `-`, rồi chạy
nguyên văn khối `if __name__ == "__main__":` của `main.py` với đúng tham số của nhánh `cpu` trong `run.sh`.
Sau khi chạy: lấy `main.test_result`, `main.val_result`, tính điểm bất thường bằng `evaluate.get_full_err_scores`
(như `Main.get_score`), kiểm điểm hữu hạn, lưu điểm và mô hình để so hai lần chạy.
Cách dùng (thư mục làm việc có data/msl): <python của py38-gdn> chay_gdn.py
"""
import datetime as _dt
import hashlib
import importlib.util
import json
import sys
import textwrap

GDN = r"D:\RCA-ext\src\GDN"
sys.path.insert(0, GDN)

# tham số nhánh cpu của run.sh, DATASET=msl
RUN_SH_ARGS = ["-dataset", "msl", "-save_path_pattern", "msl", "-slide_stride", "1", "-slide_win", "5", "-batch", "32",
               "-epoch", "30", "-comment", "msl", "-random_seed", "5", "-decay", "0", "-dim", "64", "-out_layer_num", "1",
               "-out_layer_inter_dim", "128", "-decay", "0", "-val_ratio", "0.2", "-report", "best", "-topk", "5",
               "-device", "cpu"]

spec = importlib.util.spec_from_file_location("gdn_main", GDN + r"\main.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class NgayGioWindows(_dt.datetime):
    def strftime(self, fmt):
        return super().strftime(fmt).replace("|", "_").replace(":", "-")


m.datetime = NgayGioWindows
src = open(GDN + r"\main.py", encoding="utf-8").read()
body = textwrap.dedent(src.split('if __name__ == "__main__":', 1)[1])
sys.argv = ["main.py"] + RUN_SH_ARGS
exec(compile(body, GDN + r"\main.py:__main__", "exec"), m.__dict__)

# ---- kiểm sau khi chạy ----
import numpy as np  # noqa: E402
import torch  # noqa: E402
from evaluate import get_full_err_scores  # noqa: E402

main = m.__dict__["main"]
test_scores, normal_scores = get_full_err_scores(main.test_result, main.val_result)
test_scores, normal_scores = np.asarray(test_scores, dtype=float), np.asarray(normal_scores, dtype=float)
np.save("test_scores.npy", test_scores)
np.save("normal_scores.npy", normal_scores)
model_path = main.get_save_path()[0]
sd = torch.load(model_path)
h = hashlib.sha256()
for k in sorted(sd):
    h.update(k.encode())
    h.update(sd[k].cpu().numpy().tobytes())
kq = {"model_path": model_path, "sha256_trong_so": h.hexdigest(),
      "test_scores_shape": list(test_scores.shape), "test_scores_huu_han": bool(np.isfinite(test_scores).all()),
      "normal_scores_huu_han": bool(np.isfinite(normal_scores).all()),
      "test_scores_min_max": [float(np.nanmin(test_scores)), float(np.nanmax(test_scores))],
      "sha256_test_scores": hashlib.sha256(test_scores.tobytes()).hexdigest()}
print("KET-QUA", json.dumps(kq, ensure_ascii=False))
json.dump(kq, open("ket-qua-gdn.json", "w"), ensure_ascii=False, indent=1)
