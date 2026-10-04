# MIT code extracted verbatim from IntelligentDDS/MicroRank; see PROVENANCE.json.
import numpy as np
import math

def trace_pagerank(operation_operation, operation_trace, trace_operation, pr_trace, anomaly):
    operation_length = len(operation_operation)
    trace_length = len(operation_trace)

    p_ss = np.zeros((operation_length, operation_length), dtype=np.float32)
    p_sr = np.zeros((operation_length, trace_length), dtype=np.float32)
    p_rs = np.zeros((trace_length, operation_length), dtype=np.float32)

    # matrix = np.zeros((n, n), dtype=np.float32)
    pr = np.zeros((trace_length, 1), dtype=np.float32)

    node_list = []
    for key in operation_operation.keys():
        node_list.append(key)

    trace_list = []
    for key in operation_trace.keys():
        trace_list.append(key)

    # matrix node*node
    for operation in operation_operation:
        child_num = len(operation_operation[operation])

        for child in operation_operation[operation]:
            p_ss[node_list.index(child)][node_list.index(
                operation)] = 1.0 / child_num

    # matrix node*request
    for trace_id in operation_trace:
        child_num = len(operation_trace[trace_id])
        for child in operation_trace[trace_id]:
            p_sr[node_list.index(child)][trace_list.index(trace_id)] \
                = 1.0 / child_num

    # matrix request*node
    for operation in trace_operation:
        child_num = len(trace_operation[operation])

        for child in trace_operation[operation]:
            p_rs[trace_list.index(child)][node_list.index(operation)] \
                = 1.0 / child_num

    kind_list = np.zeros(len(trace_list))
    p_srt = p_sr.T
    for i in range(len(trace_list)):
        index_list = [i]
        if kind_list[i] != 0:
            continue
        n = 0
        for j in range(i, len(trace_list)):
            if (p_srt[i] == p_srt[j]).all():
                index_list.append(j)
                n += 1
        for index in index_list:
            kind_list[index] = n

    num_sum_trace = 0
    kind_sum_trace = 0
    if not anomaly:
        for trace_id in pr_trace:
            num_sum_trace += 1.0 / kind_list[trace_list.index(trace_id)]
        for trace_id in pr_trace:
            pr[trace_list.index(trace_id)] = 1.0 / \
                kind_list[trace_list.index(trace_id)] / num_sum_trace
    else:
        for trace_id in pr_trace:
            kind_sum_trace += 1.0 / kind_list[trace_list.index(trace_id)]
            num_sum_trace += 1.0 / len(pr_trace[trace_id])
        for trace_id in pr_trace:
            pr[trace_list.index(trace_id)] = 1.0 / (kind_list[trace_list.index(trace_id)] / kind_sum_trace * 0.5
                                                    + 1.0 / len(pr_trace[trace_id])) / num_sum_trace * 0.5

    if anomaly:
        print('\nAnomaly_PageRank:')
    else:
        print('\nNormal_PageRank:')
    result = pageRank(p_ss, p_sr, p_rs, pr, operation_length, trace_length)

    weight = {}
    sum = 0
    for operation in operation_operation:
        sum += result[node_list.index(operation)][0]

    trace_num_list = {}
    for operation in operation_operation:
        trace_num_list[operation] = 0
        i = node_list.index(operation)
        for j in range(len(trace_list)):
            if p_sr[i][j] != 0:
                trace_num_list[operation] += 1

    for operation in operation_operation:
        weight[operation] = result[node_list.index(
            operation)][0] * sum / len(operation_operation)

    # for score in sorted(weight.items(), key=lambda x: x[1], reverse=True):
    #     print('%-50s: %.5f' % (score[0], score[1]))

    return weight, trace_num_list

def pageRank(p_ss, p_sr, p_rs, v, operation_length, trace_length, d=0.85, alpha=0.01):
    iteration = 25
    service_ranking_vector = np.ones(
        (operation_length, 1)) / float(operation_length + trace_length)
    request_ranking_vector = np.ones(
        (trace_length, 1)) / float(operation_length + trace_length)

    for i in range(iteration):
        updated_service_ranking_vector = d * \
            (np.dot(p_sr, request_ranking_vector) +
             alpha * np.dot(p_ss, service_ranking_vector))
        updated_request_ranking_vector = d * \
            np.dot(p_rs, service_ranking_vector) + (1.0 - d) * v
        service_ranking_vector = updated_service_ranking_vector / \
            np.amax(updated_service_ranking_vector)
        request_ranking_vector = updated_request_ranking_vector / \
            np.amax(updated_request_ranking_vector)

    normalized_service_ranking_vector = service_ranking_vector / \
        np.amax(service_ranking_vector)
    return normalized_service_ranking_vector

