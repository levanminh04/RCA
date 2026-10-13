"""Known-answer checks for B2/B3 and V7 valid-domain denominators."""
from analyze_step5 import intervention_flags,v7,put,OUT,sha,log

checks=[]
def check(name,actual,expected):
    checks.append({'name':name,'actual':actual,'expected':expected,'pass':actual==expected})
check('I1 absent => B2 True, B3 NA',
      [intervention_flags(300,[306],[300],5)[k] for k in ('B2','B3')],[True,None])
check('inclusive tolerance, I2 absent => B3 True',
      [intervention_flags(300,[305],[306],5)[k] for k in ('B2','B3')],[False,True])
check('both present => both False',
      [intervention_flags(300,[295],[305],5)[k] for k in ('B2','B3')],[False,False])
check('upper domain inclusive',intervention_flags(714,[714],[714],5)['valid'],True)
check('outside upper domain => NA',
      [intervention_flags(715,[715],[715],5)[k] for k in ('B2','B3')],[None,None])
check('no first => NA',intervention_flags(None,[],[],5)['B2'],None)
check('sensitivity2 excludes delta3',intervention_flags(300,[303],[300],2)['B2'],True)
check('sensitivity5 includes delta3',intervention_flags(300,[303],[300],5)['B2'],False)
check('sensitivity10 includes delta8',intervention_flags(300,[308],[308],10)['B2'],False)
row={'opaque_id':'synthetic','detector':'bocpd','root':'synthetic-root','fault':'synthetic-fault','cell':'synthetic-cell'}
bf={'synthetic':{'alarms_indices':[100],
    'B1_all_Nv':{'1':{'valid':False,'flag':None},'100':{'valid':True,'flag':True},
                 '101':{'valid':True,'flag':True},'102':{'valid':True,'flag':False}},
    'B1_t_hat':{'valid':True,'flag':True},
    'B4_all_Nv':{str(w):{'1':{'valid':False,'flags':{str(k):None for k in (2,3,5)}},
                       '100':{'valid':True,'flags':{str(k):True for k in (2,3,5)}},
                       '101':{'valid':True,'flags':{'2':True,'3':False,'5':False}}} for w in (15,30,60)},
    'B4_t_hat':{str(w):{'valid':True,'flags':{str(k):True for k in (2,3,5)}} for w in (15,30,60)}}}
result=v7([row],bf)
check('V7 B1 excludes alarm and invalid',result['cases']['synthetic']['B1']['control_n'],2)
check('V7 B1 fraction',result['cases']['synthetic']['B1']['control_rate'],.5)
for w in (15,30,60):
    for k in (2,3,5):
        check(f'V7 B4 valid denominator w{w}/k{k}',result['cases']['synthetic']['B4'][str(w)][str(k)]['control_n'],1)
        check(f'V7 B4 fraction w{w}/k{k}',result['cases']['synthetic']['B4'][str(w)][str(k)]['control_rate'],1. if k==2 else 0.)
output={'status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','checks':checks,
        'check_count':len(checks),'implementation_sha256':sha(OUT/'scripts/analyze_step5.py'),'test_sha256':sha(__file__)}
log('Lệnh có ghi: T014main Python -B -W ignore test_step5.py; chuỗi giả, không nhãn/dev; tạo V6-step5-001/check.json.')
version=1
while (OUT/f'runs/V6-step5-{version:03d}').exists(): version+=1
put(OUT/f'runs/V6-step5-{version:03d}/check.json',output)
assert output['status']=='PASS',output
print({'status':output['status'],'checks':len(checks)})
