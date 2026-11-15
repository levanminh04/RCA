import fs from 'node:fs/promises';
import crypto from 'node:crypto';
import path from 'node:path';

const base = 'results/T-065';
const output = `${base}/kiem/003-trinh-duyet`;
const read = async file => JSON.parse((await fs.readFile(file, 'utf8')).replace(/^\uFEFF/, ''));
const write = (file, value) => fs.writeFile(file, JSON.stringify(value, null, 2) + '\n');
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const group = (rows, field) => Object.fromEntries(Object.entries(Object.groupBy(rows, row => row[field])).map(([key, values]) => [key, values.length]));

async function summarize() {
  const pages = await read(`${output}/doi-chieu-hien-thi.json`);
  const links = await read(`${output}/kiem-lien-ket-that.json`);
  const panels = await read(`${output}/panel-rong.json`);
  const operations = await read(`${output}/kiem-thao-tac-that.json`);
  const services = await read(`${output}/kiem-service-that.json`);
  const versions = await read(`${output}/kiem-doi-ban-that.json`);
  const position = await read(`${output}/sau-tien-do.json`);
  const plan = await read(`${output}/mau-sau-plan.json`);
  const original = await read(`${base}/codex/manifest-L4.json`);
  const snapshotFile = 'kiem/002/api-snapshot.json';
  const snapshotBytes = await fs.readFile(`${base}/${snapshotFile}`);
  if (original.files[snapshotFile].sha256 !== sha(snapshotBytes)) throw Error('Hash snapshot L4 lệch');
  const snapshot = await read(`${base}/${snapshotFile}`);
  const currentResults = (await fs.readFile(`${output}/api-doi-chieu-rong-tiep-nhan.jsonl`, 'utf8').catch(() => '')).replace(/^\uFEFF/, '').trim().split('\n').filter(Boolean).map(line => JSON.parse(line));
  currentResults.push(await read(`${output}/loki-rong-1ad-event-api.json`));
  currentResults.push(await read(`${output}/loki-rong-2e2a-booking-api.json`));
  const images = new Set(await fs.readdir(`${output}/anh`));
  const expected = plan.cases.flatMap(pair => pair.services.flatMap(service => service.ops.flatMap(operation => operation.lien_ket.map(link => ({
    ban: pair.ban, ca: pair.ca, service: service.service, op: operation.id, kho: link.kho
  })))));
  const key = row => [row.ban, row.ca, row.service, row.op, row.kho].join('/');
  const observed = new Map(links.map(link => [key(link), link]));
  const recheckLinks = [...observed.values()].filter(link => link.checks && !Object.values(link.checks).every(Boolean));
  const byPage = new Map(pages.map(page => [`${page.ban}/${page.ca}`, page]));
  const blankPanels = [];
  const falseBlankPanels = [];
  const unique = new Set();
  // Các quan sát rộng được thu trước UI-04. Dùng đúng lời noValue của lượt đó.
  const dash = await read(`${base}/grafana-l5/t065-l4-rca-truoc-ui04.json`);
  for (const panel of panels) {
    const id = [panel.ban, panel.ca, panel.service, panel.panel].join('/');
    if (unique.has(id)) continue;
    unique.add(id);
    const page = byPage.get(`${panel.ban}/${panel.ca}`);
    const saved = page?.panel_checks?.panels?.find(item => Number(item.id.split('-').at(-1)) === panel.panel);
    const actual = saved?.text ?? panel.quan_sat;
    const data = dash.panels.find(item => item.id === panel.panel);
    const noValue = data?.fieldConfig?.defaults?.noValue;
    const tableHasData = data?.type === 'table' && actual !== undefined && noValue && actual.includes(noValue) && !actual.trimEnd().endsWith(noValue);
    const ordinaryNull = noValue === '—' || (data?.type === 'timeseries' && actual?.includes('Series color'));
    if (tableHasData || ordinaryNull) {
      falseBlankPanels.push({ key: id, panel: panel.panel, reason: tableHasData || data?.type === 'timeseries' ? 'Có bảng hoặc chú giải chuỗi. noValue được dùng cho một ô hoặc một chuỗi riêng.' : 'Dấu gạch trong dữ liệu hay tiêu đề không chứng minh panel rỗng.' });
      continue;
    }
    const record = snapshot[`${panel.ca}/${panel.service}`];
    const query = record?.queries.find(item => item.panel === panel.panel);
    const params = page ? new URL(page.url).searchParams : null;
    const epoch = value => /^\d+$/.test(value ?? '') ? Number(value) : Date.parse(value);
    const exactWindow = record?.window[0] === epoch(params?.get('from')) && record?.window[1] === epoch(params?.get('to'));
    const result = { ...panel };
    if (query && exactWindow) {
      result.snapshot = { path: `${base}/${snapshotFile}`, pointer: `/${panel.ca}~1${panel.service}/queries/${record.queries.indexOf(query)}`, utc: query.utc, status: query.trang_thai, rows: query.so_dong, query: query.request, window: record.window };
      result.loai = query.trang_thai === 'rong' && query.so_dong === 0 ? 'i' : 'iii';
      result.can_cu = result.loai === 'i' ? 'Cùng ca, service, panel và cửa sổ. Snapshot L4 cũng trả 0 dòng.' : 'Snapshot L4 có trạng thái khác. Cần truy vấn lại đúng biểu thức và cửa sổ tại thời điểm kiểm.';
      const latest = currentResults.find(item => item.ca === panel.ca && item.service === panel.service && item.panel === panel.panel && Number(item.range.from) === record.window[0] && Number(item.range.to) === record.window[1]);
      if (result.loai === 'iii' && latest?.state === 'co_du_lieu') {
        result.api_tiep_nhan = latest;
        result.can_cu = 'Snapshot L4 và API lúc tiếp nhận đều có dữ liệu. Thiếu query inspector của đúng lượt Chrome để tách trạng thái tải, khác tham số truy vấn hoặc lỗi hiển thị.';
      }
    }
    blankPanels.push(result);
  }
  const blankLinks = links.filter(link => !link.co_du_lieu).map(link => {
    const record = snapshot[`${link.ca}/${link.service}`];
    const exact = record?.window[0] === link.range[0] && record?.window[1] === link.range[1] ? record.queries.find(q => q.kho === link.kho && (q.request.query ?? q.request.expr) === link.query) : undefined;
    const latest = currentResults.find(item => item.ca === link.ca && item.service === link.service && item.kho === link.kho && item.query === link.query && Number(item.range.from) === link.range[0] && Number(item.range.to) === link.range[1]);
    const accepted = link.loai_rong === 'i' || exact?.trang_thai === 'rong' || latest?.state === 'rong';
    return { key: key(link), dom: link.dom, query: link.query, range: link.range, loai: accepted ? 'i' : 'iii', api_tiep_nhan: latest, can_cu: link.loai_rong === 'i' ? link.can_cu : latest?.state === 'rong' ? 'Snapshot L4 không ghi truy vấn thao tác này. API lúc tiếp nhận cùng query và cửa sổ trả HTTP 200, 0 dòng.' : exact ? `Snapshot L4 trùng truy vấn, trạng thái ${exact.trang_thai}` : 'Snapshot L4 không có chính xác truy vấn thao tác này. Cần đối chiếu API cùng truy vấn và cửa sổ.' };
  });
  const folderBefore = await read(`${output}/may-truoc.json`);
  // UI06 final inventory preserves may-cuoi.json as the earlier observation.
  const finalInventory = (await fs.readdir(output)).includes('may-ui06-cuoi.json') ? 'may-ui06-cuoi.json' : 'may-cuoi.json';
  const folderAfter = await read(`${output}/${finalInventory}`);
  const folderPlan = await read(`${output}/folder-plan.json`);
  const provision = '/opt/flash-ticket-obs/pinned/provisioning/dashboards';
  const folderFiles = [];
  for (const entry of folderPlan.moves) {
    const archive = !entry.name.startsWith('t065-l4-');
    const oldFile = `${provision}/${entry.name}`;
    const newFile = `${provision}/${entry.dir}/${entry.name}`;
    const before = folderBefore.files[oldFile].sha256;
    const after = folderAfter.files[newFile]?.sha256;
    const local = archive ? before : sha(await fs.readFile(`${base}/grafana-l4/${entry.name}`));
    folderFiles.push({ file: entry.name, oldFile, newFile, before, after, archive, match: after === local });
  }
  if (folderFiles.some(file => !file.match)) throw Error('Hash sáu dashboard trên máy không khớp');
  await write(`${output}/doi-chieu-hash-may-l5.json`, { files: folderFiles, provider: { before: folderBefore.files[`${provision}/provider.yaml`], after: folderAfter.files[`${provision}/provider.yaml`] }, new_index: folderAfter.files[`${provision}/${folderPlan.new_dir}/t065-l5-muc-luc.json`], compose_unchanged: folderBefore.files['/opt/flash-ticket-obs/pinned/compose.json'].sha256 === folderAfter.files['/opt/flash-ticket-obs/pinned/compose.json'].sha256 });
  const summary = {
    utc: new Date().toISOString(), pages: pages.length, pages_passed: pages.filter(page => page.status === 'dat_dom').length, pages_by_version: group(pages, 'ban'), page_png_missing: pages.filter(page => !images.has(path.basename(page.anh))).map(page => page.anh),
    visible_query_errors: pages.flatMap(page => page.panel_checks?.errors ?? []).length,
    operations: operations.length, services: services.length, switches: versions.length, deep_pairs_completed: position.pair,
    links_expected: expected.length, links_observed: observed.size, links_by_store: group([...observed.values()], 'kho'), links_with_data_by_store: group([...observed.values()].filter(link => link.co_du_lieu), 'kho'),
    links_without_pending_check: observed.size - recheckLinks.length,
    links_to_recheck: recheckLinks.map(link => ({ key: key(link), checks: link.checks, dom: link.dom, anh: link.anh })),
    link_png_missing: [...observed.values()].filter(link => link.anh && !images.has(path.basename(link.anh))).map(link => link.anh),
    links_missing: expected.filter(entry => !observed.has(key(entry))), blank_panels_by_class: group(blankPanels, 'loai'), blank_links_by_class: group(blankLinks, 'loai'),
    pending: { pair: position.pair, service: position.service, op: position.op, link: position.link, tabId: position.pending?.tabId, kho: position.pending?.kho }
  };
  await write(`${output}/doi-chieu-rong-snapshot.json`, { panels: blankPanels, false_positives: falseBlankPanels, links: blankLinks });
  await write(`${output}/tien-do.json`, summary);
  console.log(JSON.stringify({ ...summary, links_missing: summary.links_missing.length }));
}

