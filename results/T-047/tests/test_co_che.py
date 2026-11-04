"""Bằng chứng tổng hợp: cờ → F_I → khóa → M5/hạng; không đọc dữ liệu dev."""
import copy
from fractions import Fraction

import co_che_t047 as mechanism


def native(root_inherited=False):
    root_key = [1, .9, 1, .9] if root_inherited else [2, .9, 1, .9]
    blocks = [{'key': [2, .8, 1, .8], 'groups': [['caller']]},
              {'key': root_key, 'groups': [['root']]}] if root_inherited else [
                  {'key': root_key, 'groups': [['root']]},
                  {'key': [2, .8, 1, .8], 'groups': [['caller']]}]
    return dict(config_id='K-E5' if root_inherited else 'K-R0', opaque_id='synthetic', status='OK',
                method_version='synthetic', blocks=blocks, coverage={'trace': {'trang_thai': 'OK'}},
                window={'N': [0, 1], 'A': [1, 2]}, sets={'observed_entities': ['root', 'caller']},
                diagnostics={'span': {'so_span': 40}}, inherited_by=[{'thuc_the': 'root', 'ma': 'root-channel',
                    'giai_thich': ['caller', 'cpu'], 'trang_thai': 'ap_dung'}] if root_inherited else [],
                worlds={w: {'blocks': blocks, 'don_vi_dem': []} for w in ('P', 'S_lo', 'S_hi')},
                extra=dict(G_N=[['caller', 'root']], canh=[['caller', 'root']],
                           tang_P={'root': 2 if root_inherited else 1, 'caller': 1},
                           K_raw_P={'root': [.9, 1, .9], 'caller': [.8, 1, .8]},
                           K_I_P={'root': [0, 0, 0] if root_inherited else [.9, 1, .9], 'caller': [.8, 1, .8]},
                           kenh_co=[dict(ma='root-channel', thuc_the='root', don_vi='op|root|handle',
                                         F_I=0 if root_inherited else 1, s=.9, lop='lan_nguoc'),
                                    dict(ma='caller-channel', thuc_the='caller', don_vi='metric|caller_cpu',
                                         F_I=1, s=.8, lop='khong_lan')],
                           don_vi_phan_vi=[dict(ma='op|root|handle', p_len=.001, F_raw_len=1,
                                               r_len_N=.05, r_len_A=.9, h=10, trang_thai='OK')]))


LABEL = dict(root='root', dataset='SYNTHETIC', loai_loi='cpu', o='cell')


def snap(rec):
    return mechanism.snapshot(rec, {'file': 'synthetic.jsonl', 'line': 1}, LABEL)


def test_e5_chain_separates_same_raw_from_intrinsic_and_rank():
    before, after = snap(native()), snap(native(True))
    delta = mechanism.chain_delta(before, after, 'root')
    assert not delta['units_changed']  # Cổng/điểm thô giữ nguyên; E5 đổi F_I.
    root = next(c for c in delta['channels'] if c['ma'] == 'root-channel')
    assert root['before']['s'] == root['after']['s'] == .9
    assert (root['before']['F_I'], root['after']['F_I']) == (1, 0)
    assert delta['entity_keys']['root']['tang'] == {'before': 1, 'after': 2}
    assert delta['rank']['P']['delta_RR'] == -Fraction(1, 2)
    assert delta['rank']['P']['before']['M5'] is False and delta['rank']['P']['after']['M5'] is True
    assert delta['status'] == 'FACTS_ONLY'


def test_missing_graph_is_open_not_negative_m5():
    rec = native()
    del rec['extra']['G_N']
    result = snap(rec)
    assert result['rank']['P']['M5'] is None
    assert '/extra/G_N' in result['missing']


def test_gate_change_retains_unit_pointer_and_absent_channel_uncertainty():
    a, b = native(), native()
    b['extra']['don_vi_phan_vi'][0]['p_len'] = .2
    b['extra']['don_vi_phan_vi'][0]['F_raw_len'] = 0
    b['extra']['kenh_co'] = b['extra']['kenh_co'][1:]
    delta = mechanism.chain_delta(snap(a), snap(b), 'root')
    unit = delta['units_changed'][0]
    assert unit['before_pointer'] == unit['after_pointer'] == '/extra/don_vi_phan_vi/0'
    assert unit['values']['p_len'] == {'before': .001, 'after': .2, 'before_present': True, 'after_present': True}
    channel = next(c for c in delta['channels'] if c['ma'] == 'root-channel')
    assert channel['after'] is None  # Không chế F_raw=0 cho kênh vắng.


