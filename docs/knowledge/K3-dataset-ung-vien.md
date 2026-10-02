# K3 — Kiến thức nền: các dataset ứng viên

> Trích nguyên văn từ ghi chú nghiên cứu ngày 01–02/10/2026 (`second_dataset_candidates.md`). Chỉ giữ các mục "Cited Findings" (dữ kiện có trích nguồn). Đã bỏ "Takeaway", "Inferences" (phần suy luận, dễ neo) và "Gaps". Câu hỏi ở mỗi mục là câu hỏi của đợt khảo sát cũ, giữ để định vị nội dung, không phải định hướng hiện hành.
>
> **Chưa kiểm lại.** Mỗi dữ kiện phải kiểm trên nguồn gốc trước khi dùng. Nhãn [VERIFIED] là của người viết ghi chú cũ, không phải của repo này.

## Q1. RCAEval siblings (RE2-OB, RE2-SS, RE3-*, TORAI): what is verified, and do they meet the must-haves?

### Cited Findings
- [VERIFIED] Scope: RCAEval is "nine datasets with 735 real failure cases", organised as three suites (RE1, RE2, RE3) × three systems (Online Boutique, Sock Shop, Train Ticket). Each case has an "annotated root cause service and root cause indicator". — [RCAEval README](https://github.com/phamquiluan/RCAEval)
- [VERIFIED] Dataset table from the README — [RCAEval README](https://github.com/phamquiluan/RCAEval):

  | Dataset | Cases | Fault types | Metrics | Logs | Traces |
  |---|---|---|---|---|---|
  | RE2-OB | 90 | cpu, mem, disk, delay, loss, socket | 69–77 | Yes | Yes |
  | RE2-SS | 90 | same six | 74–82 | Yes | **N/A** |
  | RE2-TT | 90 | same six | 340–376 | Yes | Yes |
  | RE3-OB | 30 | f1–f5 | 68–101 | Yes | Yes |
  | RE3-SS | 30 | f1–f4 | 80–107 | Yes | N/A |
  | RE3-TT | 30 | f1–f4 | 294–322 | Yes | Yes |
  | TORAI-OB/SS/TT | 90 each | same as RE2 | same as RE2 | Yes | Yes / N/A / Yes |

- [VERIFIED] RE2 design: "Six fault types (adds SOCKET) across five services per system, with three repetitions per fault-service pair". That gives 15 cases per fault type per system; the 15 is arithmetic. — [RCAEval README](https://github.com/phamquiluan/RCAEval)
- [VERIFIED] Per-case layout: the folder is named `{benchmark}_{service}_{fault}_{instance}` and contains:
  - `metrics.json`
  - `inject_time.txt` (Unix timestamp)
  - `logs.csv` and `traces.csv` (RE2/RE3 only)
  - pre-aggregated `logts.csv`, `tracets_err.csv` and `tracets_lat.csv` (RE2/RE3), which the multi-source methods use.

  An example case path is `data/re1ob_adservice_cpu_1`. — [RCAEval README](https://github.com/phamquiluan/RCAEval)
- [VERIFIED] System sizes in the RCAEval paper: Online Boutique has 12 services (gRPC), Sock Shop 15 (HTTP) and Train Ticket 64. — [RCAEval paper, arXiv 2412.17015v2](https://arxiv.org/html/2412.17015v2)
- [VERIFIED] Normal window: "We allow the microservice systems to run normally for ten minutes to collect normal telemetry data. Then, we inject a fault into a randomly selected running service…". The post-injection duration is not stated in the paper. — [RCAEval paper](https://arxiv.org/html/2412.17015v2)
- [VERIFIED] Fault injection:
  - CPU, MEM, DISK and SOCKET use stress-ng.
  - DELAY and LOSS use traffic control (tc).
  - RE3 faults are code modifications: F1 incorrect parameter values, F2 missing parameters, F3 missing function call, F4 incorrect return values, F5 missing exception handlers.

  Source: [RCAEval paper](https://arxiv.org/html/2412.17015v2)
- [VERIFIED] Telemetry stack: Prometheus with cAdvisor and the Istio service mesh for metrics, Jaeger for traces, and Vector plus Loki for logs (stored in Elasticsearch). — [RCAEval paper](https://arxiv.org/html/2412.17015v2)
- [VERIFIED from code] RCAEval's trace-based baseline reads parent links directly: `parent_span_id = row["parentSpanID"]` in `RCAEval/e2e/microrank.py` (lines 604 and 624). `read_traces()` reads either `traces.parquet` or `traces.csv`. — [microrank.py](https://github.com/phamquiluan/RCAEval/blob/main/RCAEval/e2e/microrank.py); [utility/__init__.py](https://github.com/phamquiluan/RCAEval/blob/main/RCAEval/utility/__init__.py)
- [VERIFIED from code] Evaluation window in `main.py`:
  - The default is `--length 20` (minutes); the code comment reads "convert length from minutes to seconds".
  - It selects `data[data.time < inject_time].tail(length*60//2)` and `data[data.time >= inject_time].head(length*60//2)`, so the default is 10 minutes either side of `inject_time`.
  - `main.py` also has a dataset-specific branch for `RE2-OB`, `RE2-SS`, `RE3-OB` and `RE3-SS` paths (line ~354).
  - The utility code drops a duplicate `time.1` column, removes `*latency-50` columns and renames `*latency-90` columns to `latency`.

  Source: [main.py](https://github.com/phamquiluan/RCAEval/blob/main/main.py); [utility/__init__.py](https://github.com/phamquiluan/RCAEval/blob/main/RCAEval/utility/__init__.py)
- [VERIFIED] OB metric naming is `<service>_<metric>`. The README's BARO example prints `['emailservice_mem', 'recommendationservice_mem', 'cartservice_mem', 'checkoutservice_latency', 'cartservice_latency']`. — [RCAEval README](https://github.com/phamquiluan/RCAEval)
- [VERIFIED] Download options — [RCAEval README](https://github.com/phamquiluan/RCAEval):
  - **Hugging Face** (recommended): Parquet, "3.4GB on disk", downloadable one suite or one case at a time via `snapshot_download(..., allow_patterns="re2*")`.
  - **Zenodo** 10.5281/zenodo.14590730: 5.2 GB of zips, about 38 GB extracted; `RE2.zip` is 4.21 GB.
  - **Figshare** 31048672.
- [VERIFIED] The Hugging Face `cases.parquet` index has these columns: `case`, `dataset`, `system`, `root_cause_service`, `fault`, `fault_description`, `repetition`, `inject_time`, `time_start`, `time_end`, `duration_minutes`, `normal_timesteps`, `faulty_timesteps`, `n_metrics`, `has_logs`, `n_logs`, `has_traces`, `n_traces`. The licence is shown as MIT. — [HF dataset card](https://huggingface.co/datasets/phamquiluan/RCAEval)
- [VERIFIED] Licence: "For the code implemented by us and for our datasets, we distribute them under the MIT LICENSE". — [RCAEval README](https://github.com/phamquiluan/RCAEval)
- [VERIFIED] Recommended machine: "at least 8 cores, 16GB RAM, and ~50GB available disk space". — [RCAEval README](https://github.com/phamquiluan/RCAEval)
- [VERIFIED] September 2026 changelog — [RCAEval README](https://github.com/phamquiluan/RCAEval):
  - "Fixed PageRank-based methods and CIRCA silently falling back to column order (scikit-network ≥0.32 and networkx ≥3.0 API removals…)".
  - Added `--report-chance` (Chance@5, Lift@5).
  - Added `--report-decomposition K` (Retrieval@K, Rerank@1) from "Where Root Cause Analysis Fails: A Retrieval-Reranking Decomposition" (NeurIPS 2026 Evaluations and Datasets track).
- [VERIFIED] TORAI datasets are "A processed version of the RE2 datasets, containing pre-aggregated time-series…" and are hosted on Figshare (10.6084/m9.figshare.31925976). The TORAI paper (FSE 2026) is titled "Multi-source Root Cause Analysis for Blind Spots in Microservice Service Call Graph". — [RCAEval README](https://github.com/phamquiluan/RCAEval)
- [VERIFIED] Online Boutique's service table lists: frontend, cartservice, productcatalogservice, currencyservice, paymentservice, shippingservice, emailservice, checkoutservice, recommendationservice, adservice and loadgenerator. — [microservices-demo README](https://github.com/GoogleCloudPlatform/microservices-demo)


## Q2. Nezha (FSE'23; Online Boutique + Train Ticket): what is in the release, and does it fit?

### Cited Findings
- [VERIFIED] Repo layout — [Nezha README](https://github.com/IntelligentDDS/Nezha):
  - Fault-suffering data in `rca_data/<date>` (2022-08-22 and 2022-08-23 for OB; 2023-01-29 and 2023-01-30 for TT).
  - Fault-free data in `construct_data/<date>`.
  - Each date folder has `log/`, `metric/`, `trace/` and `traceid/`.
  - Service-level labels in `<date>-fault_list.json`.
  - Inner-service labels in `root_cause_hipster.json` and `root_cause_ts.json`.
  - The README reports "hipster Fault numbuer : 56" and "ts Fault numbuer : 45".
- [VERIFIED: counted from the four fault-list JSON files] Fault counts — [2022-08-22 list](https://github.com/IntelligentDDS/Nezha/blob/main/rca_data/2022-08-22/2022-08-22-fault_list.json), [2022-08-23 list](https://github.com/IntelligentDDS/Nezha/blob/main/rca_data/2022-08-23/2022-08-23-fault_list.json), [2023-01-29 list](https://github.com/IntelligentDDS/Nezha/blob/main/rca_data/2023-01-29/2023-01-29-fault_list.json), [2023-01-30 list](https://github.com/IntelligentDDS/Nezha/blob/main/rca_data/2023-01-30/2023-01-30-fault_list.json):

  | System / date | Cases | Breakdown | Distinct pods |
  |---|---|---|---|
  | OB 2022-08-22 | 24 | cpu_contention 8, network_delay 7, cpu_consumed 3, return 3, exception 3 | 10 |
  | OB 2022-08-23 | 32 | cpu_contention 8, network_delay 9, cpu_consumed 7, return 4, exception 4 | 10 |
  | **OB total** | **56** | cpu_contention 16, cpu_consumed 10, network_delay 16, return 7, exception 7 | |
  | TT 2023-01-29 | 28 | exception 13, return 11, cpu_contention 4 | 9 |
  | TT 2023-01-30 | 17 | network_delay 14, cpu_contention 3 | 8 |
  | **TT total** | **45** | network_delay 14, cpu_contention 7, return 11, exception 13 | |

- [VERIFIED] Label record format: `{"inject_time": "2023-01-29 08:43:04", "inject_timestamp": "1674953044", "inject_pod": "ts-contacts-service-866bd68c97-xcqfx", "inject_type": "return"}`, grouped by hour. — [2023-01-29 fault list](https://github.com/IntelligentDDS/Nezha/blob/main/rca_data/2023-01-29/2023-01-29-fault_list.json)
- [VERIFIED] Inner-service labels map each fault to a code region or a metric. Example for ts-basic-service: `return` → `f.m.s.BasicServiceImpl#405_f.m.s.BasicServiceImpl#418`; `cpu_contention` → `CpuUsageRate(%)`; `network_delay` → `NetworkP90(ms)`. — [root_cause_ts.json](https://github.com/IntelligentDDS/Nezha/blob/main/construct_data/root_cause_ts.json)
- [VERIFIED] Trace CSV header: `TraceID,SpanID,ParentID,PodName,OperationName,StartTimeUnixNano,EndTimeUnixNano,Duration`. Root spans have `ParentID = root`; for example, the first span is `ts-gateway-service-…` with operation `/*`. — [08_43_trace.csv](https://github.com/IntelligentDDS/Nezha/blob/main/rca_data/2023-01-29/trace/08_43_trace.csv)
- [VERIFIED] Metric CSV, one per pod, with columns:
  - `Time, TimeStamp, PodName`
  - `CpuUsage(m), CpuUsageRate(%), MemoryUsage(Mi), MemoryUsageRate(%)`
  - `SyscallRead, SyscallWrite, NetworkReceiveBytes, NetworkTransmitBytes`
  - `PodClientLatencyP90/P95/P99(s), PodServerLatencyP90/P95/P99(s)`
  - `PodWorkload(Ops), PodSuccessRate(%)`
  - `NodeCpuUsageRate(%), NodeMemoryUsageRate(%), NodeNetworkReceiveBytes`

  Source: [metric example](https://github.com/IntelligentDDS/Nezha/blob/main/rca_data/2023-01-29/metric/ts-admin-basic-info-service-5f55b6cf68-77cfw_metric.csv)
- [VERIFIED: counted from the repo tree] `construct_data/2023-01-29/metric` holds 47 files (per-pod files such as `ts-admin-basic-info-service-5f55b6cf68-77cfw_metric.csv`, plus `front_service.csv`). Each OB date holds 14 metric files. — [Nezha construct_data](https://github.com/IntelligentDDS/Nezha/tree/main/construct_data)
- [VERIFIED] Licence: "MIT License, Copyright (c) 2023 IntelligentDDS". — [LICENSE](https://github.com/IntelligentDDS/Nezha/blob/main/LICENSE)
- [VERIFIED: computed] **Timezone mismatch between labels and telemetry**, with sources [fault list](https://github.com/IntelligentDDS/Nezha/blob/main/rca_data/2023-01-29/2023-01-29-fault_list.json), [trace](https://github.com/IntelligentDDS/Nezha/blob/main/rca_data/2023-01-29/trace/08_43_trace.csv) and [metric](https://github.com/IntelligentDDS/Nezha/blob/main/rca_data/2023-01-29/metric/ts-admin-basic-info-service-5f55b6cf68-77cfw_metric.csv):
  - Label side: `inject_timestamp` 1674953526 is 2023-01-29 00:52:06 UTC, which is 08:52:06 at UTC+8 and matches its `inject_time` string.
  - Telemetry side: rows from the same morning carry epoch 1674981669 with `Time` "2023-01-29 08:41:09… +0000 UTC". Spans start at 1674981768697000000 ns, which is 08:42:48 UTC.
  - So label epochs and telemetry epochs differ by about 8 h. A naive epoch join is off by 8 h; the wall-clock strings line up.
- [VERIFIED: computed] **Label timestamp errors** — [2023-01-29 fault list](https://github.com/IntelligentDDS/Nezha/blob/main/rca_data/2023-01-29/2023-01-29-fault_list.json):
  - The 08:43:04 entry has epoch 1674953044, which is 08:44:04 at UTC+8 (60 s off).
  - The 09:03:53 and 09:12:56 entries share the same `inject_timestamp` 1674954273 (09:04:33 at UTC+8).
- [VERIFIED] **Back-to-back injections**: 08:43:04, 08:52:06 and 08:58:16; 09:21:39 then 09:25:39 (4 min apart). — [2023-01-29 fault list](https://github.com/IntelligentDDS/Nezha/blob/main/rca_data/2023-01-29/2023-01-29-fault_list.json)
- [VERIFIED] The FSE'26 benchmark paper found a simple rule-based method ("SimpleRCA") reaches Top@1 0.93 on Nezha-TT, against 0.87 for Nezha itself. — [arXiv 2510.04711v2](https://www.arxiv.org/pdf/2510.04711v2)


## Q3. Eadro (ICSE'23; Train Ticket + DeathStarBench SocialNetwork): what is released?

### Cited Findings
- [VERIFIED] Systems: TT has "41 microservices… 27 of them are business-related"; SN has "21 microservices", of which "14 of them are related to business logic". — [Eadro paper (arXiv 2302.05092)](https://arxiv.org/pdf/2302.05092)
- [VERIFIED] Faults, injected with ChaosBlade: CPU exhaustion ("putting a hog to consume CPU resource heavily"), network delay, and "randomly drop network packets". There were "162 and 72 injection operations in TT and SN, respectively". — [Eadro paper](https://arxiv.org/pdf/2302.05092)
- [VERIFIED] Timing — [Eadro paper](https://arxiv.org/pdf/2302.05092):
  - Normal data: "7 hours for TT and 1.2 hours for SN".
  - TT: "each fault duration to 10 mins (with a 2-min interval between two injections)".
  - SN: "fault duration is 2 mins and SN's interval is half a minute".
- [VERIFIED] Collection: traces to Jaeger; KPIs via cAdvisor and Prometheus, stored in InfluxDB; logs via Elasticsearch, Fluentd and Kibana; "48,296 and 126,384 traces". The paper states "All the collected data and our code are released for replication". — [Eadro paper](https://arxiv.org/pdf/2302.05092)
- [VERIFIED] The GitHub README says only "Our data are at https://doi.org/10.5281/zenodo.7615393". The repo holds only code: `Readme.md`, `codes/{base,main,model,utils}.py`, `codes/preprocess/{align,single_process,util}.py` and `requirements.txt`. No licence file is shown. — [Eadro GitHub](https://github.com/BEbillionaireUSD/Eadro)
- [VERIFIED from code] The preprocessing (`codes/preprocess/*.py`) reads `parsed_data/<name>/`:
  - `logs<idx>.csv` and `templates.json`;
  - `metrics<idx>/<service>.csv`;
  - `traces<idx>.json`, keyed by time slot and holding per-node latency lists;
  - `records<idx>.json`, whose faults carry `s`, `e` and `service`.

  It writes `../chunks/<name>/<idx>/{logs,metrics,traces}.pkl`. — [Eadro GitHub](https://github.com/BEbillionaireUSD/Eadro)
- [VERIFIED from code] Metric names are `cpu_usage_system, cpu_usage_total, cpu_usage_user, memory_usage, memory_working_set, rx_bytes, tx_bytes`. The SN node list has 12 services (nginx-web-server, compose-post-service, home-timeline-service, and others) with a hard-coded caller→callee `edge_info`. — [Eadro GitHub (codes/preprocess/util.py)](https://github.com/BEbillionaireUSD/Eadro)
- [VERIFIED] The FSE'26 preliminary study used Eadro-TT and Eadro-SN. — [arXiv 2510.04711v2](https://www.arxiv.org/pdf/2510.04711v2)
- [UNVERIFIED] The contents, size and licence of Zenodo 10.5281/zenodo.7615393. The record page returned HTTP 429 and the Zenodo API is disallowed by robots.txt for the fetch tool. — [Zenodo DOI](https://doi.org/10.5281/zenodo.7615393)


## Q4. FSE 2026 fault-propagation-aware benchmark (Fang et al., arXiv 2510.04711; Zenodo 19513398)

### Cited Findings
- [VERIFIED] Title: "Rethinking the Evaluation of Microservice RCA with a Fault Propagation-Aware Benchmark". Authors: Aoyang Fang, Songhan Zhang, Yifan Yang, Haotong Wu, Junjielong Xu, Xuyang Wang, Rui Wang, Manyi Wang, Qisheng Lu, Pinjia He (CUHK-Shenzhen). The abstract reports "1,430 validated failure cases from 9,152 fault injections, covering 25 fault types across 6 categories, dynamic workloads, and hierarchical ground-truth labels that map failures from services down to code-level causes". Mean Top@1 across 11 state-of-the-art models is 0.21. — [arXiv 2510.04711](https://arxiv.org/abs/2510.04711)
- [VERIFIED] Scale: Train-Ticket with 50 services; 188.1 h of collection; 154.7M log lines; 11.2M traces; 84% service coverage; maximum call depth 7; 78 unique metric types; trace-correlated logs; L4/L7 network telemetry. — [arXiv 2510.04711](https://arxiv.org/abs/2510.04711)
- [VERIFIED] Per case: "4 minutes of normal operation data followed by 4 minutes of failure data". There is a 4-minute warm-up and the environment is redeployed between cases. Traces use OpenTelemetry. Data are normalised into a unified schema stored in ClickHouse. Labels cover Service, Pod, Container, Metric, Span and Function levels. — [arXiv 2510.04711v2 PDF](https://www.arxiv.org/pdf/2510.04711v2)
- [VERIFIED] Initial 31 fault types, of which 25 were kept — [v2 PDF](https://www.arxiv.org/pdf/2510.04711v2):
  - Resource: PodKill, PodFailure, ContainerKill, MemoryStress, CPUStress.
  - Network: Delay, Loss, Duplicate, Corrupt, Bandwidth, Partition.
  - HTTP: request/response abort, delay and replace variants.
  - JVM: Latency, Return, Exception, GC, CPUStress, MemoryStress, MySQLLatency, MySQLException.
  - DNS: DNSError, DNSRandom.
  - Time: TimeSkew.
- [VERIFIED] Preliminary study on Eadro, Nezha, RCAEval (RE1–RE3) and AIOps-2021: "SimpleRCA's Top@1 accuracy is comparable to or surpasses SOTA methods on multiple datasets". — [v2 PDF](https://www.arxiv.org/pdf/2510.04711v2)
- [VERIFIED] v2 (23 Dec 2025) has no data URL, only "We promise that we will release all the code, baseline implementations, and datasets as open source." — [v2 PDF](https://www.arxiv.org/pdf/2510.04711v2)
- [VERIFIED] Zenodo 19513398, "Artifact for Rethinking the Evaluation of Microservice RCA with a Fault Propagation-Aware Benchmark" — [Zenodo 19513398](https://zenodo.org/records/19513398):
  - v4, 11 April 2026, Apache-2.0, described as supporting an FSE 2026 paper.
  - Single file `FSE_26_RCA_dataset_study_reviewer.tar.gz` (96.1 MB), containing "the paper PDF, documentation, a reduced benchmark, Docker reviewer scripts, and reproducible validation inputs".
  - Entry point `bash scripts/run_review.sh`; an "optional extended raw-data replay pathway" is documented.


## Q5. GAIA / MicroSS (CloudWise): does it fit?

### Cited Findings
- [VERIFIED] MicroSS "contains more than 6,500 metrics, 7,000,000 log items and detailed trace data continuously collected for two weeks", with a "record for all anomaly injections". Licence is Apache 2.0. — [GAIA README](https://github.com/CloudWise-OpenSource/GAIA-DataSet)
- [VERIFIED] Trace fields: `timestamp, host_ip, service_name, trace_id, span_id, parent_id, start_time, end_time, url, status_code, message`. Metric CSVs hold `timestamp` (13-digit ms) and `value`. The V1.10 update (2022-05-12) added August 2021 data but "omitted the trace data whose pattern is quite similar". — [GAIA README](https://github.com/CloudWise-OpenSource/GAIA-DataSet)
- [VERIFIED] Architecture: the front end calls webservice, which calls redisservice, mobservice and loginservice; loginservice calls dbservice, which calls MySQL; zookeeper is the registry. "Two container instances are deployed for each type of service… on different hosts". — [MicroSS system description.docx](https://github.com/CloudWise-OpenSource/GAIA-DataSet/tree/main/MicroSS)
- [VERIFIED] Storage: multi-part zips committed directly to git, as `business_split.z01–.z45+.zip`, `trace_split.z01–.z31+.zip`, `metric_split.*` parts (35 files, by subtraction from the 122-file tree) and `run/run.zip` (823,135 bytes). The split parts are not Git LFS: `.gitattributes` marks only `*.csv`, `Companion_Data.zip` and `MicroSS.zip`, and the blobs are real ZIP bytes. An example metric file inside is `metric/dbservice1_0.0.0.4_docker_cpu_core_5_norm_pct_2021-08-01_2021-08-31.csv`. — [GAIA repo](https://github.com/CloudWise-OpenSource/GAIA-DataSet); [.gitattributes](https://github.com/CloudWise-OpenSource/GAIA-DataSet/blob/main/.gitattributes)
- [VERIFIED: counted from `run_table_2021-07.csv` and `run_table_2021-08.csv`] Source: [run.zip](https://github.com/CloudWise-OpenSource/GAIA-DataSet/blob/main/MicroSS/run/run.zip)
  - 1,448 injection records: `[memory_anomalies]` 1,367 and `[cpu_anomalies]` 81.
  - Also 29 `[normal memory freed label]` lines and 30 `[Errno 111]` lines.
  - Spread over 10 instances: dbservice1 182, mobservice2 167, dbservice2 166, logservice1 143, webservice2 140, webservice1 134, mobservice1 134, logservice2 130, redisservice2 128, redisservice1 124.
  - Example record: "[memory_anomalies] trigger a high memory program, start at 2021-07-01 11:44:26.882752 and lasts 600 seconds and use 1g memory".
  - One CPU record says "lasts 1631517.6494772434 seconds" (about 19 days), which is a corrupt duration.


## Q6. OpenRCA / AIOps Challenge data (Telecom, Bank, Market): does any subset fit?

### Cited Findings
- [VERIFIED] From the OpenRCA paper — [OpenRCA paper (ICLR 2025)](https://netman.aiops.org/wp-content/uploads/2025/05/13411_OpenRCA_Can_Large_Langua.pdf):
  - Cases: Telecom 51, Bank 136, Market 148 (335 total). Size: "over 68 GB" (Telecom 17.6G, Bank 26.4G, Market 24.5G).
  - Modalities: Telecom has traces and metrics only; Bank and Market have log, trace and metric.
  - Metrics are at 1-minute frequency. Traces carry span IDs, parent IDs and timestamps.
  - Components: Telecom has 22 OS, 8 pods, 13 DBs and 12 Redis; Bank has 14 pods and 6 services; Market has 6 nodes, 40 pods and 10 services.
  - Labels: originating component, start time, failure reason.
  - Faults: CPU, memory, disk and network, plus JVM (Bank) and process termination (Market); examples include "network latency" and "packet loss".
  - Licence: CC BY-NC 4.0. Origin: the AIOps Challenge series.
- [VERIFIED] From the OpenRCA README — [OpenRCA README](https://github.com/microsoft/OpenRCA):
  - Telemetry is downloaded from a Google Drive folder.
  - Layout is `{SYSTEM}/{query.csv, record.csv, telemetry/{YYYY_MM_DD}/{log,metric,trace}}`, with Market split into cloudbed-1 and cloudbed-2.
  - Timestamps are UTC+8.
  - Recommended resources (for the agent): at least 80 GB storage and 32 GB memory.
  - FAQ: network faults "usually cannot be identified using KPIs alone. Consider examining the latency relationship between parent spans and child spans in traces".
  - Market pods are named like `node-5.adservice-2`.
- [VERIFIED: existence only] An "OpenRCA 2.0: From Outcome Labels to Causal Process Supervision" paper exists (arXiv 2606.27154); its content was not read. — [arXiv 2606.27154](https://arxiv.org/html/2606.27154v2)


## Q7. Smaller or weaker candidates (AnoMod, TrainTicketTrace, LEMMA-RCA, DejaVu, TraceRCA, MicroRCA) and other leads

### Cited Findings
- [VERIFIED] **AnoMod** (Zenodo 18342898) — [Zenodo 18342898](https://zenodo.org/records/18342898):
  - v1, 13 April 2026, CC-BY-4.0, single file `AnoMod.zip` (201.9 MB).
  - Systems: SocialNetwork and TrainTicket.
  - Four anomaly categories: performance, service, database and code level.
  - Five modalities: logs, Prometheus metrics, Jaeger/SkyWalking traces, API responses and code coverage.
  - Workloads generated with EvoMaster; injection adapted from ChaosMesh and ChaosBlade.
  - MSR'26 Data and Tool Showcase paper (DOI 10.1145/3793302.3793324).
- [VERIFIED] The AnoMod GitHub README says "Data has been relocated to Zenodo only". — [AnoMod GitHub](https://github.com/EvoTestOps/AnoMod)
- [VERIFIED, moderate confidence (tool summary of the arXiv HTML)] AnoMod details — [arXiv 2601.22881](https://arxiv.org/html/2601.22881v1):
  - **24 cases in total.** Each category has 3 types, for 12 types across 2 systems.
  - Performance-level types: CPU contention, network performance degradation, disk I/O stress.
  - SN has 21 services; TT has 41.
  - 33 metrics (TT) and 29 metrics (SN).
  - Per-case labels and window lengths are not stated.
- [VERIFIED: title only] Zenodo 17811972 is "Dataset for: TrainTicketTrace: A Multi-Fault Distributed Dataset for Microservice Fault Detection and Localization". The record page returned **HTTP 429** and was not retried. Search results loosely associate it with Stefan Fischer and the VST 2026 workshop (UNVERIFIED). — [Zenodo 17811972](https://zenodo.org/records/17811972)
- [VERIFIED] **LEMMA-RCA** "Cloud_Computing_Original" on Hugging Face — [HF README](https://huggingface.co/datasets/Lemma-RCA-NEC/Cloud_Computing_Original/blob/main/README.md):
  - Licence cc-by-nc-4.0, with a conflicting "cc-by-nd-4.0: NoDerivatives" note.
  - Modalities: "system metrics (json format) and log data (json format)"; traces are not mentioned.
  - Six fault types: "cryptojacking, silent pod degradation fault, malware attack, mistakes made by GitOps, configuration change failure, and bug infection".
  - Size class 100M–1B.
  - A Product Review subset also exists: [HF Product_Review_Preprocessed](https://huggingface.co/datasets/Lemma-RCA-NEC/Product_Review_Preprocessed); see also [project page](https://lemma-rca.github.io/).
- [VERIFIED] **DejaVu**: datasets A–D are on Dropbox and on Zenodo 10.5281/zenodo.6955909 ("including the raw data of the Train-Ticket dataset"). Each dataset has `graph.yml` or `graphs/*.yml` (FDGs), `metrics.csv` and `faults.csv` (ground truths). `FDG.pkl` pickles break across Python and Pandas versions. — [DejaVu README](https://github.com/NetManAIOps/DejaVu)
- [VERIFIED] **TraceRCA** (IWQoS 2021): data on OneDrive and Tsinghua Cloud; contents are not described in the README. — [TraceRCA README](https://github.com/NetManAIOps/TraceRCA)
- [VERIFIED] **MicroRCA** (NOMS 2020): "An example of the data is given in folder data". The method uses response times between communicating services plus container and host resource usage, not span traces. — [MicroRCA README](https://github.com/elastisys/MicroRCA)
- [VERIFIED: existence only, not assessed] Other leads, which a follow-up could screen:
  - "How Far Can Root Cause Analysis Go on Real-World Telemetry Data?" (arXiv 2607.13548; the fetch returned unreadable content) — [link](https://arxiv.org/html/2607.13548v1)
  - "Why Do AI Agents Systematically Fail at Cloud Root Cause Analysis?" — [arXiv 2602.09937](https://arxiv.org/html/2602.09937v2)
  - "Check Your Trace First…" (Zenodo 19335897) — [link](https://zenodo.org/records/19335897)
  - "train-ticket dataset for FAMOS" (Zenodo 13120167) — [link](https://zenodo.org/records/13120167)
  - LO2, whose title says logs and metrics only — [arXiv 2504.12067](https://arxiv.org/html/2504.12067v1)


## Q8. Assessment against the must-haves, and ranked top-3 with risks

### Cited Findings
- RE2-OB facts: [RCAEval README](https://github.com/phamquiluan/RCAEval), [RCAEval paper](https://arxiv.org/html/2412.17015v2), [main.py](https://github.com/phamquiluan/RCAEval/blob/main/main.py), [microrank.py](https://github.com/phamquiluan/RCAEval/blob/main/RCAEval/e2e/microrank.py)
- Nezha facts: [Nezha repo](https://github.com/IntelligentDDS/Nezha) and the files cited in Q2.
- OpenRCA facts: [OpenRCA paper](https://netman.aiops.org/wp-content/uploads/2025/05/13411_OpenRCA_Can_Large_Langua.pdf), [OpenRCA README](https://github.com/microsoft/OpenRCA)
- FSE'26 facts: [arXiv 2510.04711v2](https://www.arxiv.org/pdf/2510.04711v2), [Zenodo 19513398](https://zenodo.org/records/19513398)
- Eadro facts: [Eadro paper](https://arxiv.org/pdf/2302.05092), [Eadro GitHub](https://github.com/BEbillionaireUSD/Eadro)
- GAIA facts: [GAIA repo](https://github.com/CloudWise-OpenSource/GAIA-DataSet)
