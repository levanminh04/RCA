"""T-075 bản 2 — ghi các đầu ra mẫu VIẾT TAY (khuôn T075-ra-2) ra ca-thu-2/<ca>/dau-ra-<tên>.json.
Nội dung do người làm soạn; script chỉ để ghi file nhất quán. Mẫu ca E5 viết khi người làm đã biết ô của lượt E5.
Chạy: py -3 -I -B -X utf8 viet_mau_2.py
"""
import json
import os

GOC = os.path.dirname(os.path.abspath(__file__))
R = 'T075-ra-2'


def T(*a):
    return [{'con_tro': x} if isinstance(x, str) else {'con_tro': x[0], 'gia_tri': x[1]} for x in a]


NHOM17 = ['api-gateway', 'booking-service', 'booking_db', 'broker', 'cache', 'config-discovery', 'event-service',
          'event_db', 'keycloak', 'keycloak_db', 'mongodb-instance', 'payment-service', 'payment_db',
          'postgresql-shared-instance', 'ticket-service', 'ticket_db', 'user-service']

MAU = {}
MAU[('e5-su-co', 'dung')] = {
    'khuon': R, 'trang_thai': 'KHONG_DU_BANG_CHUNG', 'xep_hang_nhac_lai': [['booking-service']],
    'khang_dinh': [
        {'id': 'k1', 'loai': 'quan_sat',
         'cau': 'Lõi RCA (V082-V066+H8a) kết luận CAUSE_FOUND, nhóm hạng 1 là booking-service.',
         'trich_dan': T(('/ket_qua_rca/ket_luan', 'CAUSE_FOUND'), '/ket_qua_rca/nhom_hang_1',
                        '/ket_qua_rca/ban_phuong_phap')},
        {'id': 'k2', 'loai': 'quan_sat',
         'cau': 'Cảnh báo đầu tiên là t072-live (tín hiệu live) tại t̂; t072-p95-payment bắt đầu sau 50 s và '
                't072-loi-payment sau 60 s.',
         'trich_dan': T('/canh_bao/0', '/canh_bao/1', '/canh_bao/2')},
        {'id': 'k3', 'loai': 'quan_sat',
         'cau': 'Trong đầu vào P7 cơ sở, payment-service có 17502 span và 584 dòng log ở nửa nền, và không có khóa A '
                'ở cả hai, tức không có mẫu nào ở nửa sự cố.',
         'trich_dan': T('/so_mau_theo_thuc_the/span/payment-service', '/so_mau_theo_thuc_the/log/payment-service',
                        '/so_mau_theo_thuc_the/ghi_chu', '/so_mau_theo_thuc_the/pham_vi')},
        {'id': 'k4', 'loai': 'quan_sat',
         'cau': 'Sáu nguồn metric cơ sở của payment-service thiếu phủ cửa sổ, lỗ lớn nhất khoảng 365 s; phép phủ '
                'này không gồm kênh liveness bổ sung.',
         'trich_dan': T('/do_phu/thieu_bat_buoc', '/do_phu/lo_lon_nhat_s', '/do_phu/pham_vi')}],
    'goi_y_xu_ly': [
        {'id': 'g1', 'loai': 'kiem_tra',
         'cau': 'Kiểm tra trạng thái payment-service: trong đầu vào P7 cơ sở nó không có span và log ở nửa sự cố, '
                'và sáu nguồn metric cơ sở thiếu phủ cửa sổ.',
         'can_cu': T('/so_mau_theo_thuc_the/span/payment-service', '/so_mau_theo_thuc_the/log/payment-service',
                     '/so_mau_theo_thuc_the/ghi_chu', '/do_phu/thieu_bat_buoc')},
        {'id': 'g2', 'loai': 'thu_them_du_lieu',
         'cau': 'Dùng file G1 đầy đủ của ca để có bảng bằng chứng theo kênh rồi giải thích lại.',
         'can_cu': T('/thieu_trong_goi/0')}],
    'thieu_bang_chung': [
        {'cau': 'Nguồn này không có bảng bằng chứng theo kênh của V082, nên không giải thích được vì sao '
                'booking-service đứng hạng 1.',
         'trich_dan': T('/thieu_trong_goi/0', '/ket_qua_rca/nhom_hang_1'), 'vang': ['/bang_chung', '/ke_thua']},
        {'cau': 'Nguồn này không có trạng thái chạy của V082, chỉ có trạng thái bước P7.',
         'trich_dan': T('/ket_qua_rca/nguon_trang_thai'), 'vang': ['/ket_qua_rca/trang_thai_chay']},
        {'cau': 'Độ phủ cửa sổ không đủ ở sáu nguồn metric cơ sở của payment-service.',
         'trich_dan': T(('/do_phu/du_cua_so', False), '/do_phu/thieu_bat_buoc')}]}

