import fs from 'node:fs/promises';

const base = 'results/T-065/kiem/003-trinh-duyet/';
const read = async file => JSON.parse((await fs.readFile(base + file, 'utf8')).replace(/^\uFEFF/, ''));
const journal = (await fs.readFile(base + 'nhat-ky-bam.jsonl', 'utf8')).trim().split('\n').map(line => JSON.parse(line));
const plan = (await read('mau-sau-plan.json')).cases;
const links = await read('kiem-lien-ket-that.json');
const operations = await read('kiem-thao-tac-that.json');
const services = await read('kiem-service-that.json');
const versions = await read('kiem-doi-ban-that.json');
const same = (row, pair, service, op, store) => row.ban === pair.ban && row.ca === pair.ca
  && (service === undefined || row.service === service)
  && (op === undefined || row.op === op)
  && (store === undefined || row.kho === store);
const actions = (tag, suffix) => journal.filter(row => row.stt <= 1366 && row.quan_sat_file?.endsWith(tag + suffix));
const identity = raw => {
  const url = new URL(raw);
  const get = key => url.searchParams.get(key);
  const ms = value => /^\d+$/.test(value) ? Number(value) : Date.parse(value);
  return { ban: get('var-ban'), ca: get('var-ca'), service: get('var-dv'), op: get('var-op'), from: ms(get('from')), to: ms(get('to')) };
};
const inWindow = (seen, pair) => seen.from === pair.cua_so_ms[0] && seen.to === pair.cua_so_ms[1] - 1;
const good = checks => Object.values(checks).every(Boolean);
const sourceFile = action => action.quan_sat_file;

