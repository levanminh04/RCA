# K4 — Kiến thức nền: ba họ thuật toán cô nêu làm ví dụ (PageRank, đồ thị con, GNN)

> Trích nguyên văn từ ghi chú nghiên cứu ngày 01–02/10/2026 (`advisor_method_families.md`). Chỉ giữ các mục "Cited Findings" (dữ kiện có trích nguồn). Đã bỏ "Takeaway", "Inferences" (phần suy luận, dễ neo) và "Gaps". Câu hỏi ở mỗi mục là câu hỏi của đợt khảo sát cũ, giữ để định vị nội dung, không phải định hướng hiện hành.
>
> **Chưa kiểm lại.** Mỗi dữ kiện phải kiểm trên nguồn gốc trước khi dùng. Nhãn [VERIFIED] là của người viết ghi chú cũ, không phải của repo này.

## Q1. Across the three families, what is the "anomaly", which graph is used, what are the inputs and outputs, and does the graph DETECT anomalies or only RANK them?

### Cited Findings
**Shared vocabulary (general graph anomaly detection, GAD)**
- The deep-learning GAD survey defines the task as "identifying anomalous graph objects (i.e., nodes, edges and sub-graphs) in a single graph, or anomalous graphs in a database/set of graphs". This gives four anomaly units: node, edge, subgraph and whole graph. — [Ma et al., TKDE 2021, arXiv 2106.07178](https://arxiv.org/abs/2106.07178)

**PageRank / random-walk family: detection versus ranking**
- **MonitorRank (Kim et al., SIGMETRICS 2013; older).** Inputs are a call graph between "sensors" (services/APIs), latency, error-count and throughput time series, and a frontend metric that has *already* been flagged as anomalous, plus an approximate time range. The paper explicitly restricts its "focus to diagnosis after an anomaly has been reported, thereby distinguishing our work from the anomaly detection literature". The output is a ranked list of candidate root causes. — [MonitorRank paper PDF](https://netman.aiops.org/~peidan/ANM2018Fall/11.CausalInference/LectureCoverage/2013SIGMETRICS13_Root%20Cause%20Detection%20in%20a%20Service-Oriented%20Architecture.pdf)
- **MicroRCA (Wu et al., NOMS 2020; older).**
  - It needs "response times between two communicating services" and container/host resource usage. — [MicroRCA README](https://github.com/elastisys/MicroRCA)
  - In the reference code, detection is local: BIRCH clustering on smoothed, normalized response-time series (rolling mean, window 12; `Birch(branching_factor=50, n_clusters=None, threshold=...)`), and a series that produces more than one cluster is flagged anomalous.
  - The graph is used afterwards: an attributed graph of services and hosts is built, an "anomalous subgraph" is extracted, and personalized PageRank ranks services. — [MicroRCA.py](https://raw.githubusercontent.com/elastisys/MicroRCA/master/MicroRCA.py)
- **MicroRank (Yu et al., WWW 2021; older).** It "extracts service latency from tracing data then conducts the anomaly detection procedure". Traces are judged against expected per-operation latency, and `trace_list_partition` divides them into normal and abnormal traces. Only then does it combine "PageRank and spectrum analysis" to rank service instances. — [MicroRank README](https://github.com/IntelligentDDS/MicroRank)
- **Causal-graph random walks.** CloudRanger (2018), MS-Rank (2019), AutoMAP (2020), MicroCause (2020), CAR (2022), CORAL (2023) and REASON (2023) are all classified as "random walk on causality graph", where the graph is *learned* from metrics (for example with the PC algorithm). MonitorRank is classed as a "specially designed random walk" on a dependency graph, TraceRank as a "PageRank-inspired algorithm on service dependency graphs", and MicroRCA as a "random walk on topology graphs" built from trace requests. — [Wang & Qi 2024 survey, arXiv 2408.00803](https://arxiv.org/html/2408.00803v1)
- **AnomRank (Yoon, Hooi, Shin, Faloutsos, KDD 2019; general dynamic graphs, not microservices).**
  - The graph-derived scores *are* the detection signal. It computes two PageRank-variant node scores: ScoreS on the unweighted adjacency and ScoreW on the weighted adjacency.
  - The anomaly signal is the first and second derivatives of these scores across graph snapshots: "AnomRankS is an (n × 2) matrix [p′s p″s]".
  - It is unsupervised and outputs a graph-level anomaly score per snapshot. It localizes "culprits of anomalies by ranking AnomRank scores of each node". — [AnomRank, arXiv 2011.13085](https://arxiv.org/pdf/2011.13085)

**Subgraph family: detection versus scoping**
- **MicroRCA's anomalous subgraph.** It contains the nodes flagged anomalous plus all their incoming and outgoing edges. Anomalous edges get a fixed weight α = 0.55; other edges are weighted by the Pearson correlation of response times. — [MicroRCA.py](https://raw.githubusercontent.com/elastisys/MicroRCA/master/MicroRCA.py)
- **MicroHECL (Liu et al., ICSE 2021, Alibaba).**
  - The anomaly unit is the service-call *edge*. Each anomaly type has its own local detector: OC-SVM on response time, Random Forest on error counts, and the 3-sigma rule on QPS.
  - The graph is a dynamically built service call graph covering about the last 30 minutes. It is used to grow and prune an "anomaly propagation chain".
  - The output is a set of ranked candidate root causes. — [MicroHECL PDF](https://netman.aiops.org/~peidan/ANM2023/11.CausalInference/ICSE-2021-MicroHECL.pdf)
- **Graph-pattern RCA (Brandón et al., JSS preprint 2019).** Detection is explicitly external: "we assume the existence of this submodule, as we focus on the problem of finding a root cause for the detected anomaly and not the detection of the anomaly per se". A configurable function extracts an "anomalous region" (typically the k-hop neighbours of anomalous nodes), which is then matched against a library of labeled anomalous patterns. — [Brandón et al. PDF](https://www.datsi.fi.upm.es/~mperez/pub/jss-2019.pdf)
- **Graph-level (whole-trace) detection.** DeepTraLog flags anomalous *traces*: one anomaly score per request graph, computed as the distance to a learned hypersphere. — [DeepTraLog, ICSE 2022 PDF](https://cspengxin.github.io/publications/icse22-DeepTraLog.pdf)
- **Other trace-graph detectors, from the survey.** TraceVAE (2023) is a "dual-variable graph variational autoencoder" targeting structural and time-consumption anomalies. CRISP (2022) uses critical-path analysis and "detects anomalies via dependency graphs". — [Wang & Qi 2024 survey](https://arxiv.org/html/2408.00803v1)

**GNN family: the graph participates in detection**
- **GDN (Deng & Hooi, AAAI 2021; multivariate sensor time series, not microservices).**
  - It learns a directed graph between variables (top-k cosine similarity of learned embeddings) and forecasts each variable with graph attention.
  - It flags a time step as anomalous when the maximum robust-normalized forecast error exceeds a threshold. The variable with the largest deviation gives the attribution. — [GDN, arXiv 2106.06947](https://arxiv.org/pdf/2106.06947)
- **Eadro (Lee et al., 2023; venue ICSE 2023 not echoed on the fetched page, so UNVERIFIED).**
  - Two outputs: a binary anomaly label per time window ("0 (normal) or 1 (abnormal)") and a culprit probability for each microservice.
  - The dependency graph is extracted from historical traces ("nodes and invocations as directional edges") and processed by a Graph Attention Network inside the detector. — [Eadro, arXiv 2302.05092](https://arxiv.org/pdf/2302.05092)
- **ART (Sun et al., ASE 2024).**
  - The graph is a directed instance graph in which an edge "represents an actual call or deployment", built from spans and deployment data. GraphSAGE runs over it, together with a Transformer for channel dependencies and a GRU for time.
  - System-level deviations drive anomaly detection, using an Extreme Value Theory threshold. Instance-level deviations drive root-cause localization, via cosine similarity to the system-level deviation. — [ART paper PDF](https://nkcs.iops.ai/wp-content/uploads/2024/09/ART24_to_ASE.pdf); venue: [ASE 2024 program](https://conf.researchr.org/details/ase-2024/ase-2024-research/95/ART-A-Unified-Unsupervised-Framework-for-Incident-Management-in-Microservice-Systems)
- **MSTGAD.** It builds a "microservice system twin" graph in which nodes are service instances and edges are scheduling relationships. A transformer with spatial and temporal attention runs over metrics, logs and traces for real-time anomaly detection, trained semi-supervised. — [MSTGAD, arXiv 2310.04701](https://arxiv.org/abs/2310.04701)
- **DiagFusion.** It "combines deployment data and traces to build a dependency graph, and uses a graph neural network to localize the root cause instance and determine the failure type". This is diagnosis after a failure is known, not detection. — [DiagFusion, arXiv 2302.10512](https://arxiv.org/abs/2302.10512)


## Q2. PageRank family: how do MicroRCA, MicroRank, MonitorRank, CloudRanger and TraceRank use personalized PageRank / random walk? Does any method use a PageRank or centrality SHIFT as the anomaly signal? Datasets, results and failure modes?

### Cited Findings
**MonitorRank (Kim et al., SIGMETRICS 2013; older; LinkedIn)**
- **Mechanics.**
  - Personalized PageRank in which each edge's strength is the "pattern similarity score", defined as "the correlation of two given metrics on a time window of fixed length" between a neighbour's metric and the anomalous frontend metric.
  - Self-edges have strength "the similarity score Si subtracted by the maximum similarity score of child nodes".
  - For each call edge vi→vj, a backward edge vj→vi is added with strength "ρSi for some constant ρ ∈ [0, 1)".
  - The teleport (restart) vector is built from the similarity scores, and the frontend node itself has zero restart probability. — [MonitorRank PDF](https://netman.aiops.org/~peidan/ANM2018Fall/11.CausalInference/LectureCoverage/2013SIGMETRICS13_Root%20Cause%20Detection%20in%20a%20Service-Oriented%20Architecture.pdf)
- **Pseudo-anomaly clustering.** An offline step finds historical "pseudo-anomalies" with a heuristic based on "the ratio of current metric value and the maximum value in the previous time window". It then groups sensors with correlated patterns (an L1-regularized convex problem) to capture external factors, such as co-location, that the call graph does not show. At diagnosis time the best-matching cluster's sensors get a score boost before the random walk. — [MonitorRank PDF](https://netman.aiops.org/~peidan/ANM2018Fall/11.CausalInference/LectureCoverage/2013SIGMETRICS13_Root%20Cause%20Detection%20in%20a%20Service-Oriented%20Architecture.pdf)
- **Evaluation.**
  - Data: 131 labeled production anomalies over 3 months (25 latency, 71 error-count, 35 throughput). Metrics: PR@1/3/5 and MAP.
  - Reported gain: a "26% to 51% improvement in mean average precision" over baselines, which included TBAC and heuristics.
  - As extracted from the PDF: PR@1 of 1.000 for latency, 0.901 for error count and 1.000 for throughput. — [MonitorRank PDF](https://netman.aiops.org/~peidan/ANM2018Fall/11.CausalInference/LectureCoverage/2013SIGMETRICS13_Root%20Cause%20Detection%20in%20a%20Service-Oriented%20Architecture.pdf)

**MicroRCA (Wu, Tordsson, Elmroth, Kao, NOMS 2020; older). Details verified from the authors' code.**
- **Graph construction.** Database and message-queue nodes are filtered out. Nodes whose name contains "kubernetes" are typed as hosts.
- **Anomalous subgraph and edge weights.** The subgraph keeps the in- and out-edges of anomalous nodes. Anomalous edges get weight `alpha` (0.55); other edges get `baseline_df[v].corr(latency_df[normal_edge])`.
- **Personalization.** `personalization = edges_weight_avg * max_corr`, where `max_corr` is the largest absolute correlation between the service's latency and its container CPU, network and memory metrics.
- **Ranking.** The graph is **reversed** (`anomaly_graph.reverse(copy=True)`) and then ranked with `nx.pagerank(anomaly_graph, alpha=0.85, personalization=personalization, max_iter=10000)`. — [MicroRCA.py](https://raw.githubusercontent.com/elastisys/MicroRCA/master/MicroRCA.py)
- **Test system.** The repository ships a `sock-shop-deployment.yml`, so Sock Shop is the testbed; the tunable parameters are `alpha` and `ad_threshold`. — [MicroRCA README](https://github.com/elastisys/MicroRCA)

**MicroRank (Yu, Chen et al., WWW 2021; older; trace-based).** The pipeline is:
1. Latency-based anomaly detection on traces.
2. Partition into normal and abnormal traces (`trace_list_partition`).
3. Combine PageRank with "spectrum analysis" (function `calculate_spectrum_without_delay_list`).
4. Rank service instances.

— [MicroRank README](https://github.com/IntelligentDDS/MicroRank)

**TraceRank (Yu et al., 2023), CloudRanger (Wang et al., 2018), MicroCause (Meng et al., 2020), GROOT (Wang et al., 2021)**
- TraceRank is a "PageRank-inspired algorithm on service dependency graphs". CloudRanger, MS-Rank, AutoMAP and MicroCause do a "random walk on causality graph" built with the PC algorithm (MicroCause additionally captures temporal relationships). GROOT applies a "variant PageRank on causality graphs from tracing and log analysis". — [Wang & Qi 2024 survey](https://arxiv.org/html/2408.00803v1)
- TraceRank's full title is "Abnormal service localization with dis-aggregated end-to-end tracing data in cloud native systems". — [ResearchGate record](https://www.researchgate.net/publication/356855394_TraceRank_Abnormal_service_localization_with_dis-aggregated_end-to-end_tracing_data_in_cloud_native_systems)

**Newest random-walk work: eIRWR (Khan & Farea, arXiv 2608.08073, Aug 2026; newer; preprint)**
- **Stated problem.** Existing anomaly-restart walks "restart from the raw anomaly vector, which is dominated by loud downstream victims rather than the quieter source".
- **Damping finding.** "Resilience damping" applied to the transition matrix is "mathematically equivalent to raising the restart probability", so the authors compare against a restart-tuned PPR.
- **Method.** "Power-law teleportation sharpening", plus self-loops and backward edges "so that probability accumulates at cascade sources", plus an outer refinement loop. — [eIRWR](https://arxiv.org/html/2608.08073)
- **Stated limitations of standard walks:**
  - "the walker can disperse probability toward irrelevant regions of the graph, especially when the root cause has low visibility in the anomaly vector";
  - the standard walk "does not model the direction of fault cascades (backward, from callees to callers)";
  - "downstream victims … frequently exhibit louder symptoms than the source itself". — [eIRWR](https://arxiv.org/html/2608.08073)
- **Evaluation.**
  - Data: three Alibaba trace-dataset topologies with 12K–25K nodes.
  - Results: MRR 0.75 at moderate root-cause "visibility", 2.8× the best aggregate-metric baseline (whose MRR was 0.27); MRR 0.94 at high visibility; under 25 ms on 17K nodes.
  - Baselines: MicroRCA (PPR), CloudRanger, MonitorRank, In-Degree Centrality, MicroHECL, TraceDiag and others. MicroRank and TraceRank were excluded as "trace-level". — [eIRWR](https://arxiv.org/html/2608.08073)

**PageRank or centrality SHIFT as the anomaly signal**
- **AnomRank (KDD 2019; general dynamic graphs).**
  - Anomaly types: "AnomalyS" (a node redirects out-edges to new neighbours, i.e. a structure change) and "AnomalyW" (a node adds or removes out-edges to an existing neighbour, i.e. an edge-weight change).
  - Signal: first derivatives catch the size of a change; second derivatives catch abrupt trend shifts.
  - Threshold: mean + 0.5σ in the experiments. Cost is linear in the number of edges ("processes 1M edges within 1 second"), and the paper claims to be "up to 49.5× faster or 35% more accurate" than prior methods.
  - Datasets: DARPA (4.5M IP communications, 1,463 snapshots, 288 labeled attacks), ENRON, and a synthetic set. About 0.85 precision@100 on DARPA, as extracted from Fig. 1. — [AnomRank, arXiv 2011.13085](https://arxiv.org/pdf/2011.13085)
  - Code: [github.com/minjiyoon/KDD19-AnomRank](https://github.com/minjiyoon/KDD19-AnomRank). The paper text gives github.com/minjiyoon/anomrank — [AnomRank](https://arxiv.org/pdf/2011.13085)

**Benchmarks on Train Ticket**
- **ASE 2024 study (Pham, Ha, Zhang).**
  - Scope: 21 RCA methods, including 12 "causal discovery + scoring" variants: {PC, FCI, Granger, ICALiNGAM, fGES, NTLR} × {PageRank, random walk}.
  - Train Ticket here has 64 services and 212 metrics. Avg@5 results: BARO 0.90, NSigma 0.70, CIRCA 0.57, RCD 0.12. The PC/FCI/Granger PageRank variants scored 0.07–0.15, against a random "Dummy" at 0.07, i.e. "no better or only slightly better than random selection".
  - Setting: these are the paper's tΔ=0 setting on metric data. My reading is that tΔ=0 means the failure time is supplied without offset. — [arXiv 2408.13729](https://arxiv.org/pdf/2408.13729)
- **Runtime and stated finding (same study).** NSigma and BARO take about 0.01 s; PC/FCI 129–155 s on Train Ticket; CausalRCA 1,326 s; RUN exceeded the 2-hour timeout. Finding: "All common causal discovery methods have difficulties in dealing with large graphs and estimating edge directions". — [arXiv 2408.13729](https://arxiv.org/pdf/2408.13729)
- **RCAEval.** MicroRank is one of RCAEval's trace-based baselines. The paper notes that BARO "shows limitations when dealing with network faults". — [RCAEval paper, arXiv 2412.17015](https://arxiv.org/pdf/2412.17015)
- **RCAEval README example.** Reported Avg@5 for BARO on RE2-TT by fault type: CPU 0.72, MEM 0.99, DISK 1.0, SOCKET 0.83, DELAY 0.63, LOSS 0.64. — [RCAEval README](https://github.com/phamquiluan/RCAEval)

**Failure modes named in surveys**
- Random-walk RCA depends on graph quality: "Ambiguous correspondences between upstream and downstream calls may exist", which produces "unexpected edges" and "misjudgments". In addition, "determining the directionality and strength of relationships in the constructed graph requires careful consideration and validation". — [Wang & Qi 2024 survey](https://arxiv.org/html/2408.00803v1)


## Q3. Subgraph family: which methods extract an anomalous subgraph or affected region, how is it formed (thresholds, connectivity), and how is it evaluated?

### Cited Findings
**Definition.** GAD distinguishes anomalous nodes, edges and sub-graphs in one graph from anomalous whole graphs in a set of graphs. — [Ma et al., TKDE 2021](https://arxiv.org/abs/2106.07178)

**MicroRCA (NOMS 2020).** `anomaly_subgraph()` keeps the nodes flagged anomalous by BIRCH and all their in- and out-edges, with a fixed weight α = 0.55 on anomalous edges and correlation weights on the others. The PPR ranking then runs only on this subgraph. — [MicroRCA.py](https://raw.githubusercontent.com/elastisys/MicroRCA/master/MicroRCA.py)

**MicroHECL (Liu, He, Peng et al., ICSE 2021; Fudan University + Alibaba)**
- **Windows.** The service call graph is built from "a latest time window (e.g., the last 30 minutes)", metrics cover "the last 60 minutes", and the detection window is "the last 10 minutes". — [MicroHECL PDF](https://netman.aiops.org/~peidan/ANM2023/11.CausalInference/ICSE-2021-MicroHECL.pdf)
- **Detectors per anomaly type.**
  - Performance: OC-SVM on response time, using four feature kinds (over-max, max-delta, over-average, average-ratio).
  - Reliability: Random Forest on error-count features.
  - Traffic: the 3-sigma rule on QPS, plus a correlation check against business metrics. — [MicroHECL PDF](https://netman.aiops.org/~peidan/ANM2023/11.CausalInference/ICSE-2021-MicroHECL.pdf)
- **Subgraph formation.** Starting from the initial anomalous service, the chain is "iteratively extend[ed] … by backtracking along the anomaly propagation direction" (upstream or downstream, depending on the anomaly type). Pruning: "If the correlation coefficient is lower than a threshold (e.g., 0.7), the current edge will be pruned." Candidates are ranked by Pearson correlation of change trends with the initial anomaly. — [MicroHECL PDF](https://netman.aiops.org/~peidan/ANM2023/11.CausalInference/ICSE-2021-MicroHECL.pdf)
- **Evaluation.**
  - Data: 75 availability issues from 28 subsystems, about 265 services each on average.
  - Results (MicroHECL vs MonitorRank vs Microscope): HR@1 0.48 vs 0.32 vs 0.35; HR@3 0.67 vs 0.40 vs 0.49; HR@5 0.72 vs 0.43 vs 0.59; MRR 0.58 vs 0.37 vs 0.44.
  - In production: "more than 5 months", "more than 600 availability issues", a "top-3 hit ratio of 68%", and localization time reduced "from 30 minutes to 5 minutes". — [MicroHECL PDF](https://netman.aiops.org/~peidan/ANM2023/11.CausalInference/ICSE-2021-MicroHECL.pdf)

**Graph-pattern matching of anomalous regions (Brandón, Solé, Huélamo, Solans, Pérez, Muntés-Mulero; JSS preprint, Oct 2019)**
- **Representation.** The system is a multi-attributed directed graph: containers, hosts and external clients as nodes; network connections as edges. Attributes are numerical, categorical or ontological. — [Brandón et al.](https://www.datsi.fi.upm.es/~mperez/pub/jss-2019.pdf)
- **Region extraction.** A configurable function such as k-hop neighbours, whose goal is "to limit the number of nodes and edges that are going to be included in the similarity calculation".
- **Matching.** Inexact graph matching solved by hill climbing, with similarity defined per attribute type, against "a pattern … that has already been revised and labeled by an expert". A match is declared at a similarity threshold of about 0.8–0.9. — [Brandón et al.](https://www.datsi.fi.upm.es/~mperez/pub/jss-2019.pdf)
- **Evaluation.**
  - Setup: Grid'5000 scenarios (HAProxy + WordPress + MySQL; Kafka; Spark + HDFS), each under 45 nodes, with faults including CPU, disk, bandwidth, memory, misconfiguration and endpoint flooding.
  - Results: 83.89% precision versus 70.25% for a boosted-tree baseline; 237 patterns from 832 anomalous regions; 0.64 s to compare two 30-node graphs.
  - Limitations: a cold-start pattern library, manual weight tuning, and the method "is maybe too complex for any anomaly in which the symptoms are isolated". — [Brandón et al.](https://www.datsi.fi.upm.es/~mperez/pub/jss-2019.pdf)

**Trace-based narrowing and frequent-pattern methods**
- TraceRCA (2021) uses "frequent pattern mining" to narrow the search space and ranks "less-normal traces". — [Wang & Qi 2024 survey](https://arxiv.org/html/2408.00803v1)
- TraceRCA is one of RCAEval's runnable trace-based baselines. — [RCAEval README](https://github.com/phamquiluan/RCAEval)
- FacGraph, "Frequent Anomaly Correlation Graph Mining for Root Cause Diagnose in Micro-Service Architecture", is an older frequent-subgraph approach; I have the title only. — [ResearchGate record](https://www.researchgate.net/publication/333076934_FacGraph_Frequent_Anomaly_Correlation_Graph_Mining_for_Root_Cause_Diagnose_in_Micro-Service_Architecture)

**Graph-level (per-trace) anomaly detection: the closest analogue to "subgraph" detection**
- **DeepTraLog (ICSE 2022).**
  - Graph: a Trace Event Graph whose nodes are span events and log events, and whose edges are sequence, synchronous request/response and asynchronous request. Node features are TF-IDF-weighted GloVe embeddings (300 dimensions).
  - Model: GGNN + Deep SVDD. Each trace's anomaly score is its distance to a hypersphere, and the radius is set from a training-distance percentile. — [DeepTraLog PDF](https://cspengxin.github.io/publications/icse22-DeepTraLog.pdf)
- **Other trace-graph detectors.** TraceVAE: a dual-variable graph VAE for "structural and time-consumption anomalies". CRISP: critical-path analysis. Sage: a "graphical variational autoencoder with Causal Bayesian Networks and counterfactuals". — [Wang & Qi 2024 survey](https://arxiv.org/html/2408.00803v1)


## Q4. GNN family (GDN, GTA, MTAD-GAT, DeepTraLog, TraceAnomaly-style, Eadro, MSTGAD, ART, DiagFusion, 2023–2026 works): training data, supervision, compute, code, and reproducibility on RE2-TT by a small team without ML experience

### Cited Findings
**GDN (Deng & Hooi, AAAI 2021; general multivariate time series, older)**
- **Graph learning.** Each variable has an embedding $v_i$; candidate edges are scored by cosine similarity and the top-k are kept as directed edges. Forecasting uses graph attention over a sliding window w.
- **Scoring.** $Err_i(t) = |s_i(t) − ŝ_i(t)|$ is normalized with each variable's "median and inter-quartile range (IQR)". The anomaly score is $A(t) = \max_i a_i(t)$, smoothed with a simple moving average; the threshold is the "max of A_s(t) over the validation data". — [GDN, arXiv 2106.06947](https://arxiv.org/pdf/2106.06947)
- **Training.** "The training data is assumed to consist of only normal data". Settings: w = 5; embedding size 64 (SWaT) and 128 (WADI); k = 15 and 30; up to 50 epochs with early stopping (patience 10); Adam with learning rate 1e-3.
- **Data and results.** Training samples: SWaT ≈ 47.5K (51 variables), WADI ≈ 119K (127 variables). F1: SWaT 0.81 (MAD-GAN 0.77), WADI 0.57 (MAD-GAN 0.37). Code: [github.com/d-ailin/GDN](https://github.com/d-ailin/GDN) — [GDN](https://arxiv.org/pdf/2106.06947)

**DeepTraLog (Zhang, Peng et al., ICSE 2022; trace + log, unsupervised)**
- **Training assumption.** It "just requires that the majority of traces in the training set are produced in normal execution". — [DeepTraLog PDF](https://cspengxin.github.io/publications/icse22-DeepTraLog.pdf)
- **Data.**
  - TrainTicket v0.2.0 with 14 fault types in 4 categories and 73 faults.
  - 132,485 traces in total, 23,334 (17.6%) of them anomalous.
  - Split: 60% of normal traces for training, 10% of normal traces for validation, and the remaining normal traces plus all anomalous traces for testing. — [DeepTraLog PDF](https://cspengxin.github.io/publications/icse22-DeepTraLog.pdf)
- **Results (precision / recall / F1).**
  - DeepTraLog 0.930 / 0.978 / 0.954.
  - GRU-based Deep SVDD 0.864 / 0.776 / 0.818.
  - MultimodalTrace 0.591 / 0.776 / 0.671.
  - TraceAnomaly 0.742 / 0.205 / 0.321. — [DeepTraLog PDF](https://cspengxin.github.io/publications/icse22-DeepTraLog.pdf)
- **Compute.** 67.1 min of training on 65,490 traces; 77 s to test 56,080 traces; about 4 ms per trace of 800–900 events. Hardware: i9-10900X, RTX 3090 (24 GB), 128 GB RAM.
- **Replication package.** [fudanselab.github.io/DeepTraLog](https://fudanselab.github.io/DeepTraLog/) — [DeepTraLog PDF](https://cspengxin.github.io/publications/icse22-DeepTraLog.pdf)

**Eadro (Lee et al., 2023; supervised, multimodal)**
- **Model.** Logs (Drain templates modeled by Hawkes processes), KPIs and trace latency are encoded per modality (dilated causal convolution + self-attention) and fused with a GLU. A GAT runs over the trace-derived dependency graph. Detection is trained with binary cross-entropy and localization with cross-entropy, jointly. — [Eadro, arXiv 2302.05092](https://arxiv.org/pdf/2302.05092)
- **Data and labels.** The authors collected their own data:
  - TrainTicket: 162 fault injections over 7 hours;
  - SocialNetwork: 72 injections over 1.2 hours;
  - 3 fault types (CPU exhaustion, network jam, packet loss);
  - a 60/40 train/test split;
  - 48,296 (TT) and 126,384 (SN) traces. — [Eadro](https://arxiv.org/pdf/2302.05092)
- **Results.** Detection F1 0.989 (TT) and 0.986 (SN). Localization HR@1 0.990 (TT) and 0.974 (SN). The paper claims "290%~5068% higher in HR@1 than five advanced baselines", which included MonitorRank and CloudRanger.
- **Compute and code.** One GTX 1080 GPU; code at [github.com/BEbillionaireUSD/Eadro](https://github.com/BEbillionaireUSD/Eadro). — [Eadro](https://arxiv.org/pdf/2302.05092)

**MSTGAD (twin-graph anomaly detection; venue ASE 2023 from memory, UNVERIFIED)**
- Semi-supervised. Builds a "microservice system twin" graph (service instances as nodes, scheduling relationships as edges) and runs a "transformer-based neural network with both spatial and temporal attention mechanisms" over metrics, logs and traces.
- Code: [github.com/alipay/microservice_system_twin_graph_based_anomaly_detection](https://github.com/alipay/microservice_system_twin_graph_based_anomaly_detection) — [arXiv 2310.04701](https://arxiv.org/abs/2310.04701)

**DiagFusion (Zhang, Jin, … Pei; arXiv Feb 2023; IEEE TSC venue UNVERIFIED)**
- **Method.** It "leverages embedding techniques and data augmentation to represent the multimodal data of service instances, combines deployment data and traces to build a dependency graph, and uses a graph neural network to localize the root cause instance and determine the failure type".
- **Reported gains.** Root-cause instance localization improves by 20.9%–368%; failure-type determination by 11.0%–169%. — [DiagFusion, arXiv 2302.10512](https://arxiv.org/abs/2302.10512)

**ART (Sun et al., ASE 2024; unsupervised; newer)**
- **Training and labels.** Trained without labels on "normal hours" of multimodal data, by predicting the next system snapshot with MSE loss. Labels are needed only to map unsupervised failure-type clusters to type names. Anomaly detection uses an EVT threshold; root-cause localization uses cosine similarity between each instance's deviation and the system-level deviation. — [ART PDF](https://nkcs.iops.ai/wp-content/uploads/2024/09/ART24_to_ASE.pdf)
- **Data and results.**
  - D1: a simulated e-commerce system (46 instances, 210 failures, 3,714 normal periods). D2: a bank system (18 instances, 133 failures, 12,297 normal periods).
  - Detection F1: 0.942 on D1 (Hades: 0.865) and 0.917 on D2 (Eadro: 0.842).
  - Localization Top-1: 0.667 on D1 and 0.722 on D2.
  - Baselines: Eadro, DejaVu, DiagFusion, Hades, MicroCBR, PDiagnose. — [ART PDF](https://nkcs.iops.ai/wp-content/uploads/2024/09/ART24_to_ASE.pdf)
- **Compute and code.** Training takes 460 s (D1) and 1,086 s (D2); online diagnosis takes 0.87–1.36 s per case. Hardware: "12 × Intel(R) Xeon(R) CPU E5-2650 v4 … and 128G RAM (without GPUs)". Code: [github.com/bbyldebb/ART](https://github.com/bbyldebb/ART) — [ART PDF](https://nkcs.iops.ai/wp-content/uploads/2024/09/ART24_to_ASE.pdf)

**Other GNN and trace methods, from the survey**
- Sleuth (Gan et al.) uses a "graph neural network (GNN)" to capture the causal impact of each span in traces. REASON uses "hierarchical graph neural networks". TraceAnomaly (2020) is a *VAE*, not a GNN, and sets intervals with the three-sigma rule. — [Wang & Qi 2024 survey](https://arxiv.org/html/2408.00803v1)
- Sleuth's full title is "Sleuth: A Trace-Based Root Cause Analysis System for Large-Scale Microservices with Graph Neural Networks" (ACM DOI 10.1145/3623278.3624758). — [ACM DL](https://dl.acm.org/doi/10.1145/3623278.3624758)

**2025–2026 GNN works found by search (titles and venues only; mechanics UNVERIFIED)**
- "Hypergraph Neural Network-based Multi-Granular Root Cause Localization for Microservice Systems" (ASE 2025). — [ASE 2025 program](https://conf.researchr.org/details/ase-2025/ase-2025-papers/161/Hypergraph-Neural-Network-based-Multi-Granular-Root-Cause-Localization-for-Microservi)
- "Troubleshooting Microservices with Heterogeneous Graph Neural Network" (Springer, 2025). — [Springer](https://link.springer.com/chapter/10.1007/978-3-031-97207-2_30)
- "Graph Neural AI with Temporal Dynamics for Comprehensive Anomaly Detection in Microservices" (arXiv 2511.03285). — [listing](https://awesomepapers.io/graph-learning/papers/2511.03285)
- "GALR: Graph-Based Root Cause Localization and LLM-Assisted Recovery for Microservice Systems" (MDPI Electronics 15(1):243). — [MDPI](https://www.mdpi.com/2079-9292/15/1/243)

**What RCAEval provides**
- The 15 RCAEval baselines are:
  - metric-based: BARO, CausalRCA, CIRCA, RCD, MicroCause, EasyRCA, MSCRED, ε-Diagnosis, RUN;
  - trace-based: TraceRCA, MicroRank;
  - multi-source: PDiagnose and multi-source BARO / RCD / CIRCA. — [RCAEval paper](https://arxiv.org/pdf/2412.17015)
- The README classes PDiagnose as trace-based and adds two FSE 2026 multi-source methods: TORAI (arXiv 2604.13522) and EventADL (arXiv 2605.00936). — [RCAEval README](https://github.com/phamquiluan/RCAEval)
- Stated requirements: "at least 8 cores, 16GB RAM, and ~50GB available disk space", Ubuntu 20.04/22.04, Python 3.12. — [RCAEval README](https://github.com/phamquiluan/RCAEval)


## Q5. What do 2023–2026 surveys and benchmark studies say about these families and their trade-offs?

### Cited Findings
**Wang & Qi 2024 survey (Southeast University; arXiv 2408.00803)**
- **Taxonomy.** By data: metrics, traces, logs and multi-modal. By technique, separate classes for "Random walk/PageRank algorithms", "Causal discovery (PC algorithm, Granger causality)", "Deep learning (autoencoders, LSTMs, GNNs)", "Spectrum analysis" and others. — [Wang & Qi 2024](https://arxiv.org/html/2408.00803v1)
- **Weakness of random-walk methods.** Graph quality ("unexpected edges", "misjudgments") and the need to validate edge direction and strength. — [Wang & Qi 2024](https://arxiv.org/html/2408.00803v1)
- **Open challenges.** "Keeping the relational graph up-to-date with dynamic evolving system architectures … is challenging". It calls for tools "capable of verifying the dependability of constructed relational graphs, minimizing spurious correlations" and for explainability. — [Wang & Qi 2024](https://arxiv.org/html/2408.00803v1)
- **On LLM-based RCA.** It warns of "low accuracy due to the intrinsic difficulty of the task, a propensity for LLM-based approaches to hallucinate". This is relevant to the advisor's step (5), LLM explanation. — [Wang & Qi 2024](https://arxiv.org/html/2408.00803v1)

**ASE 2024 "How far are we?" (Pham, Ha, Zhang)**
- "No method stands out in all situations; each method tends to either fall short in effectiveness, efficiency, or shows sensitivity to specific parameters". In addition, "performance … on synthetic datasets may not accurately reflect their performance in real systems". — [arXiv 2408.13729](https://arxiv.org/abs/2408.13729)
- "Long input data lengths could significantly improve the performance of causal discovery and RCA methods". On Online Boutique, RCD rose from 0.13 to 0.79 Avg@5 when input grew from 60 to 600 points. — [arXiv 2408.13729](https://arxiv.org/pdf/2408.13729)

**RCAEval (Pham et al., WWW 2025)**
- "There is still ample room for further improvement. Existing methods mostly obtain moderate results". — [RCAEval paper](https://arxiv.org/pdf/2412.17015)
- **RE2.** Three systems; 270 cases (90 per system); six fault types across five services, with three repetitions each. Per system: 77–376 metrics, 8.6–26.9 million log lines, 39.6–76.7 million traces. Traces "are collected using Jaeger and sent to Elasticsearch". Train Ticket is described as 64 services. — [RCAEval paper](https://arxiv.org/pdf/2412.17015); [RCAEval v1 HTML](https://arxiv.org/html/2412.17015v1)
- **Metrics.** AC@k, "the probability the top k results … include the true root causes", and Avg@k, the mean of AC@1 through AC@k. — [RCAEval paper](https://arxiv.org/pdf/2412.17015)

**GAD surveys**
- The deep GAD survey (Ma, Wu, Xue, Yang, Zhou, Sheng, Xiong, Akoglu; TKDE 2021) distinguishes anomalous nodes, edges and sub-graphs within a graph from anomalous graphs within a set of graphs. — [arXiv 2106.07178](https://arxiv.org/abs/2106.07178)

**Other surveys located (titles only; content not read)**
- Soldani & Brogi, "Anomaly Detection and Failure Root Cause Analysis in (Micro)Service-Based Cloud Applications: A Survey" (ACM CSUR). — [ACM DL](https://dl.acm.org/doi/full/10.1145/3501297)
- "Intelligent Root Cause Localization in MicroService Systems: A Survey and New Perspectives" (ACM, DOI 10.1145/3736755). — [ACM DL](https://dl.acm.org/doi/full/10.1145/3736755)
- "Anomaly detection and root-cause identification in microservices: a survey" (Cluster Computing, 2026). — [Springer](https://link.springer.com/article/10.1007/s10586-026-06095-9)

**Newer graph + LLM direction (titles only; mechanics UNVERIFIED)**
- GALA, "Can Graph-Augmented Large Language Model Agentic Workflows Elevate Root Cause Analysis?" — [arXiv 2508.12472](https://arxiv.org/html/2508.12472v1)
- GALR, graph-based root-cause localization with LLM-assisted recovery. — [MDPI](https://www.mdpi.com/2079-9292/15/1/243)


## Q6. Which family most directly satisfies "graph-based anomaly detection" in the strict sense (the graph helps decide what is anomalous), which only provide graph-based ranking, and how feasible is each for RE2-TT versus a production OpenTelemetry system?

### Cited Findings
**Graph used after detection (ranking or scoping)**
- MonitorRank works only "after an anomaly has been reported". — [MonitorRank PDF](https://netman.aiops.org/~peidan/ANM2018Fall/11.CausalInference/LectureCoverage/2013SIGMETRICS13_Root%20Cause%20Detection%20in%20a%20Service-Oriented%20Architecture.pdf)
- Brandón et al. "assume the existence of this submodule" (an external detector). — [Brandón et al.](https://www.datsi.fi.upm.es/~mperez/pub/jss-2019.pdf)
- MicroRCA flags anomalies with BIRCH before any graph step. — [MicroRCA.py](https://raw.githubusercontent.com/elastisys/MicroRCA/master/MicroRCA.py)
- MicroRank detects on latency and partitions traces before PageRank. — [MicroRank README](https://github.com/IntelligentDDS/MicroRank)
- MicroHECL runs local per-edge detectors and uses the graph to grow and prune propagation chains. — [MicroHECL PDF](https://netman.aiops.org/~peidan/ANM2023/11.CausalInference/ICSE-2021-MicroHECL.pdf)

**Graph inside the detector**
- GDN forecasts each variable from its learned graph neighbours and flags anomalies from the normalized forecast deviation. — [GDN](https://arxiv.org/pdf/2106.06947)
- DeepTraLog scores each trace graph with GGNN + Deep SVDD. — [DeepTraLog PDF](https://cspengxin.github.io/publications/icse22-DeepTraLog.pdf)
- Eadro applies a GAT over the trace dependency graph inside a jointly trained detector and localizer. — [Eadro](https://arxiv.org/pdf/2302.05092)
- ART uses GraphSAGE over the call/deployment graph inside the model whose system-level deviation is thresholded with EVT. — [ART PDF](https://nkcs.iops.ai/wp-content/uploads/2024/09/ART24_to_ASE.pdf)
- AnomRank's detection signal is the derivative of PageRank-variant scores. — [AnomRank](https://arxiv.org/pdf/2011.13085)

**Cost of graph-learning methods on Train Ticket.** Methods that learn graphs from metrics are slow and inaccurate there: PC/FCI took 129–155 s and the PageRank variants scored near random, while BARO and NSigma took about 0.01 s. — [arXiv 2408.13729](https://arxiv.org/pdf/2408.13729)

**Production evidence for subgraph scoping.** The MicroHECL-style approach ran for more than 5 months at Alibaba with a top-3 hit ratio of 68%. — [MicroHECL PDF](https://netman.aiops.org/~peidan/ANM2023/11.CausalInference/ICSE-2021-MicroHECL.pdf)