def test_case_groups_and_counterparts_do_not_drop_unmatched_cases():
    a, b = snap(native()), snap(native(True))
    assert mechanism.group_case(a, a, a, b)['effect'] == 'tut'
    assert mechanism.group_case(a, a, b, a)['effect'] == 'len'
    assert mechanism.group_case(a, a, a, a)['correctness'] == 'dung'
    cond = mechanism.signal_signature(a, LABEL)
    rows = {'bad': {'condition': cond, 'group': {'correctness': 'sai'}},
            'good': {'condition': cond, 'group': {'correctness': 'dung'}},
            'unmatched': {'condition': dict(cond, loai_loi='different'), 'group': {'correctness': 'sai'}}}
    found = mechanism.counterparts(rows)
    assert found['bad']['dung'] == ['good']
    assert found['unmatched']['same_condition'] == [] and found['unmatched']['status'] == 'OPEN_NO_MATCH'
    assert set(found) == set(rows)


def test_change_only_S_hi_retains_native_channels_and_does_not_borrow_P():
    before, after = native(), native()
    for rec in (before, after):
        rec['extra']['kenh_co_the_gioi'] = {
            w: copy.deepcopy(rec['extra']['kenh_co']) for w in mechanism.lc.WORLDS}
    # P vẫn đúng; chỉ một đơn vị đếm và kênh của S_hi đổi.
    counted = dict(ma='log|caller', n_N=10, n_A=30, p_len=.2, F_raw_len=0, trang_thai='OK')
    before['worlds']['S_hi']['don_vi_dem'] = [copy.deepcopy(counted)]
    after['worlds']['S_hi']['don_vi_dem'] = [dict(counted, p_len=.001, F_raw_len=1)]
    # Caller có thêm kênh giải thích; root giữ điểm thô nhưng mất F_I ở đúng S_hi.
    before['extra']['kenh_co_the_gioi']['S_hi'] = before['extra']['kenh_co_the_gioi']['S_hi'][:1]
    before['worlds']['S_hi']['blocks'] = copy.deepcopy(before['worlds']['S_hi']['blocks'])
    before['worlds']['S_hi']['blocks'][1]['key'] = [0, 0, 0, 0]
    after['extra']['kenh_co_the_gioi']['S_hi'][1]['don_vi'] = 'log|caller'
    after['extra']['kenh_co_the_gioi']['S_hi'][0]['F_I'] = 0
    after['worlds']['S_hi']['blocks'] = copy.deepcopy(native(True)['blocks'])
    delta = mechanism.chain_delta(snap(before), snap(after), 'root')
    assert not any(c['changed'] for c in delta['channels'])
    assert delta['rank']['P']['delta_RR'] == 0
    hi = delta['chain_by_world']['S_hi']
    root = next(c for c in hi['channels'] if c['ma'] == 'root-channel')
    assert (root['before']['F_I'], root['after']['F_I']) == (1, 0)
    assert root['before_pointer'] == root['after_pointer'] == '/extra/kenh_co_the_gioi/S_hi/0'
    assert hi['rank']['delta_RR'] == -Fraction(1, 2)
    unit = next(u for u in hi['units_changed'] if u['ma'] == 'log|caller')
    assert unit['world'] == 'S_hi' and unit['relevant']
    assert unit['values']['F_raw_len']['before'] == 0 and unit['values']['F_raw_len']['after'] == 1
    assert not hi['missing']['before'] and not hi['missing']['after']
    assert hi['entity_keys']['status'] == hi['inherited_by']['status'] == 'OPEN_NOT_SAVED'
    assert hi['entity_keys']['value'] is None and hi['inherited_by']['value'] is None
    assert not any(c['changed'] for c in delta['chain_by_world']['S_lo']['channels'])
    assert delta['chain_by_world']['P']['uses_top_level_P']


def test_missing_nonP_channel_native_is_open_not_no_change():
    a, b = snap(native()), snap(native())
    delta = mechanism.chain_delta(a, b, 'root')
    lo = delta['chain_by_world']['S_lo']
    assert lo['channels'] == []
    assert lo['missing']['before'] == ['/extra/kenh_co_the_gioi/S_lo']
    assert lo['missing']['after'] == ['/extra/kenh_co_the_gioi/S_lo']
