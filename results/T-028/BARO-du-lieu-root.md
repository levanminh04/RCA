# Dữ liệu root BARO theo quy ước SimpleRCA

Nguồn mọi số: `results/T-028/runs/phan-hoi-review-001/BARO-root-data.json`; mỗi ca có source file aggregate và bản ghi BARO. Không dùng các số này làm threshold/nhãn của BARO; local_nonpositive/M6=N/A. Metric là raw finite, trace start-split, log A; proxy end-split giữ riêng.

## RE2-TT / dev-03d4910932

Root `ts-route-service`; status `OK`. Score entity BARO `[803.9999999991951]`; O=68, R=68; Hit@1=1, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-03d4910932-sNone-h0-cbbe5c/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-03d4910932.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-route-service_cpu / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 4.25891 | 0.367563 | 290 | available |
| ts-route-service_diskio / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 51595.4 | 16102.6 | 0 | available |
| ts-route-service_latency-50 / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 0.00321006 | 2.14873e-05 | 292 | available |
| ts-route-service_latency-90 / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 0.00506528 | 0.00019398 | 292 | available |
| ts-route-service_mem / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 2.6754e+08 | 35385.6 | 290 | available |
| ts-route-service_socket / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 13.2167 | 0.767934 | 290 | available |
| ts-route-service_workload / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 34.8953 | 3.1686 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-route-service_mem | ts-route-service | [803.9999999991951] |
| ts-route-service_latency | ts-route-service | [423.66643754793375] |
| ts-route-service_cpu | ts-route-service | [241.4880904580487] |
| ts-route-service_socket | ts-route-service | [20.0] |
| ts-route-service_workload | ts-route-service | [1.4070077666449263] |
| ts-route-service_diskio | ts-route-service | [1.324583759759712] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-route-service | ts-route-service | 15768 | 14622 | 3291.65 | 88817.5 | True | True | True | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-route-service | ts-route-service | 15768 | 14622 | 3291.65 | 88817.5 | True | True | True | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-route-service | ts-route-service | 4882 | 0 | available |

## RE2-TT / dev-12a1a88069

Root `ts-order-service`; status `OK`. Score entity BARO `[488346.9281628153]`; O=68, R=68; Hit@1=1, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-12a1a88069-sNone-h0-23307e/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-12a1a88069.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-order-service_cpu / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 5.3552 | 2.09547 | 271 | available |
| ts-order-service_diskio / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 53246.4 | 16479.4 | 295 | available |
| ts-order-service_error / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 0 | 0 | 0 | available |
| ts-order-service_latency-50 / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 0.0104459 | 0.0013046 | 300 | available |
| ts-order-service_latency-90 / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 0.0987284 | 0.161946 | 0 | available |
| ts-order-service_mem / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 2.76339e+08 | 1.36353e+06 | 295 | available |
| ts-order-service_socket / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 11.93 | 1.18818 | 213 | available |
| ts-order-service_workload / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 5.94554 | 2.47958 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-order-service_diskio | ts-order-service | [488346.9281628153] |
| ts-order-service_mem | ts-order-service | [101.33612040133757] |
| ts-order-service_cpu | ts-order-service | [9.774102701644333] |
| ts-order-service_latency | ts-order-service | [5.41678094317462] |
| ts-order-service_socket | ts-order-service | [3.0] |
| ts-order-service_workload | ts-order-service | [0.6833591372590894] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-order-service | ts-order-service | 2970 | 2965 | 48984.5 | 125126 | True | False | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-order-service | ts-order-service | 2970 | 2965 | 48984.5 | 125126 | True | False | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-order-service | ts-order-service | 1778 | 0 | available |

## RE2-TT / dev-14372e1209

Root `ts-route-service`; status `OK`. Score entity BARO `[3907.4188034195304]`; O=68, R=68; Hit@1=0, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-14372e1209-sNone-h0-9b694a/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-14372e1209.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-route-service_cpu / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 5.49181 | 1.39121 | 275 | available |
| ts-route-service_diskio / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 52998.8 | 16655.5 | 294 | available |
| ts-route-service_latency-50 / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 0.00325867 | 9.11583e-05 | 276 | available |
| ts-route-service_latency-90 / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 0.00577557 | 0.00105772 | 282 | available |
| ts-route-service_mem / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 2.65837e+08 | 109661 | 294 | available |
| ts-route-service_socket / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 12.4567 | 1.01725 | 294 | available |
| ts-route-service_workload / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 33.4692 | 2.82137 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-route-service_mem | ts-route-service | [3907.4188034195304] |
| ts-route-service_diskio | ts-route-service | [1428.2441977336578] |
| ts-route-service_latency | ts-route-service | [63.44080654002317] |
| ts-route-service_cpu | ts-route-service | [41.07618604564801] |
| ts-route-service_socket | ts-route-service | [10.0] |
| ts-route-service_workload | ts-route-service | [1.9082397003745328] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-route-service | ts-route-service | 15018 | 14904 | 3337.15 | 71292.6 | True | True | True | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-route-service | ts-route-service | 15018 | 14904 | 3337.15 | 71292.6 | True | True | True | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-route-service | ts-route-service | 4970 | 0 | available |

## RE2-TT / dev-16597725c1

Root `ts-auth-service`; status `OK`. Score entity BARO `[47.48000000000497]`; O=68, R=68; Hit@1=0, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-16597725c1-sNone-h0-b83c52/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-16597725c1.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-auth-service_cpu / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 14.0649 | 1.33966 | 290 | available |
| ts-auth-service_diskio / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 50188.6 | 16405.2 | 0 | available |
| ts-auth-service_latency-50 / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 0.221016 | 0.0184259 | 277 | available |
| ts-auth-service_latency-90 / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 0.521312 | 0.119303 | 277 | available |
| ts-auth-service_mem / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 2.5786e+08 | 47391.8 | 290 | available |
| ts-auth-service_socket / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 12.1067 | 0.745177 | 258 | available |
| ts-auth-service_workload / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 2.78353 | 0.221149 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-auth-service_mem | ts-auth-service | [47.48000000000497] |
| ts-auth-service_latency | ts-auth-service | [43.97026593233664] |
| ts-auth-service_cpu | ts-auth-service | [20.178943661904235] |
| ts-auth-service_socket | ts-auth-service | [6.0] |
| ts-auth-service_diskio | ts-auth-service | [1.1932618644832744] |
| ts-auth-service_workload | ts-auth-service | [1.0037593984962419] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-auth-service | ts-auth-service | 2085 | 1994 | 328295 | 938884 | True | False | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-auth-service | ts-auth-service | 2085 | 1994 | 328295 | 938884 | True | False | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-auth-service | ts-auth-service | 1592 | 0 | available |

## RE2-TT / dev-16870e660c

Root `ts-route-service`; status `OK`. Score entity BARO `[9738.500000001522]`; O=68, R=68; Hit@1=1, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-16870e660c-sNone-h0-fab858/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-16870e660c.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-route-service_cpu / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 4.00906 | 0.435439 | 295 | available |
| ts-route-service_diskio / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 50575.8 | 15548.7 | 295 | available |
| ts-route-service_latency-50 / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 0.00320811 | 2.57282e-05 | 287 | available |
| ts-route-service_latency-90 / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 0.00508548 | 0.000277706 | 287 | available |
| ts-route-service_mem / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 2.55359e+08 | 51615.3 | 295 | available |
| ts-route-service_socket / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 14.1833 | 0.936156 | 295 | available |
| ts-route-service_workload / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 32.9107 | 2.72391 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-route-service_mem | ts-route-service | [9738.500000001522] |
| ts-route-service_latency | ts-route-service | [2687.9510538900877] |
| ts-route-service_diskio | ts-route-service | [1431.0266318134156] |
| ts-route-service_cpu | ts-route-service | [69.94690344361655] |
| ts-route-service_socket | ts-route-service | [7.0] |
| ts-route-service_workload | ts-route-service | [1.5155000000000007] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-route-service | ts-route-service | 14667 | 13653 | 3305 | 69328.8 | True | True | True | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-route-service | ts-route-service | 14667 | 13653 | 3305 | 69328.8 | True | True | True | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-route-service | ts-route-service | 4558 | 0 | available |

## RE2-TT / dev-1e6d61b5ec

Root `ts-order-service`; status `OK`. Score entity BARO `[568989.4013078625]`; O=68, R=68; Hit@1=1, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-1e6d61b5ec-sNone-h0-ed1564/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-1e6d61b5ec.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-order-service_cpu / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 1.17882 | 0.585273 | 281 | available |
| ts-order-service_diskio / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 52665.3 | 16473.9 | 279 | available |
| ts-order-service_latency-50 / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 0.0196259 | 0.00234495 | 90 | available |
| ts-order-service_latency-90 / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 0.0487246 | 0.0149578 | 233 | available |
| ts-order-service_mem / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 2.50349e+08 | 1.57044e+06 | 279 | available |
| ts-order-service_socket / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 9.18333 | 0.759203 | 279 | available |
| ts-order-service_workload / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 0.418243 | 0.30241 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-order-service_diskio | ts-order-service | [568989.4013078625] |
| ts-order-service_mem | ts-order-service | [106.73843700159448] |
| ts-order-service_cpu | ts-order-service | [36.27441245544689] |
| ts-order-service_latency | ts-order-service | [6.387947269303194] |
| ts-order-service_socket | ts-order-service | [4.0] |
| ts-order-service_workload | ts-order-service | [1.5717344753747322] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-order-service | ts-order-service | 236 | 167 | 27452.5 | 100090 | True | True | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-order-service | ts-order-service | 236 | 167 | 27452.5 | 100090 | True | True | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-order-service | ts-order-service | 133 | 0 | available |

## RE2-TT / dev-20acb4402d

Root `ts-order-service`; status `OK`. Score entity BARO `[4209.481568627397]`; O=68, R=68; Hit@1=1, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-20acb4402d-sNone-h0-22e6bd/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-20acb4402d.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-order-service_cpu / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 0.452463 | 0.133995 | 5 | available |
| ts-order-service_diskio / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 53198.6 | 16536.5 | 0 | available |
| ts-order-service_error / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 0 | 0 | 0 | available |
| ts-order-service_latency-50 / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 0.0137356 | 0.00134103 | 30 | available |
| ts-order-service_latency-90 / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 0.0231785 | 0.000699898 | 180 | available |
| ts-order-service_mem / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 2.68994e+08 | 219041 | 17 | available |
| ts-order-service_socket / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 9.7 | 0.732575 | 0 | available |
| ts-order-service_workload / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 0.441387 | 0.245998 | 8 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-order-service_latency | ts-order-service | [4209.481568627397] |
| ts-order-service_mem | ts-order-service | [13.018518518519052] |
| ts-order-service_cpu | ts-order-service | [3.012899374080423] |
| ts-order-service_workload | ts-order-service | [2.0957827019299495] |
| ts-order-service_diskio | ts-order-service | [1.0387442893992664] |
| ts-order-service_socket | ts-order-service | [0.0] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-order-service | ts-order-service | 234 | 271 | 18793 | 212267 | True | True | True | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-order-service | ts-order-service | 234 | 271 | 18793 | 212267 | True | True | True | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-order-service | ts-order-service | 213 | 0 | available |

## RE2-TT / dev-260d332c8d

Root `ts-order-service`; status `OK`. Score entity BARO `[5307.411003236236]`; O=68, R=68; Hit@1=1, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-260d332c8d-sNone-h0-dbdbd7/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-260d332c8d.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-order-service_cpu / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 0.416221 | 0.467813 | 13 | available |
| ts-order-service_diskio / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 52961.5 | 18024.4 | 0 | available |
| ts-order-service_error / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 0 | 0 | 0 | available |
| ts-order-service_latency-50 / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 0.0135427 | 0.00154018 | 90 | available |
| ts-order-service_latency-90 / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 0.0229575 | 0.000657856 | 184 | available |
| ts-order-service_mem / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 2.72361e+08 | 106570 | 300 | available |
| ts-order-service_socket / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 9.27333 | 0.696627 | 0 | available |
| ts-order-service_workload / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 0.401307 | 0.236012 | 8 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-order-service_latency | ts-order-service | [5307.411003236236] |
| ts-order-service_cpu | ts-order-service | [15.718548932925136] |
| ts-order-service_mem | ts-order-service | [13.900000000005413] |
| ts-order-service_workload | ts-order-service | [2.7556390977443606] |
| ts-order-service_diskio | ts-order-service | [1.3494407594292588] |
| ts-order-service_socket | ts-order-service | [1.0] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-order-service | ts-order-service | 206 | 219 | 18527.5 | 213391 | True | True | True | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-order-service | ts-order-service | 206 | 219 | 18527.5 | 213391 | True | True | True | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-order-service | ts-order-service | 177 | 0 | available |

## RE2-TT / dev-3ae0a6c15a

Root `ts-train-service`; status `OK`. Score entity BARO `[1882.7374317907058]`; O=68, R=68; Hit@1=1, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-3ae0a6c15a-sNone-h0-f83ef5/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-3ae0a6c15a.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-train-service_cpu / ts-train-service | ts-train-service | 297 | 300 | 3 / 0 | 3.06948 | 0.365732 | 291 | available |
| ts-train-service_diskio / ts-train-service | ts-train-service | 297 | 300 | 3 / 0 | 52444.6 | 15884.4 | 0 | available |
| ts-train-service_error / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 0 | 0 | 0 | available |
| ts-train-service_latency-50 / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 0.00656947 | 0.000157946 | 273 | available |
| ts-train-service_latency-90 / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 0.0094231 | 3.01471e-05 | 288 | available |
| ts-train-service_mem / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 2.64251e+08 | 70285.9 | 291 | available |
| ts-train-service_socket / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 11.2433 | 0.835138 | 177 | available |
| ts-train-service_workload / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 21.4891 | 2.42902 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-train-service_latency | ts-train-service | [1882.7374317907058] |
| ts-train-service_mem | ts-train-service | [233.00000000041356] |
| ts-train-service_cpu | ts-train-service | [175.19230015285262] |
| ts-train-service_socket | ts-train-service | [6.0] |
| ts-train-service_diskio | ts-train-service | [1.4368076454140324] |
| ts-train-service_workload | ts-train-service | [1.236674461736958] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-train-service | ts-train-service | 16225 | 15155 | 4554 | 53078.9 | True | True | True | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-train-service | ts-train-service | 16225 | 15155 | 4554 | 53078.9 | True | True | True | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-train-service | ts-train-service | 2 | 0 | available |

## RE2-TT / dev-3defe3d34b

Root `ts-auth-service`; status `OK`. Score entity BARO `[382.333333332954]`; O=68, R=68; Hit@1=1, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-3defe3d34b-sNone-h0-dfc9c4/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-3defe3d34b.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-auth-service_cpu / ts-auth-service | ts-auth-service | 300 | 297 | 0 / 3 | 13.9821 | 1.25574 | 293 | available |
| ts-auth-service_diskio / ts-auth-service | ts-auth-service | 300 | 297 | 0 / 3 | 49831.9 | 14993.3 | 40 | available |
| ts-auth-service_latency-50 / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 0.178933 | 0.00291813 | 279 | available |
| ts-auth-service_latency-90 / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 0.250266 | 0.0185425 | 279 | available |
| ts-auth-service_mem / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 2.57349e+08 | 6076.5 | 297 | available |
| ts-auth-service_socket / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 13.5333 | 0.579272 | 252 | available |
| ts-auth-service_workload / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 2.8133 | 0.213987 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-auth-service_mem | ts-auth-service | [382.333333332954] |
| ts-auth-service_latency | ts-auth-service | [71.66862714530694] |
| ts-auth-service_cpu | ts-auth-service | [33.68700512825861] |
| ts-auth-service_diskio | ts-auth-service | [10.369238387414125] |
| ts-auth-service_socket | ts-auth-service | [5.0] |
| ts-auth-service_workload | ts-auth-service | [1.1746031746031749] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-auth-service | ts-auth-service | 2105 | 2085 | 161529 | 401617 | True | False | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-auth-service | ts-auth-service | 2105 | 2085 | 161529 | 401617 | True | False | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-auth-service | ts-auth-service | N/A | N/A | missing_channel |

## RE2-TT / dev-4e68956051

