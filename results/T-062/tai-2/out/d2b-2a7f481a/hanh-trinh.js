import http from 'k6/http';
import exec from 'k6/execution';
import encoding from 'k6/encoding';
import crypto from 'k6/crypto';
import { sleep } from 'k6';
import { Counter, Trend } from 'k6/metrics';

if (__ENV.FT_TEST_ENVIRONMENT !== 'true') throw new Error('Isolated test environment required');
const cfg = JSON.parse(open('/scripts/cau-hinh.json'));
const seeds = JSON.parse(open('/secret/l1-tokens.json')).tokens;
const seconds = Number(__ENV.FT_LOAD_SECONDS || cfg.seconds);
const multiplier = Number(__ENV.FT_LOAD_MULTIPLIER || 1);
const standardRate = Number(__ENV.FT_JOURNEY_RATE || cfg.rate);
const stepSeconds = Number(__ENV.FT_LOAD_STEP_SECONDS || 0);
const rate = standardRate * multiplier;
if (!Number.isInteger(rate) || rate < 1 || rate > 300 || !Number.isInteger(seconds) || seconds < 1 || seconds > 3600) throw new Error('Invalid load configuration');
if (!Number.isInteger(stepSeconds) || stepSeconds < 0 || stepSeconds >= seconds) throw new Error('Step must be inside the run');
if (seeds.length < cfg.maxVUs * (stepSeconds ? 2 : 1)) throw new Error('A distinct session per VU is required, including both scenarios');
const mix = JSON.parse(__ENV.FT_MIX || JSON.stringify(cfg.mix));
if (Object.values(mix).some(v => !Number.isInteger(v) || v < 0) || Object.values(mix).reduce((a,b)=>a+b,0)!==100) throw new Error('Invalid mix');
const gcd=(a,b)=>b?gcd(b,a%b):a;
const unit=Object.values(mix).reduce((a,b)=>gcd(a,b),100);
const cycle=100/unit;
let stride=7; while(gcd(stride,cycle)!==1) stride++;
const schedule=[];
for(const journey of ['browse','purchase','abandon','cancel']) for(let i=0;i<mix[journey]/unit;i++) schedule.push(journey);

