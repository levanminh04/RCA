# TRCA — Check Your Trace First_Toward Timely Root Cause Analysis via Trace-Triggered Detection

## Three-Stage Pipeline

```
    Stage 1: Early Trigger (decoder_only) 
                                 ↓
    Stage 2: Anomaly Graph Builder (run_full_rca)                 
                                 ↓
    Stage 3: Interpretable Reasoner (run_multi_agent_rca)               
```

## Execution Order

### 1. Train Early Trigger Model (one-time)

```bash
cd early_trigger && bash run.sh
```

### 2. Stage 1 — Early Trigger

```bash
python -m early_trigger.detection_exporter \
    --checkpoint_dir ./early_trigger/checkpoints/hipster \
    --rca_data_dir ./rca_data \
    --dates 2022-08-22 \
    --ns hipster \
    --output_dir ./outputs/early_trigger_detection
```

**Inputs:** Trace data, metrics, logs under `rca_data/<date>/`
**Output:** `outputs/early_trigger_detection/<date>/detection.json`

### 3. Stage 2 — Anomaly Graph Builder

```bash
python -m anomaly_graph_builder.run_full_rca \
    --date 2022-08-22 \
    --early_trigger_detection_dir ./outputs/early_trigger_detection
```

**Inputs:** `rca_data/`, `detection.json` (optional)
**Key steps:**
- Alarm channel: `get_metric_with_time` → `generate_alarm` → per-pod/service alarm scores
- JS(sliding_max) channel: Drain3 log parsing → Jensen-Shannon divergence vs. baseline
- Early trigger seeds fusion: merge alarm / JS / early_trigger seeds
- Graph construction: `G_window` (pod call graph) → `G_anom` (k-hop induced subgraph)

**Output:** `outputs/full_run/<date>/<fault_id>/` containing alarm/JS/subgraph JSONs

### 4. Stage 3 — Interpretable Reasoner

```bash
python -m anomaly_graph_builder.interpretable_reasoner.run_multi_agent_rca \
    --date 2022-08-22
```

**Inputs:** `G_anom`, alarm/JS seed evidence from Stage 2
**Agents:**
| Agent | Role |
|-------|------|
| Guard | Filter noise, generate structured priors |
| Localization | Identify and rank root cause candidates |
| Propagation | Analyze anomaly propagation paths |
| Explanation | Generate human-readable RCA report |
| Coordinator | Orchestrate multi-agent workflow |

## Directory Structure

```
.
├── early_trigger/                          # Stage 1: anomaly detection model
│   ├── model/
│   ├── train.py
│   ├── detection_exporter.py
│   └── run.sh
├── anomaly_graph_builder/                  # Stage 2: alarm + JS + graph
│   ├── run_full_rca.py                    # Stage 2 entry
│   └── interpretable_reasoner/            # Stage 3: multi-agent RCA
│       ├── run_multi_agent_rca.py         # Stage 3 entry
│       └── agents/                        # Agent implementations
├── rca_data/                               # Input data (gitignored)
│   └── <date>/
├── outputs/                                # All pipeline outputs (gitignored)
│   ├── early_trigger_detection/
│   └── full_run/
└── utils/                                  # Shared utilities
```


## Quick Start

```bash
# Full pipeline
cd early_trigger && bash run.sh                 # train
python -m early_trigger.detection_exporter \
    --dates 2022-08-22 --ns hipster \
    --output_dir ./outputs/early_trigger_detection
python -m anomaly_graph_builder.run_full_rca \
    --date 2022-08-22
python -m anomaly_graph_builder.interpretable_reasoner.run_multi_agent_rca \
    --date 2022-08-22
```
