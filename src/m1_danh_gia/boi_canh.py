"""Kiểm bối cảnh KB (SPEC T-043 B4, luật chọn khối bước 11; fixture 48): đảo trạng thái từng thành phần của K ở
chuỗi cuối; kết cục khác lúc chọn thì ghi "phụ thuộc bối cảnh" và trình Minh; không tự đổi."""


def kiem(ket_cuc_luc_chon, ket_cuc_dao):
    khac = ket_cuc_luc_chon != ket_cuc_dao
    return {'nhan': 'PHU_THUOC_BOI_CANH' if khac else 'KHONG_DOI', 'trinh_Minh': khac, 'tu_doi': False,
            'luc_chon': ket_cuc_luc_chon, 'dao': ket_cuc_dao}