Root `ts-train-service`; status `OK`. Score entity BARO `[8131.705430224151]`; O=68, R=68; Hit@1=1, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-4e68956051-sNone-h0-70526f/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-4e68956051.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-train-service_cpu / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 3.25626 | 0.249118 | 33 | available |
| ts-train-service_diskio / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 53225.3 | 18212.7 | 0 | available |
| ts-train-service_latency-50 / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 0.00548679 | 0.000211215 | 283 | available |
| ts-train-service_latency-90 / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 0.00929022 | 5.99518e-05 | 287 | available |
| ts-train-service_mem / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 2.59046e+08 | 29075.1 | 287 | available |
| ts-train-service_socket / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 13.9633 | 0.7585 | 287 | available |
| ts-train-service_workload / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 21.0185 | 1.75037 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-train-service_latency | ts-train-service | [8131.705430224151] |
| ts-train-service_mem | ts-train-service | [276.50000000164107] |
| ts-train-service_cpu | ts-train-service | [5.876517383028243] |
| ts-train-service_socket | ts-train-service | [5.5] |
| ts-train-service_diskio | ts-train-service | [1.3011352756134125] |
| ts-train-service_workload | ts-train-service | [0.08276432857438418] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-train-service | ts-train-service | 15780 | 11574 | 4223 | 405062 | True | True | True | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-train-service | ts-train-service | 15780 | 11574 | 4223 | 405062 | True | True | True | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-train-service | ts-train-service | 4 | 0 | available |

## RE2-TT / dev-4f8a844308

Root `ts-route-service`; status `OK`. Score entity BARO `[38037.66666680458]`; O=68, R=68; Hit@1=1, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-4f8a844308-sNone-h0-05dc03/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-4f8a844308.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-route-service_cpu / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 3.84693 | 0.45022 | 295 | available |
| ts-route-service_diskio / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 51857.3 | 16385.3 | 295 | available |
| ts-route-service_error / ts-route-service | ts-route-service | 0 | 270 | 300 / 30 | N/A | N/A | N/A | insufficient_N |
| ts-route-service_latency-50 / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 0.00346895 | 0.000105608 | 285 | available |
| ts-route-service_latency-90 / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 0.00747958 | 0.000382362 | 285 | available |
| ts-route-service_mem / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 2.66628e+08 | 88849.2 | 254 | available |
| ts-route-service_socket / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 19.2833 | 0.854238 | 32 | available |
| ts-route-service_workload / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 28.8277 | 3.66187 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-route-service_mem | ts-route-service | [38037.66666680458] |
| ts-route-service_diskio | ts-route-service | [1685.6967830870576] |
| ts-route-service_latency | ts-route-service | [505.46653587127287] |
| ts-route-service_cpu | ts-route-service | [88.18625455238262] |
| ts-route-service_socket | ts-route-service | [4.0] |
| ts-route-service_workload | ts-route-service | [1.4998557830977794] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-route-service | ts-route-service | 13101 | 12270 | 3624 | 78897.4 | True | True | True | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-route-service | ts-route-service | 13101 | 12270 | 3624 | 78897.4 | True | True | True | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-route-service | ts-route-service | 4417 | 23 | available |

## RE2-TT / dev-57546fd87b

Root `ts-auth-service`; status `OK`. Score entity BARO `[3.105726872246616]`; O=68, R=68; Hit@1=0, Hit@5=0. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-57546fd87b-sNone-h0-3fb7f2/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-57546fd87b.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-auth-service_cpu / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 14.9808 | 1.36448 | 0 | available |
| ts-auth-service_diskio / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 50157.8 | 16661.5 | 0 | available |
| ts-auth-service_latency-50 / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 0.255191 | 0.0372951 | 267 | available |
| ts-auth-service_latency-90 / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 0.857059 | 0.392153 | 0 | available |
| ts-auth-service_mem / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 2.43466e+08 | 506589 | 242 | available |
| ts-auth-service_socket / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 16.9267 | 1.31452 | 0 | available |
| ts-auth-service_workload / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 2.7458 | 0.224719 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-auth-service_mem | ts-auth-service | [3.105726872246616] |
| ts-auth-service_latency | ts-auth-service | [2.401298004744095] |
| ts-auth-service_workload | ts-auth-service | [1.2318339100346025] |
| ts-auth-service_diskio | ts-auth-service | [1.1685735191602569] |
| ts-auth-service_socket | ts-auth-service | [1.0] |
| ts-auth-service_cpu | ts-auth-service | [0.7642559248269525] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-auth-service | ts-auth-service | 2065 | 1995 | 393143 | 799459 | True | False | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-auth-service | ts-auth-service | 2065 | 1995 | 393143 | 799459 | True | False | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-auth-service | ts-auth-service | 1600 | 0 | available |

## RE2-TT / dev-59f696a169

Root `ts-auth-service`; status `OK`. Score entity BARO `[102.54545454548047]`; O=68, R=68; Hit@1=0, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-59f696a169-sNone-h0-db76fe/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-59f696a169.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-auth-service_cpu / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 13.9859 | 2.19968 | 279 | available |
| ts-auth-service_diskio / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 50522.1 | 22148.7 | 0 | available |
| ts-auth-service_latency-50 / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 0.239071 | 0.0285015 | 270 | available |
| ts-auth-service_latency-90 / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 0.623765 | 0.148506 | 276 | available |
| ts-auth-service_mem / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 2.59292e+08 | 48859.6 | 298 | available |
| ts-auth-service_socket / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 12.5167 | 1.02456 | 220 | available |
| ts-auth-service_workload / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 2.76797 | 0.203604 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-auth-service_mem | ts-auth-service | [102.54545454548047] |
| ts-auth-service_cpu | ts-auth-service | [14.106753881489544] |
| ts-auth-service_latency | ts-auth-service | [7.421296244722441] |
| ts-auth-service_socket | ts-auth-service | [5.0] |
| ts-auth-service_workload | ts-auth-service | [2.0] |
| ts-auth-service_diskio | ts-auth-service | [1.1860416390945756] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-auth-service | ts-auth-service | 2055 | 2032 | 368347 | 1.00456e+06 | True | False | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-auth-service | ts-auth-service | 2055 | 2032 | 368347 | 1.00456e+06 | True | False | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-auth-service | ts-auth-service | 1626 | 0 | available |

## RE2-TT / dev-746fd74313

Root `ts-auth-service`; status `OK`. Score entity BARO `[30.68613180352903]`; O=68, R=68; Hit@1=0, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-746fd74313-sNone-h0-7cac1b/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-746fd74313.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-auth-service_cpu / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 13.8785 | 1.87525 | 0 | available |
| ts-auth-service_diskio / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 51343.1 | 17096.3 | 41 | available |
| ts-auth-service_latency-50 / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 0.177508 | 0.00437469 | 284 | available |
| ts-auth-service_latency-90 / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 0.262237 | 0.0363062 | 284 | available |
| ts-auth-service_mem / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 2.57481e+08 | 26537.7 | 33 | available |
| ts-auth-service_socket / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 10.5467 | 0.497817 | 228 | available |
| ts-auth-service_workload / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 2.81874 | 0.259002 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-auth-service_latency | ts-auth-service | [30.68613180352903] |
| ts-auth-service_mem | ts-auth-service | [17.333333333261375] |
| ts-auth-service_diskio | ts-auth-service | [8.196234291387997] |
| ts-auth-service_socket | ts-auth-service | [3.0] |
| ts-auth-service_cpu | ts-auth-service | [0.24050874283432544] |
| ts-auth-service_workload | ts-auth-service | [0.1981981981981976] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-auth-service | ts-auth-service | 1792 | 1608 | 140291 | 530416 | True | True | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-auth-service | ts-auth-service | 1792 | 1608 | 140291 | 530416 | True | True | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-auth-service | ts-auth-service | 1572 | 0 | available |

## RE2-TT / dev-7f1b6b071d

Root `ts-travel-service`; status `OK`. Score entity BARO `[103.25000000001648]`; O=68, R=68; Hit@1=1, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-7f1b6b071d-sNone-h0-b833aa/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-7f1b6b071d.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-travel-service_cpu / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 3.41554 | 0.647029 | 55 | available |
| ts-travel-service_diskio / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 51786.5 | 15684.6 | 0 | available |
| ts-travel-service_error / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 0 | 0 | 60 | available |
| ts-travel-service_latency-50 / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 0.0180825 | 0.000309225 | 255 | available |
| ts-travel-service_latency-90 / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 0.188345 | 0.0873376 | 239 | available |
| ts-travel-service_mem / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 2.84654e+08 | 92530.5 | 276 | available |
| ts-travel-service_socket / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 17.9167 | 2.02066 | 0 | available |
| ts-travel-service_workload / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 9.98756 | 2.69176 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-travel-service_mem | ts-travel-service | [103.25000000001648] |
| ts-travel-service_cpu | ts-travel-service | [9.541587888933153] |
| ts-travel-service_latency | ts-travel-service | [4.33492292477771] |
| ts-travel-service_workload | ts-travel-service | [1.6936026936026933] |
| ts-travel-service_socket | ts-travel-service | [1.6666666666666667] |
| ts-travel-service_diskio | ts-travel-service | [1.3429227959946166] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-travel-service | ts-travel-service | 9868 | 8327 | 50930.9 | 264990 | True | True | True | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-travel-service | ts-travel-service | 9868 | 8327 | 50930.9 | 264990 | True | True | True | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-travel-service | ts-travel-service | 11196 | 110 | available |

## RE2-TT / dev-8017c6dc70

Root `ts-order-service`; status `OK`. Score entity BARO `[520871.5182156458]`; O=68, R=68; Hit@1=1, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-8017c6dc70-sNone-h0-b7d8f1/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-8017c6dc70.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-order-service_cpu / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 0.566482 | 0.151725 | 278 | available |
| ts-order-service_diskio / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 52861.2 | 17370.2 | 298 | available |
| ts-order-service_latency-50 / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 0.014451 | 0.0013101 | 221 | available |
| ts-order-service_latency-90 / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 0.0241673 | 0.00186338 | 280 | available |
| ts-order-service_mem / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 2.52305e+08 | 380060 | 298 | available |
| ts-order-service_socket / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 9.54 | 0.573062 | 295 | available |
| ts-order-service_workload / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 0.466083 | 0.28851 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-order-service_diskio | ts-order-service | [520871.5182156458] |
| ts-order-service_mem | ts-order-service | [677.4591836734635] |
| ts-order-service_cpu | ts-order-service | [120.23308113515641] |
| ts-order-service_latency | ts-order-service | [97.93607305936051] |
| ts-order-service_socket | ts-order-service | [4.0] |
| ts-order-service_workload | ts-order-service | [0.8583690987124464] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-order-service | ts-order-service | 256 | 211 | 20611.2 | 92687.5 | True | True | True | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-order-service | ts-order-service | 256 | 211 | 20611.2 | 92687.5 | True | True | True | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-order-service | ts-order-service | 177 | 0 | available |

## RE2-TT / dev-98bc73c499

Root `ts-train-service`; status `OK`. Score entity BARO `[609.5732880456266]`; O=68, R=68; Hit@1=1, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-98bc73c499-sNone-h0-de6480/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-98bc73c499.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-train-service_cpu / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 2.77513 | 0.270588 | 288 | available |
| ts-train-service_diskio / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 51614.5 | 16315 | 0 | available |
| ts-train-service_error / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 0 | 0 | 0 | available |
| ts-train-service_latency-50 / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 0.00392385 | 5.90531e-05 | 273 | available |
| ts-train-service_latency-90 / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 0.00863178 | 8.10048e-05 | 288 | available |
| ts-train-service_mem / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 2.70827e+08 | 45860.2 | 299 | available |
| ts-train-service_socket / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 12.21 | 0.657698 | 142 | available |
| ts-train-service_workload / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 21.0009 | 1.94453 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-train-service_latency | ts-train-service | [609.5732880456266] |
| ts-train-service_mem | ts-train-service | [279.5000000006922] |
| ts-train-service_cpu | ts-train-service | [179.7461015271511] |
| ts-train-service_socket | ts-train-service | [4.0] |
| ts-train-service_workload | ts-train-service | [2.7573778422835025] |
| ts-train-service_diskio | ts-train-service | [1.6873890735107298] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-train-service | ts-train-service | 15840 | 15185 | 3885.05 | 42854.2 | True | True | True | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-train-service | ts-train-service | 15840 | 15185 | 3885.05 | 42854.2 | True | True | True | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-train-service | ts-train-service | 0 | 0 | available |

## RE2-TT / dev-a505ab3f65

Root `ts-train-service`; status `OK`. Score entity BARO `[25035.619515801132]`; O=68, R=68; Hit@1=1, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-a505ab3f65-sNone-h0-2075b5/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-a505ab3f65.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-train-service_cpu / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 2.97678 | 0.456706 | 0 | available |
| ts-train-service_diskio / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 51164.8 | 15372 | 0 | available |
| ts-train-service_error / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 0 | 0 | 0 | available |
| ts-train-service_latency-50 / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 0.00709721 | 6.22014e-05 | 281 | available |
| ts-train-service_latency-90 / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 0.00952086 | 2.46771e-05 | 283 | available |
| ts-train-service_mem / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 2.64637e+08 | 63771.2 | 256 | available |
| ts-train-service_socket / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 13.0567 | 0.496779 | 284 | available |
| ts-train-service_workload / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 20.1406 | 2.18114 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-train-service_latency | ts-train-service | [25035.619515801132] |
| ts-train-service_mem | ts-train-service | [57.33333333341043] |
| ts-train-service_socket | ts-train-service | [14.0] |
| ts-train-service_cpu | ts-train-service | [2.615109673956151] |
| ts-train-service_diskio | ts-train-service | [1.5810744196933149] |
| ts-train-service_workload | ts-train-service | [0.73514705882353] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-train-service | ts-train-service | 15280 | 11329 | 4819 | 405502 | True | True | True | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-train-service | ts-train-service | 15280 | 11329 | 4819 | 405502 | True | True | True | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-train-service | ts-train-service | 5 | 0 | available |

## RE2-TT / dev-a5cabe5fa7

Root `ts-travel-service`; status `OK`. Score entity BARO `[17.28571428571457]`; O=68, R=68; Hit@1=0, Hit@5=0. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-a5cabe5fa7-sNone-h0-5a663b/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-a5cabe5fa7.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-travel-service_cpu / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 3.5096 | 0.615994 | 0 | available |
| ts-travel-service_diskio / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 53464.4 | 18172.8 | 0 | available |
| ts-travel-service_error / ts-travel-service | ts-travel-service | 0 | 0 | 300 / 300 | N/A | N/A | N/A | insufficient_N |
| ts-travel-service_latency-50 / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 0.0179499 | 0.000218627 | 288 | available |
| ts-travel-service_latency-90 / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 0.19481 | 0.0956599 | 250 | available |
| ts-travel-service_mem / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 2.81562e+08 | 43582.8 | 274 | available |
| ts-travel-service_socket / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 16.83 | 1.86219 | 72 | available |
| ts-travel-service_workload / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 10.032 | 2.86329 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-travel-service_mem | ts-travel-service | [17.28571428571457] |
| ts-travel-service_latency | ts-travel-service | [3.483120238615436] |
| ts-travel-service_socket | ts-travel-service | [2.6666666666666665] |
| ts-travel-service_cpu | ts-travel-service | [1.3772763380456459] |
| ts-travel-service_diskio | ts-travel-service | [1.3591171567392577] |
| ts-travel-service_workload | ts-travel-service | [0.9836605292037554] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-travel-service | ts-travel-service | 9839 | 8895 | 50647.6 | 266567 | True | True | True | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-travel-service | ts-travel-service | 9839 | 8895 | 50647.6 | 266567 | True | True | True | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-travel-service | ts-travel-service | 8487 | 0 | available |

## RE2-TT / dev-a915aa2424

