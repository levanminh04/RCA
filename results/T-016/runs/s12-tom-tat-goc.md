mốc tiêm: 1705354566

## So với lượt chính thức

```
{
 "service_list": true,
 "X_train_sai_lech_tuong_doi_max": 0.0,
 "bic_sai_lech_tuong_doi_max": 0.0,
 "bic_tu_tinh_vs_sklearn_max": 7.296203795908045e-16,
 "n_comp": true,
 "y_pred": true,
 "so_cum_chay_rcd": [
  3,
  3
 ],
 "cum": [
  {
   "services": true,
   "aa": 0.0,
   "rcd_ranks": true,
   "du_phong": true,
   "so_lan_pc": [
    50,
    50
   ],
   "cot_moi_lan_pc": true,
   "du_lieu_roi_rac": true,
   "f_con": true,
   "p_value_sai_lech_max": 4.617844371322165e-16
  },
  {
   "services": true,
   "aa": 0.0,
   "rcd_ranks": true,
   "du_phong": true,
   "so_lan_pc": [
    28,
    28
   ],
   "cot_moi_lan_pc": true,
   "du_lieu_roi_rac": true,
   "f_con": true,
   "p_value_sai_lech_max": 1.2932839406780627e-15
  },
  {
   "services": true,
   "aa": 0.0,
   "rcd_ranks": true,
   "du_phong": true,
   "so_lan_pc": [
    0,
    0
   ],
   "cot_moi_lan_pc": true,
   "du_lieu_roi_rac": true,
   "f_con": true,
   "p_value_sai_lech_max": 0.0
  }
 ],
 "ranks_cuoi": true
}
```

## Điểm từng chuỗi (max |z|), 10 cao nhất mỗi nguồn

- metric (45 chuỗi): checkoutservice_cpu 264.9; checkoutservice_mem 29.58; recommendationservice_cpu 12.5; shippingservice_cpu 6.258; emailservice_mem 5.176; cartservice_latency 4.894; emailservice_latency 4.76; redis_mem 4.211; frontend_cpu 4.202; shippingservice_mem 3.935
- log (30 chuỗi): frontend_19 2.96; frontend_20 2.559; checkoutservice_21 2.559; currencyservice_1 2.378; paymentservice_22 2.344; paymentservice_23 2.344; checkoutservice_24 2.344; shippingservice_25 2.344; shippingservice_26 2.344; cartservice_27 2.344
- trace_lat (17 chuỗi): shippingservice_GetQuote 10.48; cartservice_AddItem 8.947; traceservice_Export 8.947; health_Check 4.359; checkoutservice_PlaceOrder 3; cartservice_EmptyCart 3; currencyservice_Convert 2.979; frontendservice_frontend 2.106; cartservice_GetCart 2.074; emailservice_SendOrderConfirmation 2
- trace_err (0 chuỗi): 
- trace_err nhân 1e9: []

## Vectơ mức nghiêm trọng (đã chuẩn hóa từng nguồn) và điểm service

| service | metric | log | trace_lat | trace_err | trung bình | cụm |
|---|---|---|---|---|---|---|
| adservice | 0.0212 | 0.1072 | 0.0204 | 0.0000 | 0.0372 | 2 |
| cartservice | 0.0275 | 0.1110 | 0.2450 | 0.0000 | 0.0959 | 0 |
| checkoutservice | 0.7087 | 0.1211 | 0.0524 | 0.0000 | 0.2205 | 1 |
| currencyservice | 0.0259 | 0.1126 | 0.0768 | 0.0000 | 0.0538 | 2 |
| emailservice | 0.0348 | 0.1110 | 0.0349 | 0.0000 | 0.0452 | 2 |
| frontend | 0.0276 | 0.1401 | 0.0368 | 0.0000 | 0.0511 | 2 |
| frontend-external | 0.0044 | 0.0000 | 0.0000 | 0.0000 | 0.0011 | 3 |
| health | 0.0000 | 0.0000 | 0.0762 | 0.0000 | 0.0190 | 3 |
| paymentservice | 0.0210 | 0.1110 | 0.0175 | 0.0000 | 0.0374 | 2 |
| productcatalogservice | 0.0168 | 0.0000 | 0.0563 | 0.0000 | 0.0183 | 3 |
| recommendationservice | 0.0505 | 0.0751 | 0.0268 | 0.0000 | 0.0381 | 2 |
| redis | 0.0244 | 0.0000 | 0.0000 | 0.0000 | 0.0061 | 3 |
| shippingservice | 0.0374 | 0.1110 | 0.2005 | 0.0000 | 0.0872 | 0 |
| traceservice | 0.0000 | 0.0000 | 0.1563 | 0.0000 | 0.0391 | 3 |

## BIC theo số cụm

| k | BIC (sklearn) | BIC tự tính |
|---|---|---|
| 1 | -216.393 | -216.393 |
| 2 | -270.031 | -270.031 |
| 3 | -261.795 | -261.795 |
| 4 | -282.826 | -282.826 |
| 5 | -255.919 | -255.919 |
| 6 | -240.857 | -240.857 |
| 7 | -233.725 | -233.725 |
| 8 | -214.030 | -214.030 |
| 9 | -186.175 | -186.175 |
| 10 | -168.872 | -168.872 |
| 11 | -138.782 | -138.782 |
| 12 | -113.229 | -113.229 |
| 13 | -82.088 | -82.088 |
| 14 | -45.291 | -45.291 |

chọn k = 4

## Cụm theo thứ tự điểm cụm