MAU[('e5-su-co', 'sai-doi-hang')] = {
    'khuon': R, 'trang_thai': 'GIAI_THICH', 'xep_hang_nhac_lai': [['payment-service']],
    'khang_dinh': [{'id': 'k1', 'loai': 'suy_luan',
                    'cau': 'payment-service mới là nguyên nhân hạng 1 vì nó ngừng phát span sau t̂.',
                    'trich_dan': T('/so_mau_theo_thuc_the/span/payment-service')}],
    'goi_y_xu_ly': [{'id': 'g1', 'loai': 'giam_thieu', 'cau': 'Khởi động lại payment-service ngay.',
                     'can_cu': T('/so_mau_theo_thuc_the/span/payment-service')}],
    'thieu_bang_chung': []}

MAU[('e5-g1', 'dung')] = {
    'khuon': R, 'trang_thai': 'GIAI_THICH', 'xep_hang_nhac_lai': [['booking-service'], ['api-gateway']],
    'khang_dinh': [
        {'id': 'k1', 'loai': 'quan_sat', 'cau': 'Lõi RCA kết luận CAUSE_FOUND và xếp booking-service hạng 1.',
         'trich_dan': T(('/ket_qua_rca/ket_luan', 'CAUSE_FOUND'), '/ket_qua_rca/xep_hang/0')},
        {'id': 'k2', 'loai': 'quan_sat',
         'cau': 'booking-service có hai kênh tạo hạng (F_I = 1): thao tác SELECT booking_db với điểm s 380,3 và '
                'SELECT booking_schema.tbl_orders với điểm s 254,89, cùng khởi phát tại t̂.',
         'trich_dan': T('/bang_chung/0', '/bang_chung/1')},
        {'id': 'k3', 'loai': 'suy_luan',
         'cau': 'Bất thường log_loi và error ở api-gateway được lõi giải thích là lan ngược từ các thao tác SQL của '
                'booking-service.',
         'trich_dan': T('/ke_thua/0', '/ke_thua/2')},
        {'id': 'k4', 'loai': 'quan_sat', 'cau': 'api-gateway hạng 2 có kênh workload giảm với điểm s 17,25 và F_I = 1.',
         'trich_dan': T('/bang_chung/2', '/ket_qua_rca/xep_hang/1')},
        {'id': 'k5', 'loai': 'quan_sat',
         'cau': 'Kênh workload của booking-service cũng giảm, nhưng lõi coi đó là lan xuôi từ api-gateway nên kênh '
                'này không tạo hạng.',
         'trich_dan': T('/bang_chung/5', '/ke_thua/4')}],
    'goi_y_xu_ly': [
        {'id': 'g1', 'loai': 'kiem_tra',
         'cau': 'Mở trace của hai thao tác SELECT booking_db và SELECT booking_schema.tbl_orders ở booking-service '
                'quanh t̂ để xem vì sao chúng bất thường.',
         'can_cu': T('/thao_tac_co_co/0', '/thao_tac_co_co/1')},
        {'id': 'g2', 'loai': 'kiem_tra',
         'cau': 'Kiểm tra payment-service vì sáu nguồn metric cơ sở của nó thiếu phủ cửa sổ.',
         'can_cu': T('/do_phu/thieu_bat_buoc')}],
    'thieu_bang_chung': [
        {'cau': 'Sáu nguồn metric cơ sở của payment-service thiếu phủ cửa sổ, nên nhận định về payment-service yếu '
                'hơn các thực thể khác.',
         'trich_dan': T(('/do_phu/du_cua_so', False), '/do_phu/thieu_bat_buoc', '/do_phu/pham_vi')},
        {'cau': 'Nửa nền trước t̂ có thể đã chứa phần đầu sự cố khi cảnh báo đến trễ.',
         'trich_dan': T('/gioi_han/1')}]}

