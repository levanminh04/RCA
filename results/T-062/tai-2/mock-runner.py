"""L1 adapter around the unchanged deploy/rca-test/mock_vnpay.py.

Adds return callback and safe audit. Binds only loopback, reachable from k6 over SSH.
"""
import json
import os
from pathlib import Path
import time
from urllib.parse import parse_qs, urlencode, urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler, urlopen
from urllib.error import HTTPError
import mock_vnpay as m

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args):
        return None

class Handler(m.Handler):
    def do_GET(self):
        path=urlsplit(self.path)
        if path.path!='/checkout':
            return super().do_GET()
        started=time.monotonic_ns(); attempt=''; status=400
        try:
            values=parse_qs(path.query,keep_blank_values=True)
            if any(len(v)!=1 for v in values.values()):
                raise ValueError('DUPLICATE_PARAMETER')
            params={k:v[0] for k,v in values.items()}
            charge=self.server.state.charge(params)
            attempt=params['vnp_TxnRef']
            callback={'vnp_TmnCode':self.server.state.merchant,'vnp_TxnRef':attempt,
                'vnp_Amount':str(charge['amount']),'vnp_TransactionNo':charge['transaction'],
                'vnp_ResponseCode':'00','vnp_TransactionStatus':'00','vnp_PayDate':charge['date']}
            callback['vnp_SecureHash']=m.callback_signature(self.server.state.secret,callback)
            with urlopen(self.server.ipn_url+'?'+urlencode(callback),timeout=15) as r:
                acknowledgment=json.load(r)
            self.server.state.audit('ipn',attempt,started,int(acknowledgment.get('RspCode','99')))
            if acknowledgment.get('RspCode') not in {'00','02'}:
                raise ValueError('IPN_NOT_ACCEPTED')
            request=Request(self.server.return_url+'?'+urlencode(callback))
            try:
                with build_opener(NoRedirect()).open(request,timeout=15) as r:
                    return_status=r.code
            except HTTPError as r:
                return_status=r.code
            self.server.state.audit('return',attempt,started,return_status)
            if return_status!=302:
                raise ValueError('RETURN_NOT_ACCEPTED')
            status=200
            self.reply(status,{'attemptId':attempt,'ipn':acknowledgment,'returnStatus':return_status})
        except (ValueError,KeyError,TypeError,OSError):
            self.reply(status,{'code':'TEST_CHECKOUT_FAILED'})
        finally:
            self.server.state.audit('checkout',attempt,started,status)

if __name__=='__main__':
    if os.environ.get('FT_TEST_ENVIRONMENT')!='true':
        raise SystemExit('Test environment required')
    root=Path(__file__).parent
    e=dict(x.split('=',1) for x in (root/'mock.env').read_text().splitlines() if x and not x.startswith('#'))
    server=m.ThreadingHTTPServer(('127.0.0.1',19090),Handler)
    server.state=m.State(e['VNPAY_HASH_SECRET'],e['VNPAY_TMN_CODE'],root/'state.json',root/'audit.jsonl')
    server.ipn_url='http://127.0.0.1:8083/api/v1/payments/vnpay/ipn'
    server.return_url='http://127.0.0.1:8083/api/v1/payments/vnpay/return'
    server.serve_forever()