Root `ts-travel-service`; status `OK`. Score entity BARO `[4.81283212032114]`; O=68, R=68; Hit@1=0, Hit@5=0. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-a915aa2424-sNone-h0-714b10/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-a915aa2424.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-travel-service_cpu / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 3.57415 | 1.74063 | 8 | available |
| ts-travel-service_diskio / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 50082.6 | 16214.1 | 0 | available |
| ts-travel-service_error / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 0.00665333 | 0.0284806 | 0 | available |
| ts-travel-service_latency-50 / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 0.0177307 | 0.000485761 | 300 | available |
| ts-travel-service_latency-90 / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 0.144424 | 0.0881831 | 266 | available |
| ts-travel-service_mem / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 2.93588e+08 | 57927.7 | 229 | available |
| ts-travel-service_socket / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 20.3167 | 2.30284 | 0 | available |
| ts-travel-service_workload / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 8.92241 | 3.11426 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-travel-service_cpu | ts-travel-service | [4.81283212032114] |
| ts-travel-service_latency | ts-travel-service | [4.790065721183073] |
| ts-travel-service_mem | ts-travel-service | [4.466666666666173] |
| ts-travel-service_workload | ts-travel-service | [2.7692307692307687] |
| ts-travel-service_socket | ts-travel-service | [2.5] |
| ts-travel-service_diskio | ts-travel-service | [1.604298309749789] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-travel-service | ts-travel-service | 8983 | 9819 | 53220.8 | 260925 | True | True | True | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-travel-service | ts-travel-service | 8983 | 9819 | 53220.8 | 260925 | True | True | True | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-travel-service | ts-travel-service | 9383 | 0 | available |

## RE2-TT / dev-b8bd0abf60

Root `ts-route-service`; status `OK`. Score entity BARO `[987.4527448772192]`; O=68, R=68; Hit@1=1, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-b8bd0abf60-sNone-h0-b7738b/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-b8bd0abf60.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-route-service_cpu / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 5.08519 | 0.462871 | 291 | available |
| ts-route-service_diskio / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 50030.5 | 14132.2 | 47 | available |
| ts-route-service_error / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 0 | 0 | 0 | available |
| ts-route-service_latency-50 / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 0.00502411 | 0.000230116 | 281 | available |
| ts-route-service_latency-90 / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 0.00915618 | 6.95092e-05 | 292 | available |
| ts-route-service_mem / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 2.63827e+08 | 110838 | 296 | available |
| ts-route-service_socket / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 16.05 | 0.668954 | 296 | available |
| ts-route-service_workload / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 32.7898 | 3.79824 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-route-service_latency | ts-route-service | [987.4527448772192] |
| ts-route-service_mem | ts-route-service | [168.99999999996817] |
| ts-route-service_cpu | ts-route-service | [86.96773980180171] |
| ts-route-service_socket | ts-route-service | [72.0] |
| ts-route-service_diskio | ts-route-service | [29.819129645757172] |
| ts-route-service_workload | ts-route-service | [1.2459790467758582] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-route-service | ts-route-service | 14829 | 14196 | 4235.6 | 95833.5 | True | True | True | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-route-service | ts-route-service | 14829 | 14196 | 4235.6 | 95833.5 | True | True | True | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-route-service | ts-route-service | 4743 | 0 | available |

## RE2-TT / dev-ba831dbeb8

Root `ts-train-service`; status `OK`. Score entity BARO `[464.46036799668826]`; O=68, R=68; Hit@1=1, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-ba831dbeb8-sNone-h0-3d9c16/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-ba831dbeb8.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-train-service_cpu / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 2.7456 | 0.22314 | 294 | available |
| ts-train-service_diskio / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 54638.7 | 17588.5 | 0 | available |
| ts-train-service_error / ts-train-service | ts-train-service | 0 | 159 | 300 / 141 | N/A | N/A | N/A | insufficient_N |
| ts-train-service_latency-50 / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 0.00360457 | 6.731e-05 | 279 | available |
| ts-train-service_latency-90 / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 0.00802526 | 0.000195597 | 286 | available |
| ts-train-service_mem / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 2.67103e+08 | 145637 | 297 | available |
| ts-train-service_socket / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 13.73 | 0.690724 | 151 | available |
| ts-train-service_workload / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 20.8771 | 2.26678 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-train-service_latency | ts-train-service | [464.46036799668826] |
| ts-train-service_cpu | ts-train-service | [147.4567007124181] |
| ts-train-service_mem | ts-train-service | [32.28124999999569] |
| ts-train-service_socket | ts-train-service | [4.0] |
| ts-train-service_workload | ts-train-service | [1.8700514823362342] |
| ts-train-service_diskio | ts-train-service | [0.8881466259192407] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-train-service | ts-train-service | 15725 | 15683 | 3708.6 | 50953.1 | True | True | True | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-train-service | ts-train-service | 15725 | 15683 | 3708.6 | 50953.1 | True | True | True | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-train-service | ts-train-service | 165 | 11 | available |

## RE2-TT / dev-bcbd4f46ae

Root `ts-route-service`; status `OK`. Score entity BARO `[101.4074074074104]`; O=68, R=68; Hit@1=1, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-bcbd4f46ae-sNone-h0-05442c/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-bcbd4f46ae.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-route-service_cpu / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 5.31213 | 0.998836 | 292 | available |
| ts-route-service_diskio / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 51704 | 16613.7 | 0 | available |
| ts-route-service_latency-50 / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 0.00333228 | 6.96146e-05 | 282 | available |
| ts-route-service_latency-90 / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 0.00657456 | 0.000748108 | 283 | available |
| ts-route-service_mem / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 2.66579e+08 | 80146.9 | 292 | available |
| ts-route-service_socket / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 13.44 | 0.774425 | 292 | available |
| ts-route-service_workload / ts-route-service | ts-route-service | 300 | 300 | 0 / 0 | 32.8464 | 2.45301 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-route-service_mem | ts-route-service | [101.4074074074104] |
| ts-route-service_latency | ts-route-service | [55.52816804124074] |
| ts-route-service_cpu | ts-route-service | [40.33990799338858] |
| ts-route-service_socket | ts-route-service | [16.0] |
| ts-route-service_workload | ts-route-service | [1.532077880625598] |
| ts-route-service_diskio | ts-route-service | [1.0360689407684396] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-route-service | ts-route-service | 14892 | 14715 | 3470.45 | 67143.1 | True | True | True | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-route-service | ts-route-service | 14892 | 14715 | 3470.45 | 67143.1 | True | True | True | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-route-service | ts-route-service | 4909 | 0 | available |

## RE2-TT / dev-db293894ab

Root `ts-travel-service`; status `OK`. Score entity BARO `[514304.58647720725]`; O=68, R=68; Hit@1=1, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-db293894ab-sNone-h0-56c980/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-db293894ab.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-travel-service_cpu / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 6.77882 | 2.78112 | 271 | available |
| ts-travel-service_diskio / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 52876.9 | 15980.4 | 287 | available |
| ts-travel-service_error / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 0 | 0 | 0 | available |
| ts-travel-service_latency-50 / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 0.0193904 | 0.000759322 | 259 | available |
| ts-travel-service_latency-90 / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 0.14994 | 0.0880841 | 56 | available |
| ts-travel-service_mem / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 2.7921e+08 | 951983 | 287 | available |
| ts-travel-service_socket / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 15.78 | 2.67923 | 0 | available |
| ts-travel-service_workload / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 8.55975 | 3.37814 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-travel-service_diskio | ts-travel-service | [514304.58647720725] |
| ts-travel-service_mem | ts-travel-service | [264.6460176991104] |
| ts-travel-service_cpu | ts-travel-service | [7.425108707237281] |
| ts-travel-service_latency | ts-travel-service | [2.6266201889990253] |
| ts-travel-service_socket | ts-travel-service | [2.0] |
| ts-travel-service_workload | ts-travel-service | [1.2236145428873988] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-travel-service | ts-travel-service | 8757 | 9245 | 56447 | 120461 | True | False | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-travel-service | ts-travel-service | 8757 | 9245 | 56447 | 120461 | True | False | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-travel-service | ts-travel-service | 8725 | 0 | available |

## RE2-TT / dev-de89e2f9e9

Root `ts-travel-service`; status `OK`. Score entity BARO `[596241.3974909716]`; O=68, R=68; Hit@1=1, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-de89e2f9e9-sNone-h0-bb8481/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-de89e2f9e9.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-travel-service_cpu / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 1.86276 | 0.981157 | 268 | available |
| ts-travel-service_diskio / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 52440.8 | 17624.9 | 297 | available |
| ts-travel-service_error / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 0 | 0 | 0 | available |
| ts-travel-service_latency-50 / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 0.0387316 | 0.00569096 | 180 | available |
| ts-travel-service_latency-90 / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 0.0872225 | 0.0022503 | 285 | available |
| ts-travel-service_mem / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 2.66171e+08 | 354022 | 297 | available |
| ts-travel-service_socket / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 12.84 | 1.23602 | 86 | available |
| ts-travel-service_workload / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 1.74773 | 0.289498 | 15 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-travel-service_diskio | ts-travel-service | [596241.3974909716] |
| ts-travel-service_mem | ts-travel-service | [516.213114754052] |
| ts-travel-service_cpu | ts-travel-service | [77.04608503418098] |
| ts-travel-service_latency | ts-travel-service | [61.93040739587951] |
| ts-travel-service_socket | ts-travel-service | [3.0] |
| ts-travel-service_workload | ts-travel-service | [2.308136180034621] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-travel-service | ts-travel-service | 1866 | 2102 | 55806.5 | 84004.6 | False | False | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-travel-service | ts-travel-service | 1866 | 2102 | 55806.5 | 84004.6 | False | False | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-travel-service | ts-travel-service | 2690 | 0 | available |

## RE2-TT / dev-f36d0647d5

Root `ts-order-service`; status `OK`. Score entity BARO `[77.07496570138956]`; O=68, R=68; Hit@1=0, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-f36d0647d5-sNone-h0-d73bb4/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-f36d0647d5.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-order-service_cpu / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 3.38383 | 0.760373 | 0 | available |
| ts-order-service_diskio / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 50765.3 | 16828 | 48 | available |
| ts-order-service_error / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 0 | 0 | 0 | available |
| ts-order-service_latency-50 / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 0.00981914 | 0.00161036 | 45 | available |
| ts-order-service_latency-90 / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 0.0347783 | 0.00519394 | 282 | available |
| ts-order-service_mem / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 2.91489e+08 | 299008 | 289 | available |
| ts-order-service_socket / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 14.1167 | 1.44328 | 0 | available |
| ts-order-service_workload / ts-order-service | ts-order-service | 300 | 300 | 0 / 0 | 6.14512 | 2.27527 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-order-service_diskio | ts-order-service | [77.07496570138956] |
| ts-order-service_latency | ts-order-service | [57.92585887842953] |
| ts-order-service_mem | ts-order-service | [4.257575757576029] |
| ts-order-service_socket | ts-order-service | [1.5] |
| ts-order-service_cpu | ts-order-service | [1.4613266135331073] |
| ts-order-service_workload | ts-order-service | [1.4334536702767748] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-order-service | ts-order-service | 3223 | 3324 | 25495.6 | 228391 | True | True | True | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-order-service | ts-order-service | 3223 | 3324 | 25495.6 | 228391 | True | True | True | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-order-service | ts-order-service | 1811 | 0 | available |

## RE2-TT / dev-f81f88234e

Root `ts-auth-service`; status `OK`. Score entity BARO `[4.887212977968917]`; O=68, R=68; Hit@1=0, Hit@5=0. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-f81f88234e-sNone-h0-ed16f9/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-f81f88234e.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-auth-service_cpu / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 14.6095 | 2.29248 | 0 | available |
| ts-auth-service_diskio / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 50109.9 | 15565.8 | 0 | available |
| ts-auth-service_latency-50 / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 0.248105 | 0.0269923 | 293 | available |
| ts-auth-service_latency-90 / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 0.755262 | 0.178162 | 158 | available |
| ts-auth-service_mem / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 2.46142e+08 | 707056 | 245 | available |
| ts-auth-service_socket / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 13.7433 | 1.39193 | 0 | available |
| ts-auth-service_workload / ts-auth-service | ts-auth-service | 300 | 300 | 0 / 0 | 2.8458 | 0.203978 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-auth-service_latency | ts-auth-service | [4.887212977968917] |
| ts-auth-service_mem | ts-auth-service | [3.2392026578072692] |
| ts-auth-service_workload | ts-auth-service | [2.3350000000000035] |
| ts-auth-service_diskio | ts-auth-service | [1.8289536832737294] |
| ts-auth-service_cpu | ts-auth-service | [0.6869149431945288] |
| ts-auth-service_socket | ts-auth-service | [0.3333333333333333] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-auth-service | ts-auth-service | 2120 | 2055 | 416612 | 782776 | False | False | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-auth-service | ts-auth-service | 2120 | 2055 | 416612 | 782776 | False | False | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-auth-service | ts-auth-service | 1642 | 0 | available |

## RE2-TT / dev-f9a8e05ed7

Root `ts-travel-service`; status `OK`. Score entity BARO `[640830.4840839492]`; O=68, R=68; Hit@1=1, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-f9a8e05ed7-sNone-h0-43732b/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-f9a8e05ed7.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-travel-service_cpu / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 3.0397 | 2.11559 | 274 | available |
| ts-travel-service_diskio / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 50289.1 | 16300.6 | 274 | available |
| ts-travel-service_error / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 0 | 0 | 0 | available |
| ts-travel-service_latency-50 / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 0.0433378 | 0.00511066 | 101 | available |
| ts-travel-service_latency-90 / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 0.0925099 | 0.00316526 | 268 | available |
| ts-travel-service_mem / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 2.66148e+08 | 1.22039e+06 | 274 | available |
| ts-travel-service_socket / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 13.5733 | 0.897007 | 106 | available |
| ts-travel-service_workload / ts-travel-service | ts-travel-service | 300 | 300 | 0 / 0 | 1.6153 | 0.320384 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-travel-service_diskio | ts-travel-service | [640830.4840839492] |
| ts-travel-service_mem | ts-travel-service | [123.11957052220794] |
| ts-travel-service_latency | ts-travel-service | [61.23586309244042] |
| ts-travel-service_cpu | ts-travel-service | [19.50115520979479] |
| ts-travel-service_socket | ts-travel-service | [5.0] |
| ts-travel-service_workload | ts-travel-service | [1.1235955056179776] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-travel-service | ts-travel-service | 1787 | 1727 | 60102.3 | 90791.1 | False | False | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-travel-service | ts-travel-service | 1787 | 1727 | 60102.3 | 90791.1 | False | False | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-travel-service | ts-travel-service | 2117 | 0 | available |

## RE2-TT / dev-fbc45b0c67

