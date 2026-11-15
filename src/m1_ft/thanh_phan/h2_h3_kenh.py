# -*- coding: utf-8 -*-
"""H2 (JVM/cgroup) và H3 (pool kết nối) — kênh metric mới từ gói bổ sung (`results/T-063/dong-goi/xuat_bo_sung.py`).

Nút: service JVM (đã có trong inventory, `service_name` → thực thể theo `m1.adapter_flashticket._owner`). Không thêm cạnh.
Tín hiệu (Prometheus `exp-obs`, bước 15 s, cửa sổ [t−300, t+300]):
  H2: `throttle` (giây throttle/giây), `throttle-ratio`, `gc` (giây GC/giây), `heap` (byte heap dùng), `threads-blocked`,
      `jvm-cpu` (tỷ lệ CPU của JVM).
  H3: `pool-pending` (request chờ connection), `pool-used`, `pool-wait` (ms chờ trung bình).
Phép tính: kênh lớp **"tài nguyên"** của M1 (`m1.kenh.LOP_HUONG`): hướng lên = `khong_lan` (bằng chứng tự sinh tại thành
phần), hướng xuống = `lan_xuoi`; chấm bằng E4 như kênh metric P7 (cổng G3, D1 theo cấu hình P7). Dựng lại metric một lần
qua `m1_ft.chay._duong_ong_metric` + adapter ghim.
Điều kiện thất bại: tranh CPU máy làm `pool-wait`/`gc` của nạn nhân cũng tăng (đã thấy ở CPU-BOOK T-062: pool-wait Event
×3,3) → thêm bằng chứng "tự sinh" sai chỗ; `throttle` chỉ có từ 12/11 21:39Z (không có trên 9 ca cũ); kênh vắng khi giá trị
bằng 0 không được báo (vd. `threads-blocked`). Đối chứng: bản không có thành phần.
"""
from m1_ft.chay import ThanhPhan, dang_ky

H2 = ('throttle', 'throttle-ratio', 'gc', 'heap', 'threads-blocked', 'jvm-cpu')
H3 = ('pool-pending', 'pool-used', 'pool-wait')


class _KenhMoi(ThanhPhan):
    KENH = ()

    def __init__(self, tham_so):
        super().__init__(tham_so)
        self.bo_sung = None

    def can_bo_sung(self):
        return ('bundles', 'bundles_bo_sung')

    def kenh_moi(self):
        return {k: 'tài nguyên' for k in self.tham_so.get('kenh', self.KENH)}

    def ra(self, rec, inputs, ctx):
        ft = rec.setdefault('extra', {}).setdefault('m1_ft', {}).setdefault('chu_thich', {})
        co = [k['don_vi'] for k in (rec.get('extra') or {}).get('kenh_co', []) if any(k['don_vi'].endswith('_' + c) for c in self.kenh_moi())]
        ft[self.ma] = {'kenh': sorted(self.kenh_moi()), 'don_vi_co_co': co, 'chan_doan_metric': getattr(self, 'chan_doan_metric', None)}
        return rec


@dang_ky
class KenhJVM(_KenhMoi):
    ma = 'H2-jvm'
    KENH = H2


@dang_ky
class KenhPool(_KenhMoi):
    ma = 'H3-pool'
    KENH = H3