- cụm 1 (điểm 0.2205): checkoutservice 0.2205
- cụm 0 (điểm 0.0915): cartservice 0.0959, shippingservice 0.0872
  - RCD nhận 21+21 dòng, 8 cột: ['cartservice_5', 'cartservice_13', 'shippingservice_15', 'shippingservice_16', 'cartservice_17', 'shippingservice_25', 'shippingservice_26', 'cartservice_27']
  - pha 1, mức với 8 cột, khối: [['shippingservice_26', 'shippingservice_15', 'cartservice_13', 'cartservice_27', 'shippingservice_16'], ['cartservice_5', 'shippingservice_25', 'cartservice_17']]
  - pha 1, mức với 6 cột, khối: [['cartservice_13', 'cartservice_5', 'shippingservice_15', 'shippingservice_16', 'shippingservice_26'], ['shippingservice_25']]
  - số lần chạy Ψ-PC: 50; RCD trả: ['cartservice_13', 'shippingservice_16', 'shippingservice_15', 'shippingservice_26']; nội bộ: ['cartservice', 'shippingservice']; dự phòng: False
    - PC #0: α=0.010, cột ['shippingservice_26', 'shippingservice_15', 'cartservice_13', 'cartservice_27', 'shippingservice_16'], số bin {'shippingservice_26': 5, 'shippingservice_15': 5, 'cartservice_13': 5, 'cartservice_27': 5, 'shippingservice_16': 5}, F kề: []
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_27 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
    - PC #1: α=0.110, cột ['shippingservice_26', 'shippingservice_15', 'cartservice_13', 'cartservice_27', 'shippingservice_16'], số bin {'shippingservice_26': 5, 'shippingservice_15': 5, 'cartservice_13': 5, 'cartservice_27': 5, 'shippingservice_16': 5}, F kề: []
      - kiểm F ⊥ cartservice_27 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #2: α=0.210, cột ['shippingservice_26', 'shippingservice_15', 'cartservice_13', 'cartservice_27', 'shippingservice_16'], số bin {'shippingservice_26': 5, 'shippingservice_15': 5, 'cartservice_13': 5, 'cartservice_27': 5, 'shippingservice_16': 5}, F kề: []
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_27 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #3: α=0.310, cột ['shippingservice_26', 'shippingservice_15', 'cartservice_13', 'cartservice_27', 'shippingservice_16'], số bin {'shippingservice_26': 5, 'shippingservice_15': 5, 'cartservice_13': 5, 'cartservice_27': 5, 'shippingservice_16': 5}, F kề: []
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_27 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #4: α=0.410, cột ['shippingservice_26', 'shippingservice_15', 'cartservice_13', 'cartservice_27', 'shippingservice_16'], số bin {'shippingservice_26': 5, 'shippingservice_15': 5, 'cartservice_13': 5, 'cartservice_27': 5, 'shippingservice_16': 5}, F kề: []
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_27 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #5: α=0.510, cột ['shippingservice_26', 'shippingservice_15', 'cartservice_13', 'cartservice_27', 'shippingservice_16'], số bin {'shippingservice_26': 5, 'shippingservice_15': 5, 'cartservice_13': 5, 'cartservice_27': 5, 'shippingservice_16': 5}, F kề: []
      - kiểm F ⊥ cartservice_27 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #6: α=0.610, cột ['shippingservice_26', 'shippingservice_15', 'cartservice_13', 'cartservice_27', 'shippingservice_16'], số bin {'shippingservice_26': 5, 'shippingservice_15': 5, 'cartservice_13': 5, 'cartservice_27': 5, 'shippingservice_16': 5}, F kề: ['shippingservice_15', 'cartservice_13']
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_27 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_16 | ['shippingservice_15']: χ²=0.000, df=0, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | ['shippingservice_15']: χ²=5.762, df=4, p=0.2177 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_15 | ['cartservice_13']: χ²=5.033, df=4, p=0.2839 → phụ thuộc, giữ
    - PC #7: α=0.710, cột ['shippingservice_26', 'shippingservice_15', 'cartservice_13', 'cartservice_27', 'shippingservice_16'], số bin {'shippingservice_26': 5, 'shippingservice_15': 5, 'cartservice_13': 5, 'cartservice_27': 5, 'shippingservice_16': 5}, F kề: ['cartservice_13', 'shippingservice_16']
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_27 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_15 | ['cartservice_13']: χ²=5.033, df=4, p=0.2839 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_15 | ['shippingservice_16']: χ²=0.000, df=0, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | ['shippingservice_16']: χ²=5.762, df=4, p=0.2177 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_16 | ['cartservice_13']: χ²=5.033, df=4, p=0.2839 → phụ thuộc, giữ
    - PC #8: α=0.810, cột ['shippingservice_26', 'shippingservice_15', 'cartservice_13', 'cartservice_27', 'shippingservice_16'], số bin {'shippingservice_26': 5, 'shippingservice_15': 5, 'cartservice_13': 5, 'cartservice_27': 5, 'shippingservice_16': 5}, F kề: ['cartservice_13', 'shippingservice_16']
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_27 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_15 | ['cartservice_13']: χ²=5.033, df=4, p=0.2839 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_15 | ['shippingservice_16']: χ²=0.000, df=0, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_16 | ['cartservice_13']: χ²=5.033, df=4, p=0.2839 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_13 | ['shippingservice_16']: χ²=5.762, df=4, p=0.2177 → phụ thuộc, giữ
    - PC #9: α=0.910, cột ['shippingservice_26', 'shippingservice_15', 'cartservice_13', 'cartservice_27', 'shippingservice_16'], số bin {'shippingservice_26': 5, 'shippingservice_15': 5, 'cartservice_13': 5, 'cartservice_27': 5, 'shippingservice_16': 5}, F kề: ['shippingservice_26', 'cartservice_13', 'shippingservice_16']
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_27 | []: χ²=1.562, df=4, p=0.8156 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_27 | ['shippingservice_26']: χ²=0.000, df=0, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_15 | ['shippingservice_26']: χ²=8.539, df=9, p=0.4808 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_15 | ['cartservice_13']: χ²=5.033, df=4, p=0.2839 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_15 | ['shippingservice_16']: χ²=0.000, df=0, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_26 | ['cartservice_13']: χ²=3.795, df=6, p=0.7043 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_26 | ['shippingservice_16']: χ²=7.281, df=9, p=0.6078 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_16 | ['shippingservice_26']: χ²=8.539, df=9, p=0.4808 → phụ thuộc, giữ
      - ... 6 phép kiểm nữa
    - PC #10: α=0.010, cột ['cartservice_5', 'shippingservice_25', 'cartservice_17'], số bin {'cartservice_5': 5, 'shippingservice_25': 5, 'cartservice_17': 4}, F kề: []
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_5 | []: χ²=1.111, df=4, p=0.8925 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_17 | []: χ²=0.000, df=2, p=1 → độc lập, bỏ cạnh
    - PC #11: α=0.110, cột ['cartservice_5', 'shippingservice_25', 'cartservice_17'], số bin {'cartservice_5': 5, 'shippingservice_25': 5, 'cartservice_17': 4}, F kề: []
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_17 | []: χ²=0.000, df=2, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_5 | []: χ²=1.111, df=4, p=0.8925 → độc lập, bỏ cạnh
    - PC #12: α=0.210, cột ['cartservice_5', 'shippingservice_25', 'cartservice_17'], số bin {'cartservice_5': 5, 'shippingservice_25': 5, 'cartservice_17': 4}, F kề: []
      - kiểm F ⊥ cartservice_17 | []: χ²=0.000, df=2, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_5 | []: χ²=1.111, df=4, p=0.8925 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #13: α=0.310, cột ['cartservice_5', 'shippingservice_25', 'cartservice_17'], số bin {'cartservice_5': 5, 'shippingservice_25': 5, 'cartservice_17': 4}, F kề: []
      - kiểm F ⊥ cartservice_17 | []: χ²=0.000, df=2, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_5 | []: χ²=1.111, df=4, p=0.8925 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #14: α=0.410, cột ['cartservice_5', 'shippingservice_25', 'cartservice_17'], số bin {'cartservice_5': 5, 'shippingservice_25': 5, 'cartservice_17': 4}, F kề: []
      - kiểm F ⊥ cartservice_17 | []: χ²=0.000, df=2, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_5 | []: χ²=1.111, df=4, p=0.8925 → độc lập, bỏ cạnh
    - PC #15: α=0.510, cột ['cartservice_5', 'shippingservice_25', 'cartservice_17'], số bin {'cartservice_5': 5, 'shippingservice_25': 5, 'cartservice_17': 4}, F kề: []
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_17 | []: χ²=0.000, df=2, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_5 | []: χ²=1.111, df=4, p=0.8925 → độc lập, bỏ cạnh
    - PC #16: α=0.610, cột ['cartservice_5', 'shippingservice_25', 'cartservice_17'], số bin {'cartservice_5': 5, 'shippingservice_25': 5, 'cartservice_17': 4}, F kề: []
      - kiểm F ⊥ cartservice_17 | []: χ²=0.000, df=2, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_5 | []: χ²=1.111, df=4, p=0.8925 → độc lập, bỏ cạnh
    - PC #17: α=0.710, cột ['cartservice_5', 'shippingservice_25', 'cartservice_17'], số bin {'cartservice_5': 5, 'shippingservice_25': 5, 'cartservice_17': 4}, F kề: []
      - kiểm F ⊥ cartservice_17 | []: χ²=0.000, df=2, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_5 | []: χ²=1.111, df=4, p=0.8925 → độc lập, bỏ cạnh
    - PC #18: α=0.810, cột ['cartservice_5', 'shippingservice_25', 'cartservice_17'], số bin {'cartservice_5': 5, 'shippingservice_25': 5, 'cartservice_17': 4}, F kề: []
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_17 | []: χ²=0.000, df=2, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_5 | []: χ²=1.111, df=4, p=0.8925 → độc lập, bỏ cạnh
    - PC #19: α=0.910, cột ['cartservice_5', 'shippingservice_25', 'cartservice_17'], số bin {'cartservice_5': 5, 'shippingservice_25': 5, 'cartservice_17': 4}, F kề: ['cartservice_5', 'shippingservice_25']
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_17 | []: χ²=0.000, df=2, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_5 | []: χ²=1.111, df=4, p=0.8925 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_25 | ['cartservice_5']: χ²=10.262, df=9, p=0.3297 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_5 | ['shippingservice_25']: χ²=9.785, df=9, p=0.3682 → phụ thuộc, giữ
    - PC #20: α=0.010, cột ['cartservice_13', 'cartservice_5', 'shippingservice_15', 'shippingservice_16', 'shippingservice_26'], số bin {'cartservice_13': 5, 'cartservice_5': 5, 'shippingservice_15': 5, 'shippingservice_16': 5, 'shippingservice_26': 5}, F kề: []
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_5 | []: χ²=1.111, df=4, p=0.8925 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
    - PC #21: α=0.110, cột ['cartservice_13', 'cartservice_5', 'shippingservice_15', 'shippingservice_16', 'shippingservice_26'], số bin {'cartservice_13': 5, 'cartservice_5': 5, 'shippingservice_15': 5, 'shippingservice_16': 5, 'shippingservice_26': 5}, F kề: []
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_5 | []: χ²=1.111, df=4, p=0.8925 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
    - PC #22: α=0.210, cột ['cartservice_13', 'cartservice_5', 'shippingservice_15', 'shippingservice_16', 'shippingservice_26'], số bin {'cartservice_13': 5, 'cartservice_5': 5, 'shippingservice_15': 5, 'shippingservice_16': 5, 'shippingservice_26': 5}, F kề: []
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_5 | []: χ²=1.111, df=4, p=0.8925 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
    - PC #23: α=0.310, cột ['cartservice_13', 'cartservice_5', 'shippingservice_15', 'shippingservice_16', 'shippingservice_26'], số bin {'cartservice_13': 5, 'cartservice_5': 5, 'shippingservice_15': 5, 'shippingservice_16': 5, 'shippingservice_26': 5}, F kề: []
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_5 | []: χ²=1.111, df=4, p=0.8925 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
    - PC #24: α=0.410, cột ['cartservice_13', 'cartservice_5', 'shippingservice_15', 'shippingservice_16', 'shippingservice_26'], số bin {'cartservice_13': 5, 'cartservice_5': 5, 'shippingservice_15': 5, 'shippingservice_16': 5, 'shippingservice_26': 5}, F kề: []
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_5 | []: χ²=1.111, df=4, p=0.8925 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
    - PC #25: α=0.510, cột ['cartservice_13', 'cartservice_5', 'shippingservice_15', 'shippingservice_16', 'shippingservice_26'], số bin {'cartservice_13': 5, 'cartservice_5': 5, 'shippingservice_15': 5, 'shippingservice_16': 5, 'shippingservice_26': 5}, F kề: []
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_5 | []: χ²=1.111, df=4, p=0.8925 → độc lập, bỏ cạnh
    - PC #26: α=0.610, cột ['cartservice_13', 'cartservice_5', 'shippingservice_15', 'shippingservice_16', 'shippingservice_26'], số bin {'cartservice_13': 5, 'cartservice_5': 5, 'shippingservice_15': 5, 'shippingservice_16': 5, 'shippingservice_26': 5}, F kề: ['cartservice_13', 'shippingservice_16']
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_5 | []: χ²=1.111, df=4, p=0.8925 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_13 | ['shippingservice_15']: χ²=5.762, df=4, p=0.2177 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_13 | ['shippingservice_16']: χ²=5.762, df=4, p=0.2177 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_15 | ['cartservice_13']: χ²=5.033, df=4, p=0.2839 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_15 | ['shippingservice_16']: χ²=0.000, df=0, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_16 | ['cartservice_13']: χ²=5.033, df=4, p=0.2839 → phụ thuộc, giữ
    - PC #27: α=0.710, cột ['cartservice_13', 'cartservice_5', 'shippingservice_15', 'shippingservice_16', 'shippingservice_26'], số bin {'cartservice_13': 5, 'cartservice_5': 5, 'shippingservice_15': 5, 'shippingservice_16': 5, 'shippingservice_26': 5}, F kề: ['cartservice_13', 'shippingservice_15']
      - kiểm F ⊥ cartservice_5 | []: χ²=1.111, df=4, p=0.8925 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_16 | ['cartservice_13']: χ²=5.033, df=4, p=0.2839 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_16 | ['shippingservice_15']: χ²=0.000, df=0, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_15 | ['cartservice_13']: χ²=5.033, df=4, p=0.2839 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_13 | ['shippingservice_15']: χ²=5.762, df=4, p=0.2177 → phụ thuộc, giữ
    - PC #28: α=0.810, cột ['cartservice_13', 'cartservice_5', 'shippingservice_15', 'shippingservice_16', 'shippingservice_26'], số bin {'cartservice_13': 5, 'cartservice_5': 5, 'shippingservice_15': 5, 'shippingservice_16': 5, 'shippingservice_26': 5}, F kề: ['cartservice_13', 'shippingservice_16']
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_5 | []: χ²=1.111, df=4, p=0.8925 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_15 | ['cartservice_13']: χ²=5.033, df=4, p=0.2839 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_15 | ['shippingservice_16']: χ²=0.000, df=0, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | ['shippingservice_16']: χ²=5.762, df=4, p=0.2177 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_16 | ['cartservice_13']: χ²=5.033, df=4, p=0.2839 → phụ thuộc, giữ
    - PC #29: α=0.910, cột ['cartservice_13', 'cartservice_5', 'shippingservice_15', 'shippingservice_16', 'shippingservice_26'], số bin {'cartservice_13': 5, 'cartservice_5': 5, 'shippingservice_15': 5, 'shippingservice_16': 5, 'shippingservice_26': 5}, F kề: ['cartservice_13', 'shippingservice_15', 'shippingservice_26']
      - kiểm F ⊥ cartservice_5 | []: χ²=1.111, df=4, p=0.8925 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_5 | ['cartservice_13']: χ²=1.510, df=5, p=0.9119 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_26 | ['cartservice_13']: χ²=3.795, df=6, p=0.7043 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_26 | ['shippingservice_15']: χ²=7.281, df=9, p=0.6078 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_26 | ['shippingservice_16']: χ²=7.281, df=9, p=0.6078 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_16 | ['cartservice_13']: χ²=5.033, df=4, p=0.2839 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_16 | ['shippingservice_15']: χ²=0.000, df=0, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_15 | ['cartservice_13']: χ²=5.033, df=4, p=0.2839 → phụ thuộc, giữ
      - ... 6 phép kiểm nữa
    - PC #30: α=0.010, cột ['shippingservice_25'], số bin {'shippingservice_25': 5}, F kề: []
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #31: α=0.110, cột ['shippingservice_25'], số bin {'shippingservice_25': 5}, F kề: []
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #32: α=0.210, cột ['shippingservice_25'], số bin {'shippingservice_25': 5}, F kề: []
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #33: α=0.310, cột ['shippingservice_25'], số bin {'shippingservice_25': 5}, F kề: []
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #34: α=0.410, cột ['shippingservice_25'], số bin {'shippingservice_25': 5}, F kề: []
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #35: α=0.510, cột ['shippingservice_25'], số bin {'shippingservice_25': 5}, F kề: []
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #36: α=0.610, cột ['shippingservice_25'], số bin {'shippingservice_25': 5}, F kề: []
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #37: α=0.710, cột ['shippingservice_25'], số bin {'shippingservice_25': 5}, F kề: []
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #38: α=0.810, cột ['shippingservice_25'], số bin {'shippingservice_25': 5}, F kề: []
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #39: α=0.910, cột ['shippingservice_25'], số bin {'shippingservice_25': 5}, F kề: ['shippingservice_25']
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → phụ thuộc, giữ
    - PC #40: α=0.001, cột ['cartservice_13', 'shippingservice_16', 'shippingservice_15', 'shippingservice_26', 'shippingservice_25'], số bin {'cartservice_13': 5, 'shippingservice_16': 5, 'shippingservice_15': 5, 'shippingservice_26': 5, 'shippingservice_25': 5}, F kề: []
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
    - PC #41: α=0.101, cột ['cartservice_13', 'shippingservice_16', 'shippingservice_15', 'shippingservice_26', 'shippingservice_25'], số bin {'cartservice_13': 5, 'shippingservice_16': 5, 'shippingservice_15': 5, 'shippingservice_26': 5, 'shippingservice_25': 5}, F kề: []
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #42: α=0.201, cột ['cartservice_13', 'shippingservice_16', 'shippingservice_15', 'shippingservice_26', 'shippingservice_25'], số bin {'cartservice_13': 5, 'shippingservice_16': 5, 'shippingservice_15': 5, 'shippingservice_26': 5, 'shippingservice_25': 5}, F kề: []
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
    - PC #43: α=0.301, cột ['cartservice_13', 'shippingservice_16', 'shippingservice_15', 'shippingservice_26', 'shippingservice_25'], số bin {'cartservice_13': 5, 'shippingservice_16': 5, 'shippingservice_15': 5, 'shippingservice_26': 5, 'shippingservice_25': 5}, F kề: []
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
    - PC #44: α=0.401, cột ['cartservice_13', 'shippingservice_16', 'shippingservice_15', 'shippingservice_26', 'shippingservice_25'], số bin {'cartservice_13': 5, 'shippingservice_16': 5, 'shippingservice_15': 5, 'shippingservice_26': 5, 'shippingservice_25': 5}, F kề: []
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #45: α=0.501, cột ['cartservice_13', 'shippingservice_16', 'shippingservice_15', 'shippingservice_26', 'shippingservice_25'], số bin {'cartservice_13': 5, 'shippingservice_16': 5, 'shippingservice_15': 5, 'shippingservice_26': 5, 'shippingservice_25': 5}, F kề: []
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #46: α=0.601, cột ['cartservice_13', 'shippingservice_16', 'shippingservice_15', 'shippingservice_26', 'shippingservice_25'], số bin {'cartservice_13': 5, 'shippingservice_16': 5, 'shippingservice_15': 5, 'shippingservice_26': 5, 'shippingservice_25': 5}, F kề: ['cartservice_13', 'shippingservice_16']
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | ['shippingservice_16']: χ²=5.762, df=4, p=0.2177 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_13 | ['shippingservice_15']: χ²=5.762, df=4, p=0.2177 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_15 | ['cartservice_13']: χ²=5.033, df=4, p=0.2839 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_15 | ['shippingservice_16']: χ²=0.000, df=0, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_16 | ['cartservice_13']: χ²=5.033, df=4, p=0.2839 → phụ thuộc, giữ
    - PC #47: α=0.701, cột ['cartservice_13', 'shippingservice_16', 'shippingservice_15', 'shippingservice_26', 'shippingservice_25'], số bin {'cartservice_13': 5, 'shippingservice_16': 5, 'shippingservice_15': 5, 'shippingservice_26': 5, 'shippingservice_25': 5}, F kề: ['cartservice_13', 'shippingservice_15']
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_13 | ['shippingservice_16']: χ²=5.762, df=4, p=0.2177 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_13 | ['shippingservice_15']: χ²=5.762, df=4, p=0.2177 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_16 | ['cartservice_13']: χ²=5.033, df=4, p=0.2839 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_16 | ['shippingservice_15']: χ²=0.000, df=0, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_15 | ['cartservice_13']: χ²=5.033, df=4, p=0.2839 → phụ thuộc, giữ
    - PC #48: α=0.801, cột ['cartservice_13', 'shippingservice_16', 'shippingservice_15', 'shippingservice_26', 'shippingservice_25'], số bin {'cartservice_13': 5, 'shippingservice_16': 5, 'shippingservice_15': 5, 'shippingservice_26': 5, 'shippingservice_25': 5}, F kề: ['cartservice_13', 'shippingservice_16']
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_15 | ['cartservice_13']: χ²=5.033, df=4, p=0.2839 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_15 | ['shippingservice_16']: χ²=0.000, df=0, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | ['shippingservice_16']: χ²=5.762, df=4, p=0.2177 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_16 | ['cartservice_13']: χ²=5.033, df=4, p=0.2839 → phụ thuộc, giữ
    - PC #49: α=0.901, cột ['cartservice_13', 'shippingservice_16', 'shippingservice_15', 'shippingservice_26', 'shippingservice_25'], số bin {'cartservice_13': 5, 'shippingservice_16': 5, 'shippingservice_15': 5, 'shippingservice_26': 5, 'shippingservice_25': 5}, F kề: ['cartservice_13', 'shippingservice_15', 'shippingservice_26']
      - kiểm F ⊥ shippingservice_15 | []: χ²=2.929, df=4, p=0.5698 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_26 | []: χ²=1.562, df=4, p=0.8156 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_16 | []: χ²=2.929, df=4, p=0.5698 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_25 | []: χ²=1.562, df=4, p=0.8156 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_13 | []: χ²=3.245, df=4, p=0.5177 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_25 | ['cartservice_13']: χ²=3.795, df=6, p=0.7043 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_25 | ['shippingservice_16']: χ²=7.281, df=9, p=0.6078 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_25 | ['shippingservice_15']: χ²=7.281, df=9, p=0.6078 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_25 | ['shippingservice_26']: χ²=0.000, df=0, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_16 | ['cartservice_13']: χ²=5.033, df=4, p=0.2839 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_16 | ['shippingservice_15']: χ²=0.000, df=0, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_26 | ['cartservice_13']: χ²=3.795, df=6, p=0.7043 → phụ thuộc, giữ
      - ... 8 phép kiểm nữa