Root `ts-train-service`; status `OK`. Score entity BARO `[18498.855870791547]`; O=68, R=68; Hit@1=1, Hit@5=1. Nguồn: `results/T-024/runs/baro-30-001/luot/baro-a-dev-fbc45b0c67-sNone-h0-c1d73b/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-fbc45b0c67.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ts-train-service_cpu / ts-train-service | ts-train-service | 300 | 298 | 0 / 2 | 3.24399 | 0.326594 | 0 | available |
| ts-train-service_diskio / ts-train-service | ts-train-service | 300 | 298 | 0 / 2 | 50837.5 | 17117.3 | 0 | available |
| ts-train-service_latency-50 / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 0.00556999 | 0.000223537 | 272 | available |
| ts-train-service_latency-90 / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 0.00929249 | 3.77383e-05 | 287 | available |
| ts-train-service_mem / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 2.61693e+08 | 89607.3 | 0 | available |
| ts-train-service_socket / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 18.3967 | 0.582514 | 279 | available |
| ts-train-service_workload / ts-train-service | ts-train-service | 300 | 300 | 0 / 0 | 21.3459 | 2.27264 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| ts-train-service_latency | ts-train-service | [18498.855870791547] |
| ts-train-service_socket | ts-train-service | [9.0] |
| ts-train-service_mem | ts-train-service | [1.9249999999999219] |
| ts-train-service_diskio | ts-train-service | [1.4542842736021206] |
| ts-train-service_cpu | ts-train-service | [-0.32853771789455727] |
| ts-train-service_workload | ts-train-service | [-0.37229588276343345] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | ts-train-service | ts-train-service | 15855 | 11172 | 4255 | 404959 | True | True | True | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | ts-train-service | ts-train-service | 15855 | 11172 | 4255 | 404959 | True | True | True | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| ts-train-service | ts-train-service | 0 | 0 | available |

## Nezha-OB / dev-14701a3bbb

Root `shippingservice`; status `OK`. Score entity BARO `[341.725758793045]`; O=10, R=10; Hit@1=1, Hit@5=1. Nguồn: `results/T-026/runs/full-001/baro-main-dev-14701a3bbb-h0-full/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-14701a3bbb.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| shippingservice_CpuUsage-m / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 0.586543 | 0.0698617 | 5 | available |
| shippingservice_CpuUsageRate-pct / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 2.9327 | 0.349345 | 5 | available |
| shippingservice_MemoryUsage-Mi / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 41.9492 | 0 | 1 | available |
| shippingservice_MemoryUsageRate-pct / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 32.7728 | 0 | 1 | available |
| shippingservice_NetworkReceiveBytes / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 1964.58 | 332.644 | 0 | available |
| shippingservice_NetworkTransmitBytes / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 19032 | 8469.97 | 0 | available |
| shippingservice_PodClientLatencyP90-s / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 0.05305 | 0.0762047 | 0 | available |
| shippingservice_PodClientLatencyP95-s / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 0.058525 | 0.084722 | 0 | available |
| shippingservice_PodClientLatencyP99-s / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 0.062905 | 0.0915375 | 0 | available |
| shippingservice_PodServerLatencyP90-s / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 0.0046 | 3.87896e-19 | 5 | available |
| shippingservice_PodServerLatencyP95-s / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 0.0048 | 7.75792e-19 | 5 | available |
| shippingservice_PodServerLatencyP99-s / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 0.00496 | 1.02628e-18 | 5 | available |
| shippingservice_PodSuccessRate-pct / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 0 | 0 | 0 | available |
| shippingservice_PodWorkload-Ops / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 2.58667 | 0.232475 | 0 | available |
| shippingservice_SyscallRead / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 736.8 | 60.6445 | 0 | available |
| shippingservice_SyscallWrite / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 1549.2 | 120.317 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| shippingservice_CpuUsageRate-pct | shippingservice | [341.725758793045] |
| shippingservice_CpuUsage-m | shippingservice | [304.2385389954114] |
| shippingservice_PodClientLatencyP99-s | shippingservice | [14.804020100502514] |
| shippingservice_PodClientLatencyP95-s | shippingservice | [14.000000000000004] |
| shippingservice_PodClientLatencyP90-s | shippingservice | [12.947368421052632] |
| shippingservice_SyscallWrite | shippingservice | [2.1136363636363638] |
| shippingservice_NetworkReceiveBytes | shippingservice | [1.962354479366818] |
| shippingservice_NetworkTransmitBytes | shippingservice | [1.9433113581775712] |
| shippingservice_SyscallRead | shippingservice | [1.0666666666666667] |
| shippingservice_PodServerLatencyP99-s | shippingservice | [0.9233733333333334] |
| shippingservice_PodServerLatencyP95-s | shippingservice | [0.6368666666666657] |
| shippingservice_PodServerLatencyP90-s | shippingservice | [0.38706666666666645] |
| shippingservice_PodWorkload-Ops | shippingservice | [0.25000000000000083] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | shippingservice | shippingservice | 708 | 704 | 526.65 | 99989.2 | True | True | True | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | shippingservice | shippingservice | 708 | 704 | 526.65 | 99989.2 | True | True | True | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| shippingservice | shippingservice | 1408 | 0 | available |

## Nezha-OB / dev-1ac905bc95

Root `frontend`; status `OK`. Score entity BARO `[1.1889938916035074]`; O=10, R=10; Hit@1=0, Hit@5=0. Nguồn: `results/T-026/runs/full-001/baro-main-dev-1ac905bc95-h0-full/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-1ac905bc95.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| frontend_CpuUsage-m / frontend | frontend | 5 | 5 | 0 / 0 | 9.97499 | 6.90703 | 0 | available |
| frontend_CpuUsageRate-pct / frontend | frontend | 5 | 5 | 0 / 0 | 47.8746 | 31.5821 | 0 | available |
| frontend_FrontLatencyP50-s / frontend | frontend | 5 | 5 | 0 / 0 | 1.71179 | 2.35542 | 0 | available |
| frontend_FrontLatencyP90-s / frontend | frontend | 5 | 5 | 0 / 0 | 3.12658 | 3.5553 | 0 | available |
| frontend_FrontLatencyP95-s / frontend | frontend | 5 | 5 | 0 / 0 | 5.36175 | 6.07474 | 0 | available |
| frontend_FrontLatencyP99-s / frontend | frontend | 5 | 5 | 0 / 0 | 10.3777 | 11.6566 | 0 | available |
| frontend_FrontSuccessRate-pct / frontend | frontend | 5 | 5 | 0 / 0 | 100 | 0 | 0 | available |
| frontend_MemoryUsage-Mi / frontend | frontend | 5 | 5 | 0 / 0 | 35.1289 | 24.1936 | 0 | available |
| frontend_MemoryUsageRate-pct / frontend | frontend | 5 | 5 | 0 / 0 | 27.4445 | 18.9012 | 0 | available |
| frontend_NetworkReceiveBytes / frontend | frontend | 5 | 5 | 0 / 0 | 25257.6 | 10568.6 | 0 | available |
| frontend_NetworkTransmitBytes / frontend | frontend | 5 | 5 | 0 / 0 | 262770 | 41811.7 | 0 | available |
| frontend_PodClientLatencyP90-s / frontend | frontend | 5 | 5 | 0 / 0 | 0.0660557 | 0.037296 | 0 | available |
| frontend_PodClientLatencyP95-s / frontend | frontend | 5 | 5 | 0 / 0 | 0.133111 | 0.0591158 | 0 | available |
| frontend_PodClientLatencyP99-s / frontend | frontend | 5 | 5 | 0 / 0 | 0.344364 | 0.142846 | 0 | available |
| frontend_PodServerLatencyP90-s / frontend | frontend | 5 | 5 | 0 / 0 | 3.12658 | 3.5553 | 0 | available |
| frontend_PodServerLatencyP95-s / frontend | frontend | 5 | 5 | 0 / 0 | 5.36175 | 6.07474 | 0 | available |
| frontend_PodServerLatencyP99-s / frontend | frontend | 5 | 5 | 0 / 0 | 10.3777 | 11.6566 | 0 | available |
| frontend_PodSuccessRate-pct / frontend | frontend | 5 | 5 | 0 / 0 | 0 | 0 | 0 | available |
| frontend_PodWorkload-Ops / frontend | frontend | 5 | 5 | 0 / 0 | 6.69333 | 2.71051 | 0 | available |
| frontend_SyscallRead / frontend | frontend | 5 | 5 | 0 / 0 | 12262.8 | 9159.69 | 0 | available |
| frontend_SyscallWrite / frontend | frontend | 5 | 5 | 0 / 0 | 8977.2 | 6154.78 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| frontend_NetworkTransmitBytes | frontend | [1.1889938916035074] |
| frontend_PodClientLatencyP90-s | frontend | [0.7044353658369834] |
| frontend_SyscallRead | frontend | [0.4042979037185294] |
| frontend_SyscallWrite | frontend | [0.36823844819429113] |
| frontend_PodWorkload-Ops | frontend | [0.29032258064516103] |
| frontend_NetworkReceiveBytes | frontend | [0.10748972390809151] |
| frontend_MemoryUsage-Mi | frontend | [0.09375] |
| frontend_MemoryUsageRate-pct | frontend | [0.09375] |
| frontend_FrontLatencyP99-s | frontend | [0.04873180553419358] |
| frontend_PodServerLatencyP99-s | frontend | [0.04873180553419358] |
| frontend_FrontLatencyP50-s | frontend | [0.012578358480938828] |
| frontend_FrontLatencyP90-s | frontend | [0.008041046896155715] |
| frontend_PodServerLatencyP90-s | frontend | [0.008041046896155715] |
| frontend_FrontLatencyP95-s | frontend | [0.007981590185646958] |
| frontend_PodServerLatencyP95-s | frontend | [0.007981590185646958] |
| frontend_CpuUsageRate-pct | frontend | [-0.11594253948607888] |
| frontend_CpuUsage-m | frontend | [-0.11595260737364715] |
| frontend_PodClientLatencyP99-s | frontend | [-0.3088911559287232] |
| frontend_PodClientLatencyP95-s | frontend | [-0.4055464563563672] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | frontend | frontend | 4736 | 6661 | 183840 | 119703 | False | False | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | frontend | frontend | 4734 | 6663 | 183772 | 120286 | False | False | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| frontend | frontend | 5256 | 1040 | available |

## Nezha-OB / dev-27252dca60

Root `productcatalogservice`; status `OK`. Score entity BARO `[3.2251980228734562]`; O=10, R=10; Hit@1=0, Hit@5=0. Nguồn: `results/T-026/runs/full-001/baro-main-dev-27252dca60-h0-full/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-27252dca60.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productcatalogservice_CpuUsage-m / productcatalogservice | productcatalogservice | 5 | 5 | 0 / 0 | 8.2995 | 1.69686 | 0 | available |
| productcatalogservice_CpuUsageRate-pct / productcatalogservice | productcatalogservice | 5 | 5 | 0 / 0 | 47.4963 | 20.2098 | 0 | available |
| productcatalogservice_MemoryUsage-Mi / productcatalogservice | productcatalogservice | 5 | 5 | 0 / 0 | 14.4375 | 0 | 4 | available |
| productcatalogservice_MemoryUsageRate-pct / productcatalogservice | productcatalogservice | 5 | 5 | 0 / 0 | 11.2793 | 0 | 4 | available |
| productcatalogservice_NetworkReceiveBytes / productcatalogservice | productcatalogservice | 5 | 5 | 0 / 0 | 165772 | 16974.5 | 0 | available |
| productcatalogservice_NetworkTransmitBytes / productcatalogservice | productcatalogservice | 5 | 5 | 0 / 0 | 314344 | 28104.1 | 0 | available |
| productcatalogservice_PodClientLatencyP90-s / productcatalogservice | productcatalogservice | 5 | 5 | 0 / 0 | 0.37 | 0.210927 | 0 | available |
| productcatalogservice_PodClientLatencyP95-s / productcatalogservice | productcatalogservice | 5 | 5 | 0 / 0 | 0.41 | 0.250744 | 0 | available |
| productcatalogservice_PodClientLatencyP99-s / productcatalogservice | productcatalogservice | 5 | 5 | 0 / 0 | 0.442 | 0.283328 | 0 | available |
| productcatalogservice_PodServerLatencyP90-s / productcatalogservice | productcatalogservice | 5 | 5 | 0 / 0 | 0.00802885 | 0.00477272 | 0 | available |
| productcatalogservice_PodServerLatencyP95-s / productcatalogservice | productcatalogservice | 5 | 5 | 0 / 0 | 0.0214626 | 0.0141476 | 0 | available |
| productcatalogservice_PodServerLatencyP99-s / productcatalogservice | productcatalogservice | 5 | 5 | 0 / 0 | 0.056523 | 0.018018 | 0 | available |
| productcatalogservice_PodSuccessRate-pct / productcatalogservice | productcatalogservice | 5 | 5 | 0 / 0 | 0 | 0 | 0 | available |
| productcatalogservice_PodWorkload-Ops / productcatalogservice | productcatalogservice | 5 | 5 | 0 / 0 | 47.9633 | 1.26294 | 1 | available |
| productcatalogservice_SyscallRead / productcatalogservice | productcatalogservice | 5 | 5 | 0 / 0 | 45577.2 | 5592.76 | 0 | available |
| productcatalogservice_SyscallWrite / productcatalogservice | productcatalogservice | 5 | 5 | 0 / 0 | 33453.2 | 3358.7 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| productcatalogservice_PodWorkload-Ops | productcatalogservice | [3.2251980228734562] |
| productcatalogservice_CpuUsageRate-pct | productcatalogservice | [2.388148927842089] |
| productcatalogservice_CpuUsage-m | productcatalogservice | [2.3875786178762683] |
| productcatalogservice_PodServerLatencyP99-s | productcatalogservice | [1.0738925199709257] |
| productcatalogservice_PodClientLatencyP99-s | productcatalogservice | [0.9858585858585857] |
| productcatalogservice_PodClientLatencyP95-s | productcatalogservice | [0.9263157894736848] |
| productcatalogservice_PodClientLatencyP90-s | productcatalogservice | [0.8444444444444447] |
| productcatalogservice_NetworkTransmitBytes | productcatalogservice | [0.7743856207110382] |
| productcatalogservice_NetworkReceiveBytes | productcatalogservice | [0.3931103246491301] |
| productcatalogservice_PodServerLatencyP95-s | productcatalogservice | [0.2900400333163142] |
| productcatalogservice_PodServerLatencyP90-s | productcatalogservice | [0.0012763788842711213] |
| productcatalogservice_SyscallRead | productcatalogservice | [-0.14067278287461796] |
| productcatalogservice_SyscallWrite | productcatalogservice | [-0.17188540972685118] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | productcatalogservice | productcatalogservice | 9705 | 3795 | 3217 | 3309 | False | False | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | productcatalogservice | productcatalogservice | 9705 | 3795 | 3217 | 3309 | False | False | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| productcatalogservice | productcatalogservice | 5346 | 768 | available |

## Nezha-OB / dev-2bfc97b01e

Root `checkoutservice`; status `OK`. Score entity BARO `[94.00000000000095]`; O=10, R=10; Hit@1=0, Hit@5=1. Nguồn: `results/T-026/runs/pilot-001/baro-main-dev-2bfc97b01e-h0-lower_median/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-2bfc97b01e.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| checkoutservice_CpuUsage-m / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.891369 | 0.23512 | 2 | available |
| checkoutservice_CpuUsageRate-pct / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 4.45668 | 1.1755 | 2 | available |
| checkoutservice_MemoryUsage-Mi / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 54.75 | 0 | 5 | available |
| checkoutservice_MemoryUsageRate-pct / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 42.7734 | 0 | 5 | available |
| checkoutservice_NetworkReceiveBytes / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 5327.96 | 484.975 | 2 | available |
| checkoutservice_NetworkTransmitBytes / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 142152 | 30961.9 | 0 | available |
| checkoutservice_PodClientLatencyP90-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.0464085 | 0.0310283 | 0 | available |
| checkoutservice_PodClientLatencyP95-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.064256 | 0.0457047 | 0 | available |
| checkoutservice_PodClientLatencyP99-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.114715 | 0.0909369 | 0 | available |
| checkoutservice_PodServerLatencyP90-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.438 | 0.162407 | 0 | available |
| checkoutservice_PodServerLatencyP95-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.494 | 0.202223 | 0 | available |
| checkoutservice_PodServerLatencyP99-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.5388 | 0.236245 | 0 | available |
| checkoutservice_PodSuccessRate-pct / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0 | 0 | 0 | available |
| checkoutservice_PodWorkload-Ops / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.213333 | 0.106667 | 0 | available |
| checkoutservice_SyscallRead / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 2361.6 | 687.912 | 0 | available |
| checkoutservice_SyscallWrite / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 2043.6 | 594.176 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| checkoutservice_PodServerLatencyP99-s | checkoutservice | [94.00000000000095] |
| checkoutservice_NetworkReceiveBytes | checkoutservice | [45.99103647574196] |
| checkoutservice_PodServerLatencyP95-s | checkoutservice | [13.999999999999975] |
| checkoutservice_CpuUsageRate-pct | checkoutservice | [6.523424915362571] |
| checkoutservice_CpuUsage-m | checkoutservice | [6.5222260605735025] |
| checkoutservice_PodServerLatencyP90-s | checkoutservice | [4.000000000000005] |
| checkoutservice_PodWorkload-Ops | checkoutservice | [2.0000000000000004] |
| checkoutservice_NetworkTransmitBytes | checkoutservice | [1.6982041368201726] |
| checkoutservice_SyscallWrite | checkoutservice | [0.8361904761904762] |
| checkoutservice_SyscallRead | checkoutservice | [0.7290322580645161] |
| checkoutservice_PodClientLatencyP99-s | checkoutservice | [0.6596226415094331] |
| checkoutservice_PodClientLatencyP95-s | checkoutservice | [0.6314666666666634] |
| checkoutservice_PodClientLatencyP90-s | checkoutservice | [0.07774936061381041] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | checkoutservice | checkoutservice | 420 | 608 | 154342 | 169124 | False | False | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | checkoutservice | checkoutservice | 420 | 608 | 154342 | 169124 | False | False | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| checkoutservice | checkoutservice | 794 | 0 | available |

## Nezha-OB / dev-396c8dbf7d

Root `emailservice`; status `OK`. Score entity BARO `[688.4850650019675]`; O=10, R=10; Hit@1=1, Hit@5=1. Nguồn: `results/T-026/runs/full-001/baro-main-dev-396c8dbf7d-h0-full/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-396c8dbf7d.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| emailservice_CpuUsage-m / emailservice | emailservice | 5 | 5 | 0 / 0 | 0.116053 | 0.0132434 | 4 | available |
| emailservice_CpuUsageRate-pct / emailservice | emailservice | 5 | 5 | 0 / 0 | 0.580263 | 0.066217 | 4 | available |
| emailservice_MemoryUsage-Mi / emailservice | emailservice | 5 | 5 | 0 / 0 | 24.7422 | 0 | 5 | available |
| emailservice_MemoryUsageRate-pct / emailservice | emailservice | 5 | 5 | 0 / 0 | 4.83246 | 0 | 5 | available |
| emailservice_NetworkReceiveBytes / emailservice | emailservice | 5 | 5 | 0 / 0 | 883.495 | 133.223 | 0 | available |
| emailservice_NetworkTransmitBytes / emailservice | emailservice | 5 | 5 | 0 / 0 | 13847.8 | 2326.4 | 0 | available |
| emailservice_PodClientLatencyP90-s / emailservice | emailservice | 5 | 5 | 0 / 0 | 0.00456 | 8e-05 | 1 | available |
| emailservice_PodClientLatencyP95-s / emailservice | emailservice | 5 | 5 | 0 / 0 | 0.00478 | 4e-05 | 1 | available |
| emailservice_PodClientLatencyP99-s / emailservice | emailservice | 5 | 5 | 0 / 0 | 0.004956 | 8e-06 | 1 | available |
| emailservice_PodServerLatencyP90-s / emailservice | emailservice | 5 | 5 | 0 / 0 | 0.0046 | 0 | 3 | available |
| emailservice_PodServerLatencyP95-s / emailservice | emailservice | 5 | 5 | 0 / 0 | 0.0048 | 3.87896e-19 | 3 | available |
| emailservice_PodServerLatencyP99-s / emailservice | emailservice | 5 | 5 | 0 / 0 | 0.00496 | 1.02628e-18 | 3 | available |
| emailservice_PodSuccessRate-pct / emailservice | emailservice | 5 | 5 | 0 / 0 | 0 | 0 | 0 | available |
| emailservice_PodWorkload-Ops / emailservice | emailservice | 5 | 5 | 0 / 0 | 0.346667 | 0.0979796 | 0 | available |
| emailservice_SyscallRead / emailservice | emailservice | 5 | 5 | 0 / 0 | 39.2 | 10.7033 | 0 | available |
| emailservice_SyscallWrite / emailservice | emailservice | 5 | 5 | 0 / 0 | 80 | 21.8358 | 1 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| emailservice_CpuUsageRate-pct | emailservice | [688.4850650019675] |
| emailservice_CpuUsage-m | emailservice | [274.9170798047618] |
| emailservice_SyscallWrite | emailservice | [3.25] |
| emailservice_PodServerLatencyP99-s | emailservice | [2.45004] |
| emailservice_PodServerLatencyP95-s | emailservice | [2.2702] |
| emailservice_SyscallRead | emailservice | [1.1666666666666667] |
| emailservice_PodWorkload-Ops | emailservice | [0.9999999999999996] |
| emailservice_NetworkTransmitBytes | emailservice | [0.8049245597716914] |
| emailservice_NetworkReceiveBytes | emailservice | [0.6919764138382084] |
| emailservice_PodClientLatencyP99-s | emailservice | [0.004989999999999999] |
| emailservice_PodClientLatencyP95-s | emailservice | [0.004950000000000001] |
| emailservice_PodClientLatencyP90-s | emailservice | [0.0049] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | emailservice | emailservice | 22 | 38 | 661.65 | 999681 | True | True | True | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | emailservice | emailservice | 22 | 38 | 661.65 | 999681 | True | True | True | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| emailservice | emailservice | 76 | 0 | available |

