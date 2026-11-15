import http from 'k6/http';
import exec from 'k6/execution';
import encoding from 'k6/encoding';
import { check } from 'k6';
import { Counter } from 'k6/metrics';

// Derived from deploy/rca-test/workload.js, read-only source in platform repo.
if (__ENV.FT_TEST_ENVIRONMENT !== 'true') throw new Error('Isolated test environment required');
const config = JSON.parse(open('/scripts/cau-hinh.json'));
const machine = __ENV.FT_MACHINE || 'tai';
if (!config.targets[machine]) throw new Error('Expected machine tai or obs');
const base = __ENV.FT_GATEWAY_URL || config.targets[machine].gateway;
const tokenUrl = (config.targets[machine].keycloak + '/realms/flash-ticket/protocol/openid-connect/token');
const fixtures = JSON.parse(open('/scripts/fixtures.json'));
const seed = JSON.parse(open('/secret/tokens.json'));
const rate = Number(__ENV.FT_LOAD_RATE || config.FT_LOAD_RATE);
const seconds = Number(__ENV.FT_LOAD_SECONDS || config.FT_LOAD_SECONDS);
if (!Number.isInteger(rate) || rate < 1 || rate > 100 || !Number.isInteger(seconds) || seconds < 1 || seconds > 3600) {
  throw new Error('Declare rate 1..100 and duration 1..3600 seconds');
}
if (!fixtures.events.length || !fixtures.orders.length) throw new Error('Prepared event/order fixtures required');
let access = seed.access_token;
let refresh = seed.refresh_token;
function issuedAt(token) {
  return Number(JSON.parse(encoding.b64decode(token.split('.')[1], 'rawurl', 's')).iat) * 1000;
}
let refreshedAt = issuedAt(access);
const refreshes = new Counter('token_refresh_success');
const refreshFailures = new Counter('token_refresh_failure');
const accepted = new Counter('gateway_accepted');
const throttled = new Counter('gateway_throttled');
const routeResponses = new Counter('route_responses');
export const options = {
  scenarios: {common_routes: {
    executor: 'constant-arrival-rate', rate, timeUnit: '1s', duration: String(seconds) + 's',
    preAllocatedVUs: config.preAllocatedVUs, maxVUs: config.maxVUs, exec: 'readMix', gracefulStop: '40s',
  }},
  summaryTrendStats: ['avg', 'p(95)', 'p(99)', 'max'],
  // Do not serialize URLs with auth parameters, request headers, or response bodies.
  systemTags: ['status', 'method', 'name', 'scenario', 'expected_response', 'error_code'],
};
function accessToken() {
  if (Date.now() - refreshedAt < config.refreshAgeSeconds * 1000) return access;
  const response = http.post(tokenUrl, {
    grant_type: 'refresh_token', client_id: 'frontend', refresh_token: refresh,
  }, {tags: {name: 'Keycloak refresh', route: 'auth'}, timeout: '15s', responseType: 'text'});
  if (response.status !== 200) {
    refreshFailures.add(1, {status: String(response.status)});
    exec.test.abort('Keycloak refresh failed; secret values omitted');
    return null;
  }
  let value;
  try { value = response.json(); } catch (_) { exec.test.abort('Invalid token response'); return null; }
  if (!value.access_token || !value.refresh_token) { exec.test.abort('Incomplete token response'); return null; }
  access = value.access_token; refresh = value.refresh_token; refreshedAt = issuedAt(access);
  refreshes.add(1);
  return access;
}
export function readMix() {
  const token = accessToken();
  if (!token) return;
  const iteration = exec.scenario.iterationInTest;
  const event = fixtures.events[iteration % fixtures.events.length];
  const order = fixtures.orders[iteration % fixtures.orders.length];
  const slot = iteration % 100;
  let path, route;
  if (slot < 50) {path = '/api/v1/events/' + event.eventId; route = 'GET /api/v1/events/{id}';}
  else if (slot < 75) {path = '/api/v1/orders/' + order.orderId; route = 'GET /api/v1/orders/{id}';}
  else if (slot < 90) {path = '/api/v1/orders/' + order.orderId + '/payment'; route = 'GET /api/v1/orders/{id}/payment';}
  else {path = '/api/v1/orders/' + order.orderId + '/tickets'; route = 'GET /api/v1/orders/{id}/tickets';}
  const response = http.get(base + path, {
    headers: {Authorization: 'Bearer ' + token}, tags: {name: route, route}, timeout: '35s',
    redirects: 0, responseType: 'none',
  });
  routeResponses.add(1, {route, status: String(response.status)});
  if (response.status === 429) throttled.add(1, {route});
  else if (response.status >= 200 && response.status < 400) accepted.add(1, {route});
  check(response, {'successful baseline response': r => r.status === 200}, {route});
}
// Opaque run code stays in output directory/container name, never in request headers/URLs.