MAU[('cu-1', 'dung')] = {
    'khuon': R, 'trang_thai': 'GIAI_THICH', 'xep_hang_nhac_lai': [['payment-service'], ['ticket-service']],
    'khang_dinh': [
        {'id': 'k1', 'loai': 'quan_sat', 'cau': 'Lõi RCA kết luận CAUSE_FOUND và xếp payment-service hạng 1.',
         'trich_dan': T(('/ket_qua_rca/ket_luan', 'CAUSE_FOUND'), '/ket_qua_rca/xep_hang/0')},
        {'id': 'k2', 'loai': 'quan_sat',
         'cau': 'payment-service có một kênh tạo hạng: cpu tăng, F_I = 1, điểm s 2,76, khởi phát khoảng 290 s sau mốc.',
         'trich_dan': T('/bang_chung/0', ('/bang_chung/0/diem_s', 2.76))},
        {'id': 'k3', 'loai': 'quan_sat',
         'cau': 'ticket-service hạng 2 có kênh live-ms tăng với điểm s 5,04, khởi phát khoảng 30 s sau mốc, nhưng lõi '
                'xếp nó vào lớp kế thừa.',
         'trich_dan': T('/bang_chung/1', '/ket_qua_rca/xep_hang/1')},
        {'id': 'k4', 'loai': 'suy_luan',
         'cau': 'Theo quy tắc nhom_vong, bất thường live-ms của ticket-service được giải thích bởi cpu của '
                'payment-service, nên payment-service đứng trước dù điểm s thấp hơn.',
         'trich_dan': T('/ke_thua/0', '/bang_chung/1/diem_s', '/bang_chung/0/diem_s')}],
    'goi_y_xu_ly': [
        {'id': 'g1', 'loai': 'kiem_tra',
         'cau': 'Mở metric cpu của payment-service quanh lúc khởi phát để xác nhận mức tăng.',
         'can_cu': T('/bang_chung/0')},
        {'id': 'g2', 'loai': 'giam_thieu',
         'cau': 'Nếu cpu của payment-service còn cao, cân nhắc giảm tải hoặc khởi động lại payment-service theo quy '
                'trình vận hành.',
         'can_cu': T('/bang_chung/0')}],
    'thieu_bang_chung': [{'cau': 'Chế độ a không có khối độ phủ cửa sổ; chưa biết dữ liệu có thiếu hay không.',
                          'trich_dan': T('/thieu_trong_goi/0'), 'vang': ['/do_phu']}]}

MAU[('cu-2', 'dung')] = {
    'khuon': R, 'trang_thai': 'KHONG_DU_BANG_CHUNG', 'xep_hang_nhac_lai': [NHOM17],
    'khang_dinh': [{'id': 'k1', 'loai': 'quan_sat',
                    'cau': 'Lõi RCA kết luận NO_INTRINSIC_ANOMALY; cả 17 thực thể cùng hạng 1, không thực thể nào có '
                           'kênh cờ.',
                    'trich_dan': T(('/ket_qua_rca/ket_luan', 'NO_INTRINSIC_ANOMALY'), '/ket_qua_rca/xep_hang')}],
    'goi_y_xu_ly': [{'id': 'g1', 'loai': 'thu_them_du_lieu',
                     'cau': 'Nếu cảnh báo vẫn còn, xem cửa sổ sau đó hoặc kiểm tra tín hiệu chưa được quan sát trước '
                            'khi kết luận nguyên nhân.',
                     'can_cu': T('/ket_qua_rca/ket_luan')}],
    'thieu_bang_chung': [{'cau': 'Gói không có mục bằng chứng nào, nên không có căn cứ để chỉ ra thực thể gây lỗi.',
                          'trich_dan': T('/bang_chung'), 'vang': ['/bang_chung']}]}

