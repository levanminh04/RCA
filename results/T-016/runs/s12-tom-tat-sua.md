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
    24,
    24
   ],
   "cot_moi_lan_pc": true,
   "du_lieu_roi_rac": true,
   "f_con": true,
   "p_value_sai_lech_max": 2.210064467819799e-15
  },
  {
   "services": true,
   "aa": 0.0,
   "rcd_ranks": true,
   "du_phong": true,
   "so_lan_pc": [
    34,
    34
   ],
   "cot_moi_lan_pc": true,
   "du_lieu_roi_rac": true,
   "f_con": true,
   "p_value_sai_lech_max": 1.0506969454505104e-15
  },
  {
   "services": true,
   "aa": 0.0,
   "rcd_ranks": true,
   "du_phong": true,
   "so_lan_pc": [
    43,
    43
   ],
   "cot_moi_lan_pc": true,
   "du_lieu_roi_rac": true,
   "f_con": true,
   "p_value_sai_lech_max": 7.876110541211517e-15
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
  - RCD nhận 20+20 dòng, 16 cột: ['cartservice_cpu', 'shippingservice_cpu', 'cartservice_mem', 'shippingservice_mem', 'cartservice_workload', 'shippingservice_workload', 'cartservice_latency', 'shippingservice_latency', 'cartservice_5', 'cartservice_13', 'shippingservice_15', 'shippingservice_16', 'cartservice_17', 'shippingservice_25', 'shippingservice_26', 'cartservice_27']
  - pha 1, mức với 16 cột, khối: [['shippingservice_cpu', 'cartservice_latency', 'cartservice_5', 'cartservice_13', 'shippingservice_25'], ['cartservice_workload', 'cartservice_mem', 'shippingservice_26', 'shippingservice_15', 'shippingservice_latency'], ['cartservice_27', 'shippingservice_16', 'shippingservice_mem', 'cartservice_cpu', 'shippingservice_workload'], ['cartservice_17']]
  - số lần chạy Ψ-PC: 24; RCD trả: ['cartservice_mem', 'cartservice_latency', 'shippingservice_16']; nội bộ: ['cartservice', 'shippingservice']; dự phòng: False
    - PC #0: α=0.010, cột ['shippingservice_cpu', 'cartservice_latency', 'cartservice_5', 'cartservice_13', 'shippingservice_25'], số bin {'shippingservice_cpu': 5, 'cartservice_latency': 5, 'cartservice_5': 5, 'cartservice_13': 5, 'shippingservice_25': 5}, F kề: []
      - kiểm F ⊥ shippingservice_25 | []: χ²=3.636, df=4, p=0.4574 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_cpu | []: χ²=3.034, df=4, p=0.5522 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | []: χ²=3.515, df=4, p=0.4756 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_5 | []: χ²=1.200, df=4, p=0.8781 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_latency | []: χ²=6.433, df=4, p=0.169 → độc lập, bỏ cạnh
    - PC #1: α=0.110, cột ['shippingservice_cpu', 'cartservice_latency', 'cartservice_5', 'cartservice_13', 'shippingservice_25'], số bin {'shippingservice_cpu': 5, 'cartservice_latency': 5, 'cartservice_5': 5, 'cartservice_13': 5, 'shippingservice_25': 5}, F kề: []
      - kiểm F ⊥ shippingservice_cpu | []: χ²=3.034, df=4, p=0.5522 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_5 | []: χ²=1.200, df=4, p=0.8781 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | []: χ²=3.515, df=4, p=0.4756 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_25 | []: χ²=3.636, df=4, p=0.4574 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_latency | []: χ²=6.433, df=4, p=0.169 → độc lập, bỏ cạnh
    - PC #2: α=0.210, cột ['shippingservice_cpu', 'cartservice_latency', 'cartservice_5', 'cartservice_13', 'shippingservice_25'], số bin {'shippingservice_cpu': 5, 'cartservice_latency': 5, 'cartservice_5': 5, 'cartservice_13': 5, 'shippingservice_25': 5}, F kề: ['cartservice_latency']
      - kiểm F ⊥ cartservice_5 | []: χ²=1.200, df=4, p=0.8781 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_13 | []: χ²=3.515, df=4, p=0.4756 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_25 | []: χ²=3.636, df=4, p=0.4574 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_latency | []: χ²=6.433, df=4, p=0.169 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_cpu | []: χ²=3.034, df=4, p=0.5522 → độc lập, bỏ cạnh
    - PC #3: α=0.010, cột ['cartservice_workload', 'cartservice_mem', 'shippingservice_26', 'shippingservice_15', 'shippingservice_latency'], số bin {'cartservice_workload': 5, 'cartservice_mem': 5, 'shippingservice_26': 5, 'shippingservice_15': 5, 'shippingservice_latency': 5}, F kề: []
      - kiểm F ⊥ shippingservice_26 | []: χ²=3.636, df=4, p=0.4574 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_latency | []: χ²=2.374, df=4, p=0.6674 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_mem | []: χ²=6.756, df=4, p=0.1494 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_15 | []: χ²=5.493, df=4, p=0.2404 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_workload | []: χ²=1.861, df=4, p=0.7613 → độc lập, bỏ cạnh
    - PC #4: α=0.110, cột ['cartservice_workload', 'cartservice_mem', 'shippingservice_26', 'shippingservice_15', 'shippingservice_latency'], số bin {'cartservice_workload': 5, 'cartservice_mem': 5, 'shippingservice_26': 5, 'shippingservice_15': 5, 'shippingservice_latency': 5}, F kề: []
      - kiểm F ⊥ shippingservice_15 | []: χ²=5.493, df=4, p=0.2404 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_mem | []: χ²=6.756, df=4, p=0.1494 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_latency | []: χ²=2.374, df=4, p=0.6674 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_26 | []: χ²=3.636, df=4, p=0.4574 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_workload | []: χ²=1.861, df=4, p=0.7613 → độc lập, bỏ cạnh
    - PC #5: α=0.210, cột ['cartservice_workload', 'cartservice_mem', 'shippingservice_26', 'shippingservice_15', 'shippingservice_latency'], số bin {'cartservice_workload': 5, 'cartservice_mem': 5, 'shippingservice_26': 5, 'shippingservice_15': 5, 'shippingservice_latency': 5}, F kề: ['cartservice_mem']
      - kiểm F ⊥ cartservice_workload | []: χ²=1.861, df=4, p=0.7613 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_latency | []: χ²=2.374, df=4, p=0.6674 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_26 | []: χ²=3.636, df=4, p=0.4574 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_mem | []: χ²=6.756, df=4, p=0.1494 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_15 | []: χ²=5.493, df=4, p=0.2404 → độc lập, bỏ cạnh
    - PC #6: α=0.010, cột ['cartservice_27', 'shippingservice_16', 'shippingservice_mem', 'cartservice_cpu', 'shippingservice_workload'], số bin {'cartservice_27': 5, 'shippingservice_16': 5, 'shippingservice_mem': 5, 'cartservice_cpu': 5, 'shippingservice_workload': 5}, F kề: []
      - kiểm F ⊥ shippingservice_workload | []: χ²=1.943, df=4, p=0.7463 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_mem | []: χ²=4.327, df=4, p=0.3635 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_cpu | []: χ²=2.459, df=4, p=0.652 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_16 | []: χ²=5.493, df=4, p=0.2404 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_27 | []: χ²=3.636, df=4, p=0.4574 → độc lập, bỏ cạnh
    - PC #7: α=0.110, cột ['cartservice_27', 'shippingservice_16', 'shippingservice_mem', 'cartservice_cpu', 'shippingservice_workload'], số bin {'cartservice_27': 5, 'shippingservice_16': 5, 'shippingservice_mem': 5, 'cartservice_cpu': 5, 'shippingservice_workload': 5}, F kề: []
      - kiểm F ⊥ shippingservice_16 | []: χ²=5.493, df=4, p=0.2404 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_workload | []: χ²=1.943, df=4, p=0.7463 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_mem | []: χ²=4.327, df=4, p=0.3635 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_cpu | []: χ²=2.459, df=4, p=0.652 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_27 | []: χ²=3.636, df=4, p=0.4574 → độc lập, bỏ cạnh
    - PC #8: α=0.210, cột ['cartservice_27', 'shippingservice_16', 'shippingservice_mem', 'cartservice_cpu', 'shippingservice_workload'], số bin {'cartservice_27': 5, 'shippingservice_16': 5, 'shippingservice_mem': 5, 'cartservice_cpu': 5, 'shippingservice_workload': 5}, F kề: []
      - kiểm F ⊥ cartservice_27 | []: χ²=3.636, df=4, p=0.4574 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_16 | []: χ²=5.493, df=4, p=0.2404 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_workload | []: χ²=1.943, df=4, p=0.7463 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_mem | []: χ²=4.327, df=4, p=0.3635 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_cpu | []: χ²=2.459, df=4, p=0.652 → độc lập, bỏ cạnh
    - PC #9: α=0.310, cột ['cartservice_27', 'shippingservice_16', 'shippingservice_mem', 'cartservice_cpu', 'shippingservice_workload'], số bin {'cartservice_27': 5, 'shippingservice_16': 5, 'shippingservice_mem': 5, 'cartservice_cpu': 5, 'shippingservice_workload': 5}, F kề: ['shippingservice_16']
      - kiểm F ⊥ shippingservice_16 | []: χ²=5.493, df=4, p=0.2404 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_cpu | []: χ²=2.459, df=4, p=0.652 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_27 | []: χ²=3.636, df=4, p=0.4574 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_mem | []: χ²=4.327, df=4, p=0.3635 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_workload | []: χ²=1.943, df=4, p=0.7463 → độc lập, bỏ cạnh
    - PC #10: α=0.010, cột ['cartservice_17'], số bin {'cartservice_17': 2}, F kề: []
      - kiểm F ⊥ cartservice_17 | []: χ²=0.000, df=1, p=1 → độc lập, bỏ cạnh
    - PC #11: α=0.110, cột ['cartservice_17'], số bin {'cartservice_17': 2}, F kề: []
      - kiểm F ⊥ cartservice_17 | []: χ²=0.000, df=1, p=1 → độc lập, bỏ cạnh
    - PC #12: α=0.210, cột ['cartservice_17'], số bin {'cartservice_17': 2}, F kề: []
      - kiểm F ⊥ cartservice_17 | []: χ²=0.000, df=1, p=1 → độc lập, bỏ cạnh
    - PC #13: α=0.310, cột ['cartservice_17'], số bin {'cartservice_17': 2}, F kề: []
      - kiểm F ⊥ cartservice_17 | []: χ²=0.000, df=1, p=1 → độc lập, bỏ cạnh
    - PC #14: α=0.410, cột ['cartservice_17'], số bin {'cartservice_17': 2}, F kề: []
      - kiểm F ⊥ cartservice_17 | []: χ²=0.000, df=1, p=1 → độc lập, bỏ cạnh
    - PC #15: α=0.510, cột ['cartservice_17'], số bin {'cartservice_17': 2}, F kề: []
      - kiểm F ⊥ cartservice_17 | []: χ²=0.000, df=1, p=1 → độc lập, bỏ cạnh
    - PC #16: α=0.610, cột ['cartservice_17'], số bin {'cartservice_17': 2}, F kề: []
      - kiểm F ⊥ cartservice_17 | []: χ²=0.000, df=1, p=1 → độc lập, bỏ cạnh
    - PC #17: α=0.710, cột ['cartservice_17'], số bin {'cartservice_17': 2}, F kề: []
      - kiểm F ⊥ cartservice_17 | []: χ²=0.000, df=1, p=1 → độc lập, bỏ cạnh
    - PC #18: α=0.810, cột ['cartservice_17'], số bin {'cartservice_17': 2}, F kề: []
      - kiểm F ⊥ cartservice_17 | []: χ²=0.000, df=1, p=1 → độc lập, bỏ cạnh
    - PC #19: α=0.910, cột ['cartservice_17'], số bin {'cartservice_17': 2}, F kề: []
      - kiểm F ⊥ cartservice_17 | []: χ²=0.000, df=1, p=1 → độc lập, bỏ cạnh
    - PC #20: α=0.001, cột ['cartservice_latency', 'cartservice_mem', 'shippingservice_16'], số bin {'cartservice_latency': 5, 'cartservice_mem': 5, 'shippingservice_16': 5}, F kề: []
      - kiểm F ⊥ shippingservice_16 | []: χ²=5.493, df=4, p=0.2404 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_mem | []: χ²=6.756, df=4, p=0.1494 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_latency | []: χ²=6.433, df=4, p=0.169 → độc lập, bỏ cạnh
    - PC #21: α=0.101, cột ['cartservice_latency', 'cartservice_mem', 'shippingservice_16'], số bin {'cartservice_latency': 5, 'cartservice_mem': 5, 'shippingservice_16': 5}, F kề: []
      - kiểm F ⊥ shippingservice_16 | []: χ²=5.493, df=4, p=0.2404 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_latency | []: χ²=6.433, df=4, p=0.169 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_mem | []: χ²=6.756, df=4, p=0.1494 → độc lập, bỏ cạnh
    - PC #22: α=0.201, cột ['cartservice_latency', 'cartservice_mem', 'shippingservice_16'], số bin {'cartservice_latency': 5, 'cartservice_mem': 5, 'shippingservice_16': 5}, F kề: ['cartservice_latency', 'cartservice_mem']
      - kiểm F ⊥ cartservice_mem | []: χ²=6.756, df=4, p=0.1494 → phụ thuộc, giữ
      - kiểm F ⊥ shippingservice_16 | []: χ²=5.493, df=4, p=0.2404 → độc lập, bỏ cạnh
      - kiểm F ⊥ cartservice_latency | []: χ²=6.433, df=4, p=0.169 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_latency | ['cartservice_mem']: χ²=11.712, df=8, p=0.1645 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_mem | ['cartservice_latency']: χ²=14.902, df=9, p=0.09367 → phụ thuộc, giữ
    - PC #23: α=0.301, cột ['cartservice_latency', 'cartservice_mem', 'shippingservice_16'], số bin {'cartservice_latency': 5, 'cartservice_mem': 5, 'shippingservice_16': 5}, F kề: ['cartservice_mem', 'shippingservice_16']
      - kiểm F ⊥ shippingservice_16 | []: χ²=5.493, df=4, p=0.2404 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_mem | []: χ²=6.756, df=4, p=0.1494 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_latency | []: χ²=6.433, df=4, p=0.169 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_mem | ['cartservice_latency']: χ²=14.902, df=9, p=0.09367 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_mem | ['shippingservice_16']: χ²=21.547, df=13, p=0.06279 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_latency | ['cartservice_mem']: χ²=11.712, df=8, p=0.1645 → phụ thuộc, giữ
      - kiểm F ⊥ cartservice_latency | ['shippingservice_16']: χ²=8.909, df=9, p=0.4458 → độc lập, bỏ cạnh
      - kiểm F ⊥ shippingservice_16 | ['cartservice_mem']: χ²=19.129, df=12, p=0.08545 → phụ thuộc, giữ
- cụm 2 (điểm 0.0438): adservice 0.0372, currencyservice 0.0538, emailservice 0.0452, frontend 0.0511, paymentservice 0.0374, recommendationservice 0.0381
  - RCD nhận 20+20 dòng, 45 cột: ['adservice_cpu', 'currencyservice_cpu', 'emailservice_cpu', 'frontend_cpu', 'paymentservice_cpu', 'recommendationservice_cpu', 'adservice_mem', 'currencyservice_mem', 'emailservice_mem', 'frontend_mem', 'paymentservice_mem', 'recommendationservice_mem', 'adservice_diskio', 'adservice_workload', 'currencyservice_workload', 'emailservice_workload', 'frontend_workload', 'frontend-external_workload', 'paymentservice_workload', 'recommendationservice_workload', 'adservice_latency', 'currencyservice_latency', 'emailservice_latency', 'frontend_latency', 'paymentservice_latency', 'recommendationservice_latency', 'currencyservice_1', 'frontend_2', 'frontend_3', 'currencyservice_4', 'frontend_6', 'frontend_7', 'frontend_8', 'adservice_9', 'frontend_10', 'recommendationservice_11', 'frontend_12', 'frontend_14', 'frontend_18', 'frontend_19', 'frontend_20', 'paymentservice_22', 'paymentservice_23', 'emailservice_28', 'frontend_30']
  - pha 1, mức với 45 cột, khối: [['frontend_latency', 'paymentservice_mem', 'currencyservice_4', 'emailservice_cpu', 'paymentservice_latency'], ['currencyservice_latency', 'frontend_7', 'currencyservice_mem', 'frontend_workload', 'frontend_14'], ['frontend_mem', 'emailservice_latency', 'emailservice_28', 'frontend_20', 'frontend-external_workload'], ['recommendationservice_cpu', 'adservice_workload', 'recommendationservice_workload', 'recommendationservice_latency', 'frontend_12'], ['frontend_10', 'emailservice_mem', 'currencyservice_1', 'frontend_3', 'adservice_9'], ['frontend_cpu', 'frontend_8', 'emailservice_workload', 'frontend_6', 'adservice_mem'], ['paymentservice_cpu', 'paymentservice_23', 'adservice_latency', 'adservice_diskio', 'currencyservice_workload'], ['adservice_cpu', 'frontend_2', 'paymentservice_workload', 'recommendationservice_mem', 'frontend_18'], ['recommendationservice_11', 'paymentservice_22', 'frontend_19', 'frontend_30', 'currencyservice_cpu']]
  - pha 1, mức với 9 cột, khối: [['currencyservice_mem', 'emailservice_latency', 'adservice_9', 'recommendationservice_11', 'paymentservice_cpu'], ['paymentservice_mem', 'frontend_12', 'recommendationservice_mem', 'adservice_mem']]
  - số lần chạy Ψ-PC: 34; RCD trả: ['adservice_mem', 'paymentservice_cpu']; nội bộ: ['adservice', 'paymentservice']; dự phòng: True
    - PC #0: α=0.010, cột ['frontend_latency', 'paymentservice_mem', 'currencyservice_4', 'emailservice_cpu', 'paymentservice_latency'], số bin {'frontend_latency': 5, 'paymentservice_mem': 5, 'currencyservice_4': 5, 'emailservice_cpu': 5, 'paymentservice_latency': 5}, F kề: []
      - kiểm F ⊥ emailservice_cpu | []: χ²=6.667, df=4, p=0.1546 → độc lập, bỏ cạnh
      - kiểm F ⊥ paymentservice_latency | []: χ²=3.503, df=4, p=0.4774 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_4 | []: χ²=2.188, df=4, p=0.7012 → độc lập, bỏ cạnh
      - kiểm F ⊥ paymentservice_mem | []: χ²=8.118, df=4, p=0.08734 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_latency | []: χ²=3.700, df=4, p=0.4481 → độc lập, bỏ cạnh
    - PC #1: α=0.110, cột ['frontend_latency', 'paymentservice_mem', 'currencyservice_4', 'emailservice_cpu', 'paymentservice_latency'], số bin {'frontend_latency': 5, 'paymentservice_mem': 5, 'currencyservice_4': 5, 'emailservice_cpu': 5, 'paymentservice_latency': 5}, F kề: ['paymentservice_mem']
      - kiểm F ⊥ paymentservice_latency | []: χ²=3.503, df=4, p=0.4774 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_4 | []: χ²=2.188, df=4, p=0.7012 → độc lập, bỏ cạnh
      - kiểm F ⊥ paymentservice_mem | []: χ²=8.118, df=4, p=0.08734 → phụ thuộc, giữ
      - kiểm F ⊥ emailservice_cpu | []: χ²=6.667, df=4, p=0.1546 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_latency | []: χ²=3.700, df=4, p=0.4481 → độc lập, bỏ cạnh
    - PC #2: α=0.010, cột ['currencyservice_latency', 'frontend_7', 'currencyservice_mem', 'frontend_workload', 'frontend_14'], số bin {'currencyservice_latency': 5, 'frontend_7': 5, 'currencyservice_mem': 5, 'frontend_workload': 5, 'frontend_14': 5}, F kề: []
      - kiểm F ⊥ frontend_14 | []: χ²=3.067, df=4, p=0.5467 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_7 | []: χ²=1.429, df=4, p=0.8391 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_workload | []: χ²=1.567, df=4, p=0.8147 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_mem | []: χ²=3.444, df=4, p=0.4864 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_latency | []: χ²=2.667, df=4, p=0.6151 → độc lập, bỏ cạnh
    - PC #3: α=0.110, cột ['currencyservice_latency', 'frontend_7', 'currencyservice_mem', 'frontend_workload', 'frontend_14'], số bin {'currencyservice_latency': 5, 'frontend_7': 5, 'currencyservice_mem': 5, 'frontend_workload': 5, 'frontend_14': 5}, F kề: []
      - kiểm F ⊥ currencyservice_latency | []: χ²=2.667, df=4, p=0.6151 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_7 | []: χ²=1.429, df=4, p=0.8391 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_14 | []: χ²=3.067, df=4, p=0.5467 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_workload | []: χ²=1.567, df=4, p=0.8147 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_mem | []: χ²=3.444, df=4, p=0.4864 → độc lập, bỏ cạnh
    - PC #4: α=0.210, cột ['currencyservice_latency', 'frontend_7', 'currencyservice_mem', 'frontend_workload', 'frontend_14'], số bin {'currencyservice_latency': 5, 'frontend_7': 5, 'currencyservice_mem': 5, 'frontend_workload': 5, 'frontend_14': 5}, F kề: []
      - kiểm F ⊥ currencyservice_latency | []: χ²=2.667, df=4, p=0.6151 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_7 | []: χ²=1.429, df=4, p=0.8391 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_workload | []: χ²=1.567, df=4, p=0.8147 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_14 | []: χ²=3.067, df=4, p=0.5467 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_mem | []: χ²=3.444, df=4, p=0.4864 → độc lập, bỏ cạnh
    - PC #5: α=0.310, cột ['currencyservice_latency', 'frontend_7', 'currencyservice_mem', 'frontend_workload', 'frontend_14'], số bin {'currencyservice_latency': 5, 'frontend_7': 5, 'currencyservice_mem': 5, 'frontend_workload': 5, 'frontend_14': 5}, F kề: []
      - kiểm F ⊥ currencyservice_latency | []: χ²=2.667, df=4, p=0.6151 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_7 | []: χ²=1.429, df=4, p=0.8391 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_14 | []: χ²=3.067, df=4, p=0.5467 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_mem | []: χ²=3.444, df=4, p=0.4864 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_workload | []: χ²=1.567, df=4, p=0.8147 → độc lập, bỏ cạnh
    - PC #6: α=0.410, cột ['currencyservice_latency', 'frontend_7', 'currencyservice_mem', 'frontend_workload', 'frontend_14'], số bin {'currencyservice_latency': 5, 'frontend_7': 5, 'currencyservice_mem': 5, 'frontend_workload': 5, 'frontend_14': 5}, F kề: []
      - kiểm F ⊥ currencyservice_latency | []: χ²=2.667, df=4, p=0.6151 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_workload | []: χ²=1.567, df=4, p=0.8147 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_mem | []: χ²=3.444, df=4, p=0.4864 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_7 | []: χ²=1.429, df=4, p=0.8391 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_14 | []: χ²=3.067, df=4, p=0.5467 → độc lập, bỏ cạnh
    - PC #7: α=0.510, cột ['currencyservice_latency', 'frontend_7', 'currencyservice_mem', 'frontend_workload', 'frontend_14'], số bin {'currencyservice_latency': 5, 'frontend_7': 5, 'currencyservice_mem': 5, 'frontend_workload': 5, 'frontend_14': 5}, F kề: ['currencyservice_mem']
      - kiểm F ⊥ frontend_workload | []: χ²=1.567, df=4, p=0.8147 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_latency | []: χ²=2.667, df=4, p=0.6151 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_14 | []: χ²=3.067, df=4, p=0.5467 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_mem | []: χ²=3.444, df=4, p=0.4864 → phụ thuộc, giữ
      - kiểm F ⊥ frontend_7 | []: χ²=1.429, df=4, p=0.8391 → độc lập, bỏ cạnh
    - PC #8: α=0.010, cột ['frontend_mem', 'emailservice_latency', 'emailservice_28', 'frontend_20', 'frontend-external_workload'], số bin {'frontend_mem': 5, 'emailservice_latency': 5, 'emailservice_28': 5, 'frontend_20': 5, 'frontend-external_workload': 5}, F kề: []
      - kiểm F ⊥ frontend_20 | []: χ²=1.644, df=4, p=0.8008 → độc lập, bỏ cạnh
      - kiểm F ⊥ emailservice_latency | []: χ²=7.282, df=4, p=0.1217 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_mem | []: χ²=4.336, df=4, p=0.3625 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ emailservice_28 | []: χ²=3.636, df=4, p=0.4574 → độc lập, bỏ cạnh
    - PC #9: α=0.110, cột ['frontend_mem', 'emailservice_latency', 'emailservice_28', 'frontend_20', 'frontend-external_workload'], số bin {'frontend_mem': 5, 'emailservice_latency': 5, 'emailservice_28': 5, 'frontend_20': 5, 'frontend-external_workload': 5}, F kề: []
      - kiểm F ⊥ emailservice_latency | []: χ²=7.282, df=4, p=0.1217 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_mem | []: χ²=4.336, df=4, p=0.3625 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_20 | []: χ²=1.644, df=4, p=0.8008 → độc lập, bỏ cạnh
      - kiểm F ⊥ emailservice_28 | []: χ²=3.636, df=4, p=0.4574 → độc lập, bỏ cạnh
    - PC #10: α=0.210, cột ['frontend_mem', 'emailservice_latency', 'emailservice_28', 'frontend_20', 'frontend-external_workload'], số bin {'frontend_mem': 5, 'emailservice_latency': 5, 'emailservice_28': 5, 'frontend_20': 5, 'frontend-external_workload': 5}, F kề: ['emailservice_latency']
      - kiểm F ⊥ emailservice_latency | []: χ²=7.282, df=4, p=0.1217 → phụ thuộc, giữ
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_20 | []: χ²=1.644, df=4, p=0.8008 → độc lập, bỏ cạnh
      - kiểm F ⊥ emailservice_28 | []: χ²=3.636, df=4, p=0.4574 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_mem | []: χ²=4.336, df=4, p=0.3625 → độc lập, bỏ cạnh
    - PC #11: α=0.010, cột ['recommendationservice_cpu', 'adservice_workload', 'recommendationservice_workload', 'recommendationservice_latency', 'frontend_12'], số bin {'recommendationservice_cpu': 5, 'adservice_workload': 5, 'recommendationservice_workload': 5, 'recommendationservice_latency': 5, 'frontend_12': 5}, F kề: []
      - kiểm F ⊥ adservice_workload | []: χ²=1.086, df=4, p=0.8964 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_workload | []: χ²=2.911, df=4, p=0.5728 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_12 | []: χ²=3.567, df=4, p=0.4678 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_cpu | []: χ²=3.167, df=4, p=0.5303 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_latency | []: χ²=2.267, df=4, p=0.6868 → độc lập, bỏ cạnh
    - PC #12: α=0.110, cột ['recommendationservice_cpu', 'adservice_workload', 'recommendationservice_workload', 'recommendationservice_latency', 'frontend_12'], số bin {'recommendationservice_cpu': 5, 'adservice_workload': 5, 'recommendationservice_workload': 5, 'recommendationservice_latency': 5, 'frontend_12': 5}, F kề: []
      - kiểm F ⊥ frontend_12 | []: χ²=3.567, df=4, p=0.4678 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_latency | []: χ²=2.267, df=4, p=0.6868 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_workload | []: χ²=2.911, df=4, p=0.5728 → độc lập, bỏ cạnh
      - kiểm F ⊥ adservice_workload | []: χ²=1.086, df=4, p=0.8964 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_cpu | []: χ²=3.167, df=4, p=0.5303 → độc lập, bỏ cạnh
    - PC #13: α=0.210, cột ['recommendationservice_cpu', 'adservice_workload', 'recommendationservice_workload', 'recommendationservice_latency', 'frontend_12'], số bin {'recommendationservice_cpu': 5, 'adservice_workload': 5, 'recommendationservice_workload': 5, 'recommendationservice_latency': 5, 'frontend_12': 5}, F kề: []
      - kiểm F ⊥ frontend_12 | []: χ²=3.567, df=4, p=0.4678 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_cpu | []: χ²=3.167, df=4, p=0.5303 → độc lập, bỏ cạnh
      - kiểm F ⊥ adservice_workload | []: χ²=1.086, df=4, p=0.8964 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_latency | []: χ²=2.267, df=4, p=0.6868 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_workload | []: χ²=2.911, df=4, p=0.5728 → độc lập, bỏ cạnh
    - PC #14: α=0.310, cột ['recommendationservice_cpu', 'adservice_workload', 'recommendationservice_workload', 'recommendationservice_latency', 'frontend_12'], số bin {'recommendationservice_cpu': 5, 'adservice_workload': 5, 'recommendationservice_workload': 5, 'recommendationservice_latency': 5, 'frontend_12': 5}, F kề: []
      - kiểm F ⊥ adservice_workload | []: χ²=1.086, df=4, p=0.8964 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_workload | []: χ²=2.911, df=4, p=0.5728 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_latency | []: χ²=2.267, df=4, p=0.6868 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_12 | []: χ²=3.567, df=4, p=0.4678 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_cpu | []: χ²=3.167, df=4, p=0.5303 → độc lập, bỏ cạnh
    - PC #15: α=0.410, cột ['recommendationservice_cpu', 'adservice_workload', 'recommendationservice_workload', 'recommendationservice_latency', 'frontend_12'], số bin {'recommendationservice_cpu': 5, 'adservice_workload': 5, 'recommendationservice_workload': 5, 'recommendationservice_latency': 5, 'frontend_12': 5}, F kề: []
      - kiểm F ⊥ frontend_12 | []: χ²=3.567, df=4, p=0.4678 → độc lập, bỏ cạnh
      - kiểm F ⊥ adservice_workload | []: χ²=1.086, df=4, p=0.8964 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_latency | []: χ²=2.267, df=4, p=0.6868 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_cpu | []: χ²=3.167, df=4, p=0.5303 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_workload | []: χ²=2.911, df=4, p=0.5728 → độc lập, bỏ cạnh
    - PC #16: α=0.510, cột ['recommendationservice_cpu', 'adservice_workload', 'recommendationservice_workload', 'recommendationservice_latency', 'frontend_12'], số bin {'recommendationservice_cpu': 5, 'adservice_workload': 5, 'recommendationservice_workload': 5, 'recommendationservice_latency': 5, 'frontend_12': 5}, F kề: ['frontend_12']
      - kiểm F ⊥ recommendationservice_latency | []: χ²=2.267, df=4, p=0.6868 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_cpu | []: χ²=3.167, df=4, p=0.5303 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_workload | []: χ²=2.911, df=4, p=0.5728 → độc lập, bỏ cạnh
      - kiểm F ⊥ adservice_workload | []: χ²=1.086, df=4, p=0.8964 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_12 | []: χ²=3.567, df=4, p=0.4678 → phụ thuộc, giữ
    - PC #17: α=0.010, cột ['frontend_10', 'emailservice_mem', 'currencyservice_1', 'frontend_3', 'adservice_9'], số bin {'frontend_10': 5, 'emailservice_mem': 0, 'currencyservice_1': 5, 'frontend_3': 5, 'adservice_9': 5}, F kề: []
      - kiểm F ⊥ frontend_10 | []: χ²=5.358, df=4, p=0.2525 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_1 | []: χ²=2.226, df=4, p=0.6943 → độc lập, bỏ cạnh
      - kiểm F ⊥ emailservice_mem | []: χ²=0.000, df=0, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_3 | []: χ²=3.567, df=4, p=0.4677 → độc lập, bỏ cạnh
      - kiểm F ⊥ adservice_9 | []: χ²=6.592, df=4, p=0.1591 → độc lập, bỏ cạnh
    - PC #18: α=0.110, cột ['frontend_10', 'emailservice_mem', 'currencyservice_1', 'frontend_3', 'adservice_9'], số bin {'frontend_10': 5, 'emailservice_mem': 0, 'currencyservice_1': 5, 'frontend_3': 5, 'adservice_9': 5}, F kề: []
      - kiểm F ⊥ frontend_10 | []: χ²=5.358, df=4, p=0.2525 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_3 | []: χ²=3.567, df=4, p=0.4677 → độc lập, bỏ cạnh
      - kiểm F ⊥ emailservice_mem | []: χ²=0.000, df=0, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_1 | []: χ²=2.226, df=4, p=0.6943 → độc lập, bỏ cạnh
      - kiểm F ⊥ adservice_9 | []: χ²=6.592, df=4, p=0.1591 → độc lập, bỏ cạnh
    - PC #19: α=0.210, cột ['frontend_10', 'emailservice_mem', 'currencyservice_1', 'frontend_3', 'adservice_9'], số bin {'frontend_10': 5, 'emailservice_mem': 0, 'currencyservice_1': 5, 'frontend_3': 5, 'adservice_9': 5}, F kề: ['adservice_9']
      - kiểm F ⊥ emailservice_mem | []: χ²=0.000, df=0, p=1 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_1 | []: χ²=2.226, df=4, p=0.6943 → độc lập, bỏ cạnh
      - kiểm F ⊥ adservice_9 | []: χ²=6.592, df=4, p=0.1591 → phụ thuộc, giữ
      - kiểm F ⊥ frontend_10 | []: χ²=5.358, df=4, p=0.2525 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_3 | []: χ²=3.567, df=4, p=0.4677 → độc lập, bỏ cạnh
    - PC #20: α=0.010, cột ['frontend_cpu', 'frontend_8', 'emailservice_workload', 'frontend_6', 'adservice_mem'], số bin {'frontend_cpu': 5, 'frontend_8': 5, 'emailservice_workload': 5, 'frontend_6': 5, 'adservice_mem': 5}, F kề: ['adservice_mem']
      - kiểm F ⊥ emailservice_workload | []: χ²=2.540, df=4, p=0.6375 → độc lập, bỏ cạnh
      - kiểm F ⊥ adservice_mem | []: χ²=22.821, df=4, p=0.0001375 → phụ thuộc, giữ
      - kiểm F ⊥ frontend_6 | []: χ²=1.429, df=4, p=0.8391 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_cpu | []: χ²=7.628, df=4, p=0.1062 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_8 | []: χ²=1.429, df=4, p=0.8391 → độc lập, bỏ cạnh
    - PC #21: α=0.010, cột ['paymentservice_cpu', 'paymentservice_23', 'adservice_latency', 'adservice_diskio', 'currencyservice_workload'], số bin {'paymentservice_cpu': 5, 'paymentservice_23': 5, 'adservice_latency': 5, 'adservice_diskio': 5, 'currencyservice_workload': 5}, F kề: []
      - kiểm F ⊥ currencyservice_workload | []: χ²=2.089, df=4, p=0.7194 → độc lập, bỏ cạnh
      - kiểm F ⊥ adservice_latency | []: χ²=8.810, df=4, p=0.06604 → độc lập, bỏ cạnh
      - kiểm F ⊥ paymentservice_cpu | []: χ²=13.171, df=4, p=0.01047 → độc lập, bỏ cạnh
      - kiểm F ⊥ paymentservice_23 | []: χ²=3.636, df=4, p=0.4574 → độc lập, bỏ cạnh
      - kiểm F ⊥ adservice_diskio | []: χ²=2.733, df=4, p=0.6034 → độc lập, bỏ cạnh
    - PC #22: α=0.110, cột ['paymentservice_cpu', 'paymentservice_23', 'adservice_latency', 'adservice_diskio', 'currencyservice_workload'], số bin {'paymentservice_cpu': 5, 'paymentservice_23': 5, 'adservice_latency': 5, 'adservice_diskio': 5, 'currencyservice_workload': 5}, F kề: ['paymentservice_cpu']
      - kiểm F ⊥ adservice_latency | []: χ²=8.810, df=4, p=0.06604 → phụ thuộc, giữ
      - kiểm F ⊥ paymentservice_cpu | []: χ²=13.171, df=4, p=0.01047 → phụ thuộc, giữ
      - kiểm F ⊥ paymentservice_23 | []: χ²=3.636, df=4, p=0.4574 → độc lập, bỏ cạnh
      - kiểm F ⊥ adservice_diskio | []: χ²=2.733, df=4, p=0.6034 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_workload | []: χ²=2.089, df=4, p=0.7194 → độc lập, bỏ cạnh
      - kiểm F ⊥ paymentservice_cpu | ['adservice_latency']: χ²=12.998, df=7, p=0.07217 → phụ thuộc, giữ
      - kiểm F ⊥ adservice_latency | ['paymentservice_cpu']: χ²=6.918, df=9, p=0.6456 → độc lập, bỏ cạnh
    - PC #23: α=0.010, cột ['adservice_cpu', 'frontend_2', 'paymentservice_workload', 'recommendationservice_mem', 'frontend_18'], số bin {'adservice_cpu': 5, 'frontend_2': 5, 'paymentservice_workload': 5, 'recommendationservice_mem': 5, 'frontend_18': 5}, F kề: []
      - kiểm F ⊥ paymentservice_workload | []: χ²=6.086, df=4, p=0.1928 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_mem | []: χ²=11.222, df=4, p=0.02418 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_2 | []: χ²=2.254, df=4, p=0.6892 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_18 | []: χ²=4.819, df=4, p=0.3064 → độc lập, bỏ cạnh
      - kiểm F ⊥ adservice_cpu | []: χ²=8.549, df=4, p=0.07341 → độc lập, bỏ cạnh
    - PC #24: α=0.110, cột ['adservice_cpu', 'frontend_2', 'paymentservice_workload', 'recommendationservice_mem', 'frontend_18'], số bin {'adservice_cpu': 5, 'frontend_2': 5, 'paymentservice_workload': 5, 'recommendationservice_mem': 5, 'frontend_18': 5}, F kề: ['recommendationservice_mem']
      - kiểm F ⊥ frontend_18 | []: χ²=4.819, df=4, p=0.3064 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_2 | []: χ²=2.254, df=4, p=0.6892 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_mem | []: χ²=11.222, df=4, p=0.02418 → phụ thuộc, giữ
      - kiểm F ⊥ paymentservice_workload | []: χ²=6.086, df=4, p=0.1928 → độc lập, bỏ cạnh
      - kiểm F ⊥ adservice_cpu | []: χ²=8.549, df=4, p=0.07341 → phụ thuộc, giữ
      - kiểm F ⊥ adservice_cpu | ['recommendationservice_mem']: χ²=10.793, df=7, p=0.1479 → độc lập, bỏ cạnh
    - PC #25: α=0.010, cột ['recommendationservice_11', 'paymentservice_22', 'frontend_19', 'frontend_30', 'currencyservice_cpu'], số bin {'recommendationservice_11': 5, 'paymentservice_22': 5, 'frontend_19': 5, 'frontend_30': 5, 'currencyservice_cpu': 5}, F kề: []
      - kiểm F ⊥ frontend_30 | []: χ²=3.636, df=4, p=0.4574 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_11 | []: χ²=4.833, df=4, p=0.3048 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_19 | []: χ²=3.876, df=4, p=0.423 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_cpu | []: χ²=2.144, df=4, p=0.7094 → độc lập, bỏ cạnh
      - kiểm F ⊥ paymentservice_22 | []: χ²=3.636, df=4, p=0.4574 → độc lập, bỏ cạnh
    - PC #26: α=0.110, cột ['recommendationservice_11', 'paymentservice_22', 'frontend_19', 'frontend_30', 'currencyservice_cpu'], số bin {'recommendationservice_11': 5, 'paymentservice_22': 5, 'frontend_19': 5, 'frontend_30': 5, 'currencyservice_cpu': 5}, F kề: []
      - kiểm F ⊥ frontend_19 | []: χ²=3.876, df=4, p=0.423 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_30 | []: χ²=3.636, df=4, p=0.4574 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_cpu | []: χ²=2.144, df=4, p=0.7094 → độc lập, bỏ cạnh
      - kiểm F ⊥ paymentservice_22 | []: χ²=3.636, df=4, p=0.4574 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_11 | []: χ²=4.833, df=4, p=0.3048 → độc lập, bỏ cạnh
    - PC #27: α=0.210, cột ['recommendationservice_11', 'paymentservice_22', 'frontend_19', 'frontend_30', 'currencyservice_cpu'], số bin {'recommendationservice_11': 5, 'paymentservice_22': 5, 'frontend_19': 5, 'frontend_30': 5, 'currencyservice_cpu': 5}, F kề: []
      - kiểm F ⊥ paymentservice_22 | []: χ²=3.636, df=4, p=0.4574 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_11 | []: χ²=4.833, df=4, p=0.3048 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_cpu | []: χ²=2.144, df=4, p=0.7094 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_30 | []: χ²=3.636, df=4, p=0.4574 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_19 | []: χ²=3.876, df=4, p=0.423 → độc lập, bỏ cạnh
    - PC #28: α=0.310, cột ['recommendationservice_11', 'paymentservice_22', 'frontend_19', 'frontend_30', 'currencyservice_cpu'], số bin {'recommendationservice_11': 5, 'paymentservice_22': 5, 'frontend_19': 5, 'frontend_30': 5, 'currencyservice_cpu': 5}, F kề: ['recommendationservice_11']
      - kiểm F ⊥ recommendationservice_11 | []: χ²=4.833, df=4, p=0.3048 → phụ thuộc, giữ
      - kiểm F ⊥ paymentservice_22 | []: χ²=3.636, df=4, p=0.4574 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_cpu | []: χ²=2.144, df=4, p=0.7094 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_19 | []: χ²=3.876, df=4, p=0.423 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_30 | []: χ²=3.636, df=4, p=0.4574 → độc lập, bỏ cạnh
    - PC #29: α=0.010, cột ['currencyservice_mem', 'emailservice_latency', 'adservice_9', 'recommendationservice_11', 'paymentservice_cpu'], số bin {'currencyservice_mem': 5, 'emailservice_latency': 5, 'adservice_9': 5, 'recommendationservice_11': 5, 'paymentservice_cpu': 5}, F kề: []
      - kiểm F ⊥ adservice_9 | []: χ²=6.592, df=4, p=0.1591 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_mem | []: χ²=3.444, df=4, p=0.4864 → độc lập, bỏ cạnh
      - kiểm F ⊥ paymentservice_cpu | []: χ²=13.171, df=4, p=0.01047 → độc lập, bỏ cạnh
      - kiểm F ⊥ emailservice_latency | []: χ²=7.282, df=4, p=0.1217 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_11 | []: χ²=4.833, df=4, p=0.3048 → độc lập, bỏ cạnh
    - PC #30: α=0.110, cột ['currencyservice_mem', 'emailservice_latency', 'adservice_9', 'recommendationservice_11', 'paymentservice_cpu'], số bin {'currencyservice_mem': 5, 'emailservice_latency': 5, 'adservice_9': 5, 'recommendationservice_11': 5, 'paymentservice_cpu': 5}, F kề: ['paymentservice_cpu']
      - kiểm F ⊥ paymentservice_cpu | []: χ²=13.171, df=4, p=0.01047 → phụ thuộc, giữ
      - kiểm F ⊥ recommendationservice_11 | []: χ²=4.833, df=4, p=0.3048 → độc lập, bỏ cạnh
      - kiểm F ⊥ emailservice_latency | []: χ²=7.282, df=4, p=0.1217 → độc lập, bỏ cạnh
      - kiểm F ⊥ adservice_9 | []: χ²=6.592, df=4, p=0.1591 → độc lập, bỏ cạnh
      - kiểm F ⊥ currencyservice_mem | []: χ²=3.444, df=4, p=0.4864 → độc lập, bỏ cạnh
    - PC #31: α=0.010, cột ['paymentservice_mem', 'frontend_12', 'recommendationservice_mem', 'adservice_mem'], số bin {'paymentservice_mem': 5, 'frontend_12': 5, 'recommendationservice_mem': 5, 'adservice_mem': 5}, F kề: ['adservice_mem']
      - kiểm F ⊥ adservice_mem | []: χ²=22.821, df=4, p=0.0001375 → phụ thuộc, giữ
      - kiểm F ⊥ paymentservice_mem | []: χ²=8.118, df=4, p=0.08734 → độc lập, bỏ cạnh
      - kiểm F ⊥ recommendationservice_mem | []: χ²=11.222, df=4, p=0.02418 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend_12 | []: χ²=3.567, df=4, p=0.4678 → độc lập, bỏ cạnh
    - PC #32: α=0.001, cột ['paymentservice_cpu', 'adservice_mem'], số bin {'paymentservice_cpu': 5, 'adservice_mem': 5}, F kề: ['adservice_mem']
      - kiểm F ⊥ paymentservice_cpu | []: χ²=13.171, df=4, p=0.01047 → độc lập, bỏ cạnh
      - kiểm F ⊥ adservice_mem | []: χ²=22.821, df=4, p=0.0001375 → phụ thuộc, giữ
    - PC #33: α=0.101, cột ['paymentservice_cpu', 'adservice_mem'], số bin {'paymentservice_cpu': 5, 'adservice_mem': 5}, F kề: ['paymentservice_cpu', 'adservice_mem']
      - kiểm F ⊥ paymentservice_cpu | []: χ²=13.171, df=4, p=0.01047 → phụ thuộc, giữ
      - kiểm F ⊥ adservice_mem | []: χ²=22.821, df=4, p=0.0001375 → phụ thuộc, giữ
      - kiểm F ⊥ paymentservice_cpu | ['adservice_mem']: χ²=15.553, df=7, p=0.02953 → phụ thuộc, giữ
      - kiểm F ⊥ adservice_mem | ['paymentservice_cpu']: χ²=26.194, df=12, p=0.01008 → phụ thuộc, giữ
- cụm 3 (điểm 0.0167): frontend-external 0.0011, health 0.0190, productcatalogservice 0.0183, redis 0.0061, traceservice 0.0391
  - RCD nhận 20+20 dòng, 8 cột: ['productcatalogservice_cpu', 'redis_cpu', 'productcatalogservice_mem', 'redis_mem', 'redis_diskio', 'frontend-external_workload', 'productcatalogservice_workload', 'productcatalogservice_latency']
  - pha 1, mức với 8 cột, khối: [['redis_diskio', 'productcatalogservice_cpu', 'productcatalogservice_mem', 'productcatalogservice_latency', 'frontend-external_workload'], ['productcatalogservice_workload', 'redis_cpu', 'redis_mem']]
  - pha 1, mức với 6 cột, khối: [['frontend-external_workload', 'productcatalogservice_mem', 'redis_diskio', 'redis_cpu', 'productcatalogservice_latency'], ['productcatalogservice_cpu']]
  - số lần chạy Ψ-PC: 43; RCD trả: ['redis_diskio', 'productcatalogservice_mem', 'productcatalogservice_latency', 'redis_cpu', 'productcatalogservice_cpu', 'frontend-external_workload']; nội bộ: ['redis', 'productcatalogservice', 'frontend-external']; dự phòng: True
    - PC #0: α=0.010, cột ['redis_diskio', 'productcatalogservice_cpu', 'productcatalogservice_mem', 'productcatalogservice_latency', 'frontend-external_workload'], số bin {'redis_diskio': 5, 'productcatalogservice_cpu': 5, 'productcatalogservice_mem': 5, 'productcatalogservice_latency': 5, 'frontend-external_workload': 5}, F kề: []
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → độc lập, bỏ cạnh
    - PC #1: α=0.110, cột ['redis_diskio', 'productcatalogservice_cpu', 'productcatalogservice_mem', 'productcatalogservice_latency', 'frontend-external_workload'], số bin {'redis_diskio': 5, 'productcatalogservice_cpu': 5, 'productcatalogservice_mem': 5, 'productcatalogservice_latency': 5, 'frontend-external_workload': 5}, F kề: []
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → độc lập, bỏ cạnh
    - PC #2: α=0.210, cột ['redis_diskio', 'productcatalogservice_cpu', 'productcatalogservice_mem', 'productcatalogservice_latency', 'frontend-external_workload'], số bin {'redis_diskio': 5, 'productcatalogservice_cpu': 5, 'productcatalogservice_mem': 5, 'productcatalogservice_latency': 5, 'frontend-external_workload': 5}, F kề: ['redis_diskio', 'productcatalogservice_mem']
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_mem | ['redis_diskio']: χ²=6.333, df=4, p=0.1756 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_mem']: χ²=7.496, df=4, p=0.1119 → phụ thuộc, giữ
    - PC #3: α=0.310, cột ['redis_diskio', 'productcatalogservice_cpu', 'productcatalogservice_mem', 'productcatalogservice_latency', 'frontend-external_workload'], số bin {'redis_diskio': 5, 'productcatalogservice_cpu': 5, 'productcatalogservice_mem': 5, 'productcatalogservice_latency': 5, 'frontend-external_workload': 5}, F kề: ['redis_diskio', 'productcatalogservice_mem', 'productcatalogservice_latency']
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → phụ thuộc, giữ
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_mem']: χ²=7.496, df=4, p=0.1119 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_latency']: χ²=6.159, df=5, p=0.2911 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['redis_diskio']: χ²=6.333, df=4, p=0.1756 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['productcatalogservice_latency']: χ²=18.066, df=10, p=0.05386 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['redis_diskio']: χ²=4.976, df=4, p=0.2897 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['productcatalogservice_mem']: χ²=18.619, df=11, p=0.06828 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['redis_diskio', 'productcatalogservice_latency']: χ²=15.683, df=9, p=0.0738 → phụ thuộc, giữ
      - ... 2 phép kiểm nữa
    - PC #4: α=0.410, cột ['redis_diskio', 'productcatalogservice_cpu', 'productcatalogservice_mem', 'productcatalogservice_latency', 'frontend-external_workload'], số bin {'redis_diskio': 5, 'productcatalogservice_cpu': 5, 'productcatalogservice_mem': 5, 'productcatalogservice_latency': 5, 'frontend-external_workload': 5}, F kề: ['redis_diskio', 'productcatalogservice_mem', 'productcatalogservice_latency']
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → phụ thuộc, giữ
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_mem | ['redis_diskio']: χ²=6.333, df=4, p=0.1756 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['productcatalogservice_latency']: χ²=18.066, df=10, p=0.05386 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['redis_diskio']: χ²=4.976, df=4, p=0.2897 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['productcatalogservice_mem']: χ²=18.619, df=11, p=0.06828 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_mem']: χ²=7.496, df=4, p=0.1119 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_latency']: χ²=6.159, df=5, p=0.2911 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['redis_diskio', 'productcatalogservice_latency']: χ²=15.683, df=9, p=0.0738 → phụ thuộc, giữ
      - ... 2 phép kiểm nữa
    - PC #5: α=0.510, cột ['redis_diskio', 'productcatalogservice_cpu', 'productcatalogservice_mem', 'productcatalogservice_latency', 'frontend-external_workload'], số bin {'redis_diskio': 5, 'productcatalogservice_cpu': 5, 'productcatalogservice_mem': 5, 'productcatalogservice_latency': 5, 'frontend-external_workload': 5}, F kề: ['redis_diskio', 'productcatalogservice_mem', 'productcatalogservice_latency']
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['redis_diskio']: χ²=4.976, df=4, p=0.2897 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['productcatalogservice_mem']: χ²=18.619, df=11, p=0.06828 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_mem']: χ²=7.496, df=4, p=0.1119 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_latency']: χ²=6.159, df=5, p=0.2911 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['redis_diskio']: χ²=6.333, df=4, p=0.1756 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['productcatalogservice_latency']: χ²=18.066, df=10, p=0.05386 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_mem', 'productcatalogservice_latency']: χ²=3.733, df=3, p=0.2917 → phụ thuộc, giữ
      - ... 2 phép kiểm nữa
    - PC #6: α=0.610, cột ['redis_diskio', 'productcatalogservice_cpu', 'productcatalogservice_mem', 'productcatalogservice_latency', 'frontend-external_workload'], số bin {'redis_diskio': 5, 'productcatalogservice_cpu': 5, 'productcatalogservice_mem': 5, 'productcatalogservice_latency': 5, 'frontend-external_workload': 5}, F kề: ['redis_diskio', 'productcatalogservice_mem', 'productcatalogservice_latency']
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → phụ thuộc, giữ
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_mem']: χ²=7.496, df=4, p=0.1119 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_latency']: χ²=6.159, df=5, p=0.2911 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['redis_diskio']: χ²=6.333, df=4, p=0.1756 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['productcatalogservice_latency']: χ²=18.066, df=10, p=0.05386 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['redis_diskio']: χ²=4.976, df=4, p=0.2897 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['productcatalogservice_mem']: χ²=18.619, df=11, p=0.06828 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_mem', 'productcatalogservice_latency']: χ²=3.733, df=3, p=0.2917 → phụ thuộc, giữ
      - ... 2 phép kiểm nữa
    - PC #7: α=0.710, cột ['redis_diskio', 'productcatalogservice_cpu', 'productcatalogservice_mem', 'productcatalogservice_latency', 'frontend-external_workload'], số bin {'redis_diskio': 5, 'productcatalogservice_cpu': 5, 'productcatalogservice_mem': 5, 'productcatalogservice_latency': 5, 'frontend-external_workload': 5}, F kề: ['redis_diskio', 'productcatalogservice_mem', 'productcatalogservice_latency']
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → phụ thuộc, giữ
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_cpu']: χ²=5.059, df=5, p=0.4087 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_mem']: χ²=7.496, df=4, p=0.1119 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_latency']: χ²=6.159, df=5, p=0.2911 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['redis_diskio']: χ²=4.976, df=4, p=0.2897 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['productcatalogservice_cpu']: χ²=13.829, df=14, p=0.4625 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['productcatalogservice_mem']: χ²=18.619, df=11, p=0.06828 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['redis_diskio']: χ²=6.333, df=4, p=0.1756 → phụ thuộc, giữ
      - ... 6 phép kiểm nữa
    - PC #8: α=0.810, cột ['redis_diskio', 'productcatalogservice_cpu', 'productcatalogservice_mem', 'productcatalogservice_latency', 'frontend-external_workload'], số bin {'redis_diskio': 5, 'productcatalogservice_cpu': 5, 'productcatalogservice_mem': 5, 'productcatalogservice_latency': 5, 'frontend-external_workload': 5}, F kề: ['redis_diskio', 'productcatalogservice_mem', 'productcatalogservice_latency']
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → phụ thuộc, giữ
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['redis_diskio']: χ²=4.976, df=4, p=0.2897 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['productcatalogservice_cpu']: χ²=13.829, df=14, p=0.4625 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['productcatalogservice_mem']: χ²=18.619, df=11, p=0.06828 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_cpu | ['redis_diskio']: χ²=1.400, df=4, p=0.8442 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_mem | ['redis_diskio']: χ²=6.333, df=4, p=0.1756 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['productcatalogservice_latency']: χ²=18.066, df=10, p=0.05386 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_mem']: χ²=7.496, df=4, p=0.1119 → phụ thuộc, giữ
      - ... 4 phép kiểm nữa
    - PC #9: α=0.910, cột ['redis_diskio', 'productcatalogservice_cpu', 'productcatalogservice_mem', 'productcatalogservice_latency', 'frontend-external_workload'], số bin {'redis_diskio': 5, 'productcatalogservice_cpu': 5, 'productcatalogservice_mem': 5, 'productcatalogservice_latency': 5, 'frontend-external_workload': 5}, F kề: ['redis_diskio', 'productcatalogservice_cpu', 'productcatalogservice_mem', 'productcatalogservice_latency', 'frontend-external_workload']
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → phụ thuộc, giữ
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_cpu']: χ²=5.059, df=5, p=0.4087 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_mem']: χ²=7.496, df=4, p=0.1119 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_latency']: χ²=6.159, df=5, p=0.2911 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['frontend-external_workload']: χ²=6.845, df=6, p=0.3354 → phụ thuộc, giữ
      - kiểm F ⊥ frontend-external_workload | ['redis_diskio']: χ²=1.611, df=4, p=0.8068 → phụ thuộc, giữ
      - kiểm F ⊥ frontend-external_workload | ['productcatalogservice_cpu']: χ²=19.837, df=13, p=0.09935 → phụ thuộc, giữ
      - kiểm F ⊥ frontend-external_workload | ['productcatalogservice_mem']: χ²=12.266, df=11, p=0.344 → phụ thuộc, giữ
      - ... 68 phép kiểm nữa
    - PC #10: α=0.010, cột ['productcatalogservice_workload', 'redis_cpu', 'redis_mem'], số bin {'productcatalogservice_workload': 5, 'redis_cpu': 5, 'redis_mem': 2}, F kề: []
      - kiểm F ⊥ redis_mem | []: χ²=0.360, df=1, p=0.5483 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_workload | []: χ²=0.889, df=4, p=0.9261 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_cpu | []: χ²=4.314, df=4, p=0.3651 → độc lập, bỏ cạnh
    - PC #11: α=0.110, cột ['productcatalogservice_workload', 'redis_cpu', 'redis_mem'], số bin {'productcatalogservice_workload': 5, 'redis_cpu': 5, 'redis_mem': 2}, F kề: []
      - kiểm F ⊥ redis_cpu | []: χ²=4.314, df=4, p=0.3651 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_workload | []: χ²=0.889, df=4, p=0.9261 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_mem | []: χ²=0.360, df=1, p=0.5483 → độc lập, bỏ cạnh
    - PC #12: α=0.210, cột ['productcatalogservice_workload', 'redis_cpu', 'redis_mem'], số bin {'productcatalogservice_workload': 5, 'redis_cpu': 5, 'redis_mem': 2}, F kề: []
      - kiểm F ⊥ redis_cpu | []: χ²=4.314, df=4, p=0.3651 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_workload | []: χ²=0.889, df=4, p=0.9261 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_mem | []: χ²=0.360, df=1, p=0.5483 → độc lập, bỏ cạnh
    - PC #13: α=0.310, cột ['productcatalogservice_workload', 'redis_cpu', 'redis_mem'], số bin {'productcatalogservice_workload': 5, 'redis_cpu': 5, 'redis_mem': 2}, F kề: []
      - kiểm F ⊥ redis_cpu | []: χ²=4.314, df=4, p=0.3651 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_mem | []: χ²=0.360, df=1, p=0.5483 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_workload | []: χ²=0.889, df=4, p=0.9261 → độc lập, bỏ cạnh
    - PC #14: α=0.410, cột ['productcatalogservice_workload', 'redis_cpu', 'redis_mem'], số bin {'productcatalogservice_workload': 5, 'redis_cpu': 5, 'redis_mem': 2}, F kề: ['redis_cpu']
      - kiểm F ⊥ redis_cpu | []: χ²=4.314, df=4, p=0.3651 → phụ thuộc, giữ
      - kiểm F ⊥ redis_mem | []: χ²=0.360, df=1, p=0.5483 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_workload | []: χ²=0.889, df=4, p=0.9261 → độc lập, bỏ cạnh
    - PC #15: α=0.010, cột ['frontend-external_workload', 'productcatalogservice_mem', 'redis_diskio', 'redis_cpu', 'productcatalogservice_latency'], số bin {'frontend-external_workload': 5, 'productcatalogservice_mem': 5, 'redis_diskio': 5, 'redis_cpu': 5, 'productcatalogservice_latency': 5}, F kề: []
      - kiểm F ⊥ redis_cpu | []: χ²=4.314, df=4, p=0.3651 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
    - PC #16: α=0.110, cột ['frontend-external_workload', 'productcatalogservice_mem', 'redis_diskio', 'redis_cpu', 'productcatalogservice_latency'], số bin {'frontend-external_workload': 5, 'productcatalogservice_mem': 5, 'redis_diskio': 5, 'redis_cpu': 5, 'productcatalogservice_latency': 5}, F kề: []
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_cpu | []: χ²=4.314, df=4, p=0.3651 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → độc lập, bỏ cạnh
    - PC #17: α=0.210, cột ['frontend-external_workload', 'productcatalogservice_mem', 'redis_diskio', 'redis_cpu', 'productcatalogservice_latency'], số bin {'frontend-external_workload': 5, 'productcatalogservice_mem': 5, 'redis_diskio': 5, 'redis_cpu': 5, 'productcatalogservice_latency': 5}, F kề: ['productcatalogservice_mem', 'redis_diskio']
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | []: χ²=4.314, df=4, p=0.3651 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['redis_diskio']: χ²=6.333, df=4, p=0.1756 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_mem']: χ²=7.496, df=4, p=0.1119 → phụ thuộc, giữ
    - PC #18: α=0.310, cột ['frontend-external_workload', 'productcatalogservice_mem', 'redis_diskio', 'redis_cpu', 'productcatalogservice_latency'], số bin {'frontend-external_workload': 5, 'productcatalogservice_mem': 5, 'redis_diskio': 5, 'redis_cpu': 5, 'productcatalogservice_latency': 5}, F kề: ['productcatalogservice_mem', 'redis_diskio', 'productcatalogservice_latency']
      - kiểm F ⊥ redis_cpu | []: χ²=4.314, df=4, p=0.3651 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['redis_diskio']: χ²=6.333, df=4, p=0.1756 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['productcatalogservice_latency']: χ²=18.066, df=10, p=0.05386 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_mem']: χ²=7.496, df=4, p=0.1119 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_latency']: χ²=6.159, df=5, p=0.2911 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['productcatalogservice_mem']: χ²=18.619, df=11, p=0.06828 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['redis_diskio']: χ²=4.976, df=4, p=0.2897 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['redis_diskio', 'productcatalogservice_latency']: χ²=15.683, df=9, p=0.0738 → phụ thuộc, giữ
      - ... 2 phép kiểm nữa
    - PC #19: α=0.410, cột ['frontend-external_workload', 'productcatalogservice_mem', 'redis_diskio', 'redis_cpu', 'productcatalogservice_latency'], số bin {'frontend-external_workload': 5, 'productcatalogservice_mem': 5, 'redis_diskio': 5, 'redis_cpu': 5, 'productcatalogservice_latency': 5}, F kề: ['productcatalogservice_mem', 'redis_diskio', 'productcatalogservice_latency']
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | []: χ²=4.314, df=4, p=0.3651 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['productcatalogservice_mem']: χ²=18.619, df=11, p=0.06828 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['redis_diskio']: χ²=4.976, df=4, p=0.2897 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['redis_cpu']: χ²=8.381, df=8, p=0.3972 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_mem']: χ²=7.496, df=4, p=0.1119 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['redis_cpu']: χ²=5.593, df=4, p=0.2317 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_latency']: χ²=6.159, df=5, p=0.2911 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | ['productcatalogservice_mem']: χ²=4.206, df=7, p=0.7558 → độc lập, bỏ cạnh
      - ... 5 phép kiểm nữa
    - PC #20: α=0.510, cột ['frontend-external_workload', 'productcatalogservice_mem', 'redis_diskio', 'redis_cpu', 'productcatalogservice_latency'], số bin {'frontend-external_workload': 5, 'productcatalogservice_mem': 5, 'redis_diskio': 5, 'redis_cpu': 5, 'productcatalogservice_latency': 5}, F kề: ['redis_diskio', 'redis_cpu', 'productcatalogservice_latency']
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | []: χ²=4.314, df=4, p=0.3651 → phụ thuộc, giữ
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['productcatalogservice_mem']: χ²=18.619, df=11, p=0.06828 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['redis_diskio']: χ²=4.976, df=4, p=0.2897 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['redis_cpu']: χ²=8.381, df=8, p=0.3972 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['redis_diskio']: χ²=6.333, df=4, p=0.1756 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['redis_cpu']: χ²=5.579, df=7, p=0.5897 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_cpu | ['redis_diskio']: χ²=3.812, df=3, p=0.2825 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | ['productcatalogservice_latency']: χ²=6.968, df=7, p=0.4322 → phụ thuộc, giữ
      - ... 5 phép kiểm nữa
    - PC #21: α=0.610, cột ['frontend-external_workload', 'productcatalogservice_mem', 'redis_diskio', 'redis_cpu', 'productcatalogservice_latency'], số bin {'frontend-external_workload': 5, 'productcatalogservice_mem': 5, 'redis_diskio': 5, 'redis_cpu': 5, 'productcatalogservice_latency': 5}, F kề: ['productcatalogservice_mem', 'redis_diskio', 'productcatalogservice_latency']
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | []: χ²=4.314, df=4, p=0.3651 → phụ thuộc, giữ
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_mem | ['redis_diskio']: χ²=6.333, df=4, p=0.1756 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['redis_cpu']: χ²=5.579, df=7, p=0.5897 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['productcatalogservice_latency']: χ²=18.066, df=10, p=0.05386 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_mem']: χ²=7.496, df=4, p=0.1119 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['redis_cpu']: χ²=5.593, df=4, p=0.2317 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_latency']: χ²=6.159, df=5, p=0.2911 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | ['productcatalogservice_mem']: χ²=4.206, df=7, p=0.7558 → độc lập, bỏ cạnh
      - ... 5 phép kiểm nữa
    - PC #22: α=0.710, cột ['frontend-external_workload', 'productcatalogservice_mem', 'redis_diskio', 'redis_cpu', 'productcatalogservice_latency'], số bin {'frontend-external_workload': 5, 'productcatalogservice_mem': 5, 'redis_diskio': 5, 'redis_cpu': 5, 'productcatalogservice_latency': 5}, F kề: ['productcatalogservice_mem', 'redis_diskio', 'productcatalogservice_latency']
      - kiểm F ⊥ redis_cpu | []: χ²=4.314, df=4, p=0.3651 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → phụ thuộc, giữ
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | ['productcatalogservice_mem']: χ²=4.206, df=7, p=0.7558 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_mem']: χ²=7.496, df=4, p=0.1119 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_latency']: χ²=6.159, df=5, p=0.2911 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['productcatalogservice_mem']: χ²=18.619, df=11, p=0.06828 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['redis_diskio']: χ²=4.976, df=4, p=0.2897 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['redis_diskio']: χ²=6.333, df=4, p=0.1756 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['productcatalogservice_latency']: χ²=18.066, df=10, p=0.05386 → phụ thuộc, giữ
      - ... 3 phép kiểm nữa
    - PC #23: α=0.810, cột ['frontend-external_workload', 'productcatalogservice_mem', 'redis_diskio', 'redis_cpu', 'productcatalogservice_latency'], số bin {'frontend-external_workload': 5, 'productcatalogservice_mem': 5, 'redis_diskio': 5, 'redis_cpu': 5, 'productcatalogservice_latency': 5}, F kề: ['productcatalogservice_mem', 'redis_diskio', 'redis_cpu', 'productcatalogservice_latency']
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | []: χ²=4.314, df=4, p=0.3651 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['redis_diskio']: χ²=6.333, df=4, p=0.1756 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['redis_cpu']: χ²=5.579, df=7, p=0.5897 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['productcatalogservice_latency']: χ²=18.066, df=10, p=0.05386 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | ['productcatalogservice_mem']: χ²=4.206, df=7, p=0.7558 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | ['redis_diskio']: χ²=3.812, df=3, p=0.2825 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | ['productcatalogservice_latency']: χ²=6.968, df=7, p=0.4322 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_mem']: χ²=7.496, df=4, p=0.1119 → phụ thuộc, giữ
      - ... 21 phép kiểm nữa
    - PC #24: α=0.910, cột ['frontend-external_workload', 'productcatalogservice_mem', 'redis_diskio', 'redis_cpu', 'productcatalogservice_latency'], số bin {'frontend-external_workload': 5, 'productcatalogservice_mem': 5, 'redis_diskio': 5, 'redis_cpu': 5, 'productcatalogservice_latency': 5}, F kề: ['frontend-external_workload', 'productcatalogservice_mem', 'redis_diskio', 'productcatalogservice_latency']
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → phụ thuộc, giữ
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | []: χ²=4.314, df=4, p=0.3651 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['frontend-external_workload']: χ²=6.845, df=6, p=0.3354 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_mem']: χ²=7.496, df=4, p=0.1119 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['redis_cpu']: χ²=5.593, df=4, p=0.2317 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_latency']: χ²=6.159, df=5, p=0.2911 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | ['frontend-external_workload']: χ²=6.375, df=7, p=0.4967 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | ['productcatalogservice_mem']: χ²=4.206, df=7, p=0.7558 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | ['redis_diskio']: χ²=3.812, df=3, p=0.2825 → phụ thuộc, giữ
      - ... 55 phép kiểm nữa
    - PC #25: α=0.010, cột ['productcatalogservice_cpu'], số bin {'productcatalogservice_cpu': 5}, F kề: []
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → độc lập, bỏ cạnh
    - PC #26: α=0.110, cột ['productcatalogservice_cpu'], số bin {'productcatalogservice_cpu': 5}, F kề: []
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → độc lập, bỏ cạnh
    - PC #27: α=0.210, cột ['productcatalogservice_cpu'], số bin {'productcatalogservice_cpu': 5}, F kề: []
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → độc lập, bỏ cạnh
    - PC #28: α=0.310, cột ['productcatalogservice_cpu'], số bin {'productcatalogservice_cpu': 5}, F kề: []
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → độc lập, bỏ cạnh
    - PC #29: α=0.410, cột ['productcatalogservice_cpu'], số bin {'productcatalogservice_cpu': 5}, F kề: []
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → độc lập, bỏ cạnh
    - PC #30: α=0.510, cột ['productcatalogservice_cpu'], số bin {'productcatalogservice_cpu': 5}, F kề: []
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → độc lập, bỏ cạnh
    - PC #31: α=0.610, cột ['productcatalogservice_cpu'], số bin {'productcatalogservice_cpu': 5}, F kề: []
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → độc lập, bỏ cạnh
    - PC #32: α=0.710, cột ['productcatalogservice_cpu'], số bin {'productcatalogservice_cpu': 5}, F kề: ['productcatalogservice_cpu']
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → phụ thuộc, giữ
    - PC #33: α=0.001, cột ['redis_diskio', 'productcatalogservice_mem', 'productcatalogservice_latency', 'redis_cpu', 'frontend-external_workload', 'productcatalogservice_cpu'], số bin {'redis_diskio': 5, 'productcatalogservice_mem': 5, 'productcatalogservice_latency': 5, 'redis_cpu': 5, 'frontend-external_workload': 5, 'productcatalogservice_cpu': 5}, F kề: []
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_cpu | []: χ²=4.314, df=4, p=0.3651 → độc lập, bỏ cạnh
    - PC #34: α=0.101, cột ['redis_diskio', 'productcatalogservice_mem', 'productcatalogservice_latency', 'redis_cpu', 'frontend-external_workload', 'productcatalogservice_cpu'], số bin {'redis_diskio': 5, 'productcatalogservice_mem': 5, 'productcatalogservice_latency': 5, 'redis_cpu': 5, 'frontend-external_workload': 5, 'productcatalogservice_cpu': 5}, F kề: []
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_cpu | []: χ²=4.314, df=4, p=0.3651 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → độc lập, bỏ cạnh
    - PC #35: α=0.201, cột ['redis_diskio', 'productcatalogservice_mem', 'productcatalogservice_latency', 'redis_cpu', 'frontend-external_workload', 'productcatalogservice_cpu'], số bin {'redis_diskio': 5, 'productcatalogservice_mem': 5, 'productcatalogservice_latency': 5, 'redis_cpu': 5, 'frontend-external_workload': 5, 'productcatalogservice_cpu': 5}, F kề: ['redis_diskio']
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | []: χ²=4.314, df=4, p=0.3651 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → độc lập, bỏ cạnh
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → độc lập, bỏ cạnh
    - PC #36: α=0.301, cột ['redis_diskio', 'productcatalogservice_mem', 'productcatalogservice_latency', 'redis_cpu', 'frontend-external_workload', 'productcatalogservice_cpu'], số bin {'redis_diskio': 5, 'productcatalogservice_mem': 5, 'productcatalogservice_latency': 5, 'redis_cpu': 5, 'frontend-external_workload': 5, 'productcatalogservice_cpu': 5}, F kề: ['redis_diskio', 'productcatalogservice_mem', 'productcatalogservice_latency']
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → phụ thuộc, giữ
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_cpu | []: χ²=4.314, df=4, p=0.3651 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_latency | ['redis_diskio']: χ²=4.976, df=4, p=0.2897 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['productcatalogservice_mem']: χ²=18.619, df=11, p=0.06828 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_mem']: χ²=7.496, df=4, p=0.1119 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_latency']: χ²=6.159, df=5, p=0.2911 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['redis_diskio']: χ²=6.333, df=4, p=0.1756 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['productcatalogservice_latency']: χ²=18.066, df=10, p=0.05386 → phụ thuộc, giữ
      - ... 3 phép kiểm nữa
    - PC #37: α=0.401, cột ['redis_diskio', 'productcatalogservice_mem', 'productcatalogservice_latency', 'redis_cpu', 'frontend-external_workload', 'productcatalogservice_cpu'], số bin {'redis_diskio': 5, 'productcatalogservice_mem': 5, 'productcatalogservice_latency': 5, 'redis_cpu': 5, 'frontend-external_workload': 5, 'productcatalogservice_cpu': 5}, F kề: ['redis_diskio', 'productcatalogservice_latency']
      - kiểm F ⊥ redis_cpu | []: χ²=4.314, df=4, p=0.3651 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → phụ thuộc, giữ
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['redis_diskio']: χ²=6.333, df=4, p=0.1756 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['productcatalogservice_latency']: χ²=18.066, df=10, p=0.05386 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['redis_cpu']: χ²=5.579, df=7, p=0.5897 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_cpu | ['redis_diskio']: χ²=3.812, df=3, p=0.2825 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | ['productcatalogservice_latency']: χ²=6.968, df=7, p=0.4322 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_latency']: χ²=6.159, df=5, p=0.2911 → phụ thuộc, giữ
      - ... 1 phép kiểm nữa
    - PC #38: α=0.501, cột ['redis_diskio', 'productcatalogservice_mem', 'productcatalogservice_latency', 'redis_cpu', 'frontend-external_workload', 'productcatalogservice_cpu'], số bin {'redis_diskio': 5, 'productcatalogservice_mem': 5, 'productcatalogservice_latency': 5, 'redis_cpu': 5, 'frontend-external_workload': 5, 'productcatalogservice_cpu': 5}, F kề: ['redis_diskio', 'productcatalogservice_latency', 'redis_cpu']
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → phụ thuộc, giữ
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_cpu | []: χ²=4.314, df=4, p=0.3651 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_mem | ['redis_diskio']: χ²=6.333, df=4, p=0.1756 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['productcatalogservice_latency']: χ²=18.066, df=10, p=0.05386 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['redis_cpu']: χ²=5.579, df=7, p=0.5897 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_cpu | ['redis_diskio']: χ²=3.812, df=3, p=0.2825 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | ['productcatalogservice_latency']: χ²=6.968, df=7, p=0.4322 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['redis_diskio']: χ²=4.976, df=4, p=0.2897 → phụ thuộc, giữ
      - ... 6 phép kiểm nữa
    - PC #39: α=0.601, cột ['redis_diskio', 'productcatalogservice_mem', 'productcatalogservice_latency', 'redis_cpu', 'frontend-external_workload', 'productcatalogservice_cpu'], số bin {'redis_diskio': 5, 'productcatalogservice_mem': 5, 'productcatalogservice_latency': 5, 'redis_cpu': 5, 'frontend-external_workload': 5, 'productcatalogservice_cpu': 5}, F kề: ['redis_diskio', 'productcatalogservice_mem', 'productcatalogservice_latency']
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → phụ thuộc, giữ
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_cpu | []: χ²=4.314, df=4, p=0.3651 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_mem']: χ²=7.496, df=4, p=0.1119 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_latency']: χ²=6.159, df=5, p=0.2911 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['redis_cpu']: χ²=5.593, df=4, p=0.2317 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['redis_diskio']: χ²=4.976, df=4, p=0.2897 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['productcatalogservice_mem']: χ²=18.619, df=11, p=0.06828 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | ['redis_cpu']: χ²=8.381, df=8, p=0.3972 → phụ thuộc, giữ
      - ... 8 phép kiểm nữa
    - PC #40: α=0.701, cột ['redis_diskio', 'productcatalogservice_mem', 'productcatalogservice_latency', 'redis_cpu', 'frontend-external_workload', 'productcatalogservice_cpu'], số bin {'redis_diskio': 5, 'productcatalogservice_mem': 5, 'productcatalogservice_latency': 5, 'redis_cpu': 5, 'frontend-external_workload': 5, 'productcatalogservice_cpu': 5}, F kề: ['redis_diskio', 'productcatalogservice_mem', 'productcatalogservice_latency']
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | []: χ²=4.314, df=4, p=0.3651 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | ['redis_diskio']: χ²=3.812, df=3, p=0.2825 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | ['productcatalogservice_mem']: χ²=4.206, df=7, p=0.7558 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_mem | ['redis_diskio']: χ²=6.333, df=4, p=0.1756 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['productcatalogservice_latency']: χ²=18.066, df=10, p=0.05386 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['productcatalogservice_cpu']: χ²=11.380, df=10, p=0.3287 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_mem']: χ²=7.496, df=4, p=0.1119 → phụ thuộc, giữ
      - ... 8 phép kiểm nữa
    - PC #41: α=0.801, cột ['redis_diskio', 'productcatalogservice_mem', 'productcatalogservice_latency', 'redis_cpu', 'frontend-external_workload', 'productcatalogservice_cpu'], số bin {'redis_diskio': 5, 'productcatalogservice_mem': 5, 'productcatalogservice_latency': 5, 'redis_cpu': 5, 'frontend-external_workload': 5, 'productcatalogservice_cpu': 5}, F kề: ['redis_diskio', 'productcatalogservice_mem', 'productcatalogservice_latency', 'redis_cpu']
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | []: χ²=4.314, df=4, p=0.3651 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → phụ thuộc, giữ
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → độc lập, bỏ cạnh
      - kiểm F ⊥ redis_cpu | ['redis_diskio']: χ²=3.812, df=3, p=0.2825 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | ['productcatalogservice_mem']: χ²=4.206, df=7, p=0.7558 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | ['productcatalogservice_latency']: χ²=6.968, df=7, p=0.4322 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | ['productcatalogservice_cpu']: χ²=11.830, df=8, p=0.159 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_cpu | ['redis_diskio']: χ²=1.400, df=4, p=0.8442 → độc lập, bỏ cạnh
      - kiểm F ⊥ productcatalogservice_mem | ['redis_diskio']: χ²=6.333, df=4, p=0.1756 → phụ thuộc, giữ
      - ... 24 phép kiểm nữa
    - PC #42: α=0.901, cột ['redis_diskio', 'productcatalogservice_mem', 'productcatalogservice_latency', 'redis_cpu', 'frontend-external_workload', 'productcatalogservice_cpu'], số bin {'redis_diskio': 5, 'productcatalogservice_mem': 5, 'productcatalogservice_latency': 5, 'redis_cpu': 5, 'frontend-external_workload': 5, 'productcatalogservice_cpu': 5}, F kề: ['redis_diskio', 'productcatalogservice_mem', 'productcatalogservice_latency', 'frontend-external_workload', 'productcatalogservice_cpu']
      - kiểm F ⊥ productcatalogservice_cpu | []: χ²=2.628, df=4, p=0.6219 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | []: χ²=6.000, df=4, p=0.1991 → phụ thuộc, giữ
      - kiểm F ⊥ frontend-external_workload | []: χ²=1.224, df=4, p=0.8741 → phụ thuộc, giữ
      - kiểm F ⊥ redis_cpu | []: χ²=4.314, df=4, p=0.3651 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_latency | []: χ²=5.210, df=4, p=0.2664 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | []: χ²=5.882, df=4, p=0.2081 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['redis_diskio']: χ²=6.333, df=4, p=0.1756 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['productcatalogservice_latency']: χ²=18.066, df=10, p=0.05386 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['redis_cpu']: χ²=5.579, df=7, p=0.5897 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['frontend-external_workload']: χ²=16.173, df=11, p=0.1348 → phụ thuộc, giữ
      - kiểm F ⊥ productcatalogservice_mem | ['productcatalogservice_cpu']: χ²=11.380, df=10, p=0.3287 → phụ thuộc, giữ
      - kiểm F ⊥ redis_diskio | ['productcatalogservice_mem']: χ²=7.496, df=4, p=0.1119 → phụ thuộc, giữ
      - ... 134 phép kiểm nữa

## Thứ hạng cuối

['checkoutservice_A', 'cartservice_A', 'shippingservice_A', 'currencyservice_A', 'frontend_A', 'emailservice_A', 'recommendationservice_A', 'paymentservice_A', 'adservice_A', 'traceservice_A', 'health_A', 'productcatalogservice_A', 'redis_A', 'frontend-external_A']
