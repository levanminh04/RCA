"""V6 phần N-Sigma: dữ liệu tổng hợp có đáp án; chạy trước đặc trưng dev."""
import numpy as np
import pandas as pd
from baro.anomaly_detection import nsigma
from nsigma_flags import features


def run_tests():
    tests = []
    cols = ['ts-a-service_cpu', 'ts-b-service_error']
    universe = ['ts-a-service', 'ts-b-service', 'ts-c-service']
    Z = np.zeros((1441, 2), dtype=bool)
    Z[100:110, 0] = True
    Z[400:410, 1] = True
    f = features(Z, cols, [0, 1], universe)
    assert all(f['N1'].values())  # đầu/cuối = (10/200)/(10/640) = 3,2
    assert f['N2'] == {'5': True, '10': False, '20': False}
    assert f['N3'] == {'5': False, '10': True, '20': True}
    assert f['N4'] is True
    assert f['E_services']['baseline']['ts-c-service']['first_after_index'] is None
    tests.append({'ten': 'N1_N2_N3_N4_exact_matrix', 'status': 'PASS', 'features': f})
    x = np.zeros(1441)
    x[100:720:20] = 20
    frame = pd.DataFrame({'time': np.arange(1441), cols[0]: x})
    al = nsigma(frame, k=3, startsfrom=100)
    zz = np.zeros((1441, 1), dtype=bool)
    zz[np.asarray(al, dtype=int), 0] = True
    f = features(zz, cols[:1], [0], universe)
    assert f['t_hat_index'] == 100
    assert f['N2'] == {'5': True, '10': True, '20': False}
    assert f['N4'] is True
    tests.append({'ten': 'BARO_heavy_tailed_sparse_spikes', 'status': 'PASS',
                  'p_j': f['columns'][0]['p_j'], 'N2': f['N2'], 'N4': f['N4']})
    rng = np.random.default_rng(2901)
    names = [f'ts-s{j}-service_cpu' for j in range(24)]
    frame = pd.DataFrame(rng.normal(size=(1441, 24)), columns=names)
    frame.insert(0, 'time', np.arange(1441))
    zz = np.zeros((1441, 24), dtype=bool)
    for j, name in enumerate(names):
        zz[np.asarray(nsigma(frame[['time', name]], k=3, startsfrom=100), dtype=int), j] = True
    first = int(np.flatnonzero(zz.any(axis=1))[0])
    f = features(zz, names, frame[names].iloc[:first].std().to_numpy(),
                 [c.split('_', 1)[0] for c in names])
    assert abs(f['r_obs']-f['r_ind']) < .05
    tests.append({'ten': 'BARO_independent_normal_columns', 'status': 'PASS',
                  'seed': 2901, 'd': 24, 'r_obs': f['r_obs'], 'r_ind': f['r_ind'],
                  'absolute_difference': abs(f['r_obs']-f['r_ind']), 'tolerance': .05,
                  'ly_do_tolerance': 'Chỉ kiểm tổng hợp hữu hạn 620 giây, không suy độc lập từ số dev.'})
    return {'status': 'PASS', 'tests': tests}


if __name__ == '__main__':
    import json
    print(json.dumps(run_tests(), ensure_ascii=False))