MAU[('cu-2', 'sai-bia-nguyen-nhan')] = {
    'khuon': R, 'trang_thai': 'GIAI_THICH', 'xep_hang_nhac_lai': [NHOM17],
    'khang_dinh': [{'id': 'k1', 'loai': 'suy_luan',
                    'cau': 'api-gateway đứng đầu danh sách nên nhiều khả năng là nguồn lỗi.',
                    'trich_dan': T('/ket_qua_rca/xep_hang/0')}],
    'goi_y_xu_ly': [{'id': 'g1', 'loai': 'giam_thieu', 'cau': 'Khởi động lại api-gateway ngay.',
                     'can_cu': T('/ket_qua_rca/xep_hang/0')}],
    'thieu_bang_chung': []}

MAU[('gia-1', 'dung')] = {
    'khuon': R, 'trang_thai': 'KHONG_DU_BANG_CHUNG', 'xep_hang_nhac_lai': [['payment-service']],
    'khang_dinh': [{'id': 'k1', 'loai': 'quan_sat', 'cau': 'Lõi RCA kết luận CAUSE_FOUND và xếp payment-service hạng 1.',
                    'trich_dan': T('/ket_qua_rca/ket_luan', '/ket_qua_rca/xep_hang/0')}],
    'goi_y_xu_ly': [{'id': 'g1', 'loai': 'thu_them_du_lieu',
                     'cau': 'Lấy lại bảng bằng chứng theo kênh của ca trước khi giải thích.',
                     'can_cu': T('/bang_chung')}],
    'thieu_bang_chung': [{'cau': 'Gói không có mục bằng chứng hay kế thừa nào, nên không giải thích được vì sao '
                                 'payment-service đứng hạng 1.',
                          'trich_dan': T('/bang_chung', '/ke_thua', '/ket_qua_rca/nhom_hang_1'),
                          'vang': ['/bang_chung', '/ke_thua']}]}

MAU[('gia-2', 'dung')] = {
    'khuon': R, 'trang_thai': 'KHONG_DU_BANG_CHUNG', 'xep_hang_nhac_lai': [['payment-service']],
    'khang_dinh': [{'id': 'k1', 'loai': 'quan_sat',
                    'cau': 'Lõi RCA kết luận INSUFFICIENT_EVIDENCE; thứ hạng chỉ để tham khảo, payment-service đứng '
                           'hạng 1.',
                    'trich_dan': T(('/ket_qua_rca/ket_luan', 'INSUFFICIENT_EVIDENCE'), '/ket_qua_rca/xep_hang/0')}],
    'goi_y_xu_ly': [{'id': 'g1', 'loai': 'kiem_tra',
                     'cau': 'Kiểm tra metric cpu của payment-service trước khi hành động.',
                     'can_cu': T('/bang_chung/0')}],
    'thieu_bang_chung': [{'cau': 'Lõi tự báo không đủ bằng chứng, nên lớp giải thích không nêu nguyên nhân.',
                          'trich_dan': T('/ket_qua_rca/ket_luan')}]}

if __name__ == '__main__':
    for (ca, ten), x in MAU.items():
        d = os.path.join(GOC, 'ca-thu-2', ca)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, f'dau-ra-{ten}.json'), 'w', encoding='utf-8', newline='\n') as f:
            json.dump(x, f, ensure_ascii=False, indent=1)
            f.write('\n')
    print(len(MAU), 'đầu ra viết tay')