if (links.length !== 60 || operations.length !== 25 || services.length !== 13 || versions.length !== 4) {
  throw Error('Tệp hiện tại không ở đúng mốc sau lần lưu cũ. Giữ nguyên.');
}
const saved = { links: links.length, operations: operations.length, services: services.length, versions: versions.length };
const failed = [];
for (const [pairIndex, pair] of plan.entries()) {
  if (pairIndex < 6 || pairIndex > 8) continue;
  const pairTag = 'sau-' + pairIndex + '-' + pair.ban.replaceAll('+', '_') + '-' + pair.ca + '-';
  const prefix = pairTag + pair.services[0].service + '-';
  if (pairIndex > 6) {
    const entry = actions(prefix, 'ban-chon.txt').at(-1);
    const before = identity(entry.url_truoc), after = identity(entry.url_sau);
    const checks = { ban: after.ban === pair.ban, ca: after.ca === before.ca && after.ca === pair.ca, service: after.service === before.service, window: inWindow(before, pair) && inWindow(after, pair) };
    if (!good(checks) || entry.loi) throw Error('Không xác nhận được đổi bản ' + pair.ban);
    versions.push({ utc: entry.utc, before, after, checks, dom: sourceFile(entry), phuc_hoi_tu_nhat_ky: entry.stt });
  }
  for (const service of pair.services) {
    const tag = pairTag + service.service + '-';
    if (!services.some(row => same(row, pair, service.service))) {
      const action = actions(tag, 'graph-view.txt').at(-1);
      const start = actions(tag, 'service-graph-p23.txt').at(-1);
      const last = [action, ...[0, 1, 2, 3].flatMap(i => actions(tag, 'graph-zoom' + i + '.txt'))].sort((a, b) => a.stt - b.stt).at(-1);
      const id = identity(last.url_sau);
      const dom = await fs.readFile(base + sourceFile(last), 'utf8');
      const graph = dom.split('\n').findIndex(line => line.includes('region "Đồ thị thao tác') && line.includes(service.service));
      const graphEnd = dom.split('\n').findIndex((line, i) => i > graph && /^    - '?region /.test(line));
      const graphText = dom.split('\n').slice(graph, graphEnd < 0 ? undefined : graphEnd).join('\n');
      if (id.ban !== pair.ban || id.ca !== pair.ca || id.service !== service.service || !inWindow(id, pair) || graph < 0 || !graphText.includes('Zoom out') || last.loi) {
        throw Error('Không xác nhận được đồ thị ' + tag);
      }
      const photo = 'anh/' + tag + 'graph';
      await fs.access(base + photo + '.jpg');
      services.push({ utc: last.utc, ban: pair.ban, ca: pair.ca, service: service.service, top1: pair.top1, top1_covered: pair.top1_covered, total_operations: service.tong_thao_tac, url: last.url_sau, graph_wait_ms: Date.parse(action.utc) - Date.parse(start.utc), anh: photo + '.png', dom: sourceFile(last), nodes_in_dom: graphText.includes('Node:'), kiem: 'Khôi phục URL, tiêu đề và thời gian từ nhật ký. Cần rà ảnh để xác nhận nút nhìn thấy.', phuc_hoi_tu_nhat_ky: last.stt });
    }
    for (const [i, op] of service.ops.entries()) {
      const detailAction = actions(tag, 'op-chi-tiet-' + i + '-p24.txt').at(-1);
      const linkAction = actions(tag, 'op-bang-chung-' + i + '-p25.txt').at(-1);
      if (!operations.some(row => same(row, pair, service.service, op.id))) {
        const id = identity(linkAction.url_sau);
        const [detail, evidence] = await Promise.all([detailAction, linkAction].map(row => fs.readFile(base + sourceFile(row), 'utf8')));
        const table = detail.split('\n').findIndex(line => line.includes('region "Chi tiết thao tác') && line.includes(op.ten));
        const lines = detail.split('\n');
        const end = lines.findIndex((line, n) => n > table && /^    - '?region /.test(line));
        const cells = role => lines.slice(table, end).flatMap(line => {
          const label = line.match(new RegExp("^\\s+- '?" + role + ' ("(?:[^"\\\\]|\\\\.)*")' + "'?:?$"));
          return label ? [JSON.parse(label[1])] : [];
        });
        const observed = evidence.split('\n').flatMap(line => {
          const match = line.match(/^\s+- \/url: (\/explore\?[^\s]+)$/);
          return match ? [match[1]] : [];
        });
        const checks = { op: id.op === op.id, ca: id.ca === pair.ca, ban: id.ban === pair.ban, service: id.service === service.service, window: inWindow(id, pair), links: op.lien_ket.every(link => observed.includes(link.url)), detail: table >= 0 && cells('gridcell').includes(op.ten) };
        if (!good(checks) || detailAction.loi || linkAction.loi) throw Error('Không xác nhận được thao tác ' + tag + i + ' ' + JSON.stringify(checks));
        operations.push({ utc: linkAction.utc, ban: pair.ban, ca: pair.ca, service: service.service, op: op.id, ten: op.ten, loai: op.loai, co_m1: op.co_m1, expected: op, observed_links: observed.map(href => ({ href })), detail: { headers: cells('columnheader'), rows: [cells('gridcell')] }, checks, url: linkAction.url_sau, dom: [sourceFile(detailAction), sourceFile(linkAction)], phuc_hoi_tu_nhat_ky: linkAction.stt });
      }
      for (const link of op.lien_ket) {
        if (links.some(row => same(row, pair, service.service, op.id, link.kho))) continue;
        const image = 'anh/' + tag + 'op' + i + '-' + link.kho + '.png';
        const row = journal.find(entry => entry.stt <= 1366 && entry.anh === image && entry.hanh_dong === 'Đọc Explore ' + link.kho);
        if (!row || row.ket_qua !== 'khop_nguon') {
          failed.push({ pair: pairIndex, service: service.service, op: op.id, kho: link.kho, stt: row?.stt });
          continue;
        }
        const before = identity(row.url_truoc);
        const [pane] = Object.values(JSON.parse(new URL(row.url_sau).searchParams.get('panes')));
        const query = pane.queries[0].query ?? pane.queries[0].expr;
        const range = [Number(pane.range.from), Number(pane.range.to)];
        if (before.ban !== pair.ban || before.ca !== pair.ca || before.service !== service.service || before.op !== op.id
            || pane.datasource !== link.kho || query !== link.truy_van || range[0] !== pair.cua_so_ms[0] || range[1] !== pair.cua_so_ms[1] - 1 || !good(row.quan_sat.checks)) throw Error('Không khôi phục được Explore ' + tag + i + ' ' + link.kho);
        const dom = image.slice(4).replace(/\.png$/, '.txt');
        await Promise.all([fs.access(base + dom), fs.access(base + image.replace(/\.png$/, '.jpg'))]);
        const hasData = row.quan_sat.co_du_lieu;
        links.push({ utc: row.utc, ban: pair.ban, ca: pair.ca, service: service.service, op: op.id, ten: op.ten, kho: link.kho, url: row.url_sau, datasource: pane.datasource, query, range, checks: row.quan_sat.checks, co_du_lieu: hasData, dom, anh: image, loai_rong: hasData ? null : 'iii', can_cu: hasData ? 'Nhật ký, DOM Explore và ảnh' : 'Cần đối chiếu API cùng truy vấn và khung giờ.', phuc_hoi_tu_nhat_ky: row.stt });
      }
    }
  }
}

if (links.length !== 88 || operations.length !== 36 || services.length !== 18 || versions.length !== 6
 || failed.length !== 2 || failed[0].stt !== 1366 || failed[1].kho !== 'prometheus') throw Error('Phạm vi khôi phục vượt mốc nhật ký: ' + JSON.stringify({ links: links.length, operations: operations.length, services: services.length, versions: versions.length, failed }));
const results = { 'kiem-lien-ket-that.json': links, 'kiem-thao-tac-that.json': operations, 'kiem-service-that.json': services, 'kiem-doi-ban-that.json': versions };
const report = { utc: new Date().toISOString(), saved, restored: { links: links.length - saved.links, operations: operations.length - saved.operations, services: services.length - saved.services, versions: versions.length - saved.versions }, pending: failed };
if (process.argv.includes('--write')) {
  await fs.writeFile(base + 'phuc-hoi-sau-nen-ngu-canh.json', JSON.stringify(report, null, 2) + '\n');
  for (const [file, value] of Object.entries(results)) await fs.writeFile(base + file, JSON.stringify(value, null, 2) + '\n');
  await fs.writeFile(base + 'sau-tien-do.json', JSON.stringify({ pair: 8, service: 1, op: 1, link: 1, stage: 'link', pending: null, utc: report.utc }, null, 2) + '\n');
}
console.log(JSON.stringify(report));