## Nezha-OB / dev-3b92690644

Root `checkoutservice`; status `OK`. Score entity BARO `[40.00000000000073]`; O=10, R=10; Hit@1=0, Hit@5=1. Nguồn: `results/T-026/runs/full-001/baro-main-dev-3b92690644-h0-full/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-3b92690644.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| checkoutservice_CpuUsage-m / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 1.08346 | 0.376993 | 0 | available |
| checkoutservice_CpuUsageRate-pct / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 5.41707 | 1.88492 | 0 | available |
| checkoutservice_MemoryUsage-Mi / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 20.0031 | 0.131459 | 5 | available |
| checkoutservice_MemoryUsageRate-pct / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 15.6274 | 0.102702 | 5 | available |
| checkoutservice_NetworkReceiveBytes / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 5405.45 | 954.402 | 0 | available |
| checkoutservice_NetworkTransmitBytes / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 139466 | 28303.6 | 0 | available |
| checkoutservice_PodClientLatencyP90-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.0407357 | 0.0271144 | 0 | available |
| checkoutservice_PodClientLatencyP95-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.0591206 | 0.0353631 | 0 | available |
| checkoutservice_PodClientLatencyP99-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.1633 | 0.0788279 | 1 | available |
| checkoutservice_PodServerLatencyP90-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.532 | 0.228355 | 2 | available |
| checkoutservice_PodServerLatencyP95-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.591 | 0.264124 | 2 | available |
| checkoutservice_PodServerLatencyP99-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.6382 | 0.292818 | 2 | available |
| checkoutservice_PodSuccessRate-pct / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0 | 0 | 0 | available |
| checkoutservice_PodWorkload-Ops / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.333333 | 0.163299 | 0 | available |
| checkoutservice_SyscallRead / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 2700.8 | 665.111 | 0 | available |
| checkoutservice_SyscallWrite / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 2341.2 | 569.027 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| checkoutservice_PodClientLatencyP99-s | checkoutservice | [40.00000000000073] |
| checkoutservice_MemoryUsage-Mi | checkoutservice | [12.848484848484848] |
| checkoutservice_MemoryUsageRate-pct | checkoutservice | [12.848484848484848] |
| checkoutservice_PodServerLatencyP99-s | checkoutservice | [3.9438775510204067] |
| checkoutservice_PodServerLatencyP95-s | checkoutservice | [3.6944444444444455] |
| checkoutservice_PodServerLatencyP90-s | checkoutservice | [3.3124999999999996] |
| checkoutservice_NetworkReceiveBytes | checkoutservice | [1.4036305073029585] |
| checkoutservice_CpuUsage-m | checkoutservice | [1.0239729785312552] |
| checkoutservice_CpuUsageRate-pct | checkoutservice | [1.0238187604595808] |
| checkoutservice_PodClientLatencyP95-s | checkoutservice | [0.7757766509296464] |
| checkoutservice_PodWorkload-Ops | checkoutservice | [0.6666666666666667] |
| checkoutservice_PodClientLatencyP90-s | checkoutservice | [0.6343314880053685] |
| checkoutservice_SyscallRead | checkoutservice | [0.26004228329809725] |
| checkoutservice_SyscallWrite | checkoutservice | [0.08977556109725686] |
| checkoutservice_NetworkTransmitBytes | checkoutservice | [0.08128814489810562] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | checkoutservice | checkoutservice | 326 | 600 | 222793 | 341393 | False | False | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | checkoutservice | checkoutservice | 326 | 600 | 222793 | 341393 | False | False | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| checkoutservice | checkoutservice | 734 | 32 | available |

## Nezha-OB / dev-3e27669440

Root `adservice`; status `OK`. Score entity BARO `[3477.777777777778]`; O=10, R=10; Hit@1=1, Hit@5=1. Nguồn: `results/T-026/runs/full-001/baro-main-dev-3e27669440-h0-full/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-3e27669440.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| adservice_CpuUsage-m / adservice | adservice | 5 | 5 | 0 / 0 | 1.49059 | 0.275687 | 5 | available |
| adservice_CpuUsageRate-pct / adservice | adservice | 5 | 5 | 0 / 0 | 4.96864 | 0.918957 | 5 | available |
| adservice_MemoryUsage-Mi / adservice | adservice | 5 | 5 | 0 / 0 | 210.621 | 0.0699644 | 5 | available |
| adservice_MemoryUsageRate-pct / adservice | adservice | 5 | 5 | 0 / 0 | 90.207 | 0.0233215 | 5 | available |
| adservice_NetworkReceiveBytes / adservice | adservice | 5 | 5 | 0 / 0 | 32064.1 | 1803.8 | 0 | available |
| adservice_NetworkTransmitBytes / adservice | adservice | 5 | 5 | 0 / 0 | 72680.3 | 12659.9 | 0 | available |
| adservice_PodClientLatencyP90-s / adservice | adservice | 5 | 4 | 0 / 1 | 0.06175 | 0.0222149 | 0 | available |
| adservice_PodClientLatencyP95-s / adservice | adservice | 5 | 4 | 0 / 1 | 0.065875 | 0.0233104 | 0 | available |
| adservice_PodClientLatencyP99-s / adservice | adservice | 5 | 4 | 0 / 1 | 0.069175 | 0.0242515 | 0 | available |
| adservice_PodServerLatencyP90-s / adservice | adservice | 5 | 5 | 0 / 0 | 0.0311589 | 0.00690629 | 3 | available |
| adservice_PodServerLatencyP95-s / adservice | adservice | 5 | 5 | 0 / 0 | 0.0438368 | 0.00987141 | 3 | available |
| adservice_PodServerLatencyP99-s / adservice | adservice | 5 | 5 | 0 / 0 | 0.100715 | 0.0432885 | 3 | available |
| adservice_PodSuccessRate-pct / adservice | adservice | 5 | 5 | 0 / 0 | 0 | 0 | 0 | available |
| adservice_PodWorkload-Ops / adservice | adservice | 5 | 5 | 0 / 0 | 5.13333 | 0.219089 | 1 | available |
| adservice_SyscallRead / adservice | adservice | 5 | 5 | 0 / 0 | 1061.2 | 39.5899 | 2 | available |
| adservice_SyscallWrite / adservice | adservice | 5 | 5 | 0 / 0 | 2476 | 99.374 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| adservice_MemoryUsage-Mi | adservice | [3477.777777777778] |
| adservice_MemoryUsageRate-pct | adservice | [3477.7777762133333] |
| adservice_PodServerLatencyP95-s | adservice | [561.8606170651406] |
| adservice_PodServerLatencyP90-s | adservice | [396.6273963460041] |
| adservice_SyscallRead | adservice | [249.6] |
| adservice_CpuUsageRate-pct | adservice | [66.17218953810816] |
| adservice_CpuUsage-m | adservice | [63.812163131917565] |
| adservice_PodWorkload-Ops | adservice | [41.999999999999964] |
| adservice_PodServerLatencyP99-s | adservice | [26.06376913884193] |
| adservice_PodClientLatencyP90-s | adservice | [1.0294117647058822] |
| adservice_PodClientLatencyP95-s | adservice | [1.0135135135135136] |
| adservice_PodClientLatencyP99-s | adservice | [1.00253807106599] |
| adservice_NetworkTransmitBytes | adservice | [-0.2723437786622355] |
| adservice_NetworkReceiveBytes | adservice | [-0.3444780373073926] |
| adservice_SyscallWrite | adservice | [-2.513888888888889] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | adservice | adservice | 1440 | 2148 | 36233.1 | 2.49578e+06 | True | True | True | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | adservice | adservice | 1440 | 2148 | 36233.1 | 2.49578e+06 | True | True | True | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| adservice | adservice | 2251 | 0 | available |

## Nezha-OB / dev-515c5f2190

Root `recommendationservice`; status `OK`. Score entity BARO `[982.4790850365321]`; O=10, R=10; Hit@1=1, Hit@5=1. Nguồn: `results/T-026/runs/full-001/baro-main-dev-515c5f2190-h0-full/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-515c5f2190.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| recommendationservice_CpuUsage-m / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 3.75771 | 2.89456 | 2 | available |
| recommendationservice_CpuUsageRate-pct / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 28.7876 | 30.6388 | 0 | available |
| recommendationservice_MemoryUsage-Mi / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 42.9797 | 35.4516 | 0 | available |
| recommendationservice_MemoryUsageRate-pct / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 9.55104 | 7.87812 | 0 | available |
| recommendationservice_NetworkReceiveBytes / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 11634.2 | 3937.33 | 0 | available |
| recommendationservice_NetworkTransmitBytes / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 22903 | 12108 | 0 | available |
| recommendationservice_PodClientLatencyP90-s / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 0.0107958 | 0.00491711 | 0 | available |
| recommendationservice_PodClientLatencyP95-s / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 0.0209264 | 0.00801126 | 0 | available |
| recommendationservice_PodClientLatencyP99-s / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 0.052175 | 0.0147819 | 0 | available |
| recommendationservice_PodServerLatencyP90-s / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 1.89886 | 3.77425 | 0 | available |
| recommendationservice_PodServerLatencyP95-s / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 2.01423 | 3.98632 | 0 | available |
| recommendationservice_PodServerLatencyP99-s / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 5.21651 | 10.3418 | 0 | available |
| recommendationservice_PodSuccessRate-pct / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 0 | 0 | 0 | available |
| recommendationservice_PodWorkload-Ops / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 5.4 | 1.54517 | 0 | available |
| recommendationservice_SyscallRead / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 538 | 246.379 | 0 | available |
| recommendationservice_SyscallWrite / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 1172.4 | 407.791 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| recommendationservice_PodServerLatencyP90-s | recommendationservice | [982.4790850365321] |
| recommendationservice_PodServerLatencyP95-s | recommendationservice | [419.9999999999989] |
| recommendationservice_PodServerLatencyP99-s | recommendationservice | [266.2346241457845] |
| recommendationservice_MemoryUsage-Mi | recommendationservice | [5.8984375] |
| recommendationservice_PodClientLatencyP99-s | recommendationservice | [3.477842003853501] |
| recommendationservice_CpuUsageRate-pct | recommendationservice | [2.4798332076417733] |
| recommendationservice_CpuUsage-m | recommendationservice | [2.1876026997168614] |
| recommendationservice_MemoryUsageRate-pct | recommendationservice | [1.3107638888888884] |
| recommendationservice_PodClientLatencyP90-s | recommendationservice | [1.191506646971955] |
| recommendationservice_PodClientLatencyP95-s | recommendationservice | [1.139664804469275] |
| recommendationservice_PodWorkload-Ops | recommendationservice | [0.5384615384615373] |
| recommendationservice_NetworkReceiveBytes | recommendationservice | [0.3817658935693696] |
| recommendationservice_SyscallWrite | recommendationservice | [0.11510791366906516] |
| recommendationservice_SyscallRead | recommendationservice | [0.07643312101910792] |
| recommendationservice_NetworkTransmitBytes | recommendationservice | [-0.028314804407878286] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | recommendationservice | recommendationservice | 972 | 650 | 24182 | 3.1094e+06 | True | True | True | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | recommendationservice | recommendationservice | 972 | 650 | 24182 | 3.1094e+06 | True | True | True | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| recommendationservice | recommendationservice | 650 | 0 | available |

## Nezha-OB / dev-5467884de4

Root `recommendationservice`; status `OK`. Score entity BARO `[64.09803921568745]`; O=10, R=10; Hit@1=0, Hit@5=1. Nguồn: `results/T-026/runs/full-001/baro-main-dev-5467884de4-h0-full/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5467884de4.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| recommendationservice_CpuUsage-m / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 1.44414 | 0.176601 | 0 | available |
| recommendationservice_CpuUsageRate-pct / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 7.22068 | 0.883022 | 0 | available |
| recommendationservice_MemoryUsage-Mi / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 24.0547 | 0 | 0 | available |
| recommendationservice_MemoryUsageRate-pct / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 5.34549 | 0 | 0 | available |
| recommendationservice_NetworkReceiveBytes / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 13455.8 | 357.812 | 0 | available |
| recommendationservice_NetworkTransmitBytes / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 24571.5 | 2801.13 | 0 | available |
| recommendationservice_PodClientLatencyP90-s / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 0.0352595 | 0.0119712 | 0 | available |
| recommendationservice_PodClientLatencyP95-s / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 0.0506167 | 0.0156492 | 0 | available |
| recommendationservice_PodClientLatencyP99-s / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 0.12172 | 0.0659998 | 1 | available |
| recommendationservice_PodServerLatencyP90-s / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 0.0364407 | 0.0123761 | 0 | available |
| recommendationservice_PodServerLatencyP95-s / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 0.0546213 | 0.0145828 | 0 | available |
| recommendationservice_PodServerLatencyP99-s / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 0.0879526 | 0.0062276 | 2 | available |
| recommendationservice_PodSuccessRate-pct / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 0 | 0 | 0 | available |
| recommendationservice_PodWorkload-Ops / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 6.05333 | 0.503146 | 0 | available |
| recommendationservice_SyscallRead / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 725.2 | 38.5456 | 0 | available |
| recommendationservice_SyscallWrite / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 1488.4 | 75.6138 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| recommendationservice_PodServerLatencyP99-s | recommendationservice | [64.09803921568745] |
| recommendationservice_PodClientLatencyP99-s | recommendationservice | [23.097435897436434] |
| recommendationservice_NetworkTransmitBytes | recommendationservice | [0.4797750429593534] |
| recommendationservice_PodServerLatencyP95-s | recommendationservice | [-0.30224525043177763] |
| recommendationservice_CpuUsageRate-pct | recommendationservice | [-0.3224547847291312] |
| recommendationservice_CpuUsage-m | recommendationservice | [-0.3225147083788185] |
| recommendationservice_PodServerLatencyP90-s | recommendationservice | [-0.3932307120335731] |
| recommendationservice_PodClientLatencyP90-s | recommendationservice | [-0.5388967891624894] |
| recommendationservice_PodClientLatencyP95-s | recommendationservice | [-0.7116279069767403] |
| recommendationservice_PodWorkload-Ops | recommendationservice | [-0.7499999999999974] |
| recommendationservice_SyscallWrite | recommendationservice | [-1.8571428571428572] |
| recommendationservice_NetworkReceiveBytes | recommendationservice | [-2.056985004103584] |
| recommendationservice_SyscallRead | recommendationservice | [-3.4444444444444446] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | recommendationservice | recommendationservice | 1176 | 898 | 40080.8 | 31159.3 | False | False | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | recommendationservice | recommendationservice | 1174 | 900 | 40090.6 | 31110.4 | False | False | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| recommendationservice | recommendationservice | 899 | 0 | available |