- cụm 2 (điểm 0.0438): adservice 0.0372, currencyservice 0.0538, emailservice 0.0452, frontend 0.0511, paymentservice 0.0374, recommendationservice 0.0381
  - RCD nhận 21+21 dòng, 19 cột: ['currencyservice_1', 'frontend_2', 'frontend_3', 'currencyservice_4', 'frontend_6', 'frontend_7', 'frontend_8', 'adservice_9', 'frontend_10', 'recommendationservice_11', 'frontend_12', 'frontend_14', 'frontend_18', 'frontend_19', 'frontend_20', 'paymentservice_22', 'paymentservice_23', 'emailservice_28', 'frontend_30']
  - pha 1, mức với 19 cột, khối: [['frontend_14', 'recommendationservice_11', 'frontend_2', 'emailservice_28', 'frontend_3'], ['frontend_6', 'frontend_10', 'frontend_20', 'currencyservice_1', 'adservice_9'], ['frontend_7', 'frontend_19', 'paymentservice_23', 'frontend_8', 'frontend_18'], ['frontend_12', 'frontend_30', 'paymentservice_22', 'currencyservice_4']]
  - số lần chạy Ψ-PC: 28; RCD trả: ['frontend_18', 'frontend_3', 'adservice_9', 'frontend_12']; nội bộ: ['frontend', 'adservice']; dự phòng: True
    - PC #0: α=0.010, cột ['frontend_14', 'recommendationservice_11', 'frontend_2', 'emailservice_28', 'frontend_3'], số bin {'frontend_14': 5, 'recommendationservice_11': 5, 'frontend_2': 5, 'emailservice_28': 5, 'frontend_3': 5}, F kề: []
      - kiểm F ⊥ recommendationservice_11 | []: χ²=2.803, df=4, p=0.5912 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_2 | []: χ²=1.200, df=4, p=0.8781 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_14 | []: χ²=1.285, df=4, p=0.8639 → độc lập, bỏ cạnh
      - kiểm F ⊥ emailservice_28 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_3 | []: χ²=4.086, df=4, p=0.3945 → độc lập, bỏ cạnh
    - PC #1: α=0.110, cột ['frontend_14', 'recommendationservice_11', 'frontend_2', 'emailservice_28', 'frontend_3'], số bin {'frontend_14': 5, 'recommendationservice_11': 5, 'frontend_2': 5, 'emailservice_28': 5, 'frontend_3': 5}, F kề: []
      - kiểm F ⊥ frontend_14 | []: χ²=1.285, df=4, p=0.8639 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_2 | []: χ²=1.200, df=4, p=0.8781 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_11 | []: χ²=2.803, df=4, p=0.5912 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_3 | []: χ²=4.086, df=4, p=0.3945 → độc lập, bỏ cạnh
      - kiểm F ⊥ emailservice_28 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #2: α=0.210, cột ['frontend_14', 'recommendationservice_11', 'frontend_2', 'emailservice_28', 'frontend_3'], số bin {'frontend_14': 5, 'recommendationservice_11': 5, 'frontend_2': 5, 'emailservice_28': 5, 'frontend_3': 5}, F kề: []
      - kiểm F ⊥ frontend_3 | []: χ²=4.086, df=4, p=0.3945 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_11 | []: χ²=2.803, df=4, p=0.5912 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_14 | []: χ²=1.285, df=4, p=0.8639 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_2 | []: χ²=1.200, df=4, p=0.8781 → độc lập, bỏ cạnh
      - kiểm F ⊥ emailservice_28 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #3: α=0.310, cột ['frontend_14', 'recommendationservice_11', 'frontend_2', 'emailservice_28', 'frontend_3'], số bin {'frontend_14': 5, 'recommendationservice_11': 5, 'frontend_2': 5, 'emailservice_28': 5, 'frontend_3': 5}, F kề: []
      - kiểm F ⊥ frontend_14 | []: χ²=1.285, df=4, p=0.8639 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_2 | []: χ²=1.200, df=4, p=0.8781 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_11 | []: χ²=2.803, df=4, p=0.5912 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_3 | []: χ²=4.086, df=4, p=0.3945 → độc lập, bỏ cạnh
      - kiểm F ⊥ emailservice_28 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #4: α=0.410, cột ['frontend_14', 'recommendationservice_11', 'frontend_2', 'emailservice_28', 'frontend_3'], số bin {'frontend_14': 5, 'recommendationservice_11': 5, 'frontend_2': 5, 'emailservice_28': 5, 'frontend_3': 5}, F kề: ['frontend_3']
      - kiểm F ⊥ frontend_3 | []: χ²=4.086, df=4, p=0.3945 → phụ thuộc, giữ
      - kiểm F ⊥ frontend_14 | []: χ²=1.285, df=4, p=0.8639 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_2 | []: χ²=1.200, df=4, p=0.8781 → độc lập, bỏ cạnh
      - kiểm F ⊥ emailservice_28 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_11 | []: χ²=2.803, df=4, p=0.5912 → độc lập, bỏ cạnh
    - PC #5: α=0.010, cột ['frontend_6', 'frontend_10', 'frontend_20', 'currencyservice_1', 'adservice_9'], số bin {'frontend_6': 5, 'frontend_10': 5, 'frontend_20': 5, 'currencyservice_1': 5, 'adservice_9': 5}, F kề: []
      - kiểm F ⊥ adservice_9 | []: χ²=3.543, df=4, p=0.4714 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_1 | []: χ²=1.954, df=4, p=0.7443 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_10 | []: χ²=0.410, df=4, p=0.9816 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_6 | []: χ²=0.619, df=4, p=0.9609 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_20 | []: χ²=1.000, df=4, p=0.9098 → độc lập, bỏ cạnh
    - PC #6: α=0.110, cột ['frontend_6', 'frontend_10', 'frontend_20', 'currencyservice_1', 'adservice_9'], số bin {'frontend_6': 5, 'frontend_10': 5, 'frontend_20': 5, 'currencyservice_1': 5, 'adservice_9': 5}, F kề: []
      - kiểm F ⊥ frontend_6 | []: χ²=0.619, df=4, p=0.9609 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_20 | []: χ²=1.000, df=4, p=0.9098 → độc lập, bỏ cạnh
      - kiểm F ⊥ adservice_9 | []: χ²=3.543, df=4, p=0.4714 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_10 | []: χ²=0.410, df=4, p=0.9816 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_1 | []: χ²=1.954, df=4, p=0.7443 → độc lập, bỏ cạnh
    - PC #7: α=0.210, cột ['frontend_6', 'frontend_10', 'frontend_20', 'currencyservice_1', 'adservice_9'], số bin {'frontend_6': 5, 'frontend_10': 5, 'frontend_20': 5, 'currencyservice_1': 5, 'adservice_9': 5}, F kề: []
      - kiểm F ⊥ adservice_9 | []: χ²=3.543, df=4, p=0.4714 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_1 | []: χ²=1.954, df=4, p=0.7443 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_20 | []: χ²=1.000, df=4, p=0.9098 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_6 | []: χ²=0.619, df=4, p=0.9609 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_10 | []: χ²=0.410, df=4, p=0.9816 → độc lập, bỏ cạnh
    - PC #8: α=0.310, cột ['frontend_6', 'frontend_10', 'frontend_20', 'currencyservice_1', 'adservice_9'], số bin {'frontend_6': 5, 'frontend_10': 5, 'frontend_20': 5, 'currencyservice_1': 5, 'adservice_9': 5}, F kề: []
      - kiểm F ⊥ frontend_20 | []: χ²=1.000, df=4, p=0.9098 → độc lập, bỏ cạnh
      - kiểm F ⊥ adservice_9 | []: χ²=3.543, df=4, p=0.4714 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_1 | []: χ²=1.954, df=4, p=0.7443 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_10 | []: χ²=0.410, df=4, p=0.9816 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_6 | []: χ²=0.619, df=4, p=0.9609 → độc lập, bỏ cạnh
    - PC #9: α=0.410, cột ['frontend_6', 'frontend_10', 'frontend_20', 'currencyservice_1', 'adservice_9'], số bin {'frontend_6': 5, 'frontend_10': 5, 'frontend_20': 5, 'currencyservice_1': 5, 'adservice_9': 5}, F kề: []
      - kiểm F ⊥ currencyservice_1 | []: χ²=1.954, df=4, p=0.7443 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_10 | []: χ²=0.410, df=4, p=0.9816 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_20 | []: χ²=1.000, df=4, p=0.9098 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_6 | []: χ²=0.619, df=4, p=0.9609 → độc lập, bỏ cạnh
      - kiểm F ⊥ adservice_9 | []: χ²=3.543, df=4, p=0.4714 → độc lập, bỏ cạnh
    - PC #10: α=0.510, cột ['frontend_6', 'frontend_10', 'frontend_20', 'currencyservice_1', 'adservice_9'], số bin {'frontend_6': 5, 'frontend_10': 5, 'frontend_20': 5, 'currencyservice_1': 5, 'adservice_9': 5}, F kề: ['adservice_9']
      - kiểm F ⊥ currencyservice_1 | []: χ²=1.954, df=4, p=0.7443 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_10 | []: χ²=0.410, df=4, p=0.9816 → độc lập, bỏ cạnh
      - kiểm F ⊥ adservice_9 | []: χ²=3.543, df=4, p=0.4714 → phụ thuộc, giữ
      - kiểm F ⊥ frontend_20 | []: χ²=1.000, df=4, p=0.9098 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_6 | []: χ²=0.619, df=4, p=0.9609 → độc lập, bỏ cạnh
    - PC #11: α=0.010, cột ['frontend_7', 'frontend_19', 'paymentservice_23', 'frontend_8', 'frontend_18'], số bin {'frontend_7': 5, 'frontend_19': 5, 'paymentservice_23': 5, 'frontend_8': 5, 'frontend_18': 5}, F kề: []
      - kiểm F ⊥ paymentservice_23 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_8 | []: χ²=0.619, df=4, p=0.9609 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_7 | []: χ²=0.619, df=4, p=0.9609 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_18 | []: χ²=5.876, df=4, p=0.2086 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_19 | []: χ²=2.053, df=4, p=0.7261 → độc lập, bỏ cạnh
    - PC #12: α=0.110, cột ['frontend_7', 'frontend_19', 'paymentservice_23', 'frontend_8', 'frontend_18'], số bin {'frontend_7': 5, 'frontend_19': 5, 'paymentservice_23': 5, 'frontend_8': 5, 'frontend_18': 5}, F kề: []
      - kiểm F ⊥ frontend_19 | []: χ²=2.053, df=4, p=0.7261 → độc lập, bỏ cạnh
      - kiểm F ⊥ paymentservice_23 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_18 | []: χ²=5.876, df=4, p=0.2086 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_8 | []: χ²=0.619, df=4, p=0.9609 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_7 | []: χ²=0.619, df=4, p=0.9609 → độc lập, bỏ cạnh
    - PC #13: α=0.210, cột ['frontend_7', 'frontend_19', 'paymentservice_23', 'frontend_8', 'frontend_18'], số bin {'frontend_7': 5, 'frontend_19': 5, 'paymentservice_23': 5, 'frontend_8': 5, 'frontend_18': 5}, F kề: ['frontend_18']
      - kiểm F ⊥ frontend_8 | []: χ²=0.619, df=4, p=0.9609 → độc lập, bỏ cạnh
      - kiểm F ⊥ paymentservice_23 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_19 | []: χ²=2.053, df=4, p=0.7261 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_7 | []: χ²=0.619, df=4, p=0.9609 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_18 | []: χ²=5.876, df=4, p=0.2086 → phụ thuộc, giữ
    - PC #14: α=0.010, cột ['frontend_12', 'frontend_30', 'paymentservice_22', 'currencyservice_4'], số bin {'frontend_12': 5, 'frontend_30': 5, 'paymentservice_22': 5, 'currencyservice_4': 5}, F kề: []
      - kiểm F ⊥ paymentservice_22 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_30 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_12 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_4 | []: χ²=1.000, df=4, p=0.9098 → độc lập, bỏ cạnh
    - PC #15: α=0.110, cột ['frontend_12', 'frontend_30', 'paymentservice_22', 'currencyservice_4'], số bin {'frontend_12': 5, 'frontend_30': 5, 'paymentservice_22': 5, 'currencyservice_4': 5}, F kề: []
      - kiểm F ⊥ frontend_12 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_30 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_4 | []: χ²=1.000, df=4, p=0.9098 → độc lập, bỏ cạnh
      - kiểm F ⊥ paymentservice_22 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #16: α=0.210, cột ['frontend_12', 'frontend_30', 'paymentservice_22', 'currencyservice_4'], số bin {'frontend_12': 5, 'frontend_30': 5, 'paymentservice_22': 5, 'currencyservice_4': 5}, F kề: []
      - kiểm F ⊥ paymentservice_22 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_12 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_4 | []: χ²=1.000, df=4, p=0.9098 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_30 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #17: α=0.310, cột ['frontend_12', 'frontend_30', 'paymentservice_22', 'currencyservice_4'], số bin {'frontend_12': 5, 'frontend_30': 5, 'paymentservice_22': 5, 'currencyservice_4': 5}, F kề: []
      - kiểm F ⊥ paymentservice_22 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_12 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_4 | []: χ²=1.000, df=4, p=0.9098 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_30 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #18: α=0.410, cột ['frontend_12', 'frontend_30', 'paymentservice_22', 'currencyservice_4'], số bin {'frontend_12': 5, 'frontend_30': 5, 'paymentservice_22': 5, 'currencyservice_4': 5}, F kề: []
      - kiểm F ⊥ frontend_12 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_4 | []: χ²=1.000, df=4, p=0.9098 → độc lập, bỏ cạnh
      - kiểm F ⊥ paymentservice_22 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_30 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #19: α=0.510, cột ['frontend_12', 'frontend_30', 'paymentservice_22', 'currencyservice_4'], số bin {'frontend_12': 5, 'frontend_30': 5, 'paymentservice_22': 5, 'currencyservice_4': 5}, F kề: []
      - kiểm F ⊥ currencyservice_4 | []: χ²=1.000, df=4, p=0.9098 → độc lập, bỏ cạnh
      - kiểm F ⊥ paymentservice_22 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_12 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_30 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #20: α=0.610, cột ['frontend_12', 'frontend_30', 'paymentservice_22', 'currencyservice_4'], số bin {'frontend_12': 5, 'frontend_30': 5, 'paymentservice_22': 5, 'currencyservice_4': 5}, F kề: ['frontend_12']
      - kiểm F ⊥ paymentservice_22 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_12 | []: χ²=3.245, df=4, p=0.5177 → phụ thuộc, giữ
      - kiểm F ⊥ currencyservice_4 | []: χ²=1.000, df=4, p=0.9098 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_30 | []: χ²=1.562, df=4, p=0.8156 → độc lập, bỏ cạnh
    - PC #21: α=0.001, cột ['frontend_3', 'adservice_9', 'frontend_18', 'frontend_12'], số bin {'frontend_3': 5, 'adservice_9': 5, 'frontend_18': 5, 'frontend_12': 5}, F kề: []
      - kiểm F ⊥ frontend_3 | []: χ²=4.086, df=4, p=0.3945 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_18 | []: χ²=5.876, df=4, p=0.2086 → độc lập, bỏ cạnh
      - kiểm F ⊥ adservice_9 | []: χ²=3.543, df=4, p=0.4714 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_12 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
    - PC #22: α=0.101, cột ['frontend_3', 'adservice_9', 'frontend_18', 'frontend_12'], số bin {'frontend_3': 5, 'adservice_9': 5, 'frontend_18': 5, 'frontend_12': 5}, F kề: []
      - kiểm F ⊥ adservice_9 | []: χ²=3.543, df=4, p=0.4714 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_3 | []: χ²=4.086, df=4, p=0.3945 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_18 | []: χ²=5.876, df=4, p=0.2086 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_12 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
    - PC #23: α=0.201, cột ['frontend_3', 'adservice_9', 'frontend_18', 'frontend_12'], số bin {'frontend_3': 5, 'adservice_9': 5, 'frontend_18': 5, 'frontend_12': 5}, F kề: []
      - kiểm F ⊥ frontend_3 | []: χ²=4.086, df=4, p=0.3945 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_12 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_18 | []: χ²=5.876, df=4, p=0.2086 → độc lập, bỏ cạnh
      - kiểm F ⊥ adservice_9 | []: χ²=3.543, df=4, p=0.4714 → độc lập, bỏ cạnh
    - PC #24: α=0.301, cột ['frontend_3', 'adservice_9', 'frontend_18', 'frontend_12'], số bin {'frontend_3': 5, 'adservice_9': 5, 'frontend_18': 5, 'frontend_12': 5}, F kề: ['frontend_18']
      - kiểm F ⊥ frontend_12 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
      - kiểm F ⊥ adservice_9 | []: χ²=3.543, df=4, p=0.4714 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_3 | []: χ²=4.086, df=4, p=0.3945 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_18 | []: χ²=5.876, df=4, p=0.2086 → phụ thuộc, giữ
    - PC #25: α=0.401, cột ['frontend_3', 'adservice_9', 'frontend_18', 'frontend_12'], số bin {'frontend_3': 5, 'adservice_9': 5, 'frontend_18': 5, 'frontend_12': 5}, F kề: ['frontend_3', 'frontend_18']
      - kiểm F ⊥ frontend_3 | []: χ²=4.086, df=4, p=0.3945 → phụ thuộc, giữ
      - kiểm F ⊥ frontend_18 | []: χ²=5.876, df=4, p=0.2086 → phụ thuộc, giữ
      - kiểm F ⊥ adservice_9 | []: χ²=3.543, df=4, p=0.4714 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_12 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_3 | ['frontend_18']: χ²=10.673, df=8, p=0.2209 → phụ thuộc, giữ
      - kiểm F ⊥ frontend_18 | ['frontend_3']: χ²=12.735, df=8, p=0.1213 → phụ thuộc, giữ
    - PC #26: α=0.501, cột ['frontend_3', 'adservice_9', 'frontend_18', 'frontend_12'], số bin {'frontend_3': 5, 'adservice_9': 5, 'frontend_18': 5, 'frontend_12': 5}, F kề: ['frontend_3', 'frontend_18']
      - kiểm F ⊥ frontend_18 | []: χ²=5.876, df=4, p=0.2086 → phụ thuộc, giữ
      - kiểm F ⊥ frontend_3 | []: χ²=4.086, df=4, p=0.3945 → phụ thuộc, giữ
      - kiểm F ⊥ frontend_12 | []: χ²=3.245, df=4, p=0.5177 → độc lập, bỏ cạnh
      - kiểm F ⊥ adservice_9 | []: χ²=3.543, df=4, p=0.4714 → phụ thuộc, giữ
      - kiểm F ⊥ frontend_18 | ['frontend_3']: χ²=12.735, df=8, p=0.1213 → phụ thuộc, giữ
      - kiểm F ⊥ frontend_18 | ['adservice_9']: χ²=9.822, df=9, p=0.3651 → phụ thuộc, giữ
      - kiểm F ⊥ adservice_9 | ['frontend_3']: χ²=9.895, df=8, p=0.2725 → phụ thuộc, giữ
      - kiểm F ⊥ adservice_9 | ['frontend_18']: χ²=8.202, df=9, p=0.5139 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_3 | ['frontend_18']: χ²=10.673, df=8, p=0.2209 → phụ thuộc, giữ
    - PC #27: α=0.601, cột ['frontend_3', 'adservice_9', 'frontend_18', 'frontend_12'], số bin {'frontend_3': 5, 'adservice_9': 5, 'frontend_18': 5, 'frontend_12': 5}, F kề: ['frontend_3', 'adservice_9', 'frontend_18', 'frontend_12']
      - kiểm F ⊥ frontend_3 | []: χ²=4.086, df=4, p=0.3945 → phụ thuộc, giữ
      - kiểm F ⊥ frontend_18 | []: χ²=5.876, df=4, p=0.2086 → phụ thuộc, giữ
      - kiểm F ⊥ adservice_9 | []: χ²=3.543, df=4, p=0.4714 → phụ thuộc, giữ
      - kiểm F ⊥ frontend_12 | []: χ²=3.245, df=4, p=0.5177 → phụ thuộc, giữ
      - kiểm F ⊥ adservice_9 | ['frontend_3']: χ²=9.895, df=8, p=0.2725 → phụ thuộc, giữ
      - kiểm F ⊥ adservice_9 | ['frontend_18']: χ²=8.202, df=9, p=0.5139 → phụ thuộc, giữ
      - kiểm F ⊥ adservice_9 | ['frontend_12']: χ²=8.005, df=6, p=0.2378 → phụ thuộc, giữ
      - kiểm F ⊥ frontend_12 | ['frontend_3']: χ²=6.724, df=6, p=0.3471 → phụ thuộc, giữ
      - kiểm F ⊥ frontend_12 | ['adservice_9']: χ²=10.296, df=7, p=0.1724 → phụ thuộc, giữ
      - kiểm F ⊥ frontend_12 | ['frontend_18']: χ²=15.167, df=7, p=0.03392 → phụ thuộc, giữ
      - kiểm F ⊥ frontend_3 | ['adservice_9']: χ²=10.376, df=8, p=0.2396 → phụ thuộc, giữ
      - kiểm F ⊥ frontend_3 | ['frontend_18']: χ²=10.673, df=8, p=0.2209 → phụ thuộc, giữ
      - ... 20 phép kiểm nữa
- cụm 3 (điểm 0.0167): frontend-external 0.0011, health 0.0190, productcatalogservice 0.0183, redis 0.0061, traceservice 0.0391
  - RCD nhận 21+21 dòng, 0 cột: []
  - pha 1, mức với 0 cột, khối: []
  - số lần chạy Ψ-PC: 0; RCD trả: []; nội bộ: []; dự phòng: True

## Thứ hạng cuối

['checkoutservice_A', 'cartservice_A', 'shippingservice_A', 'currencyservice_A', 'frontend_A', 'emailservice_A', 'recommendationservice_A', 'paymentservice_A', 'adservice_A', 'traceservice_A', 'health_A', 'productcatalogservice_A', 'redis_A', 'frontend-external_A']