def calculate_spectrum_without_delay_list(anomaly_result, normal_result, anomaly_list_len, normal_list_len,
                                          top_max, normal_num_list, anomaly_num_list, spectrum_method):
    spectrum = {}

    for node in anomaly_result:
        spectrum[node] = {}
        # spectrum[node]['ef'] = anomaly_result[node] * anomaly_list_len
        # spectrum[node]['nf'] = anomaly_list_len - anomaly_result[node] * anomaly_list_len
        spectrum[node]['ef'] = anomaly_result[node] * anomaly_num_list[node]
        spectrum[node]['nf'] = anomaly_result[node] * \
            (anomaly_list_len - anomaly_num_list[node])
        if node in normal_result:
            #spectrum[node]['ep'] = normal_result[node] * normal_list_len
            #spectrum[node]['np'] = normal_list_len - normal_result[node] * normal_list_len
            spectrum[node]['ep'] = normal_result[node] * normal_num_list[node]
            spectrum[node]['np'] = normal_result[node] * \
                (normal_list_len - normal_num_list[node])
        else:
            spectrum[node]['ep'] = 0.0000001
            spectrum[node]['np'] = 0.0000001

    for node in normal_result:
        if node not in spectrum:
            spectrum[node] = {}
            #spectrum[node]['ep'] = normal_result[node] * normal_list_len
            #spectrum[node]['np'] = normal_list_len - normal_result[node] * normal_list_len
            spectrum[node]['ep'] = (
                1 + normal_result[node]) * normal_num_list[node]
            spectrum[node]['np'] = normal_list_len - normal_num_list[node]
            if node not in anomaly_result:
                spectrum[node]['ef'] = 0.0000001
                spectrum[node]['nf'] = 0.0000001

    # print('\n Micro Rank Spectrum raw:')
    # print(json.dumps(spectrum))
    result = {}

    for node in spectrum:
        # Dstar2
        if spectrum_method == "dstar2":
            result[node] = spectrum[node]['ef'] * spectrum[node]['ef'] / \
                (spectrum[node]['ep'] + spectrum[node]['nf'])
        # Ochiai
        elif spectrum_method == "ochiai":
            result[node] = spectrum[node]['ef'] / \
                math.sqrt((spectrum[node]['ep'] + spectrum[node]['ef']) * (
                    spectrum[node]['ef'] + spectrum[node]['nf']))

        elif spectrum_method == "jaccard":
            result[node] = spectrum[node]['ef'] / (spectrum[node]['ef'] + spectrum[node]['ep']
                                                   + spectrum[node]['nf'])

        elif spectrum_method == "sorensendice":
            result[node] = 2 * spectrum[node]['ef'] / \
                (2 * spectrum[node]['ef'] + spectrum[node]
                 ['ep'] + spectrum[node]['nf'])

        elif spectrum_method == "m1":
            result[node] = (spectrum[node]['ef'] + spectrum[node]
                            ['np']) / (spectrum[node]['ep'] + spectrum[node]['nf'])

        elif spectrum_method == "m2":
            result[node] = spectrum[node]['ef'] / (2 * spectrum[node]['ep'] + 2 * spectrum[node]['nf'] +
                                                   spectrum[node]['ef'] + spectrum[node]['np'])
        elif spectrum_method == "goodman":
            result[node] = (2 * spectrum[node]['ef'] - spectrum[node]['nf'] - spectrum[node]['ep']) / \
                (2 * spectrum[node]['ef'] + spectrum[node]
                 ['nf'] + spectrum[node]['ep'])
        # Tarantula
        elif spectrum_method == "tarantula":
            result[node] = spectrum[node]['ef'] / (spectrum[node]['ef'] + spectrum[node]['nf']) / \
                (spectrum[node]['ef'] / (spectrum[node]['ef'] + spectrum[node]['nf']) +
                 spectrum[node]['ep'] / (spectrum[node]['ep'] + spectrum[node]['np']))
        # RussellRao
        elif spectrum_method == "russellrao":
            result[node] = spectrum[node]['ef'] / \
                (spectrum[node]['ef'] + spectrum[node]['nf'] +
                 spectrum[node]['ep'] + spectrum[node]['np'])

        # Hamann
        elif spectrum_method == "hamann":
            result[node] = (spectrum[node]['ef'] + spectrum[node]['np'] - spectrum[node]['ep'] - spectrum[node]
                            ['nf']) / (spectrum[node]['ef'] + spectrum[node]['nf'] + spectrum[node]['ep'] + spectrum[node]['np'])

        # Dice
        elif spectrum_method == "dice":
            result[node] = 2 * spectrum[node]['ef'] / \
                (spectrum[node]['ef'] + spectrum[node]
                 ['nf'] + spectrum[node]['ep'])

        # SimpleMatching
        elif spectrum_method == "simplematcing":
            result[node] = (spectrum[node]['ef'] + spectrum[node]['np']) / (spectrum[node]
                                                                            ['ef'] + spectrum[node]['np'] + spectrum[node]['nf'] + spectrum[node]['ep'])

        # RogersTanimoto
        elif spectrum_method == "rogers":
            result[node] = (spectrum[node]['ef'] + spectrum[node]['np']) / (spectrum[node]['ef'] +
                                                                            spectrum[node]['np'] + 2 * spectrum[node]['nf'] + 2 * spectrum[node]['ep'])

    # Top-n节点列表
    top_list = []
    score_list = []
    for index, score in enumerate(sorted(result.items(), key=lambda x: x[1], reverse=True)):
        if index < top_max + 6:
            top_list.append(score[0])
            score_list.append(score[1])
            #print('%-50s: %.8f' % (score[0], score[1]))
    return top_list, score_list