async function manifest() {
  const old = await read(`${base}/codex/manifest-L4.json`);
  const files = {};
  for (const file of (await fs.readdir(base, { recursive: true, withFileTypes: true })).filter(x => x.isFile())) {
    const absolute = path.join(file.parentPath, file.name);
    const rel = path.relative(base, absolute).replaceAll('\\', '/');
    if (rel === 'manifest.json' || (!Object.hasOwn(old.files, rel) && /^codex\/L[34]-/.test(rel) && rel !== 'codex/manifest-L4.json')) continue;
    const bytes = await fs.readFile(absolute);
    files[rel] = { sha256: sha(bytes), bytes: bytes.length };
  }
  const taskFile = 'tasks/T-065-giao-dien-grafana/LOG.md';
  const logBytes = await fs.readFile(taskFile);
  const status = await read(`${base}/codex/L5-trang-thai.json`);
  const newFiles = Object.keys(files).filter(name => !Object.hasOwn(old.files, name)).sort();
  const modified = Object.keys(files).filter(name => old.files[name] && old.files[name].sha256 !== files[name].sha256).sort();
  const missing = Object.keys(old.files).filter(name => !files[name]);
  // README-L4 documents the authorized UI06 URL change; source data stays pinned.
  const allowedModified = new Set(['CHECKPOINT.md', 'README-L4.md', 'XONG.md', 'thay-doi-may.md', 'prompt-ban-giao.md', 'l4-dashboard.mjs', 'grafana-l4/t065-l4-rca.json', 'grafana-l4/t065-l4-phat-lai.json']);
  if (missing.length || modified.some(name => !allowedModified.has(name))) throw Error(`Ngoài phạm vi: ${JSON.stringify({ missing, modified })}`);
  await write(`${base}/manifest.json`, { utc: new Date().toISOString(), status: status.trang_thai, prior_manifest: 'codex/manifest-L4.json', excluded: ['manifest.json (self hash)', 'codex/L3-* và codex/L4-* của điều phối, nếu chưa ghim trong L4'], task_log: { file: taskFile, sha256: sha(logBytes), bytes: logBytes.length }, new_files: newFiles, modified_files: modified, files });
  console.log(JSON.stringify({ new_files: newFiles.length, modified_files: modified, hashed: Object.keys(files).length, missing }));
}

if (process.argv[2] === 'manifest') await manifest();
else await summarize();