## Nezha-OB / dev-55f99f3e0a

Root `checkoutservice`; status `OK`. Score entity BARO `[14.159663865546555]`; O=10, R=10; Hit@1=0, Hit@5=1. Nguồn: `results/T-026/runs/pilot-001/baro-main-dev-55f99f3e0a-h0-smallest/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-55f99f3e0a.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| checkoutservice_CpuUsage-m / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 1.8587 | 0.830239 | 0 | available |
| checkoutservice_CpuUsageRate-pct / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 9.29336 | 4.15132 | 0 | available |
| checkoutservice_MemoryUsage-Mi / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 31.2117 | 26.6018 | 0 | available |
| checkoutservice_MemoryUsageRate-pct / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 24.3842 | 20.7826 | 0 | available |
| checkoutservice_NetworkReceiveBytes / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 5100.43 | 1928.28 | 0 | available |
| checkoutservice_NetworkTransmitBytes / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 120965 | 38223.9 | 0 | available |
| checkoutservice_PodClientLatencyP90-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.0361919 | 0.0250934 | 1 | available |
| checkoutservice_PodClientLatencyP95-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.0720929 | 0.0401032 | 1 | available |
| checkoutservice_PodClientLatencyP99-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.19974 | 0.0702977 | 2 | available |
| checkoutservice_PodServerLatencyP90-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.587 | 0.226332 | 2 | available |
| checkoutservice_PodServerLatencyP95-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.6685 | 0.268899 | 2 | available |
| checkoutservice_PodServerLatencyP99-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.7337 | 0.306484 | 2 | available |
| checkoutservice_PodSuccessRate-pct / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0 | 0 | 0 | available |
| checkoutservice_PodWorkload-Ops / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.306667 | 0.0997775 | 0 | available |
| checkoutservice_SyscallRead / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 2418.8 | 821.396 | 0 | available |
| checkoutservice_SyscallWrite / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 2148 | 739.085 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| checkoutservice_PodClientLatencyP99-s | checkoutservice | [14.159663865546555] |
| checkoutservice_NetworkReceiveBytes | checkoutservice | [4.522992273755279] |
| checkoutservice_NetworkTransmitBytes | checkoutservice | [4.3572711323065265] |
| checkoutservice_SyscallRead | checkoutservice | [3.804123711340206] |
| checkoutservice_SyscallWrite | checkoutservice | [3.7241379310344827] |
| checkoutservice_PodClientLatencyP95-s | checkoutservice | [3.5867768595041434] |
| checkoutservice_PodServerLatencyP90-s | checkoutservice | [3.333333333333332] |
| checkoutservice_PodServerLatencyP95-s | checkoutservice | [3.1428571428571432] |
| checkoutservice_PodServerLatencyP99-s | checkoutservice | [3.025641025641025] |
| checkoutservice_PodClientLatencyP90-s | checkoutservice | [2.986282578875172] |
| checkoutservice_PodWorkload-Ops | checkoutservice | [0.5000000000000002] |
| checkoutservice_MemoryUsage-Mi | checkoutservice | [0.18951700238249947] |
| checkoutservice_MemoryUsageRate-pct | checkoutservice | [0.18951700238249947] |
| checkoutservice_CpuUsage-m | checkoutservice | [-0.6317031942053286] |
| checkoutservice_CpuUsageRate-pct | checkoutservice | [-0.6317075605577898] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | checkoutservice | checkoutservice | 334 | 703 | 160187 | 384347 | True | False | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | checkoutservice | checkoutservice | 334 | 703 | 160187 | 384347 | True | False | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| checkoutservice | checkoutservice | 908 | 41 | available |

## Nezha-OB / dev-5ada15752d

Root `frontend`; status `OK`. Score entity BARO `[3.933649289099526]`; O=10, R=10; Hit@1=0, Hit@5=0. Nguồn: `results/T-026/runs/full-001/baro-main-dev-5ada15752d-h0-full/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5ada15752d.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| frontend_CpuUsage-m / frontend | frontend | 5 | 5 | 0 / 0 | 15.7344 | 6.0014 | 0 | available |
| frontend_CpuUsageRate-pct / frontend | frontend | 5 | 5 | 0 / 0 | 80.6711 | 29.8738 | 0 | available |
| frontend_FrontLatencyP50-s / frontend | frontend | 5 | 5 | 0 / 0 | 2.95926 | 3.5375 | 0 | available |
| frontend_FrontLatencyP90-s / frontend | frontend | 5 | 5 | 0 / 0 | 8.65921 | 8.85216 | 0 | available |
| frontend_FrontLatencyP95-s / frontend | frontend | 5 | 5 | 0 / 0 | 9.94071 | 9.3951 | 0 | available |
| frontend_FrontLatencyP99-s / frontend | frontend | 5 | 5 | 0 / 0 | 11.1479 | 9.67172 | 0 | available |
| frontend_FrontSuccessRate-pct / frontend | frontend | 5 | 5 | 0 / 0 | 100 | 0 | 0 | available |
| frontend_MemoryUsage-Mi / frontend | frontend | 5 | 5 | 0 / 0 | 34.0711 | 20.2374 | 0 | available |
| frontend_MemoryUsageRate-pct / frontend | frontend | 5 | 5 | 0 / 0 | 26.618 | 15.8105 | 0 | available |
| frontend_NetworkReceiveBytes / frontend | frontend | 5 | 5 | 0 / 0 | 19830.6 | 8751.29 | 0 | available |
| frontend_NetworkTransmitBytes / frontend | frontend | 5 | 5 | 0 / 0 | 156320 | 43792.7 | 0 | available |
| frontend_PodClientLatencyP90-s / frontend | frontend | 5 | 5 | 0 / 0 | 0.0472971 | 0.0151469 | 0 | available |
| frontend_PodClientLatencyP95-s / frontend | frontend | 5 | 5 | 0 / 0 | 0.106217 | 0.0403887 | 0 | available |
| frontend_PodClientLatencyP99-s / frontend | frontend | 5 | 5 | 0 / 0 | 0.405551 | 0.200466 | 0 | available |
| frontend_PodServerLatencyP90-s / frontend | frontend | 5 | 5 | 0 / 0 | 8.65921 | 8.85216 | 0 | available |
| frontend_PodServerLatencyP95-s / frontend | frontend | 5 | 5 | 0 / 0 | 9.94071 | 9.3951 | 0 | available |
| frontend_PodServerLatencyP99-s / frontend | frontend | 5 | 5 | 0 / 0 | 11.1479 | 9.67172 | 0 | available |
| frontend_PodSuccessRate-pct / frontend | frontend | 5 | 5 | 0 / 0 | 0 | 0 | 0 | available |
| frontend_PodWorkload-Ops / frontend | frontend | 5 | 5 | 0 / 0 | 5.52 | 2.80742 | 0 | available |
| frontend_SyscallRead / frontend | frontend | 5 | 5 | 0 / 0 | 7443.2 | 7583.45 | 0 | available |
| frontend_SyscallWrite / frontend | frontend | 5 | 5 | 0 / 0 | 5931.6 | 4943.94 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| frontend_SyscallRead | frontend | [3.933649289099526] |
| frontend_SyscallWrite | frontend | [3.6033333333333335] |
| frontend_NetworkReceiveBytes | frontend | [2.9793654004558947] |
| frontend_PodClientLatencyP90-s | frontend | [1.995949367088609] |
| frontend_NetworkTransmitBytes | frontend | [1.8841940857629655] |
| frontend_PodWorkload-Ops | frontend | [1.3088235294117647] |
| frontend_PodClientLatencyP95-s | frontend | [-0.025741830861857967] |
| frontend_PodClientLatencyP99-s | frontend | [-0.060910613674418274] |
| frontend_FrontLatencyP50-s | frontend | [-0.6452445468093754] |
| frontend_MemoryUsage-Mi | frontend | [-0.7078556263269639] |
| frontend_MemoryUsageRate-pct | frontend | [-0.7078556263269639] |
| frontend_FrontLatencyP99-s | frontend | [-1.5938699546353374] |
| frontend_PodServerLatencyP99-s | frontend | [-1.5938699546353374] |
| frontend_FrontLatencyP95-s | frontend | [-1.8653608381596924] |
| frontend_PodServerLatencyP95-s | frontend | [-1.8653608381596924] |
| frontend_CpuUsage-m | frontend | [-1.8909676606110832] |
| frontend_FrontLatencyP90-s | frontend | [-2.049570148161699] |
| frontend_PodServerLatencyP90-s | frontend | [-2.049570148161699] |
| frontend_CpuUsageRate-pct | frontend | [-2.7575059583572332] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | frontend | frontend | 4468 | 7345 | 186833 | 169753 | False | False | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | frontend | frontend | 4462 | 7351 | 186409 | 170864 | False | False | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| frontend | frontend | 5792 | 1100 | available |

## Nezha-OB / dev-607751ac0a

Root `checkoutservice`; status `OK`. Score entity BARO `[5.014259252537352]`; O=10, R=10; Hit@1=0, Hit@5=0. Nguồn: `results/T-026/runs/full-001/baro-main-dev-607751ac0a-h0-full/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-607751ac0a.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| checkoutservice_CpuUsage-m / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 7.89165 | 6.96912 | 0 | available |
| checkoutservice_CpuUsageRate-pct / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 39.4583 | 34.8456 | 0 | available |
| checkoutservice_MemoryUsage-Mi / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 58.5328 | 25.7729 | 0 | available |
| checkoutservice_MemoryUsageRate-pct / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 45.7288 | 20.1351 | 0 | available |
| checkoutservice_NetworkReceiveBytes / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 5260.18 | 965.497 | 0 | available |
| checkoutservice_NetworkTransmitBytes / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 135273 | 31164.2 | 0 | available |
| checkoutservice_PodClientLatencyP90-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.038935 | 0.0245446 | 0 | available |
| checkoutservice_PodClientLatencyP95-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.0975208 | 0.0590943 | 0 | available |
| checkoutservice_PodClientLatencyP99-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.236617 | 0.11513 | 0 | available |
| checkoutservice_PodServerLatencyP90-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 6.285 | 7.61747 | 0 | available |
| checkoutservice_PodServerLatencyP95-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 7.4925 | 9.39151 | 0 | available |
| checkoutservice_PodServerLatencyP99-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 8.4585 | 10.8437 | 0 | available |
| checkoutservice_PodSuccessRate-pct / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0 | 0 | 0 | available |
| checkoutservice_PodWorkload-Ops / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.333333 | 0.139841 | 0 | available |
| checkoutservice_SyscallRead / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 2288 | 663.794 | 0 | available |
| checkoutservice_SyscallWrite / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 2000.4 | 556.031 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| checkoutservice_NetworkReceiveBytes | checkoutservice | [5.014259252537352] |
| checkoutservice_SyscallWrite | checkoutservice | [2.557377049180328] |
| checkoutservice_NetworkTransmitBytes | checkoutservice | [1.6859720500962065] |
| checkoutservice_SyscallRead | checkoutservice | [1.6852791878172588] |
| checkoutservice_PodClientLatencyP99-s | checkoutservice | [1.6130653266331394] |
| checkoutservice_PodClientLatencyP90-s | checkoutservice | [0.7019069321180156] |
| checkoutservice_PodWorkload-Ops | checkoutservice | [0.4999999999999999] |
| checkoutservice_PodServerLatencyP90-s | checkoutservice | [-0.06249999999999995] |
| checkoutservice_PodClientLatencyP95-s | checkoutservice | [-0.06490097828680426] |
| checkoutservice_PodServerLatencyP95-s | checkoutservice | [-0.11202185792349711] |
| checkoutservice_PodServerLatencyP99-s | checkoutservice | [-0.14899257688229067] |
| checkoutservice_CpuUsageRate-pct | checkoutservice | [-0.31772622232741826] |
| checkoutservice_CpuUsage-m | checkoutservice | [-0.3177262223274183] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | checkoutservice | checkoutservice | 708 | 688 | 246441 | 188425 | False | False | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | checkoutservice | checkoutservice | 708 | 688 | 246441 | 188425 | False | False | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| checkoutservice | checkoutservice | 886 | 0 | available |

## Nezha-OB / dev-63c30faf34

Root `recommendationservice`; status `OK`. Score entity BARO `[8.861347416669172]`; O=10, R=10; Hit@1=0, Hit@5=0. Nguồn: `results/T-026/runs/full-001/baro-main-dev-63c30faf34-h0-full/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-63c30faf34.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| recommendationservice_CpuUsage-m / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 1.12804 | 0.241468 | 0 | available |
| recommendationservice_CpuUsageRate-pct / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 5.64008 | 1.20732 | 0 | available |
| recommendationservice_MemoryUsage-Mi / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 25.4141 | 0 | 0 | available |
| recommendationservice_MemoryUsageRate-pct / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 5.64757 | 0 | 0 | available |
| recommendationservice_NetworkReceiveBytes / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 13477.3 | 783.942 | 0 | available |
| recommendationservice_NetworkTransmitBytes / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 29564.6 | 3444.35 | 0 | available |
| recommendationservice_PodClientLatencyP90-s / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 0.019175 | 0.00728852 | 0 | available |
| recommendationservice_PodClientLatencyP95-s / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 0.0368357 | 0.0100577 | 0 | available |
| recommendationservice_PodClientLatencyP99-s / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 0.071375 | 0.013688 | 0 | available |
| recommendationservice_PodServerLatencyP90-s / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 0.0200801 | 0.00841163 | 0 | available |
| recommendationservice_PodServerLatencyP95-s / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 0.0414442 | 0.0156136 | 0 | available |
| recommendationservice_PodServerLatencyP99-s / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 0.0786867 | 0.0128071 | 0 | available |
| recommendationservice_PodSuccessRate-pct / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 0 | 0 | 0 | available |
| recommendationservice_PodWorkload-Ops / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 6.14667 | 0.280951 | 0 | available |
| recommendationservice_SyscallRead / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 711.2 | 58.7687 | 0 | available |
| recommendationservice_SyscallWrite / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 1464 | 117.378 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| recommendationservice_NetworkReceiveBytes | recommendationservice | [8.861347416669172] |
| recommendationservice_SyscallWrite | recommendationservice | [3.4782608695652173] |
| recommendationservice_SyscallRead | recommendationservice | [2.9333333333333296] |
| recommendationservice_NetworkTransmitBytes | recommendationservice | [0.540761711367163] |
| recommendationservice_PodWorkload-Ops | recommendationservice | [0.5] |
| recommendationservice_CpuUsage-m | recommendationservice | [-0.2497917547783507] |
| recommendationservice_CpuUsageRate-pct | recommendationservice | [-0.25020179606255627] |
| recommendationservice_PodServerLatencyP90-s | recommendationservice | [-0.5658307210031346] |
| recommendationservice_PodClientLatencyP99-s | recommendationservice | [-0.7115384615384791] |
| recommendationservice_PodServerLatencyP99-s | recommendationservice | [-1.4981949458484056] |
| recommendationservice_PodServerLatencyP95-s | recommendationservice | [-1.6564417177914141] |
| recommendationservice_PodClientLatencyP90-s | recommendationservice | [-1.9983660130719054] |
| recommendationservice_PodClientLatencyP95-s | recommendationservice | [-4.544642857142823] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | recommendationservice | recommendationservice | 1010 | 1148 | 35077.3 | 7769.05 | False | False | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | recommendationservice | recommendationservice | 1010 | 1148 | 35077.3 | 7769.05 | False | False | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| recommendationservice | recommendationservice | 1148 | 0 | available |

