---
license: cc-by-nc-4.0
tags:
- root cause analysis
- microservice system
- multi-modal learning
- time series analysis
- log analysis
pretty_name: Cloud Computing Data
size_categories:
- 100M<n<1B
task_categories:
- time-series-forecasting
---

## Data Description:

Preprocessed system metrics and log data from Cloud Computing Platform.

Constructed the metric time series (as npy format) from the original metrics data (Json format). 

Extracted the log messages from the original log data (Json format). Parsed the log messages into log event templates. 

Note: 20240207 data does not contain EKS log data; it solely comprises CloudTrail log data in CSV format. Consequently, this dataset does not require preprocessing with a log parser.

## Timezone Note (Important)

PPTX scenario slides use Japan Standard Time (JST) for measurement periods and failure timestamps, because the real testbed is located in Japan and failures were recorded locally.

All metric and log data are timestamped in UTC.

This means there is a 9-hour offset between the PPTX timestamps and the data files.
For example:
11:30 JST → 02:30 UTC

When aligning ground truth with the metric/log data, please convert all PPTX times from JST to UTC.


## Citation:

Lecheng Zheng, Zhengzhang Chen, Dongjie Wang, Chengyuan Deng, Reon Matsuoka, and Haifeng Chen: LEMMA-RCA: A Large Multi-modal Multi-domain Dataset for Root Cause Analysis. CoRR abs/2406.05375 (2024)


## License:

cc-by-nd-4.0: NoDerivatives.