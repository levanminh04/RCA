"""Tạo patch CHƯA ÁP DỤNG và kiểm đơn vị tách rời, không sửa src."""
import ast
import difflib
import hashlib
import inspect
import json
from pathlib import Path
import adapter_t047 as ad
import ung_vien_cong_tat_dinh as candidate


def main():
    output=ad.OUT/'runs/de-xuat-c1-002';output.mkdir(parents=True,exist_ok=False)
    path=ad.ROOT/'src/m1/cong.py';before=path.read_bytes();source=before.decode('utf-8')
    replacements=[
        ('    tong, dem = {}, {}','    samples = {}'),
        ('        tong[j] = tong.get(j, 0.0) + float(v)\n        dem[j] = dem.get(j, 0) + 1',
         '        samples.setdefault(j, []).append(float(v))'),
        ('    return {j: tong[j] / dem[j] for j in tong}',
         '    return {j: math.fsum(sorted(samples[j])) / len(samples[j]) for j in sorted(samples, reverse=True)}'),
        ('    x = np.array(list(o.values()), float)',
         '    order = sorted(o, reverse=True)  # thứ tự thời gian tăng, không theo thứ tự chèn dict\n    x = np.array([o[j] for j in order], float)'),
        ('        cap = [(o[j] - m) * (o[j + k] - m) for j in o if (j + k) in o]',
         '        cap = [(o[j] - m) * (o[j + k] - m) for j in order if (j + k) in o]')]
    proposed=source
    for old,new in replacements:
        if proposed.count(old)!=1:raise ValueError('nguồn không đúng điểm thay dự kiến')
        proposed=proposed.replace(old,new)
    ast.parse(proposed)
    (output/'cong-proposed.py').write_text(proposed,encoding='utf-8')
    patch=''.join(difflib.unified_diff(source.splitlines(keepends=True),proposed.splitlines(keepends=True),
                                     fromfile='a/src/m1/cong.py',tofile='b/src/m1/cong.py'))
    (output/'de-xuat.patch').write_text(patch,encoding='utf-8')
    ns={'__name__':'T047_candidate_not_M1'};exec(compile(proposed,'cong-proposed.py','exec'),ns)
    assert ns['o_1s']([1,1,1],[1e16,1.,-1e16],10**9,'N') == candidate.o_1s([1,1,1],[1e16,1.,-1e16],10**9,'N')
    observations=[]
    for p in (ad.OUT/'runs/t1-xao-dieu-tra-002').glob('dev-*.json'):
        d=json.loads(p.read_text(encoding='utf-8'));vs=d['versions'];row={}
        for name in ('original','shuffled'):
            u=vs[name];N,A,mn,ma=u['N'],u['A'],u['mocN'],u['mocA']
            # Mốc phân đôi lấy từ hai miền mẫu, các ca này có đúng1mẫu/giây trong600giây.
            t=min(ma);bounds=(t-300*10**9,t+300*10**9)
            one=ns['o_1s'](mn,N,t,'N');rho,reason=ns['tu_tuong_quan'](one)
            kb=ns['chuan_bi_khoi'](N,mn,A,ma,t,*bounds)
            from m1 import runner
            pv,cach=ns['p_theo_G3'](N,mn,A,ma,t,*bounds,'len',runner.TS_HOP_DONG,d['unit'])
            row[name]=dict(b=kb.get('b'),p=pv,cach=cach,reason=reason,
                           same_sample_pairs=sorted(zip(mn,N))==sorted(zip(vs['original']['mocN'],vs['original']['N']))
                               and sorted(zip(ma,A))==sorted(zip(vs['original']['mocA'],vs['original']['A'])))
        observations.append(dict(oid=d['oid'],unit=d['unit'],candidate=row,
                                 invariant=row['original']==row['shuffled'],
                                 matches_saved_original_p=row['original']['p']==vs['original']['saved_p']))
    out=dict(status='CANDIDATE_NOT_APPROVED_NOT_INTEGRATED',target='src/m1/cong.py',
             source_sha256=hashlib.sha256(before).hexdigest(),proposed_sha256=hashlib.sha256(proposed.encode()).hexdigest(),
             functions=['o_1s','tu_tuong_quan'],real_units=observations,
             PASS=all(x['invariant'] and x['matches_saved_original_p'] for x in observations),
             unchanged_src=path.read_bytes()==before,
             limits=['Chỉ kiểm ứng viên riêng trên2đơnvịlệch và1đối chiếu, chưa hồi quy tích hợp/toàn bộ dev.',
                     'Không thêm sàn phương sai; ý nghĩaG3 trên dữliệu gần hằng vẫn OPEN.',
                     'Không dùng ứng viên cho T1/K hoặc chọn cấu hình trước quyền sửa src.'])
    ad.ghi(output/'kiem-ung-vien.json',out);print(json.dumps(out,ensure_ascii=False,indent=1))
    if not out['PASS'] or not out['unchanged_src']:raise ValueError('ứng viên chưa đạt')


if __name__=='__main__':main()