const responses = new Counter('route_responses');
const starts = new Counter('journey_started');
const ends = new Counter('journey_finished');
const failures = new Counter('journey_failed');
const refreshes = new Counter('token_refresh_success');
const refreshFailures = new Counter('token_refresh_failure');
const unauthorized = new Counter('gateway_401');
const latency = new Trend('journey_duration_ms', true);
let access, refresh, issued;
function arrival(stageRate, duration, start=0) {
  return {executor:'constant-arrival-rate',rate:stageRate,timeUnit:cfg.timeUnit,
    duration:duration+'s',startTime:start+'s',preAllocatedVUs:cfg.preAllocatedVUs,
    maxVUs:cfg.maxVUs,exec:'journey',gracefulStop:cfg.gracefulStop};
}
export const options = {
  scenarios: stepSeconds ? {
    standard:arrival(standardRate,stepSeconds),
    increased:arrival(rate,seconds-stepSeconds,stepSeconds),
  } : {journeys:arrival(rate,seconds)},
  systemTags:['status','method','name','scenario','expected_response','error_code'],
  summaryTrendStats:['avg','p(95)','p(99)','max'],
};
function randomHex(n) { return Array.from(new Uint8Array(crypto.randomBytes(n))).map(v=>v.toString(16).padStart(2,'0')).join(''); }
function uuid() { const h=randomHex(16); return h.slice(0,8)+'-'+h.slice(8,12)+'-4'+h.slice(13,16)+'-a'+h.slice(17,20)+'-'+h.slice(20); }
function token() {
  if (!access) {
    const seed=seeds[exec.vu.idInTest-1];
    if(!seed) { exec.test.abort('No session for VU'); return null; }
    access=seed.access_token; refresh=seed.refresh_token;
    issued=Number(JSON.parse(encoding.b64decode(access.split('.')[1],'rawurl','s')).iat)*1000;
  }
  if(Date.now()-issued < cfg.refreshAgeSeconds*1000) return access;
  const r=http.post(cfg.keycloak+'/realms/flash-ticket/protocol/openid-connect/token',
    {grant_type:'refresh_token',client_id:'frontend',refresh_token:refresh},
    {tags:{name:'Keycloak refresh',route:'auth',step:'refresh',journey:'auth'},timeout:'15s'});
  if(r.status!==200) {refreshFailures.add(1,{status:String(r.status)});exec.test.abort('Token refresh failed; secret omitted');return null;}
  const value=r.json();
  access=value.access_token; refresh=value.refresh_token;
  if(!access||!refresh) {exec.test.abort('Incomplete token refresh');return null;}
  issued=Number(JSON.parse(encoding.b64decode(access.split('.')[1],'rawurl','s')).iat)*1000;
  refreshes.add(1);
  return access;
}
function request(method,path,route,routeId,step,kind,body=null,key=null) {
  const t=token(); if(!t) throw new Error('No token');
  const headers={Authorization:'Bearer '+t,'Content-Type':'application/json'};
  if(key) headers['Idempotency-Key']=key;
  const sentUtc=new Date().toISOString();
  const r=http.request(method,cfg.gateway+path,body===null?null:JSON.stringify(body),
    {headers,tags:{name:route,route,routeId,step,journey:kind},timeout:'35s',redirects:0});
  responses.add(1,{route,routeId,step,journey:kind,status:String(r.status)});
  if(r.status===401) unauthorized.add(1,{route,step});
  console.log(JSON.stringify({type:'request',utc:new Date().toISOString(),sentUtc,requestId:r.headers['X-Request-Id']||null,correlationId:r.headers['X-Correlation-Id']||null,route,routeId,step,journey:kind,status:r.status}));
  let value;try{value=r.json();}catch(_){value={};}
  if(r.status<200||r.status>=300) throw new Error('HTTP '+r.status+' at '+step);
  return value && value.data!==undefined ? value.data : value;
}
function state(order,kind) {
  console.log(JSON.stringify({type:'order_state',utc:new Date().toISOString(),orderId:order.orderId,state:order.state,journey:kind}));
}
export function journey() {
  const kind=schedule[(exec.scenario.iterationInTest*stride)%cycle];
  const began=Date.now(); starts.add(1,{journey:kind});
  console.log(JSON.stringify({type:'journey_start',utc:new Date().toISOString(),scenario:exec.scenario.name,vu:exec.vu.idInTest,journey:kind,testEpochMs:exec.scenario.startTime-(exec.scenario.name==='increased'?stepSeconds*1000:0)}));
  try {
    request('GET','/api/v1/events','GET /api/v1/events','event','list',kind);
    request('GET','/api/v1/events/'+cfg.eventId,'GET /api/v1/events/{id}','event','detail',kind);
    request('GET','/api/v1/events/'+cfg.eventId+'/availability','GET /api/v1/events/{id}/availability','booking','availability',kind);
    if(kind==='browse') {ends.add(1,{journey:kind});return;}
    const body={eventId:cfg.eventId,customerEmail:'buyer@example.invalid',selection:{mode:'QUANTITY',items:[{ticketTypeId:cfg.ticketTypeId,quantity:1}]}};
    let order=request('POST','/api/v1/orders','POST /api/v1/orders','booking','create_order',kind,body,uuid()); state(order,kind);
    if(kind==='cancel') {
      order=request('POST','/api/v1/orders/'+order.orderId+'/cancel','POST /api/v1/orders/{id}/cancel','booking','cancel_order',kind,{});
      state(order,kind);if(order.state!=='CANCELLED') throw new Error('Cancel state mismatch');
    } else if(kind==='purchase') {
      const payment=request('POST','/api/v1/payments','POST /api/v1/payments','payment','create_payment',kind,{orderId:order.orderId},uuid());
      if(!payment.paymentUrl || !payment.paymentUrl.startsWith(cfg.mock+'/checkout?')) throw new Error('Expected isolated mock URL');
      const r=http.get(payment.paymentUrl,{tags:{name:'Mock checkout',route:'mock',step:'checkout',journey:kind},timeout:'35s',redirects:0});
      if(r.status!==200 || r.json('ipn.RspCode')!=='00' || r.json('returnStatus')!==302) throw new Error('Mock callback failed');
      const deadline=Date.now()+cfg.pollTimeoutSeconds*1000;
      do {
        order=request('GET','/api/v1/orders/'+order.orderId,'GET /api/v1/orders/{id}','booking','poll_order',kind); state(order,kind);
        if(['COMPLETED','ISSUANCE_FAILED','CANCELLED'].includes(order.state)) break;
        sleep(cfg.pollSeconds);
      } while(Date.now()<deadline);
      if(order.state!=='COMPLETED') throw new Error('Order incomplete');
      const tickets=request('GET','/api/v1/orders/'+order.orderId+'/tickets','GET /api/v1/orders/{id}/tickets','ticket','get_tickets',kind);
      if(tickets.issuanceState!=='COMPLETED'||!tickets.tickets||tickets.tickets.length!==1) throw new Error('Ticket count mismatch');
    }
    ends.add(1,{journey:kind});
  } catch(err) {
    failures.add(1,{journey:kind});
    console.log(JSON.stringify({type:'journey_error',utc:new Date().toISOString(),journey:kind,reason:String(err.message)}));
  } finally {
    latency.add(Date.now()-began,{journey:kind});
    console.log(JSON.stringify({type:'journey_end',utc:new Date().toISOString(),scenario:exec.scenario.name,vu:exec.vu.idInTest,journey:kind}));
  }
}
