"""Kiểu dữ liệu dùng chung của M1.

Kênh (Kenh) là một hướng chấm của một đơn vị (đặc tả v1 §5; SPEC T-043 B1.3–B1.4):
- `lop`: lớp lan theo hướng: 'khong_lan' (E1, E2, tài nguyên tăng), 'lan_nguoc', 'lan_xuoi';
- `s`: điểm e_d của E4 khi F_raw = 1 (D24), ngược lại 0;
- `hop_le`: đơn vị có phép chấm hợp lệ (B1.7);
- `khoi_phat`: khởi phát của đơn vị phân vị (E9, Đ11), None khi không có;
- `s_q`: điểm chính xác (Fraction) từ E4 khi có; `s` là bản số thực để ghi. Xếp hạng so khóa theo `s_chinh_xac`
  (dinh-chinh-cai-dat.md C6, S20).
"""
from dataclasses import dataclass, field
from fractions import Fraction

LOP = ('khong_lan', 'lan_nguoc', 'lan_xuoi')
HUONG = ('len', 'xuong')


@dataclass(frozen=True)
class Kenh:
    thuc_the: str
    ten: str
    huong: str
    lop: str
    s: float
    F_raw: int = 1
    trang_thai: str = 'OK'
    loai: str = 'phan_vi'
    hop_le: bool = True
    khoi_phat: float = None
    nhom: str = ''
    don_vi: str = ''
    s_q: object = None

    def __post_init__(self):
        if self.huong not in HUONG:
            raise ValueError(f'hướng lạ: {self.huong}')
        if self.lop not in LOP:
            raise ValueError(f'lớp lạ: {self.lop}')

    @property
    def ma(self):
        """Mã kênh duy nhất trong một ca: thực thể|đơn vị|tên|hướng. Mã đơn vị mang tiền tố loại (op|, metric|, log|,
        canh|, tan_suat|), nên hai kênh cùng tên ở hai đơn vị khác nhau (thao tác `cpu` và metric `S_cpu`; hai cột
        metric alias về cùng thực thể và đuôi) không trùng mã (dinh-chinh-cai-dat.md S12)."""
        return f'{self.thuc_the}|{self.don_vi}|{self.ten}|{self.huong}'

    @property
    def s_chinh_xac(self):
        """Điểm chính xác: `s_q` khi có, ngược lại giá trị đúng của số thực `s`."""
        return self.s_q if self.s_q is not None else Fraction(float(self.s))

    @property
    def co(self):
        """Kênh có cờ thô (F_raw = 1) và ở trạng thái OK."""
        return self.F_raw == 1 and self.trang_thai == 'OK'
