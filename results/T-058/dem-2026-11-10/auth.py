"""Existing Keycloak client flows; credentials and tokens stay in memory."""
import base64
import hashlib
from html.parser import HTMLParser
import http.cookiejar
import json
from pathlib import Path
import secrets
import urllib.error
import urllib.parse
import urllib.request

ROOT=Path('/opt/flash-ticket-app')
def env(name='booking-service.env'):
    return dict(x.split('=',1) for x in (ROOT/'env'/name).read_text().splitlines() if x and not x.startswith('#'))

def internal_token():
    e=env()
    data=urllib.parse.urlencode({'grant_type':'client_credentials','client_id':'internal-service','client_secret':e['INTERNAL_SERVICE_CLIENT_SECRET']}).encode()
    with urllib.request.urlopen(e['KEYCLOAK_TOKEN_URI'],data=data,timeout=15) as response:
        return json.load(response)['access_token']

class Form(HTMLParser):
    def __init__(self):
        super().__init__(); self.action=None; self.fields={}; self.active=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='form' and a.get('id')=='kc-form-login':
            self.action=a.get('action'); self.active=True
        if tag=='input' and self.active and a.get('name'):
            self.fields[a['name']]=a.get('value','')
    def handle_endtag(self,tag):
        if tag=='form': self.active=False

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        return None

def role_token(role='BUYER'):
    e=env(); issuer=e['KEYCLOAK_ISSUER_URI']
    users=json.loads((ROOT/'env/test-users.json').read_text())
    user=next(x for x in users if role in x.get('realmRoles',[]))
    verifier=secrets.token_urlsafe(48)
    challenge=base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip('=')
    state=secrets.token_urlsafe(24)
    # Use the realm's registered callback identifier, but intercept the 302
    # locally. No request is ever sent to this external callback host.
    redirect='https://oauth.pstmn.io/v1/callback'
    params={'response_type':'code','client_id':'frontend','redirect_uri':redirect,'scope':'openid profile email',
            'state':state,'code_challenge':challenge,'code_challenge_method':'S256'}
    cookies=http.cookiejar.CookieJar()
    opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookies),NoRedirect())
    with opener.open(issuer+'/protocol/openid-connect/auth?'+urllib.parse.urlencode(params),timeout=15) as r:
        form=Form(); form.feed(r.read().decode())
    if not form.action or not form.action.startswith(issuer+'/'):
        raise RuntimeError('Expected same-realm login form')
    fields=form.fields|{'username':user['username'],'password':user['password'],'credentialId':''}
    try:
        with opener.open(form.action,data=urllib.parse.urlencode(fields).encode(),timeout=15) as response:
            raise RuntimeError('Login did not return authorization-code redirect')
    except urllib.error.HTTPError as response:
        if response.code not in [302,303]:
            raise RuntimeError('Login HTTP '+str(response.code)) from None
        location=response.headers['Location']
    if not location.startswith(redirect):
        raise RuntimeError('Unexpected login redirect origin')
    result=urllib.parse.parse_qs(urllib.parse.urlparse(location).query)
    if result.get('state') != [state] or 'code' not in result:
        raise RuntimeError('Authorization state/code missing')
    data=urllib.parse.urlencode({'grant_type':'authorization_code','client_id':'frontend','redirect_uri':redirect,
                                'code':result['code'][0],'code_verifier':verifier}).encode()
    with urllib.request.urlopen(issuer+'/protocol/openid-connect/token',data=data,timeout=15) as response:
        return json.load(response)['access_token']

def buyer_token():
    return role_token('BUYER')

if __name__=='__main__':
    for name,fn in [('internal-service',internal_token),('buyer via frontend PKCE',buyer_token)]:
        token=fn()
        claims=json.loads(base64.urlsafe_b64decode(token.split('.')[1]+'=='))
        print(json.dumps({'flow':name,'iss':claims['iss'],'aud':claims.get('aud'),'roles':claims.get('realm_access',{}).get('roles',[])}))
