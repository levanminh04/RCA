"""Trace-count formulas of MicroRank; the caller must supply the ORIGINAL count/SLO schema.

The formulas do not infer frontend-server roots, span.kind or pod names.
Reference: anormaly_detector.py at the revision in PROVENANCE.json.
"""
import math

def expected_duration(counts, slo, n):
    if 'duration' not in counts:
        raise ValueError('Missing frontend-server duration in microseconds')
    total=0.0
    for operation,count in counts.items():
        if operation=='duration': continue
        if operation not in slo:
            raise ValueError('Operation has no normal SLO: '+operation)
        mu,sigma=slo[operation]
        if not all(math.isfinite(v) for v in [mu,sigma,count]) or count<0 or sigma<0:
            raise ValueError('Invalid normal SLO or count')
        total += count*(mu+n*sigma)
    return total

def original_trace_partition(operation_counts,slo):
    abnormal=[]; normal=[]
    for trace,counts in operation_counts.items():
        if float(counts['duration'])/1000.0 > expected_duration(counts,slo,1.0)+50.0:
            abnormal.append(trace)
        else: normal.append(trace)
    return abnormal,normal

def original_system_alarm(operation_counts,slo):
    abnormal=[]
    for trace,counts in operation_counts.items():
        if float(counts['duration'])/1000.0 > expected_duration(counts,slo,1.5):
            abnormal.append(trace)
    return {'alarm':len(abnormal)>8,'abnormal_trace_ids':abnormal,'total':len(operation_counts)}