## Nezha-OB / dev-6c9afc9822

Root `emailservice`; status `OK`. Score entity BARO `[98.20440881763528]`; O=10, R=10; Hit@1=0, Hit@5=1. Nguồn: `results/T-026/runs/full-001/baro-main-dev-6c9afc9822-h0-full/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-6c9afc9822.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| emailservice_CpuUsage-m / emailservice | emailservice | 5 | 5 | 0 / 0 | 4.55258 | 8.3431 | 0 | available |
| emailservice_CpuUsageRate-pct / emailservice | emailservice | 5 | 5 | 0 / 0 | 22.7629 | 41.7155 | 0 | available |
| emailservice_MemoryUsage-Mi / emailservice | emailservice | 5 | 5 | 0 / 0 | 43.7484 | 38.8641 | 0 | available |
| emailservice_MemoryUsageRate-pct / emailservice | emailservice | 5 | 5 | 0 / 0 | 8.54462 | 7.59064 | 0 | available |
| emailservice_NetworkReceiveBytes / emailservice | emailservice | 5 | 5 | 0 / 0 | 1058.37 | 208.23 | 0 | available |
| emailservice_NetworkTransmitBytes / emailservice | emailservice | 5 | 5 | 0 / 0 | 15944.5 | 3010.61 | 0 | available |
| emailservice_PodClientLatencyP90-s / emailservice | emailservice | 5 | 5 | 0 / 0 | 0.01416 | 0.0167777 | 1 | available |
| emailservice_PodClientLatencyP95-s / emailservice | emailservice | 5 | 5 | 0 / 0 | 0.01458 | 0.0171922 | 1 | available |
| emailservice_PodClientLatencyP99-s / emailservice | emailservice | 5 | 5 | 0 / 0 | 0.014916 | 0.0175239 | 1 | available |
| emailservice_PodServerLatencyP90-s / emailservice | emailservice | 5 | 5 | 0 / 0 | 0.26368 | 0.51816 | 0 | available |
| emailservice_PodServerLatencyP95-s / emailservice | emailservice | 5 | 5 | 0 / 0 | 0.38384 | 0.75808 | 0 | available |
| emailservice_PodServerLatencyP99-s / emailservice | emailservice | 5 | 5 | 0 / 0 | 0.479968 | 0.950016 | 0 | available |
| emailservice_PodSuccessRate-pct / emailservice | emailservice | 5 | 5 | 0 / 0 | 0 | 0 | 0 | available |
| emailservice_PodWorkload-Ops / emailservice | emailservice | 5 | 5 | 0 / 0 | 0.306667 | 0.204831 | 0 | available |
| emailservice_SyscallRead / emailservice | emailservice | 5 | 5 | 0 / 0 | 35.2 | 7.54718 | 1 | available |
| emailservice_SyscallWrite / emailservice | emailservice | 5 | 5 | 0 / 0 | 72.8 | 14.9452 | 1 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| emailservice_PodClientLatencyP99-s | emailservice | [98.20440881763528] |
| emailservice_PodClientLatencyP95-s | emailservice | [94.98989898989896] |
| emailservice_PodClientLatencyP90-s | emailservice | [90.89795918367348] |
| emailservice_SyscallWrite | emailservice | [2.333333333333335] |
| emailservice_SyscallRead | emailservice | [2.3333333333333326] |
| emailservice_NetworkTransmitBytes | emailservice | [1.2899310370945283] |
| emailservice_NetworkReceiveBytes | emailservice | [1.2168491649573754] |
| emailservice_PodWorkload-Ops | emailservice | [0.39999999999999986] |
| emailservice_CpuUsage-m | emailservice | [0.020789659951946697] |
| emailservice_CpuUsageRate-pct | emailservice | [0.020789659951946697] |
| emailservice_PodServerLatencyP99-s | emailservice | [8.673617379884035e-19] |
| emailservice_PodServerLatencyP95-s | emailservice | [0.0] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | emailservice | emailservice | 28 | 27 | 652.35 | 655.8 | False | False | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | emailservice | emailservice | 28 | 27 | 652.35 | 655.8 | False | False | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| emailservice | emailservice | 54 | 0 | available |

## Nezha-OB / dev-70629373f9

Root `paymentservice`; status `OK`. Score entity BARO `[735.5159429383294]`; O=10, R=10; Hit@1=1, Hit@5=1. Nguồn: `results/T-026/runs/full-001/baro-main-dev-70629373f9-h0-full/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-70629373f9.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| paymentservice_CpuUsage-m / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 0.0817197 | 0.0158805 | 4 | available |
| paymentservice_CpuUsageRate-pct / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 0.408584 | 0.0793984 | 4 | available |
| paymentservice_MemoryUsage-Mi / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 31.0172 | 0.04375 | 4 | available |
| paymentservice_MemoryUsageRate-pct / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 24.2322 | 0.0341797 | 4 | available |
| paymentservice_NetworkReceiveBytes / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 923.929 | 55.1347 | 3 | available |
| paymentservice_NetworkTransmitBytes / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 18245.5 | 2004.44 | 3 | available |
| paymentservice_PodClientLatencyP90-s / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 0.0046 | 0 | 1 | available |
| paymentservice_PodClientLatencyP95-s / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 0.0048 | 0 | 1 | available |
| paymentservice_PodClientLatencyP99-s / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 0.00496 | 6.71856e-19 | 1 | available |
| paymentservice_PodServerLatencyP90-s / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 0.0046 | 0 | 4 | available |
| paymentservice_PodServerLatencyP95-s / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 0.0048 | 0 | 4 | available |
| paymentservice_PodServerLatencyP99-s / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 0.00496 | 6.71856e-19 | 4 | available |
| paymentservice_PodSuccessRate-pct / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 0 | 0 | 0 | available |
| paymentservice_PodWorkload-Ops / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 0.293323 | 0.155494 | 0 | available |
| paymentservice_SyscallRead / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 40.4 | 11.4822 | 1 | available |
| paymentservice_SyscallWrite / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 90 | 26.8328 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| paymentservice_NetworkReceiveBytes | paymentservice | [735.5159429383294] |
| paymentservice_CpuUsageRate-pct | paymentservice | [655.058909406733] |
| paymentservice_CpuUsage-m | paymentservice | [508.39869708520865] |
| paymentservice_SyscallRead | paymentservice | [379.0] |
| paymentservice_MemoryUsage-Mi | paymentservice | [52.12890625] |
| paymentservice_MemoryUsageRate-pct | paymentservice | [40.7257080078125] |
| paymentservice_SyscallWrite | paymentservice | [4.999999999999997] |
| paymentservice_NetworkTransmitBytes | paymentservice | [4.226355624027946] |
| paymentservice_PodWorkload-Ops | paymentservice | [3.0024014408645203] |
| paymentservice_PodServerLatencyP99-s | paymentservice | [0.24354000000000003] |
| paymentservice_PodClientLatencyP99-s | paymentservice | [0.004889999999999999] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | paymentservice | paymentservice | 13 | 42 | 606.2 | 859.7 | False | False | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | paymentservice | paymentservice | 13 | 42 | 606.2 | 859.7 | False | False | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| paymentservice | paymentservice | 84 | 0 | available |

## Nezha-OB / dev-7b7c973198

Root `emailservice`; status `OK`. Score entity BARO `[10.358974358974356]`; O=10, R=10; Hit@1=0, Hit@5=1. Nguồn: `results/T-026/runs/full-001/baro-main-dev-7b7c973198-h0-full/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7b7c973198.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| emailservice_CpuUsage-m / emailservice | emailservice | 5 | 5 | 0 / 0 | 4.38278 | 8.54428 | 0 | available |
| emailservice_CpuUsageRate-pct / emailservice | emailservice | 5 | 5 | 0 / 0 | 21.9139 | 42.7214 | 0 | available |
| emailservice_MemoryUsage-Mi / emailservice | emailservice | 5 | 5 | 0 / 0 | 38.9727 | 28.4609 | 0 | available |
| emailservice_MemoryUsageRate-pct / emailservice | emailservice | 5 | 5 | 0 / 0 | 7.61185 | 5.55878 | 0 | available |
| emailservice_NetworkReceiveBytes / emailservice | emailservice | 5 | 5 | 0 / 0 | 802.217 | 180.138 | 0 | available |
| emailservice_NetworkTransmitBytes / emailservice | emailservice | 5 | 5 | 0 / 0 | 10683.2 | 5619.04 | 0 | available |
| emailservice_PodClientLatencyP90-s / emailservice | emailservice | 5 | 5 | 0 / 0 | 0.00856 | 0.00615812 | 1 | available |
| emailservice_PodClientLatencyP95-s / emailservice | emailservice | 5 | 5 | 0 / 0 | 0.00928 | 0.00695202 | 1 | available |
| emailservice_PodClientLatencyP99-s / emailservice | emailservice | 5 | 5 | 0 / 0 | 0.009856 | 0.00758717 | 1 | available |
| emailservice_PodServerLatencyP90-s / emailservice | emailservice | 5 | 5 | 0 / 0 | 0.80368 | 1.59816 | 0 | available |
| emailservice_PodServerLatencyP95-s / emailservice | emailservice | 5 | 5 | 0 / 0 | 0.90384 | 1.79808 | 0 | available |
| emailservice_PodServerLatencyP99-s / emailservice | emailservice | 5 | 5 | 0 / 0 | 0.983968 | 1.95802 | 0 | available |
| emailservice_PodSuccessRate-pct / emailservice | emailservice | 5 | 5 | 0 / 0 | 0 | 0 | 0 | available |
| emailservice_PodWorkload-Ops / emailservice | emailservice | 5 | 5 | 0 / 0 | 0.293333 | 0.0326599 | 3 | available |
| emailservice_SyscallRead / emailservice | emailservice | 5 | 5 | 0 / 0 | 34.4 | 21.5184 | 0 | available |
| emailservice_SyscallWrite / emailservice | emailservice | 5 | 5 | 0 / 0 | 69.6 | 42.884 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| emailservice_PodClientLatencyP90-s | emailservice | [10.358974358974356] |
| emailservice_PodClientLatencyP95-s | emailservice | [9.595505617977526] |
| emailservice_PodClientLatencyP99-s | emailservice | [9.108384458077714] |
| emailservice_CpuUsageRate-pct | emailservice | [4.5496138527711105] |
| emailservice_PodWorkload-Ops | emailservice | [3.000000000000001] |
| emailservice_CpuUsage-m | emailservice | [1.2691709162925815] |
| emailservice_NetworkTransmitBytes | emailservice | [0.7585836488462825] |
| emailservice_SyscallWrite | emailservice | [0.6896551724137931] |
| emailservice_SyscallRead | emailservice | [0.6666666666666666] |
| emailservice_NetworkReceiveBytes | emailservice | [0.6509657043426939] |
| emailservice_PodServerLatencyP99-s | emailservice | [0.0] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | emailservice | emailservice | 20 | 41 | 798.8 | 650 | False | False | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | emailservice | emailservice | 20 | 41 | 798.8 | 650 | False | False | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| emailservice | emailservice | 82 | 0 | available |

## Nezha-OB / dev-7d3c2fe6d1

Root `shippingservice`; status `OK`. Score entity BARO `[6885.264705882348]`; O=10, R=10; Hit@1=1, Hit@5=1. Nguồn: `results/T-026/runs/full-001/baro-main-dev-7d3c2fe6d1-h0-full/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7d3c2fe6d1.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| shippingservice_CpuUsage-m / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 0.582604 | 0.0900242 | 5 | available |
| shippingservice_CpuUsageRate-pct / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 2.91305 | 0.450084 | 5 | available |
| shippingservice_MemoryUsage-Mi / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 12.707 | 0 | 4 | available |
| shippingservice_MemoryUsageRate-pct / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 9.92737 | 0 | 4 | available |
| shippingservice_NetworkReceiveBytes / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 2089.11 | 235.395 | 0 | available |
| shippingservice_NetworkTransmitBytes / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 24007.9 | 6924.31 | 0 | available |
| shippingservice_PodClientLatencyP90-s / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 0.018 | 0.0130374 | 0 | available |
| shippingservice_PodClientLatencyP95-s / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 0.0195 | 0.0143263 | 0 | available |
| shippingservice_PodClientLatencyP99-s / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 0.0207 | 0.0153613 | 0 | available |
| shippingservice_PodServerLatencyP90-s / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 0.0046418 | 5.43464e-05 | 5 | available |
| shippingservice_PodServerLatencyP95-s / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 0.00484653 | 5.90398e-05 | 5 | available |
| shippingservice_PodServerLatencyP99-s / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 0.008496 | 0.00543792 | 5 | available |
| shippingservice_PodSuccessRate-pct / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 0 | 0 | 0 | available |
| shippingservice_PodWorkload-Ops / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 2.16 | 0.229395 | 1 | available |
| shippingservice_SyscallRead / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 654.8 | 93.3518 | 0 | available |
| shippingservice_SyscallWrite / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 1386.4 | 200.289 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| shippingservice_PodServerLatencyP95-s | shippingservice | [6885.264705882348] |
| shippingservice_PodServerLatencyP90-s | shippingservice | [5059.749999999938] |
| shippingservice_PodServerLatencyP99-s | shippingservice | [253.44505494505432] |
| shippingservice_CpuUsage-m | shippingservice | [119.1088284944773] |
| shippingservice_CpuUsageRate-pct | shippingservice | [119.10882849447718] |
| shippingservice_PodWorkload-Ops | shippingservice | [23.000000000000075] |
| shippingservice_PodClientLatencyP90-s | shippingservice | [2.9555555555555544] |
| shippingservice_PodClientLatencyP95-s | shippingservice | [2.7904761904761903] |
| shippingservice_PodClientLatencyP99-s | shippingservice | [2.68888888888889] |
| shippingservice_SyscallRead | shippingservice | [1.5357142857142836] |
| shippingservice_SyscallWrite | shippingservice | [1.2173913043478262] |
| shippingservice_NetworkReceiveBytes | shippingservice | [0.27257151993266343] |
| shippingservice_NetworkTransmitBytes | shippingservice | [-0.11511041916877394] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | shippingservice | shippingservice | 687 | 893 | 498 | 100029 | True | True | True | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | shippingservice | shippingservice | 687 | 893 | 498 | 100029 | True | True | True | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| shippingservice | shippingservice | 1786 | 0 | available |

## Nezha-OB / dev-8ecd9880ed

