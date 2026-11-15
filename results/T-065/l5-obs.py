"""L5: stdin SSH helper. Never opens env files or prints authentication material."""
import base64, datetime, hashlib, json, pathlib, subprocess, sys, urllib.request, urllib.error, urllib.parse
B=pathlib.Path('/opt/flash-ticket-obs/pinned')
C='flash-ticket-obs-grafana'
def utc(): return subprocess.check_output(['date','-u','+%Y-%m-%dT%H:%M:%S.%NZ'],text=True).strip()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def docker(*args): return subprocess.check_output(['docker',*args],text=True)
def api(url,method='GET',body=None):
    env=dict(x.split('=',1) for x in json.loads(docker('inspect',C))[0]['Config']['Env'] if '=' in x)
    auth=base64.b64encode((env.get('GF_SECURITY_ADMIN_USER','admin')+':'+env['GF_SECURITY_ADMIN_PASSWORD']).encode()).decode()
    req=urllib.request.Request('http://10.0.0.215:3000'+url, data=None if body is None else json.dumps(body).encode(),method=method,headers={'Authorization':'Basic '+auth,'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=40) as r:return {'http':r.status,'data':json.load(r)}
    except urllib.error.HTTPError as e:return {'http':e.code,'data':e.read().decode()}
def machine():
    ins=json.loads(docker('inspect',C))[0]
    cmds=subprocess.check_output(['ps','-eo','cmd'],text=True).splitlines()
    return {'utc':utc(),'stop':(pathlib.Path.home()/'rca-dieu-phoi/STOP').exists(),'runner3':sum('python3 -B runner3' in x for x in cmds),'stats':docker('stats','--no-stream','--format','{{json .}}',C).strip(),'restart_count':ins['RestartCount'],'started_at':ins['State']['StartedAt'],'memory_limit':ins['HostConfig']['Memory'],'status':ins['State']['Status']}
def inventory():
    r={'utc':utc(),'machine':machine(),'files':{},'dashboards':[],'folders':[]}
    for p in [B/'compose.json',*sorted((B/'provisioning/dashboards').rglob('*'))]:
        if p.is_file():r['files'][str(p)]={'sha256':sha(p),'bytes':p.stat().st_size}
    for p in sorted((B/'provisioning/dashboards').rglob('*.yaml')):r.setdefault('providers',{})[str(p)]=p.read_text()
    r['health']=api('/api/health');r['search']=api('/api/search?limit=1000');r['root_folders']=api('/api/folders?limit=1000')
    for f in r['search'].get('data',[]):
        if f['type']=='dash-folder':r['folders'].append(api('/api/folders/'+f['uid']))
        elif f['type']=='dash-db':
            d=api('/api/dashboards/uid/'+f['uid']);r['dashboards'].append({'search':f,'meta':d.get('data',{}).get('meta'),'uid':d.get('data',{}).get('dashboard',{}).get('uid'),'version':d.get('data',{}).get('dashboard',{}).get('version')})
    return r
if sys.argv[1]=='inventory':print(json.dumps(inventory(),ensure_ascii=False))
elif sys.argv[1]=='machine':print(json.dumps(machine(),ensure_ascii=False))
elif sys.argv[1]=='dashboard-links':
    assert not (pathlib.Path.home()/'rca-dieu-phoi/STOP').exists()
    ids=('t065-l5-muc-luc','t065-l4-rca','t065-l4-phat-lai','t065-rca','t065-phat-lai','rca-g2','rca-g2-phat-lai')
    for uid in ids:
        result=api('/api/dashboards/uid/'+uid)
        payload=result['data'].get('dashboard',{}) if result['http']==200 else {}
        panels=[p for p in payload.get('panels',[]) if p.get('type')=='text']
        import re
        targets=sorted(set(re.findall(r'/d/([a-zA-Z0-9_-]+)', '\n'.join(p.get('options',{}).get('content','') for p in panels))))
        print(json.dumps({'utc':utc(),'uid':uid,'http':result['http'],'returned_uid':payload.get('uid'),'text_panel_links':targets},ensure_ascii=False),flush=True)
elif sys.argv[1]=='remove-empty-rca':
    assert not (pathlib.Path.home()/'rca-dieu-phoi/STOP').exists()
    found=api('/api/search?limit=1000')['data']
    folder=next(f for f in found if f['type']=='dash-folder' and f['title']=='RCA')
    uid=folder['uid']
    contents=api('/api/search?folderUIDs='+uid+'&limit=1000')
    children=api('/api/folders?parentUid='+uid+'&limit=1000')
    assert contents['http']==200 and children['http']==200
    assert not contents['data'] and not children['data'], 'RCA not empty'
    print(json.dumps({'utc':utc(),'uid':uid,'contents':contents,'children':children,'delete':api('/api/folders/'+uid,'DELETE')},ensure_ascii=False))
elif sys.argv[1]=='metadata':
    ds=list((B/'provisioning/dashboards').rglob('t065-l4-rca.json'))
    p=next(x for x in json.loads(ds[0].read_text())['panels'] if x['id']==3)
    r=[]
    index=json.loads(pathlib.Path('/opt/flash-ticket-obs/rca-ket-qua/t065-l4-001/chi-muc-ban.json').read_text())
    for b in index['ban']:
        t=json.loads(json.dumps(p['targets'][0],ensure_ascii=False).replace('${ban}',b['ban']).replace('${ca}','eb48d6b3'))
        t.update(intervalMs=15000,maxDataPoints=1000)
        r.append({'ban':b['ban'],'result':api('/api/ds/query','POST',{'from':'1794554360000','to':'1794554959999','queries':[t]})})
    print(json.dumps({'utc':utc(),'rows':r},ensure_ascii=False))
elif sys.argv[1] in ('evidence','resume-empty'):
    folder=pathlib.Path('/opt/flash-ticket-obs/rca-ket-qua/t065-l4-001')
    def query_one(query, start, end):
        assert not (pathlib.Path.home()/'rca-dieu-phoi/STOP').exists()
        response=api('/api/ds/query','POST',{'from':str(start),'to':str(end),'queries':[query]})
        payload=response['data'] if isinstance(response['data'],dict) else {}
        results=payload.get('results',{})
        errors=[x.get('error') for x in results.values() if x.get('error')]
        rows=sum(max((len(v) for v in f.get('data',{}).get('values',[])),default=0) for x in results.values() for f in x.get('frames',[]))
        return {'utc':utc(),'query':query.get('query',query.get('expr')),'range':{'from':str(start),'to':str(end)},'http':response['http'],'errors':errors,'rows':rows,'state':'loi' if response['http']!=200 or errors else 'co_du_lieu' if rows else 'rong'}
    def operation(ban,ca,svc,op,kho):
        d=json.loads((folder/ban/'thao-tac-vue'/ca/(svc+'.json')).read_text())
        o=next(o for o in d['thao_tac'] if o['id']==op)
        link=next(l for l in o['lien_ket'] if l['kho']==kho)
        pane=json.loads(urllib.parse.parse_qs(urllib.parse.urlparse(link['url']).query)['panes'][0])['a']
        query=pane['queries'][0]
        query.update(intervalMs=15000,maxDataPoints=1000)
        return {'ban':ban,'ca':ca,'service':svc,'op':op,'kho':kho,**query_one(query,pane['range']['from'],pane['range']['to'])}
    if sys.argv[1]=='evidence':
        print(json.dumps(operation(*sys.argv[2:7]),ensure_ascii=False))
    else:
        for ca,op in [('1ad3afeb','o301b570781fdebc61170'),('00eaea92','o24b7697fd9762cd664d5')]:
            print(json.dumps(operation('p7',ca,'booking-service',op,'loki'),ensure_ascii=False),flush=True)
        for service,panels in [('event-service',[31,32,33]),('api-gateway',[31,32,33,35])]:
            ca='e8661e0a'
            shot=json.loads((folder/'trang-thai'/ca/(service+'.json')).read_text())
            for item in shot['queries']:
                if item['panel'] in panels:
                    query=item['request']
                    start=int(datetime.datetime.fromisoformat(item['tu_utc'].replace('Z','+00:00')).timestamp()*1000)
                    end=int(datetime.datetime.fromisoformat(item['den_loai_tru'].replace('Z','+00:00')).timestamp()*1000)-1
                    print(json.dumps({'ca':ca,'service':service,'panel':item['panel'],'kho':item['kho'],**query_one(query,start,end)},ensure_ascii=False),flush=True)
