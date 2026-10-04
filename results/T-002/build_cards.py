"""Render T-002 cards from saved local and public counts; no raw-data reads."""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
LOCAL = HERE / "local-inspection" / "run-002"
PUBLIC = HERE / "public-metadata" / "run-002"


def mdtable(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)] + ["| " + " | ".join(str(v) for v in row) + " |" for row in rows])


def num(value):
    return f"{value:,}".replace(",", ".")


def pct(value):
    return f"{100 * value:.2f}%".replace(".", ",")


def outside_root_channels(channels, cases):
    """Use the same reporting scope as the saved all-metric OR rates."""
    labels = pd.DataFrame([{k: c[k] for k in ("case", "dataset", "root")} for c in cases])
    data = channels.merge(labels, on="case", validate="many_to_one")
    data[["entity", "channel"]] = data.metric.str.rsplit("_", n=1, expand=True)
    business = data.entity.str.endswith("service") | data.entity.eq("frontend")
    return data.loc[business & data.entity.ne(data.root)].copy()


def memory_rows(channels, probes, ds):
    rows = []
    for q, group in channels.loc[(channels.dataset == ds) & (channels.channel == "mem")].groupby("q"):
        means = []
        for window in ("control", "post"):
            valid = group.loc[group[f"{window}_valid_rows"] > 0].copy()
            valid["rate"] = valid[f"{window}_exceed_rows"] / valid[f"{window}_valid_rows"]
            means.append(valid.groupby("case").rate.mean().mean())
        all_metrics = probes.loc[(probes.dataset == ds) & (probes.q == q) & (probes.signal_group == "all_metrics")]
        rows.append([q, pct(means[0]), pct(means[1]),
                     pct(all_metrics.control_mean_service_rate.mean()), pct(all_metrics.post_mean_service_rate.mean())])
    return rows


def flat_or_bounds(channels, rates, ds, q):
    """Bounds from marginal counts; do not reconstruct unobserved intersections."""
    flat = channels.loc[(channels.dataset == ds) & (channels.q == q) & channels.flat_band]
    subset = rates.loc[(rates.dataset == ds) & (rates.q == q) &
                       (rates.signal_group == "all_metrics") & rates.business_name_heuristic & ~rates.is_root]
    bounds = []
    for window in ("control", "post"):
        counts = flat.groupby(["case", "entity"])[f"{window}_exceed_rows"].agg(["max", "sum"])
        valid = subset.loc[subset[f"{window}_valid_rows"] > 0].merge(
            counts, on=["case", "entity"], how="left", validate="one_to_one").fillna({"max": 0, "sum": 0})
        valid["lower"] = valid["max"] / valid[f"{window}_valid_rows"]
        valid["upper"] = valid[["sum", f"{window}_exceed_rows"]].min(axis=1) / valid[f"{window}_valid_rows"]
        means = valid.groupby("case")[["lower", "upper"]].mean().mean()
        bounds.append(f"{pct(means['lower'])}–{pct(means['upper'])}")
    return bounds