Root `checkoutservice`; status `OK`. Score entity BARO `[4.219827586206892]`; O=10, R=10; Hit@1=0, Hit@5=0. Nguồn: `results/T-026/runs/pilot-001/baro-main-dev-8ecd9880ed-h0-largest/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-8ecd9880ed.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| checkoutservice_CpuUsage-m / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 1.33434 | 0.28474 | 0 | available |
| checkoutservice_CpuUsageRate-pct / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 6.67183 | 1.42383 | 0 | available |
| checkoutservice_MemoryUsage-Mi / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 51.0789 | 0.685025 | 0 | available |
| checkoutservice_MemoryUsageRate-pct / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 39.9054 | 0.535176 | 0 | available |
| checkoutservice_NetworkReceiveBytes / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 14546.8 | 15902.9 | 0 | available |
| checkoutservice_NetworkTransmitBytes / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 175715 | 46724.2 | 0 | available |
| checkoutservice_PodClientLatencyP90-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.0522415 | 0.0278315 | 0 | available |
| checkoutservice_PodClientLatencyP95-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.0835775 | 0.0477355 | 0 | available |
| checkoutservice_PodClientLatencyP99-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.128917 | 0.0730111 | 2 | available |
| checkoutservice_PodServerLatencyP90-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.9205 | 0.615756 | 0 | available |
| checkoutservice_PodServerLatencyP95-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 1.13525 | 0.782872 | 0 | available |
| checkoutservice_PodServerLatencyP99-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 1.30705 | 0.931186 | 0 | available |
| checkoutservice_PodSuccessRate-pct / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0 | 0 | 0 | available |
| checkoutservice_PodWorkload-Ops / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.333333 | 0.139841 | 0 | available |
| checkoutservice_SyscallRead / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 2477.2 | 354.7 | 1 | available |
| checkoutservice_SyscallWrite / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 2150.4 | 305.089 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| checkoutservice_PodClientLatencyP95-s | checkoutservice | [4.219827586206892] |
| checkoutservice_PodClientLatencyP99-s | checkoutservice | [4.063095238095215] |
| checkoutservice_MemoryUsage-Mi | checkoutservice | [3.95959595959596] |
| checkoutservice_MemoryUsageRate-pct | checkoutservice | [3.95959595959596] |
| checkoutservice_SyscallRead | checkoutservice | [3.614864864864865] |
| checkoutservice_SyscallWrite | checkoutservice | [3.242424242424242] |
| checkoutservice_CpuUsageRate-pct | checkoutservice | [1.7388544396424603] |
| checkoutservice_CpuUsage-m | checkoutservice | [1.7388544396424588] |
| checkoutservice_PodServerLatencyP90-s | checkoutservice | [1.432432432432433] |
| checkoutservice_PodWorkload-Ops | checkoutservice | [1.0] |
| checkoutservice_PodServerLatencyP95-s | checkoutservice | [0.9658119658119668] |
| checkoutservice_PodClientLatencyP90-s | checkoutservice | [0.962499999999998] |
| checkoutservice_PodServerLatencyP99-s | checkoutservice | [0.7833553500660497] |
| checkoutservice_NetworkReceiveBytes | checkoutservice | [-0.392498179181028] |
| checkoutservice_NetworkTransmitBytes | checkoutservice | [-1.1217887926301953] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | checkoutservice | checkoutservice | 707 | 477 | 212483 | 308619 | False | False | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | checkoutservice | checkoutservice | 703 | 481 | 200788 | 327199 | False | False | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| checkoutservice | checkoutservice | 595 | 25 | available |

## Nezha-OB / dev-95e164235f

Root `paymentservice`; status `OK`. Score entity BARO `[1404.1746026427618]`; O=10, R=10; Hit@1=1, Hit@5=1. Nguồn: `results/T-026/runs/full-001/baro-main-dev-95e164235f-h0-full/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-95e164235f.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| paymentservice_CpuUsage-m / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 0.0701229 | 0.0284209 | 5 | available |
| paymentservice_CpuUsageRate-pct / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 0.350608 | 0.142107 | 5 | available |
| paymentservice_MemoryUsage-Mi / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 33.9922 | 0 | 5 | available |
| paymentservice_MemoryUsageRate-pct / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 26.5564 | 0 | 5 | available |
| paymentservice_NetworkReceiveBytes / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 966.203 | 94.8707 | 1 | available |
| paymentservice_NetworkTransmitBytes / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 20442 | 4242.74 | 0 | available |
| paymentservice_PodClientLatencyP90-s / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 0.007164 | 0.00516809 | 0 | available |
| paymentservice_PodClientLatencyP95-s / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 0.008082 | 0.00658402 | 0 | available |
| paymentservice_PodClientLatencyP99-s / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 0.0088164 | 0.0077168 | 0 | available |
| paymentservice_PodServerLatencyP90-s / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 0.0046 | 0 | 4 | available |
| paymentservice_PodServerLatencyP95-s / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 0.0048 | 3.87896e-19 | 4 | available |
| paymentservice_PodServerLatencyP99-s / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 0.00496 | 5.48568e-19 | 4 | available |
| paymentservice_PodSuccessRate-pct / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 0 | 0 | 0 | available |
| paymentservice_PodWorkload-Ops / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 0.306643 | 0.0998032 | 1 | available |
| paymentservice_SyscallRead / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 37.2 | 15.3154 | 0 | available |
| paymentservice_SyscallWrite / paymentservice | paymentservice | 5 | 5 | 0 / 0 | 80 | 37.4166 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| paymentservice_CpuUsage-m | paymentservice | [1404.1746026427618] |
| paymentservice_CpuUsageRate-pct | paymentservice | [1266.4053827831503] |
| paymentservice_SyscallRead | paymentservice | [3.0] |
| paymentservice_PodWorkload-Ops | paymentservice | [2.5000000000000004] |
| paymentservice_NetworkTransmitBytes | paymentservice | [1.441774873335675] |
| paymentservice_NetworkReceiveBytes | paymentservice | [1.2686725762350146] |
| paymentservice_SyscallWrite | paymentservice | [1.25] |
| paymentservice_PodServerLatencyP99-s | paymentservice | [0.24054] |
| paymentservice_PodServerLatencyP95-s | paymentservice | [0.2227] |
| paymentservice_PodClientLatencyP99-s | paymentservice | [8.673617379884035e-19] |
| paymentservice_PodClientLatencyP95-s | paymentservice | [0.0] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | paymentservice | paymentservice | 33 | 36 | 302.8 | 476.25 | False | False | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | paymentservice | paymentservice | 33 | 36 | 302.8 | 476.25 | False | False | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| paymentservice | paymentservice | 74 | 0 | available |

## Nezha-OB / dev-9b9397a4dc

Root `recommendationservice`; status `OK`. Score entity BARO `[115.34463585195282]`; O=10, R=10; Hit@1=0, Hit@5=1. Nguồn: `results/T-026/runs/full-001/baro-main-dev-9b9397a4dc-h0-full/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-9b9397a4dc.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| recommendationservice_CpuUsage-m / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 3.05169 | 2.39828 | 3 | available |
| recommendationservice_CpuUsageRate-pct / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 15.2579 | 11.9905 | 3 | available |
| recommendationservice_MemoryUsage-Mi / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 25.3195 | 2.42813 | 0 | available |
| recommendationservice_MemoryUsageRate-pct / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 5.62656 | 0.539583 | 0 | available |
| recommendationservice_NetworkReceiveBytes / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 12062 | 2620.15 | 0 | available |
| recommendationservice_NetworkTransmitBytes / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 27298.8 | 4473.11 | 0 | available |
| recommendationservice_PodClientLatencyP90-s / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 0.0328824 | 0.0118725 | 0 | available |
| recommendationservice_PodClientLatencyP95-s / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 0.0576145 | 0.0399625 | 0 | available |
| recommendationservice_PodClientLatencyP99-s / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 0.105832 | 0.0802142 | 0 | available |
| recommendationservice_PodServerLatencyP90-s / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 1.58239 | 3.08385 | 0 | available |
| recommendationservice_PodServerLatencyP95-s / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 1.83157 | 3.52196 | 0 | available |
| recommendationservice_PodServerLatencyP99-s / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 2.08177 | 3.84838 | 0 | available |
| recommendationservice_PodSuccessRate-pct / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 0 | 0 | 0 | available |
| recommendationservice_PodWorkload-Ops / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 5.64 | 1.33706 | 0 | available |
| recommendationservice_SyscallRead / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 602.4 | 101.275 | 0 | available |
| recommendationservice_SyscallWrite / recommendationservice | recommendationservice | 5 | 5 | 0 / 0 | 1297.2 | 98.5544 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| recommendationservice_PodServerLatencyP90-s | recommendationservice | [115.34463585195282] |
| recommendationservice_PodServerLatencyP95-s | recommendationservice | [45.188643902439054] |
| recommendationservice_PodServerLatencyP99-s | recommendationservice | [16.36705239713666] |
| recommendationservice_PodClientLatencyP99-s | recommendationservice | [15.880000000000257] |
| recommendationservice_CpuUsageRate-pct | recommendationservice | [10.078344830082482] |
| recommendationservice_CpuUsage-m | recommendationservice | [10.07834483008248] |
| recommendationservice_PodClientLatencyP95-s | recommendationservice | [7.840252233315857] |
| recommendationservice_MemoryUsage-Mi | recommendationservice | [6.0703125] |
| recommendationservice_SyscallRead | recommendationservice | [5.499999999999939] |
| recommendationservice_SyscallWrite | recommendationservice | [3.45454545454546] |
| recommendationservice_NetworkTransmitBytes | recommendationservice | [2.196041896716058] |
| recommendationservice_PodClientLatencyP90-s | recommendationservice | [1.593998461143884] |
| recommendationservice_MemoryUsageRate-pct | recommendationservice | [1.348958333333334] |
| recommendationservice_PodWorkload-Ops | recommendationservice | [1.2499999999999991] |
| recommendationservice_NetworkReceiveBytes | recommendationservice | [0.3229549418742398] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | recommendationservice | recommendationservice | 695 | 623 | 3.03543e+06 | 3.19883e+06 | False | False | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | recommendationservice | recommendationservice | 686 | 632 | 2.99177e+06 | 3.20179e+06 | False | False | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| recommendationservice | recommendationservice | 631 | 0 | available |

## Nezha-OB / dev-9fd793feb7

Root `shippingservice`; status `OK`. Score entity BARO `[50.38461538461538]`; O=10, R=10; Hit@1=0, Hit@5=1. Nguồn: `results/T-026/runs/full-001/baro-main-dev-9fd793feb7-h0-full/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-9fd793feb7.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| shippingservice_CpuUsage-m / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 7.15491 | 8.23252 | 0 | available |
| shippingservice_CpuUsageRate-pct / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 35.7745 | 41.1626 | 0 | available |
| shippingservice_MemoryUsage-Mi / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 32.7273 | 40.1832 | 0 | available |
| shippingservice_MemoryUsageRate-pct / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 25.5682 | 31.3932 | 0 | available |
| shippingservice_NetworkReceiveBytes / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 2114.81 | 119.053 | 1 | available |
| shippingservice_NetworkTransmitBytes / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 22703.1 | 2229.84 | 1 | available |
| shippingservice_PodClientLatencyP90-s / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 0.00979 | 0.00671062 | 2 | available |
| shippingservice_PodClientLatencyP95-s / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 0.010395 | 0.00702767 | 2 | available |
| shippingservice_PodClientLatencyP99-s / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 0.010879 | 0.00728403 | 2 | available |
| shippingservice_PodServerLatencyP90-s / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 0.116756 | 0.137698 | 3 | available |
| shippingservice_PodServerLatencyP95-s / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 0.164878 | 0.196084 | 3 | available |
| shippingservice_PodServerLatencyP99-s / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 0.242976 | 0.301227 | 0 | available |
| shippingservice_PodSuccessRate-pct / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 0 | 0 | 0 | available |
| shippingservice_PodWorkload-Ops / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 2.69333 | 0.510512 | 0 | available |
| shippingservice_SyscallRead / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 657.2 | 55.3765 | 1 | available |
| shippingservice_SyscallWrite / shippingservice | shippingservice | 5 | 5 | 0 / 0 | 1451.6 | 72.5358 | 1 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| shippingservice_PodClientLatencyP90-s | shippingservice | [50.38461538461538] |
| shippingservice_PodClientLatencyP95-s | shippingservice | [49.04494382022472] |
| shippingservice_PodClientLatencyP99-s | shippingservice | [48.19018404907976] |
| shippingservice_SyscallRead | shippingservice | [4.090909090909089] |
| shippingservice_PodServerLatencyP90-s | shippingservice | [3.486680984137747] |
| shippingservice_NetworkReceiveBytes | shippingservice | [2.9788690103806124] |
| shippingservice_NetworkTransmitBytes | shippingservice | [2.81129830994536] |
| shippingservice_PodServerLatencyP95-s | shippingservice | [2.429625131260992] |
| shippingservice_PodServerLatencyP99-s | shippingservice | [2.079904681911666] |
| shippingservice_SyscallWrite | shippingservice | [1.9152542372881356] |
| shippingservice_MemoryUsage-Mi | shippingservice | [1.8671875] |
| shippingservice_MemoryUsageRate-pct | shippingservice | [1.458740234375] |
| shippingservice_CpuUsageRate-pct | shippingservice | [1.2802847713903454] |
| shippingservice_CpuUsage-m | shippingservice | [0.9794224650646483] |
| shippingservice_PodWorkload-Ops | shippingservice | [0.599999999999999] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | shippingservice | shippingservice | 522 | 1034 | 495.85 | 577830 | True | True | True | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | shippingservice | shippingservice | 522 | 1034 | 495.85 | 577830 | True | True | True | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| shippingservice | shippingservice | 2068 | 0 | available |

## Nezha-OB / dev-b0f8b2e3ac

Root `checkoutservice`; status `OK`. Score entity BARO `[194.49999999999764]`; O=10, R=10; Hit@1=1, Hit@5=1. Nguồn: `results/T-026/runs/full-001/baro-main-dev-b0f8b2e3ac-h0-full/ban-ghi-0.json` và `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-b0f8b2e3ac.json` → `/aggregate`.

| Metric/native service | Entity | nN | nA | Thiếu N/A | μN | σN ddof0 | Events strict | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| checkoutservice_CpuUsage-m / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 1.25973 | 0.423052 | 0 | available |
| checkoutservice_CpuUsageRate-pct / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 6.29848 | 2.11513 | 0 | available |
| checkoutservice_MemoryUsage-Mi / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 37.8203 | 0 | 4 | available |
| checkoutservice_MemoryUsageRate-pct / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 29.5471 | 0 | 4 | available |
| checkoutservice_NetworkReceiveBytes / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 4326.56 | 910.49 | 1 | available |
| checkoutservice_NetworkTransmitBytes / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 99289.6 | 47507.7 | 0 | available |
| checkoutservice_PodClientLatencyP90-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.0506286 | 0.0242775 | 0 | available |
| checkoutservice_PodClientLatencyP95-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.074125 | 0.0285246 | 2 | available |
| checkoutservice_PodClientLatencyP99-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.170808 | 0.13178 | 0 | available |
| checkoutservice_PodServerLatencyP90-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.482 | 0.213532 | 2 | available |
| checkoutservice_PodServerLatencyP95-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.516 | 0.228526 | 2 | available |
| checkoutservice_PodServerLatencyP99-s / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.5432 | 0.241564 | 2 | available |
| checkoutservice_PodSuccessRate-pct / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0 | 0 | 0 | available |
| checkoutservice_PodWorkload-Ops / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 0.226667 | 0.0997775 | 1 | available |
| checkoutservice_SyscallRead / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 2672.4 | 473.265 | 0 | available |
| checkoutservice_SyscallWrite / checkoutservice | checkoutservice | 5 | 5 | 0 / 0 | 2357.6 | 415.622 | 0 | available |

| Metric BARO sau preprocessing | Entity | Signed full key |
| --- | --- | --- |
| checkoutservice_PodServerLatencyP99-s | checkoutservice | [194.49999999999764] |
| checkoutservice_PodServerLatencyP95-s | checkoutservice | [34.49999999999999] |
| checkoutservice_PodServerLatencyP90-s | checkoutservice | [14.5] |
| checkoutservice_SyscallRead | checkoutservice | [6.25] |
| checkoutservice_PodClientLatencyP99-s | checkoutservice | [4.318239795918317] |
| checkoutservice_NetworkTransmitBytes | checkoutservice | [4.179912988099636] |
| checkoutservice_NetworkReceiveBytes | checkoutservice | [3.1055086320282848] |
| checkoutservice_SyscallWrite | checkoutservice | [2.948717948717949] |
| checkoutservice_PodWorkload-Ops | checkoutservice | [2.5] |
| checkoutservice_PodClientLatencyP95-s | checkoutservice | [2.4699453551912596] |
| checkoutservice_PodClientLatencyP90-s | checkoutservice | [1.4153846153846168] |
| checkoutservice_CpuUsageRate-pct | checkoutservice | [0.4794122654846352] |
| checkoutservice_CpuUsage-m | checkoutservice | [0.47922835725707863] |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | checkoutservice | checkoutservice | 256 | 856 | 173847 | 440784 | True | False | False | available |

| Trace split | Native service | Entity | nN | nA | P95N μs | P95A μs | τ2 | τ3 | τ4 | Khả dụng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| end | checkoutservice | checkoutservice | 256 | 856 | 173847 | 440784 | True | False | False | available |

| Log native service | Entity | Dòng A | Keyword count A | Khả dụng |
| --- | --- | --- | --- | --- |
| checkoutservice | checkoutservice | 1096 | 48 | available |
