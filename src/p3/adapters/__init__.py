"""Adapter từng phương pháp. Mỗi hàm `chay(...)` chỉ nhận dữ liệu đã cắt và mốc chia (giây),
trả dict: status, method_status_raw, error, ranking_native, items [(item, entity, key)], blocks (TORAI),
observed_entities, input_shape, diagnostics, extra.

Quy ước trạng thái (§8.3, D12): ngoại lệ từ chính lời gọi phương pháp → ERROR (giữ thông điệp);
trả về bình thường với danh sách rỗng → NO_EVIDENCE (giữ status gốc). Lỗi của adapter (ví dụ khóa
dựng lại không khớp thứ tự chính thức) là lỗi runner: ném `LoiRunner`, không gán trạng thái.
"""
import os

from ..selector import LoiRunner


_MA_PHUONG_PHAP = ('rcaeval', 'baro', 'circa', os.path.join('src', 'microrank'), os.path.join('src', 'simplerca'),
                  os.path.join('src', 'circa_kien_truc'), os.path.join('src', 'torai'))


def _qua_ma_phuong_phap(exc):
    """Traceback có đi qua mã của phương pháp không (RCAEval, BARO, CIRCA, src/<phương pháp>)."""
    tb = exc.__traceback__
    while tb is not None:
        f = os.path.normcase(os.path.abspath(tb.tb_frame.f_code.co_filename))
        if os.path.join('src', 'p3') not in f and any(os.path.normcase(x) in f for x in _MA_PHUONG_PHAP):
            return True
        tb = tb.tb_next
    return False


def loi(exc):
    """Ngoại lệ đi qua mã phương pháp → ERROR (giữ thông điệp). Không đi qua (lỗi của mã src/p3) → LoiRunner."""
    if isinstance(exc, LoiRunner) or not _qua_ma_phuong_phap(exc):
        raise LoiRunner(f'lỗi adapter: {type(exc).__name__}: {exc}') from exc
    return {'status': 'ERROR', 'error': f'{type(exc).__name__}: {exc}', 'items': [], 'ranking_native': []}


__all__ = ['LoiRunner', 'loi']