def main():
    summaries = json.loads((LOCAL / "summary.json").read_text(encoding="utf-8"))
    public = {r["dataset"].lower().replace("-", ""): r for r in json.loads((PUBLIC / "count-summary.json").read_text(encoding="utf-8"))}
    cases = json.loads((LOCAL / "cases.json").read_text(encoding="utf-8"))
    positions = pd.read_csv(LOCAL / "all-service-positions.csv")
    probes = pd.read_csv(LOCAL / "probe-case-summary.csv")
    channels = pd.read_csv(LOCAL / "symptom-channel-bands.csv")
    rates = pd.read_csv(LOCAL / "symptom-entity-rates.csv")
    reporting_channels = outside_root_channels(channels, cases)
    cells = pd.read_csv(PUBLIC / "root-fault-cells.csv")
    text = ["# Thẻ dataset họ RCAEval — T-002",
            "Kiểm dữ liệu ngày 02/10/2026; bổ sung diễn giải R1–R5 ngày 04/10 sau phản biện và Minh duyệt. Mục đích: cung cấp bằng chứng cho tiêu chí MRP §4/P2, phục vụ RQ1/RQ3 và G1. Đây là thẻ mô tả, chưa chọn dataset hoặc cách chia. Bốn bộ cùng tác giả/công cụ/stack không đáp ứng riêng tiêu chí bộ độc lập. Chỉ so với ứng viên khác khi có đủ thẻ, theo Q-31.",
            "**USER_CONFIRMED:** SPEC cho phép kiểm 30 ca dev RE2-TT và 5 ca mẫu đang có. Đã kiểm schema cả 35 ca; khảo sát metric của 32 ca thuộc bốn bộ mục tiêu. Không mở dữ liệu khóa. Không chạy phương pháp RCA. Không thêm quyết định **DECIDED**.",
            "## Căn cứ chung và cách đọc",
            "- [Mẫu thẻ dùng chung](mau-the-dataset.md). Các mục 1–10 dưới mỗi bộ theo đúng mẫu; bảng khả năng chấm và phép tính chung ở cuối được áp dụng cho từng thẻ. FACT từ metadata chỉ xác nhận tên/file/số byte; FACT từ telemetry chỉ áp dụng phần đã kiểm. OPEN ghi đầu vào/người cần giải quyết. CANDIDATE không phải quyết định.",
            "- [Nguồn công khai](public-sources.md), [số đếm toàn kho](public-metadata/run-002/count-summary.json), [từng ô nhãn](public-metadata/run-002/root-fault-cells.csv). Snapshot README, LICENSE, bài v2 và tree nằm trong thư mục nguồn của lượt đó; URL/revision/hash nằm trong [manifest nguồn](public-metadata/run-002/source-manifest.json).",
            "- [Số đo tổng hợp cục bộ](local-inspection/run-002/summary.json), [từng ca và đồ thị](local-inspection/run-002/cases.json), [schema từng file](local-inspection/run-002/schemas.json), [danh sách file đã đọc](local-inspection/run-002/manifest.json). [Script kiểm](inspect_local.py) và [script tổng hợp](summarize_local.py) giữ số trung gian; lệnh tái lập ở LOG.",
            "- FACT nguồn: giấy phép dữ liệu được HF và README tác giả khai báo MIT. README nói dữ liệu/code do tác giả cung cấp dùng MIT. File LICENSE nêu điều kiện giữ thông báo bản quyền. Trạng thái truy cập được kiểm qua metadata và các mẫu có sẵn; chưa tải lại toàn kho.",
            "- FACT nguồn: RE2 dùng stress-ng cho cpu/mem/disk/socket và tc cho delay/loss. RE3 sửa mã nguồn: f1 sai giá trị tham số; f2 thiếu tham số; f3 thiếu lời gọi hàm; f4 sai giá trị trả về; f5 thiếu xử lý ngoại lệ. Thu thập trên Kubernetes bằng Prometheus/cAdvisor/Istio, Jaeger và Vector/Loki/Elasticsearch. Bài mô tả tải ngẫu nhiên 10–200 requests/s. Nguồn: bài v2 §3.1–3.3 trong snapshot đã lưu. Tên lỗi không chứng minh lỗi biểu hiện ở mọi tín hiệu.",
            "- Mốc nhãn là Unix timestamp lúc tiêm, không phải onset (lúc bắt đầu biểu hiện) độc lập. Bài v2 §3 nói mỗi ca có service gốc và root cause indicator (chỉ báo nguyên nhân gốc); §3.2 mô tả chỉ báo metric/log/response code theo loại lỗi. Tuy nhiên tree đã lưu chỉ có 8 `root_cause.txt`, đều ở RE3-SS; bốn bộ mục tiêu không có file tên này. Chưa xác minh nhãn chỉ báo chi tiết trong hình thức khác, chưa có nhãn vùng ảnh hưởng, operation gốc hoặc từng trace bất thường ở nguồn đã đọc. Không suy từ tên fault thành ground truth mới. Đối chiếu lời nguồn và artifact ở [public-sources.md](public-sources.md); các giới hạn chấm ở bảng cuối."]

    target_cases = [c for c in cases if c["dataset"] in public and c["dataset"] in ("re2tt", "re2ob", "re3tt", "re3ob")]
    symmetric = sum(c["inject_time"] - c["metric_time_min"] == c["metric_time_max"] - c["inject_time"] for c in target_cases)
    trace_gap = max(abs(c["trace"][f"epoch_{edge}"] - c[f"metric_time_{edge}"]) for c in target_cases for edge in ("min", "max"))
    log_cases = [c for c in target_cases if c["has_logs"]]
    log_gap = max(abs(c["log"][f"timestamp_{edge}"] - c[f"metric_time_{edge}"]) for c in log_cases for edge in ("min", "max"))
    text.append(f"- **FACT trên mẫu:** {symmetric}/{len(target_cases)} ca mục tiêu có injection đúng giữa timestamp metric đầu/cuối. Biên trace của {len(target_cases)} ca lệch biên metric dưới {int(trace_gap) + 1} giây; log của {len(log_cases)} ca lệch tối đa {log_gap:g} giây. Nguồn: cases.json. Đây là biên hàng quan sát, chưa chứng minh cơ chế exporter cắt cả ba nguồn. Bỏ `inject_time.txt` vẫn chưa loại nguy cơ suy injection từ biên file; chưa có bộ phát hiện nào trong task bị chứng minh khai thác đường này. Phần chưa đọc, gồm RE3-OB, còn OPEN.")

    for ds in ("re2tt", "re2ob", "re3tt", "re3ob"):
        s, p = summaries[ds], public[ds]
        name = p["dataset"]
        local_cases = [c for c in cases if c["dataset"] == ds]
        n = s["n_inspected"]
        system = "Train Ticket" if ds.endswith("tt") else "Online Boutique"
        sample_text = "30 ca dev, 10 ô × 3 lần lặp; không mở 60 ca khóa" if ds == "re2tt" else "; ".join(c["case"] for c in local_cases) if n else "0 ca; không có mẫu cục bộ"
        text += [f"## {name}", "### 1. Danh tính, nguồn và phạm vi đã kiểm",
                 f"**FACT:** {system}, họ RCAEval của Pham et al.; nguồn và giấy phép MIT áp dụng theo mục chung. Toàn kho có {p['n_cases']} ca theo directory tại revision trong manifest. Telemetry đã kiểm {n}/{p['n_cases']} ca: {sample_text}. Các ca còn lại chỉ đếm metadata file công khai, không đọc dữ liệu đo. Ngày kiểm: 02/10/2026.",
                 "### 2. Bảng tiêu chí 1–9"]
        trace_fact = f"FACT trên {n} ca: có traceID/spanID/parentSpanID; resolve {pct(s['parent_resolution_fraction'])}" if n else "OPEN — chưa kiểm schema; metadata có 30 file trace"
        metric_fact = f"FACT trên {n} ca: metric có; log {s['n_log_cases']}/{n}; không có cột trace ID" if n else "OPEN — chưa kiểm nội dung; metadata có metric/log"
        normal_fact = f"FACT: {s['normal_rows_min']}–{s['normal_rows_max']} điểm 1 giây trước tiêm; đủ cho khảo sát này, chưa khẳng định đủ học phương pháp" if n else "OPEN — chưa kiểm độ dài trên file; bài mô tả 10 phút"
        criteria = [
            [1, "FACT: công khai, MIT; metadata truy cập được", "Nguồn chung; chưa tải/kiểm toàn bộ file"],
            [2, "FACT nguồn: service gốc, fault, repeat và lúc tiêm", "Onset/end/affected-region chưa có; tiêm chưa chắc gây triệu chứng ngay"],
            [3, trace_fact, "Mất cha có thể do lấy mẫu/cắt cửa sổ/instrumentation; không suy topology đầy đủ"],
            [4, metric_fact, "File có mặt chưa bảo đảm nội dung; log có thể chỉ nối được service + thời gian"],
            [5, f"FACT: {p['n_root_services']} service gốc; vị trí ở mục 3", "Danh tính service, vị trí và loại lỗi có thể confound (lẫn tác động)"],
            [6, "FACT nguồn: tài nguyên + mạng; không có lỗi mã nguồn trong bộ" if ds.startswith("re2") else "FACT nguồn: mã nguồn; không có tài nguyên/mạng trong bộ", "Một bộ riêng không đủ ba nhóm; loại lỗi không bảo đảm có cùng mức triệu chứng" if ds.startswith("re2") else "Nhãn chỉ báo chi tiết chưa xác minh; RE3-TT mẫu có status trống, log mới rà regex (mục 4); RE3-OB chưa có mẫu"],
            [7, "FACT khảo sát: số vượt ngưỡng theo ba phân vị ở mục 6" if n else "OPEN — chưa kiểm; không có mẫu", "OR nhiều kênh và mem có thể chiếm phần lớn mức vượt; tùy bộ/ngưỡng. Tiêu chí lan truyền nhân quả vẫn chưa xác lập"],
            [8, normal_fact, "Trước tiêm chưa chắc sạch/đại diện; warm-up và drift có thể làm ngưỡng lệch"],
            [9, "FACT phả hệ: cùng nhóm RCAEval/công cụ/stack", "OPEN về bộ dataset chọn; cần ứng viên độc lập của T-003/G1"],
        ]
        text.append(mdtable(["Tiêu chí", "Kết quả/trạng thái", "Giới hạn/giải thích khác"], criteria))
        text += ["### 3. Nhãn, số ca và khả năng phân xử",
                 f"**FACT metadata:** {p['n_root_services']} service gốc, {p['n_faults']} loại lỗi, {p['n_observed_root_fault_cells']}/{p['possible_root_fault_cells']} ô gốc × lỗi có ca; {p['cell_repetition_min']}–{p['cell_repetition_max']} lần lặp/ô. Nguồn: count-summary và root-fault-cells ở mục chung. Không coi ô thiếu là ca thất bại.",
                 mdtable(["Service gốc", "Số ca công khai"], p["root_services_and_case_counts"].items()),
                 "Loại lỗi / số ca: " + "; ".join(f"`{k}`: {v}" for k, v in p["faults_and_case_counts"].items()) + "."]
        if ds.startswith("re3"):
            data = cells.loc[cells.dataset == name]
            text.append(mdtable(["Gốc", "Lỗi", "Ca/lặp"], [[r.root_service, r.fault, r.n_cases] for r in data.itertuples()]))
        degrees = positions.loc[(positions.dataset == ds) & (positions.window == "pre_injection")]
        degree_rows = []
        for root in p["root_services_and_case_counts"]:
            g = degrees.loc[degrees.service == root]
            distribution = g.groupby(["in_degree", "out_degree"]).size()
            value = "; ".join(f"({i}, {o}) ở {count}/{n} ca" for (i, o), count in distribution.items()) if len(g) else "OPEN — chưa kiểm; không có mẫu"
            degree_rows.append([root, value])
        text += [mdtable(["Service gốc", "Bậc (vào, ra) trong trace trước tiêm"], degree_rows),
                 "Cạnh là parent-service → child-service khác tên, resolve bằng (traceID, spanID) trong cùng ca. Bậc là số hàng xóm phân biệt, chưa phải quan hệ có kiểu hay nhân quả. Cửa sổ trước tiêm lọc theo start của child; parent được tra trong cùng file. Không đặt ngưỡng hub. Một node không có cạnh quan sát có thể do thiếu instrumentation hoặc workload không gọi nó."]
        if n:
            topology_text = "; ".join(f"{g['nodes']} nút/{g['edges']} cạnh ở {g['n_cases']}/{n} ca" for g in s["topology"]["full"])
            text.append(f"FACT: đồ thị toàn cửa sổ có {len(s['topology']['full'])} cấu trúc: {topology_text}. Đồ thị trước tiêm của từng ca có cùng tập nút/cạnh với toàn cửa sổ (đối chiếu cases.json). Có thể cấu trúc ổn định thật, hoặc workload/độ phủ đo giới hạn cấu trúc quan sát; chưa khái quát toàn bộ hệ.")
        if ds == "re2tt":
            root_rows = []
            for root in p["root_services_and_case_counts"]:
                root_cases = [c for c in local_cases if c["root"] == root]
                distribution = {}
                for c in root_cases:
                    degree = next(d for d in c["trace"]["graphs"]["pre_injection"]["degrees"] if d["service"] == root)
                    pair = degree["in_degree"], degree["out_degree"]
                    distribution[pair] = distribution.get(pair, 0) + 1
                root_rows.append([root, "; ".join(f"({i}, {o}) ở {count}/{len(root_cases)} ca" for (i, o), count in sorted(distribution.items()))])
            full_nodes = set().union(*(set(c["trace"]["graphs"]["pre_injection"]["nodes"]) for c in local_cases))
            small_rows = []
            for c in local_cases:
                graph = c["trace"]["graphs"]["pre_injection"]
                missing = sorted(full_nodes - set(graph["nodes"]))
                if missing:
                    small_rows.append([c["case"], f"{len(graph['nodes'])}/{len(graph['edges'])}", len(missing), ", ".join(missing)])
            text += ["Bảng bậc phía trên theo dõi mỗi service trên cả 30 ca, kể cả khi nó không phải root. Bảng sau chỉ lấy các ca chính service đó là root; mẫu số riêng cho từng root. Nguồn: cases.json, graph pre_injection. Đây là hai phạm vi khác nhau, không thay định nghĩa hub hoặc cách chia.",
                     mdtable(["Service gốc", "Bậc (vào, ra) trong chính ca làm root"], root_rows),
                     "Các graph nhỏ trước tiêm dưới đây được so với hợp tập node quan sát của dev, không phải kiến trúc đầy đủ. Nguồn: cases.json.",
                     mdtable(["Ca", "Nút/cạnh", "Node vắng", "Tên node vắng so với graph 27 nút"], small_rows),
                     "**FACT đã kiểm giới hạn:** đọc lại metric trước tiêm của order×disk lặp 1/2 và travel×disk lặp 1/3 cho thấy số workload khác nhau. Các cột preserve/preserve-other/seat/security/user/contacts vắng ở order×disk lặp 2, có nhưng bằng 0 ở travel×disk lặp 3; payment_workload cũng bằng 0 trong hai ca nhỏ này. Nguồn raw: `data/rcaeval/re2tt_ts-order-service_disk_{1,2}/metrics.parquet` và `data/rcaeval/re2tt_ts-travel-service_disk_{1,3}/metrics.parquet`; phép kiểm và số trung gian ở [LOG phiên tự soát 03/10](../../tasks/T-002-the-dataset-rcaeval/LOG.md). Các ca nhỏ khác chưa được đối chiếu raw workload trong phần này; không suy kết quả hai ca nhỏ sang cả sáu ca. **CANDIDATE — chưa kiểm nguyên nhân:** luồng đặt vé có thể ít được gọi; cũng có thể exporter, bộ đo hoặc cách tạo tải làm thiếu/zero cột. Số đo trước tiêm không chứng minh đồ thị nhỏ do lỗi được tiêm; task mô tả không có kiểm soát workload/instrumentation để phân xử."]
            text.append("K2 §2/ST3 cũ ghi 2 đồ thị (24 + 6 ca). Phép dựng literal ở đây cho 3 (24 + 5 + 1): `re2tt_ts-travel-service_disk_2` có thêm `ts-payment-service` và cạnh `ts-inside-payment-service → ts-payment-service` so với cấu trúc 20 nút/20 cạnh. K2 chưa được kiểm lại; khác biệt có thể do phép lọc/vocabulary của audit trước hoặc đếm cũ sai. Không đủ căn cứ xác định lý do từ tài liệu hiện có; không đọc archive và không sửa K2 trong task này.")
        if ds == "re2ob":
            text.append("Năm root công khai đều có mặt trong graph mẫu. Checkout có cạnh vào/ra; currency/email/productcatalog chỉ có cạnh vào trong mẫu; recommendation có cả hai. `frontend` ở metric khác literal `frontendservice` ở trace. Không tự chuẩn hóa alias hay coi 7 node mẫu là toàn kiến trúc Online Boutique.")
            text.append("**FACT trên một ca:** `adservice`, `cartservice`, `shippingservice` và `redis` có entity trong metric/log nhưng vắng graph trace; ba service đầu có cả metric latency-90. Nguồn: cases.json (graph và log.entities), schemas.json và symptom-entity-rates.csv. `frontend`/`frontendservice` là khác tên cần alias, không gộp vào nhóm chắc chắn thiếu. Phương pháp chỉ nhận graph quan sát sẽ thiếu các node này dù metric/log có tín hiệu; mapping ba nguồn phải giữ rõ độ phủ để tránh diễn giải graph mẫu thành toàn hệ. Có thể do workload, instrumentation hoặc export, chưa xác định nguyên nhân.")
        if ds == "re3tt":
            text.append("Hai root công khai có mặt trong graph mẫu: auth không có cạnh quan sát, route chỉ có cạnh vào. Đây là vị trí trong một ca route×f2, chưa chứng minh cùng cấu trúc ở cả 30 ca. HF card bảng ghi f1–f5 cho TT nhưng prose cùng card, tree và GitHub README chỉ f1–f4. Paper nói lặp 3–5; tree có ô route×f3 lặp 6. Giữ số đếm file, không sửa nguồn (public-sources.md).")
        text += ["### 4. Schema thật và chất lượng ba nguồn tín hiệu"]
        if n:
            text += [f"**FACT trên mẫu:** metric dạng wide (mỗi chỉ báo một cột), {s['metric_columns_min']}–{s['metric_columns_max']} cột ngoài `time`, bước 1 giây, {num(s['metric_missing_values'])} ô thiếu, {s['metric_duplicate_times']} timestamp trùng. Tên cột `<entity>_<metric>`; có thành phần hạ tầng, không đồng nhất số cột với số service. Đơn vị từng metric chưa kiểm toàn bộ; xem schema và case-summary.",
                     "Trace có 11 trường: `time`, `traceID`, `spanID`, `serviceName`, `methodName`, `operationName`, `parentSpanID`, `startTimeMillis`, `startTime`, `duration`, `statusCode`. Kiểu từng file ở schemas.json. `startTime // 1000 == startTimeMillis` trên phần đã kiểm; quy đổi startTimeMillis/1000 khớp epoch metric/log. Đơn vị duration còn OPEN; không dùng duration để xếp hạng. Không có span kind hay thuộc tính resource/db/messaging đủ dựng cạnh có kiểu.",
                     mdtable(["Phép đếm trace", "Số đo trên mẫu"], [
                         ["Tổng span", num(s['n_spans'])], ["Không có parent/root", num(s['root_or_empty_parent_count'])],
                         ["Có parent cần resolve", num(s['parent_reference_count'])], ["Tìm được key cha cùng trace", num(s['parent_resolved_count'])],
                         ["Không tìm được cha", num(s['parent_unresolved_count'])], ["Tỷ lệ cộng số đếm", pct(s['parent_resolution_fraction'])],
                         ["Min–max tỷ lệ theo ca", f"{pct(s['parent_fraction_min'])}–{pct(s['parent_fraction_max'])}"],
                         ["Hàng trùng (traceID,spanID) / key khác service", f"{s['duplicate_key_rows']} / {s['conflicting_service_keys']}"],
                         ["Duration thiếu / âm", f"{s['duration_null']} / {s['duration_negative']}"],
                         ["Status có giá trị / khác 0", f"{num(s['status_nonnull'])} / {s['status_nonzero']}"],
                     ]),
                     f"Log: {s['n_log_cases']}/{n} ca, {num(s['n_logs'])} hàng; ba cột `timestamp` (int64), `container_name`, `message` (string). Không có cột trace/span ID; quét tất cả message: {s['id_key_mentions']} nhắc khóa traceid/spanid/traceparent, {s['recognized_id_pattern_rows']} chuỗi ID hợp regex. Regex không bắt mọi định dạng hoặc ID không có khóa; ghép request-level còn OPEN. Nối service + thời gian là CANDIDATE, cần alias/clock hợp lệ, không phải nối từng request.",
                     "Parent resolve chỉ cho biết cha có trong artifact, không chứng minh sampling đầy đủ hay nhân quả. Status thiếu có thể do xuất/lược trường; duration không âm không chứng minh đơn vị đúng. Metric NaN có thể do không có request hoặc bộ đo thiếu; log không có ID có thể là thiết kế exporter, chưa chứng minh không có liên kết ở hệ gốc."]
            if ds == "re2tt":
                text.append("Ca `re2tt_ts-auth-service_delay_1` có tỷ lệ cha thấp nhất 82,66%; giữ ca này. Status rỗng toàn bộ phần dev. 99,10% ở đây là 30 ca dev; không đối chiếu như tái lập 98,45% của audit 90 ca trong K2. Khác tỷ lệ có thể do phạm vi ca khác nhau.")
            if ds == "re2ob":
                text.append("Độ phủ ba nguồn không trùng nhau ở các entity nêu trong mục 3. Có file trace và resolve cha cao không bảo đảm mọi service có metric/log đều có node; việc ghép theo service và thời gian còn cần kiểm mapping/clock ở adapter.")
            if ds == "re3tt":
                text.append(f"**FACT mẫu:** `statusCode` trống ở toàn bộ {num(s['n_spans'])} span, nên không dùng kênh này làm bằng chứng response code lỗi trên ca route×f2 đã đọc. Paper §3.4 nói response code khi có sẵn; thiếu có thể do exporter hoặc lược trường, không bác bỏ chẩn đoán code fault trên toàn RE3. Log của ca này đã rà bằng regex `Exception`, ký tự tab + `at `, hoặc `ERROR`; có hàng khớp sau tiêm ở service khác root. Các hàng root khớp regex là INFO khởi động chứa tên lớp/chữ ký hàm, chưa là log lỗi đã xác minh. Nguồn raw: `data/rcaeval/re3tt_ts-route-service_f2_1/logs.parquet`; đối chiếu ngữ cảnh ở [LOG phiên tự soát 03/10](../../tasks/T-002-the-dataset-rcaeval/LOG.md). Số hàng regex không là số sự cố độc lập, nhãn vùng hay code line gốc. **OPEN — chưa xác lập:** chỉ báo log thật và liên kết với nhãn chi tiết; chưa có mapping nhãn chỉ báo đã xác minh trong mẫu, regex không đủ. Không gọi log là kênh chính của toàn RE3 từ một ca.")
        else:
            text.append("**OPEN — chưa kiểm:** schema, parent resolution, chất lượng log/metric, status/duration và clock: không có mẫu RE3-OB. Metadata có 30/30 file của mỗi modality. Không lấy schema hoặc tỷ lệ RE2-OB thay cho RE3-OB; exporter/phiên bản/code faults có thể khác.")
            text.append("**CANDIDATE — chưa kiểm:** nếu instrumentation RE3-OB giống mẫu RE2-OB, ad/cart có thể thiếu node trace dù có metric/log; hai root này có 12/30 ca công khai (ad 9, cart 3; count-summary.json). Giả thuyết có thể sai khi phiên bản, exporter hoặc workload khác. Không có telemetry RE3-OB được phép đọc trong task để kiểm; giữ tiêu chí 3/4 và vị trí root OPEN, không loại dataset từ mẫu RE2-OB.")
        text += ["### 5. Dữ liệu bình thường và mốc thời gian"]
        if n:
            normal_min = s['normal_rows_min'] / 60
            normal_max = s['normal_rows_max'] / 60
            text.append(f"**FACT:** {s['normal_rows_min']}–{s['normal_rows_max']} hàng metric 1 giây trước lúc tiêm, tương đương {normal_min:g}–{normal_max:g} phút theo số điểm; sau tiêm {s['post_rows_min']}–{s['post_rows_max']} hàng. Bài nói thu bình thường 10 phút; file mẫu dài hơn. Cửa sổ lưu/export có thể khác giao thức mô tả. Mốc tiêm dùng để mô tả hai chế độ, không làm đầu vào bộ tự phát hiện. Trước tiêm chưa có kiểm chứng độc lập rằng mọi điểm sạch; clock và healthy workloads đa chế độ còn OPEN. Không gọi khoảng injection − timestamp đầu tiên là thời lượng đo nếu dữ liệu thưa hoặc injection nằm ngoài file.")
            margins = sorted({(c["inject_time"] - c["metric_time_min"], c["metric_time_max"] - c["inject_time"]) for c in local_cases})
            window_text = "; ".join(f"−{left}/+{right} giây" for left, right in margins)
            text.append(f"**FACT trên {n} ca đã đọc:** biên metric so với injection là {window_text}; điểm giữa hai timestamp đầu/cuối cho lại mốc tiêm. Đây là rò thông tin về injection có thể xảy ra qua chính telemetry, dù bỏ tên ca/file nhãn; injection chưa là onset thật. Giao thức tự phát hiện P3/P7 cần xử lý nguy cơ này trước khi chấm. Task này chưa chọn cách cắt mới hoặc kiểm một detector khai thác vị trí giữa file; biết trước mốc để khảo sát/RCA phải ghi rõ chế độ.")
        else:
            text.append("**FACT nguồn:** bài mô tả 10 phút bình thường và inject_time Unix. **OPEN — chưa kiểm** độ dài/nhịp thực tế từng ca, contamination, thời gian onset/kết thúc và clock: không có mẫu. Đủ để học ngưỡng nào phụ thuộc phương pháp sau này.")
        text += ["### 6. Ước lượng thô triệu chứng ngoài service gốc"]
        if n:
            rows = []
            subset = probes.loc[probes.dataset == ds]
            for (q, signal), g in subset.groupby(["q", "signal_group"]):
                rows.append([q, "Tất cả metric" if signal == "all_metrics" else "Latency p90", len(g),
                             pct(g.control_mean_service_rate.mean()), pct(g.post_mean_service_rate.mean()),
                             f"{100*g.delta_mean_rate.min():.2f} đến {100*g.delta_mean_rate.max():.2f}".replace(".", ",")])
            text += [mdtable(["Phân vị q", "Kênh", "Ca", "Đối chứng trước tiêm", "Sau tiêm", "Chênh min–max từng ca (điểm %)"], rows),
                     "Mỗi ô tỷ lệ là trung bình không trọng số: trước hết tỷ lệ hàng thời gian vượt band ở từng service ngoài root, rồi trung bình các service, rồi các ca. Không phải tỷ lệ ca lan hoặc tỷ lệ request lỗi. Công thức, các giới hạn và mapping chỉ để báo ở mục chung cuối. [Từng ca/ngưỡng](local-inspection/run-002/probe-case-summary.csv), [từng ô/ngưỡng](local-inspection/run-002/probe-cell-summary.csv), [từng service](local-inspection/run-002/symptom-entity-rates.csv), [band từng kênh](local-inspection/run-002/symptom-channel-bands.csv).",
                     "**CANDIDATE — chưa kiểm:** có tín hiệu ngoài root tăng sau tiêm, có thể chứa triệu chứng lan. Cũng có thể tải chung/drift/nhiễu, thay đổi metric hằng hoặc nhiều kênh OR giải thích nó. Không xác lập causal propagation, không gắn nhãn lan từng ca. Không thấy lệch metric cũng chưa loại trừ biểu hiện ở log/trace."]
            text += ["Phân rã kênh mem dưới đây dùng cùng service ngoài root và cách trung bình như bảng OR; lấy số vượt/số hợp lệ từ symptom-channel-bands.csv. Trên mẫu đã kiểm, mem và OR có cùng mẫu số hàng hợp lệ ở từng service/ca/ngưỡng. Đây là mức vượt của mem, không phải đóng góp độc lập khi bỏ mem khỏi OR.",
                     mdtable(["Phân vị q", "Mem đối chứng", "Mem sau tiêm", "OR đối chứng", "OR sau tiêm"], memory_rows(reporting_channels, probes, ds)),
                     "**OPEN — chưa phân xử nguyên nhân:** mem tăng có thể do tải, warm-up, drift, thay đổi mức nền hoặc lỗi thật; mem lớn không tự chứng minh lan hoặc drift. CSV chỉ lưu số biên từng kênh, không có giao các hàng vượt giữa kênh, nên chưa tính được OR khi bỏ mem. Chưa có đo kiểm soát tải/nhãn vùng độc lập trong task mô tả để phân xử. Không bỏ mem hoặc đổi q chỉ để giảm tỷ lệ; việc đó có thể bỏ biểu hiện mem fault thật."]
            if ds == "re2tt":
                control_flat, post_flat = flat_or_bounds(reporting_channels, rates, ds, .995)
                text.append(f"Cùng phạm vi OR ngoài root tại q=.995, cận tỷ lệ OR của riêng các kênh band0 là {control_flat} ở đối chứng và {post_flat} sau tiêm. Cận dưới lấy max số vượt từng kênh band0; cận trên lấy min(tổng số vượt band0, số vượt OR), chia mẫu số OR rồi trung bình service/ca. Nguồn: hai CSV bands/rates ở trên. Chưa có giao kênh để gọi đây là OR chính xác; không dùng tỷ lệ mọi kênh band0 với mẫu số khác để giải thích mức OR. Mem chiếm phần lớn mức vượt ở q=.995 trên RE2-TT; không khái quát sang mọi bộ/ngưỡng.")
                text.append("Không đọc nhóm 60 ca khóa. Trong dev có chênh latency p90 âm ở một số ca khi q cao (xem cột min–max); không biến mức tăng trung bình thành mẫu hình của mọi ô. Ba lần lặp/ô không phải ba topology độc lập.")
            if ds == "re3tt":
                text.append("Tất cả metric giảm từ 62,14% (q=.95) xuống 9,10% (q=.995) sau tiêm trong mẫu: ước lượng rất nhạy ngưỡng. Một ca route×f2 không đại diện f1/f3/f4 hay auth. Có thể vùng biểu hiện nhỏ, baseline biến động hoặc band rộng, chưa phân xử được cơ chế.")
        else:
            text.append("**OPEN — chưa kiểm:** không có mẫu nên không đo tiêu chí 7. Không suy từ RE2-OB hoặc từ nhãn code fault rằng triệu chứng sẽ lan. Cần mẫu được Minh cho phép; nếu chọn làm bộ giữ ngoài, giữ OPEN đến G3 theo MRP.")
        text += ["### 7. Task nào chấm được?",
                 "Áp dụng bảng nhãn chung cuối tài liệu: xếp hạng root-service theo ca có nhãn; phát hiện chỉ chấm theo injection-regime với giới hạn; vùng ảnh hưởng/operation/từng trace chưa chấm trực tiếp được. Với bộ chưa kiểm schema, khả năng thực thi adapter còn OPEN. Không lấy khảo sát mục 6 làm nhãn chuẩn.",
                 "### 8. Rò nhãn và thông tin phục vụ G1",
                 "Tên thư mục chứa root/fault/repeat; inject_time là nhãn biên. Biên file telemetry cũng có thể tiết lộ injection, như các ca có mẫu ở mục 5; phần chưa đọc còn OPEN. Chỉ bỏ file nhãn/tên ca chưa đủ loại đường rò này. Chỉ dùng nhãn cho đếm/mô tả/chấm. `metric_excursions` nhận bảng metric và mốc biên, không nhận root/fault/path; root được gắn sau để báo ngoài root. Đây là khảo sát known-window (biết trước mốc), không phải tự phát hiện. Adapter P3 và giao thức tự phát hiện cần kiểm đường biên file; chưa được làm/kiểm trong task mô tả. Rò SLI của runner chính thức được MRP P2 nêu, chưa khẳng định đã sửa. Dataset/cách chia/nhãn học còn OPEN ở G1; WHY-04 là đề xuất.",
                 "### 9. Kích thước và chi phí",
                 f"**FACT metadata:** {num(p['total_file_bytes'])} byte ({p['total_file_MB_decimal']:.3f} MB thập phân) trong các thư mục ca công khai, gồm parquet và inject_time; không phải RAM hoặc ZIP giải nén. **FACT phần đã kiểm:** {num(s['inspected_bytes'])} byte telemetry parquet. Chi phí adapter và RAM cực đại **OPEN — chưa đo**; không suy từ file nhỏ rằng huấn luyện toàn bộ chạy được. Cài gói dưới 1 GB, không tải telemetry mới; thời gian/phiên bản nằm trong manifest và install.log, chi phí riêng không cộng vào khả năng phân xử.",
                 "### 10. Điều còn mở",
                 "- Onset/end, nhãn vùng và clock độc lập: cần nguồn nhãn bổ sung hoặc thực nghiệm có nhãn thật; người làm task tương ứng báo Minh trước khi dùng cho P7.",
                 f"- Độ đại diện schema/topology/log và tiêu chí 7 của phần chưa đọc: chỉ {n}/{p['n_cases']} ca được kiểm. Người làm P2/task tiếp theo cần mẫu được phép; không mở dữ liệu khóa. Nút ít/thiếu có thể do workload hoặc đo thiếu.",
                 "- Tính đủ dữ liệu bình thường, phép chia/nhãn học và bộ độc lập: Minh quyết ở G1 sau các thẻ ứng viên; chưa kết luận từ kích thước hoặc dữ liệu sẵn có.",
                 "- Cạnh có kiểu, duration unit, alias và khả năng huấn luyện/chuyển hệ: cần xác minh exporter/adapter và giao thức của phương pháp ở task sau. Không biến OPEN thành lỗi dataset hoặc quyết định loại dataset."]
        if ds == "re2tt":
            text.append("- Cơ chế tạo sáu graph nhỏ và khác biệt bậc root: workload mới đối chiếu trên bốn ca disk, chưa là giải thích cho mọi ca. Muốn dùng vị trí để kết luận RQ1, task đo cần phân biệt danh tính root, loại lỗi, tải và độ phủ đo; T-002 chỉ mô tả bậc và số thiếu, không chốt hub hay chia lại dữ liệu.")

    text += ["## Phép tính và giới hạn chung cho mục 6 của bốn thẻ",
             "Đây là khảo sát mô tả được SPEC yêu cầu, chưa chọn detector/threshold cho P3–P7. Căn cứ mục đích: WHY-03 và MRP P2 đã yêu cầu đếm khả năng phân xử trước giả thuyết. Không bổ sung lựa chọn nghiên cứu quan trọng vào WHY hoặc DECISIONS trong task này.",
             "1. Sắp metric theo time. Chia trước tiêm: 2/3 đầu làm đoạn tham chiếu (480 điểm RE2, 600 điểm RE3-TT mẫu), 1/3 cuối làm đối chứng bình thường (240/300). Đây là cách thử tạm để nhìn drift, không khóa cách chia học/chấm.",
             "2. Với mọi cột số, trừ time, có ít nhất 30 điểm hữu hạn tham chiếu: m là median; band b(q) là phân vị q của |x−m| trên tham chiếu, q ∈ {.95,.99,.995}. Điểm vượt khi |x−m| > b(q). Không có sàn epsilon hay chia cho độ lệch chuẩn. NaN không là vượt; hàng thiếu mọi kênh của một nhóm được loại khỏi mẫu số nhóm. Nếu service/nhóm không có điểm hợp lệ, tỷ lệ không xác định và bỏ khỏi trung bình, không thay bằng 0. Band 0 coi mọi thay đổi hữu hạn là vượt và được lưu riêng.",
             "3. Tách entity bằng dấu `_` cuối tên cột. Nhóm tất cả metric dùng OR (chỉ cần một kênh vượt); nhóm latency90 chỉ dùng cột `_latency-90`. Tính band cho mọi entity trước khi biết root. Để mô tả service ngoài root, sau đó lọc tên entity kết thúc `service` hoặc là `frontend`, bỏ đúng tên root. Đây là heuristic (quy tắc thử theo tên), chưa mapping dịch vụ hoàn chỉnh; excludes DB/broker và có thể sai với hệ khác. Không chọn SLI theo root.",
             "4. Báo tỷ lệ time-row và chênh trước/sau liên tục, từng service/ca/ô. Không ngưỡng hóa chênh để tạo nhãn lan. Nhiều metric OR làm tỷ lệ cao; mẫu ít làm q=.995 không ổn định; flat bands, tải/clock/drift cùng thay đổi là lời giải thích đối lập. Vì vậy bảng chỉ cho biết sự sẵn có của tín hiệu cần kiểm tiếp, chưa chứng minh đường lan hoặc lợi ích đồ thị.",
             "5. Mức 1−q (0,5% khi q=.995) chỉ là mức danh nghĩa cho một kênh dưới phân phối tham chiếu ổn định và điều kiện phù hợp; phân vị hữu hạn, ties và phụ thuộc thời gian có thể làm lệch. Đây không phải mức kỳ vọng của OR nhiều kênh. Các số mem và cận band0 chỉ mô tả thành phần mức vượt trên cùng mẫu số; không chứng minh drift, đóng góp riêng của kênh hay tiêu chí lan truyền nhân quả. Đối chiếu thêm trên từng ô/ca trong CSV trước khi dùng cho task đo.",
             "Phép thử đối chiếu rẻ: trong RE2-OB mẫu tại q=.99, paymentservice có tỷ lệ control all_metrics 59,17% nhưng latency90 0%; post lần lượt 100% và 0%. Một nhóm kênh tăng không đồng nghĩa request chậm ở service đó. Nguồn: symptom-entity-rates.csv. Các tỷ lệ và số band0 có thể kiểm lại từ CSV, không lấy từ trí nhớ.",
             "Ca RE2-TT travel×disk lặp 2 có latency90 của ts-payment-service đủ điểm tham chiếu nhưng không có điểm hợp lệ ở control/post; rate để không xác định. Ca route×mem lặp 2 cũng thiếu mọi metric ở entity hạ tầng istio-init trong hai đoạn đó. Thiếu dữ liệu không phải bằng chứng không có triệu chứng. Nguồn: symptom-entity-rates.csv.",
             "## Bảng khả năng chấm — áp dụng riêng cho từng thẻ",
             mdtable(["Task", "Nhãn thực có theo nguồn", "Chấm được đến đâu", "Giới hạn"], [
                 ["Xếp hạng nguyên nhân gốc", "Root service đơn theo ca, fault/repeat", "MRR, Hit@k; NDCG nhị phân theo service", "Không chấm được operation/code line từ tên service; nhãn tiêm chưa là kiểm chứng causal độc lập"],
                 ["Phát hiện theo thời gian", "Timestamp tiêm; thời gian file", "Có thể chấm injection-regime khi giao thức P7 ghi rõ và xử lý nguy cơ suy injection từ biên file", "32 ca mục tiêu có metric đối xứng; phần chưa đọc OPEN. Thiếu onset/end độc lập; chưa có detector bị chứng minh khai thác rò, không gọi P/R/F1 này là phát hiện triệu chứng thật"],
                 ["Vùng ảnh hưởng", "Không thấy nhãn affected components ở nguồn đã đọc", "Chưa chấm trực tiếp Precision/Recall/F1 vùng", "Probe ngoài root không thay nhãn vùng"],
                 ["Bất thường từng trace / định vị operation", "Chưa xác minh nhãn từng trace/operation gốc; paper nói có chỉ báo, tree chỉ có 8 root_cause.txt ở RE3-SS", "Chưa chấm trực tiếp bằng artifact đã xác minh của bốn bộ", "Không thấy tên file chưa chứng minh thiếu mọi nhãn chi tiết. RE3-TT mẫu status trống; status/latency/regex log và tên fault không tự trở thành nhãn"],
                 ["Học có giám sát/chuyển hệ", "Ngân sách nhãn/cách chia chưa chốt", "OPEN ở G1/P1/P3", "5/2/4 root ít không đủ suy độ khái quát; không xếp chung điều kiện có/không giám sát thiếu ghi rõ"],
             ]),
             "## Mẫu phụ và đối chiếu nguồn",
             "Schema cũng được lưu cho RE1-OB, RE2-SS và RE3-SS có sẵn. Hai mẫu Sock Shop không có trace parquet; không biến kiểm hai mẫu thành kết luận toàn kho SS trong task này. RE1-OB mẫu chỉ có 63 điểm metric ở khoảng 62 giây và mốc tiêm ngoài cửa sổ; không dùng nó để ước lượng triệu chứng. Không viết thẻ SS/RE1 hoặc chọn thêm bộ ngoài SPEC.",
             "K2/README cũ là thông tin chưa kiểm; số mới không thay quyết định của Minh. RE3-TT F5/repeats và RE2-TT topology có điểm không khớp đã nêu rõ. Muốn sửa tài liệu nền phải đề xuất riêng theo Luật 0. Không chọn/bỏ bộ nào, chưa kết luận RCAEval hơn/kém ứng viên khác."]
    (HERE / "the-rcaeval.md").write_text("\n\n".join(text) + "\n", encoding="utf-8")
    print("Wrote the-rcaeval.md from saved run-002 results")


if __name__ == "__main__":
    main()
