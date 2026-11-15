# -*- coding: utf-8 -*-
"""DC-bo-quan-he — đối chứng bỏ quan hệ trên cùng bản (SPEC T-064: "Quan hệ (cạnh) có tác dụng tính toán không?").

Không phải thành phần đề xuất. Chỉ ghi đè `params['bat_tat']` của P7: tắt các bước dùng đồ thị/quan hệ
(mặc định E1='tat', E2='tat', E5=False) để so cùng bản có/không quan hệ, ô theo ô. Mọi thành phần khác giữ nguyên.
Điều kiện thất bại: nếu tắt xong P7 trả ERROR/UNSUPPORTED thì ô đó ghi nguyên trạng, không thay bằng giá trị khác.
Tham số `bat_tat` cho phép ghi đè từng khóa (vd. chỉ tắt E5).
"""
from m1_ft.chay import ThanhPhan, dang_ky

MAC_DINH = {'E1': 'tat', 'E2': 'tat', 'E5': False}


@dang_ky
class BoQuanHe(ThanhPhan):
    ma = 'DC-bo-quan-he'

    def vao(self, inputs):
        p = dict(inputs[6])
        bt = dict(p['bat_tat'])
        bt.update(self.tham_so.get('bat_tat') or MAC_DINH)
        p['bat_tat'] = bt
        self.bat_tat_dung = bt
        return list(inputs[:6]) + [p]

    def ra(self, rec, inputs, ctx):
        rec.setdefault('extra', {}).setdefault('m1_ft', {})['dc_bo_quan_he'] = self.bat_tat_dung
        return rec
