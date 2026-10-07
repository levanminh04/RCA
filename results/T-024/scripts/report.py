"""Viết báo cáo T-024 từ cham-a.json đã chấm; không import phương pháp hoặc nhãn.

Chạy sau evaluator: python -B results/T-024/scripts/report.py
Chỉ đầu ra mặc định results/T-024/cham-a.md; số chấm đọc từ JSON,
thống kê nhánh RCD và thứ tự TraceRCA đếm từ bản ghi đã chốt.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "results" / "T-024"
JSON_SOURCE = "results/T-024/cham-a.json"
MANIFEST = "results/T-024/ban-ghi-dua-vao-cham.json"
MODE_NOTE = "Chế độ (a): biết đúng mốc tiêm; các số này đo xếp hạng RCA quanh mốc đã biết."
MAIN_METRICS = (
    ("hit@1", "Hit@1"), ("hit@3", "Hit@3"), ("hit@5", "Hit@5"),
    ("mrr", "MRR"), ("ndcg@5", "NDCG@5"), ("avg@5", "Avg@5"),
    ("retrieval@5", "Retrieval@5"), ("retrieval@10", "Retrieval@10"),
    ("rerank@1(K=5)", "Rerank@1 K=5"), ("rerank@1(K=10)", "Rerank@1 K=10"),
)
BOOT_METRICS = (
    ("hit@1", "Hit@1"), ("hit@3", "Hit@3"), ("hit@5", "Hit@5"),
    ("rr", "MRR"), ("ndcg@5", "NDCG@5"), ("avg@5", "Avg@5"),
    ("hit@10", "Retrieval@10"), ("rerank@1(K=5)", "Rerank@1 K=5"),
    ("rerank@1(K=10)", "Rerank@1 K=10"),
)
RCAEVAL_METRICS = (
    ("AC@1", "AC@1"), ("AC@3", "AC@3"), ("AC@5", "AC@5"),
    ("Avg@5", "Avg@5"), ("retrieval_service(5)", "Retrieval 5"),
    ("retrieval_service(10)", "Retrieval 10"),
    ("rerank_service(1,5)", "Rerank 1/5"), ("rerank_service(1,10)", "Rerank 1/10"),
)
ORDER = (
    "baro", "simplerca", "microrank_full", "tracerca", "circa_ols_da", "torai_B",
    "circa_ols_rht", "circa_svr_da", "circa_svr_rht", "torai_A", "microrank_top11",
)


def cell(value):
    """Một ô Markdown; không để dữ liệu tạo cột hoặc dòng mới."""
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def number(value, digits=4):
    if value is None:
        return "N/A"
    if isinstance(value, bool):
        return "có" if value else "không"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("JSON chứa số không hữu hạn")
        return f"{value:.{digits}f}"
    return cell(value)


def statuses(counts):
    return "; ".join(f"{k}: {v}" for k, v in sorted(counts.items()) if v) or "không có ca"


def main_status(summary):
    return statuses(summary["main"]["trang_thai"])


def method_name(mid, method):
    suffix = "chính" if method["primary"] else "phụ"
    return f'{method["name"]} ({suffix})'


def bounds(summary, metric):
    val = number(summary[metric])
    if metric.startswith("rerank"):
        return val
    lo = summary["can_bi_quan"][metric]
    hi = summary["can_lac_quan"][metric]
    return f"{val} [{number(lo)}; {number(hi)}]"


def interval(obj):
    if obj["lo"] is None or obj["hi"] is None:
        val = "N/A"
    else:
        val = f'[{number(obj["lo"])}; {number(obj["hi"])}]'
    if obj["n_na"]:
        val += f' (N/A: {obj["n_na"]})'
    return val


def compact(value):
    if isinstance(value, (dict, list)):
        return cell(json.dumps(value, ensure_ascii=False, sort_keys=True))
    return number(value)


class Report:
    def __init__(self, data):
        self.data = data
        self.lines = []
        self.ids = [m for m in ORDER if m in data["methods"]]
        self.ids += sorted(set(data["methods"]) - set(self.ids))

    def add(self, text=""):
        self.lines.append(text)

    def table(self, title, headers, rows, source, status_note, scientific_cohort=True):
        self.add(f"### {title}")
        self.add()
        self.add(MODE_NOTE if scientific_cohort else
                 "Phép kiểm công thức cho báo cáo chế độ (a), dùng dữ liệu tổng hợp; "
                 "các số dưới đây không là kết quả RCA trên ca dev.")
        self.add()
        self.add(f"Trạng thái: {status_note}. " +
                 ("Mọi ca khác `OK` vẫn ở mẫu số và tính trượt." if scientific_cohort else
                  "Đây là phép tự kiểm tổng hợp, không thuộc cohort hoặc mẫu số các bảng khoa học."))
        self.add()
        self.add("| " + " | ".join(cell(x) for x in headers) + " |")
        self.add("| " + " | ".join("---" for _ in headers) + " |")
        for row in rows:
            if len(row) != len(headers):
                raise ValueError(f"Số cột không khớp: {title}")
            self.add("| " + " | ".join(cell(x) for x in row) + " |")
        self.add()
        if scientific_cohort:
            self.add(f"Nguồn số thực nghiệm trong bảng: `{JSON_SOURCE}` → `{source}`. "
                     f"Bản ghi nguồn và SHA-256: `{MANIFEST}`; đường dẫn từng ca nằm ở `methods.<id>.per_case.<ca>.source_paths`.")
        else:
            self.add(f"Nguồn số kiểm fixture: `{JSON_SOURCE}` → `{source}`. "
                     "Fixture theo ví dụ AB/CD ở `results/T-022/giao-thuc-v2.md` §8.4; "
                     "không phải bản ghi phương pháp trong manifest.")
        self.add()

    def cohort_status(self, cohort, ids=None):
        return "; ".join(f'{self.data["methods"][m]["name"]}: '
                         f'{main_status(self.data["methods"][m]["summaries"][cohort])}'
                         for m in (ids or self.ids))

    def dev19_note(self):
        cohort = self.data["cohorts"]["dev19"]
        return (f'Mọi số và khoảng dev19 chỉ mô tả {cohort["n_cases"]} ca/'
                f'{cohort["n_cells"]} ô giữ lại theo đầu ra CIRCA. '
                "Việc bỏ 11 ca đổi cả thành phần ca và số ERROR của phương pháp khác; "
                "hướng thay đổi phụ thuộc phương pháp và độ đo. Đây không phải phép sửa CIRCA trên cùng ca. "
                "Các cặp có hoặc không có CIRCA chỉ được diễn giải trong nhóm ca này; "
                "chưa suy sang toàn 30 ca hay test. "
                f'Nguồn: `{JSON_SOURCE}` → `cohorts.dev19`, `methods.<id>.per_case`.')

    def dev19_composition(self):
        excluded = self.data["cohorts"]["dev19"]["excluded_case_ids"]
        kept = self.data["cohorts"]["dev19"]["case_ids"]
        parts = []
        for mid in self.data["definitions"]["main_methods"]:
            method = self.data["methods"][mid]
            per = method["per_case"]
            hits = [sum(per[o]["hit@1"] for o in ids) for ids in (excluded, kept)]
            numerators = [number(int(v) if v.is_integer() else v) for v in hits]
            parts.append(f'{method["name"]}: {numerators[0]}/{len(excluded)} → '
                         f'{numerators[1]}/{len(kept)}')
        self.add("Hit@1 trên nhóm loại 11 ca → nhóm giữ 19 ca: " + "; ".join(parts) + ". "
                 f'Nguồn: `{JSON_SOURCE}` → `cohorts.dev19.excluded_case_ids/case_ids`, '
                 '`methods.<id>.per_case.<ca>.hit@1`. Đây là số mô tả từng phương pháp, '
                 "không xác định ca dễ hay khó chung cho mọi phương pháp hoặc mọi độ đo.")
        error_parts = []
        for mid in ("microrank_full", "tracerca"):
            method = self.data["methods"][mid]
            per = method["per_case"]
            counts = [sum(per[o]["status"] == "ERROR" for o in ids) for ids in (excluded, kept)]
            error_parts.append(f'{method["name"]}: {counts[0]} ca ERROR bị loại, '
                               f'{counts[1]} ca ERROR giữ lại')
        labels = self.data["methods"]["baro"]["per_case"]
        lost_cells = sorted({labels[o]["label"]["cell"] for o in excluded} -
                            {labels[o]["label"]["cell"] for o in kept})
        lost = "; ".join(f'`{c}` ({sum(labels[o]["label"]["cell"] == c for o in excluded)} ca)'
                         for c in lost_cells)
        self.add("Thành phần ca cũng đổi: " + "; ".join(error_parts) + ". "
                 f'Ô bị loại toàn bộ: {lost}. Nguồn: `{JSON_SOURCE}` → '
                 '`methods.<id>.per_case.<ca>.status/label.cell`, `cohorts.dev19`.')
        self.add(self.dev19_note())
        self.add()

    def summaries(self, cohort):
        methods = self.data["methods"]
        rows = []
        for mid in self.ids:
            method = methods[mid]
            summary = method["summaries"][cohort]["main"]
            rows.append([method_name(mid, method), summary["n"], statuses(summary["trang_thai"])] +
                        [bounds(summary, key) for key, _ in MAIN_METRICS])
        self.table(f"Bảng chính — {cohort}", ["Phương pháp", "Ca", "Trạng thái"] +
                   [name for _, name in MAIN_METRICS], rows,
                   f"methods.<id>.summaries.{cohort}.main", "đếm theo ca ở từng dòng")
        self.add("Mỗi ô độ đo đơn điệu ghi kỳ vọng **[cận bi quan; cận lạc quan]**. "
                 "Cận mô tả ảnh hưởng của hòa, không phải khoảng tin cậy. "
                 "Rerank là tỉ số gộp và chỉ có giá trị chính. Retrieval@5 bằng Hit@5 với một root.")
        self.add()

    def rcaeval(self, cohort):
        rows = []
        for mid in self.ids:
            method = self.data["methods"][mid]
            summary = method["summaries"][cohort]
            rc = summary["rcaeval"]
            rows.append([method_name(mid, method), "trung bình seed", main_status(summary)] +
                        [number(rc["mean"][key]) for key, _ in RCAEVAL_METRICS])
            if len(rc["by_seed"]) > 1:
                for seed, seed_table in sorted(rc["by_seed"].items()):
                    rows.append([method["name"], f"seed {seed}", main_status(summary)] +
                                [number(seed_table[key]) for key, _ in RCAEVAL_METRICS])
        self.table(f"RCAEval riêng — {cohort}", ["Phương pháp", "Seed", "Trạng thái"] +
                   [name for _, name in RCAEVAL_METRICS], rows,
                   f"methods.<id>.summaries.{cohort}.rcaeval", "đếm theo ca ở từng dòng")
        self.add("Bảng giữ thứ tự đầu ra của bản triển khai đang đánh giá, bỏ trùng thực thể, `Evaluator(max_k=10)`. "
                 "Khi có hòa, bảng này chỉ để đối chiếu cách báo của RCAEval; kết luận dùng bảng chính. "
                 "TORAI trung bình AC và Retrieval theo seed rồi tính lại tỉ số Rerank cho dòng gộp; "
                 "quy tắc giữ thứ tự đầu ra vẫn có thể khác bảng chính khi có hòa.")
        self.add(self.tracerca_order_note())
        self.add()

    def tracerca_order_note(self):
        method = self.data["methods"]["tracerca"]
        n_ok = changed = root_changed = n_nan = official_hit1 = 0
        for meta in method["source_records"]:
            record = json.loads((ROOT / meta["path"]).read_text(encoding="utf-8"))
            if record["status"] != "OK":
                continue
            n_ok += 1
            n_nan += record["diagnostics"]["key_check"] == "nan_present"
            native = record["ranking_native"]
            official = record["extra"]["ranks_chinh_thuc"]
            changed += native != official
            root = method["per_case"][meta["opaque_id"]]["label"]["root"]
            ranks = []
            for operations in (native, official):
                services = list(dict.fromkeys(op.split("_", 1)[0] for op in operations))
                ranks.append(services.index(root) + 1 if root in services else None)
            root_changed += ranks[0] != ranks[1]
            official_hit1 += ranks[1] == 1
        n_cases = self.data["cohorts"]["dev30"]["n_cases"]
        return ("Riêng TraceRCA, thứ tự trong bảng là danh sách `ji` hữu hạn do adapter sắp lại "
                "theo WHY-32, không phải thứ tự hàm RCAEval trả về. "
                f'Trên toàn dev30, hai thứ tự khác ở {changed}/{n_ok} lượt OK, '
                f'hạng root sau bỏ trùng service khác ở {root_changed}/{n_ok} lượt; '
                f'nếu dùng thứ tự hàm trả về và vẫn giữ ERROR ở mẫu số, AC@1 là '
                f'{official_hit1}/{n_cases} = {number(official_hit1 / n_cases)}. '
                "Số này chỉ mô tả tác động của thứ tự, không thay số chính và không chứng minh "
                "thứ tự chứa NaN của hàm là đúng. "
                f'{n_nan}/{n_ok} lượt OK có NaN, nên phép đối chiếu thứ tự khi không NaN '
                "ở giao thức §6.4 không áp dụng được lượt OK nào trong cohort này. "
                f'Nguồn: `{MANIFEST}` → bản ghi TraceRCA `ranking_native`, '
                '`extra.ranks_chinh_thuc`, `diagnostics.key_check`; '
                f'root và mẫu số từ `{JSON_SOURCE}` → '
                '`methods.tracerca.per_case.<ca>.label.root`, `cohorts.dev30`. '
                "Bảng này áp dụng công thức RCAEval cho bản TraceRCA lọc hữu hạn; "
                "không được coi là kết quả nguyên trạng của code TraceRCA trong RCAEval.")

    def random(self, cohort):
        keys = [f"{side}_hit@{k}" for side in ("O", "U") for k in (1, 3, 5, 10)]
        rows = []
        for mid in self.ids:
            method = self.data["methods"][mid]
            summary = method["summaries"][cohort]
            rnd = summary["random"]
            rows.append([method["name"], main_status(summary), number(rnd["O_size_mean"]),
                         number(rnd["root_coverage_O"]), number(rnd["root_coverage_returned"])] +
                        [number(rnd[key]) for key in keys])
        self.table(f"Mức ngẫu nhiên trên O và U — {cohort}",
                   ["Phương pháp", "Trạng thái", "|O| TB", "Root thuộc O", "Root được trả"] + keys,
                   rows, f"methods.<id>.summaries.{cohort}.random", "đếm theo ca ở từng dòng")
        self.add("O là tập quan sát riêng của phương pháp; U là inventory và tập chấm. "
                 "Nếu root thuộc O, kỳ vọng ngẫu nhiên Hit@k là `min(k, |O|)/|O|`; root vắng thì bằng 0. "
                 "Mức ngẫu nhiên O mô tả tập ứng viên, kể cả ở ca phương pháp lỗi; nó không thay số RCA của ca lỗi.")
        self.add()

    def bootstrap(self, cohort):
        boot = self.data["bootstrap"][cohort]
        note = self.cohort_status(cohort)
        rows = [[self.data["methods"][mid]["name"],
                 main_status(self.data["methods"][mid]["summaries"][cohort])] +
                [interval(boot["phuong_phap"][mid][key]) for key, _ in BOOT_METRICS]
                for mid in self.ids]
        self.table(f"Bootstrap theo ô, khoảng phân vị 95% — {cohort}",
                   ["Phương pháp", "Trạng thái"] + [name for _, name in BOOT_METRICS], rows,
                   f"bootstrap.{cohort}.phuong_phap", "đếm theo ca ở từng dòng")
        self.add(f'B = {boot["B"]}, seed = {boot["seed"]}, số ô = {boot["n_o"]}. '
                 "Lấy lại ô có hoàn lại; mỗi ô mang toàn bộ ca còn trong cohort. "
                 "Dùng cùng mẫu cho mọi phương pháp; Rerank tính lại trên từng mẫu và đếm mẫu N/A. "
                 "Ít ô làm khoảng có thể hẹp hơn thực. Với TORAI, trung bình từng ca qua seed trước bootstrap.")
        self.add()
        pairs = []
        for pair, metrics in sorted(boot["hieu"].items()):
            left, right = pair.split(" - ", 1)
            label = f'{self.data["methods"][left]["name"]} − {self.data["methods"][right]["name"]}'
            pairs.append([label] + [interval(metrics[key]) for key, _ in BOOT_METRICS])
        self.table(f"Hiệu từng cặp trên cùng mẫu bootstrap — {cohort}",
                   ["Cặp (trái − phải)"] + [name for _, name in BOOT_METRICS], pairs,
                   f"bootstrap.{cohort}.hieu", note)
        self.add("Khoảng chứa 0 chưa cho thấy khác biệt tách khỏi 0 theo phép bootstrap này. "
                 "Mọi khoảng ở đây là khoảng từng cặp; chưa hiệu chỉnh việc xét nhiều cặp. "
                 "Không dùng thứ tự trung bình để tuyên bố phương pháp tốt nhất.")
        if cohort == "dev19":
            self.add(self.dev19_note())
        self.add()

    def stratified(self, cohort):
        for field, title in (("fault", "loại lỗi"), ("cell", "ô root × loại lỗi"),
                             ("nhom_vi_tri_p75", "nhóm vị trí root")):
            rows = []
            for mid in self.ids:
                method = self.data["methods"][mid]
                groups = method["summaries"][cohort]["grouped"][field]
                for group, summary in sorted(groups.items()):
                    rows.append([method["name"], group, summary["n"], statuses(summary["trang_thai"])] +
                                [number(summary[key]) for key, _ in MAIN_METRICS])
            self.table(f"Chia theo {title} — {cohort}",
                       ["Phương pháp", "Nhóm", "Ca", "Trạng thái"] +
                       [name for _, name in MAIN_METRICS], rows,
                       f"methods.<id>.summaries.{cohort}.grouped.{field}", "đếm theo ca ở từng dòng")

    def seeds(self, cohort):
        for mid in ("torai_B", "torai_A"):
            method = self.data["methods"][mid]
            seed_range = method["seed_range"][cohort]
            rows = []
            for seed, summary in sorted(seed_range["by_seed"].items()):
                rows.append([f"seed {seed}", statuses(summary["trang_thai"])] +
                            [number(summary[key]) for key, _ in MAIN_METRICS])
            rows.append(["khoảng min–max giữa seed", main_status(method["summaries"][cohort])] +
                        [f'[{number(seed_range["range"][key]["min"])}; '
                         f'{number(seed_range["range"][key]["max"])}]' for key, _ in MAIN_METRICS])
            self.table(f'{method["name"]}: độ nhạy seed — {cohort}',
                       ["Seed", "Trạng thái"] + [name for _, name in MAIN_METRICS], rows,
                       f"methods.{mid}.seed_range.{cohort}", "đếm theo ca ở từng dòng")
            self.add("Khoảng giữa seed là biến thiên qua các seed đã khóa, không phải khoảng bootstrap. "
                     "Dòng chính trung bình Hit theo seed ở từng ca rồi tính Rerank từ tổng Hit; "
                     "không trung bình các tỉ số Rerank làm số chính.")
            self.add()

    def per_case(self):
        retained = set(self.data["cohorts"]["dev19"]["case_ids"])
        for mid in self.ids:
            method = self.data["methods"][mid]
            rows = []
            for oid, record in sorted(method["per_case"].items()):
                label = record["label"]
                sets = record["four_sets"]["mean"]
                dist = record["rank_distribution_by_seed"]
                ranks = "; ".join(f'{seed}: {compact(d)}' for seed, d in sorted(dist.items()))
                rows.append([oid, "có" if oid in retained else "không", label["root"], label["fault"],
                             label["cell"], label["nhom_vi_tri_p75"], record["status"],
                             number(record["hit@1"]), number(record["hit@3"]), number(record["hit@5"]),
                             number(record["rr"]), number(record["ndcg@5"]), number(record["avg@5"]),
                             number(record["hit@10"]), number(sets["quan_sat"]), number(sets["tra_ve"]), ranks])
            self.table(f'{method["name"]}: toàn bộ từng ca dev',
                       ["Mã ca", "Trong 19", "Root", "Loại lỗi", "Ô", "Vị trí", "Trạng thái",
                        "Hit@1", "Hit@3", "Hit@5", "RR", "NDCG@5", "Avg@5", "Hit@10", "|O|", "Trả về",
                        "Phân bố hạng root theo seed"], rows, f"methods.{mid}.per_case",
                       main_status(method["summaries"]["dev30"]))
            self.add("Hạng được lưu dưới dạng phân bố do hòa; root vắng hoặc ca lỗi có phân bố rỗng. "
                     "Root và nhóm ở bảng này chỉ nối sau khi đã chốt và ghi đầu ra phương pháp.")
            self.add()

    def sets(self):
        for mid in self.ids:
            method = self.data["methods"][mid]
            rows = []
            for oid, record in sorted(method["per_case"].items()):
                sets = record["four_sets"]
                for seed, s in sorted(sets["by_seed"].items()):
                    rows.append([oid, seed, record["status"], s["inventory"], s["quan_sat"], s["cham"], s["tra_ve"],
                                 ", ".join(s["quan_sat_ngoai_U"]) or "không", ", ".join(s["tra_ve_ngoai_U"]) or "không"])
            self.table(f'{method["name"]}: bốn tập từng ca/seed',
                       ["Ca", "Seed", "Trạng thái", "Inventory U", "Quan sát O", "Tập chấm", "Trả về",
                        "Quan sát ngoài U", "Trả về ngoài U"], rows, f"methods.{mid}.per_case.<ca>.four_sets",
                       main_status(method["summaries"]["dev30"]))
        self.add("Không điền thực thể vắng vào danh sách. Thực thể ngoài U giữ chỗ trong danh sách, "
                 "được đếm riêng. Nhóm 19 dùng cùng danh sách ca cho tất cả phương pháp; cột Trong 19 ở bảng từng ca xác định nhóm.")
        self.add()

    def diagnostics(self):
        for cohort in ("dev30", "dev19"):
            rows = []
            for mid in self.ids:
                method = self.data["methods"][mid]
                summary = method["summaries"][cohort]
                for key, value in sorted(summary["diagnostics"].items()):
                    if key == "source_paths":
                        continue
                    rows.append([method["name"], main_status(summary), key, compact(value)])
            self.table(f"Chẩn đoán đầu ra — {cohort}",
                       ["Phương pháp", "Trạng thái", "Trường", "Giá trị"], rows,
                       f"methods.<id>.summaries.{cohort}.diagnostics", "đếm theo ca ở từng dòng")
        self.add("CIRCA giữ nguyên OLS/RHT/DA của tác giả, SVR là cấu hình phụ. "
                 "Số nút RHT vượt ngưỡng và route hồi quy giúp đọc hạn chế của baseline. "
                 "Tỉ lệ nhánh dự phòng TORAI là chẩn đoán cách xếp trong cụm, không là bằng chứng về giá trị đồ thị.")
        self.add()

    def costs(self):
        for cohort in ("dev30", "dev19"):
            rows = []
            for mid in self.ids:
                method = self.data["methods"][mid]
                if not method["primary"]:
                    continue
                summary = method["summaries"][cohort]
                cost = summary["cost_summary"]
                rows.append([method["name"], main_status(summary), cost["execution_host"]["category"],
                             cost["n_cases"], cost["n_distinct_run_ids"],
                             number(cost["recorded_wall_s_sum"], 3),
                             number(cost["worker_process_wall_s_sum"], 3),
                             f'[{number(cost["recorded_wall_s_min"], 3)}; '
                             f'{number(cost["recorded_wall_s_max"], 3)}]',
                             number(cost["recorded_wall_s_median"], 3),
                             number(cost["peak_rss_mb_max"], 1)])
            self.table(f"Chi phí sáu phương pháp chính — {cohort}",
                       ["Phương pháp", "Trạng thái", "Thiết bị", "Ca", "Lượt riêng", "Tổng wall bản ghi (s)",
                        "Tổng wall worker (s)", "Khoảng wall mỗi lượt (s)", "Trung vị wall (s)", "RSS đỉnh (MiB)"],
                       rows, f"methods.<id>.summaries.{cohort}.cost_summary", "đếm theo ca ở từng dòng")
            self.add("TORAI chạy ba seed trên EC2; các phương pháp còn lại chạy laptop. "
                     "Không so trực tiếp tốc độ hai thiết bị. CIRCA DA/RHT-only dùng chung lượt, "
                     "MicroRank full/top11 cũng dùng chung lượt; bảng chỉ đếm sáu phương pháp chính, không cộng trùng biến thể. "
                     "RSS trong trường peak_rss_mb của runner chia byte cho 2^20, nên đơn vị ở đây là MiB. "
                     "Wall bản ghi là tổng thời gian đã ghi cho từng lượt; wall worker cộng thời gian các tiến trình "
                     "đọc/cắt/chuẩn bị/phương pháp của lượt đó. Thời gian phiên, lúc nghỉ và test không dùng làm benchmark. "
                     f"Nguồn cấu hình thiết bị và bản ghi chi phí: `{JSON_SOURCE}` → "
                     f"`methods.<id>.summaries.{cohort}.cost_summary.source_configs/source_paths`.")
            self.add()

    def columns(self):
        audit = self.data["raw_column_audit"]
        rows = []
        for oid, record in sorted(audit["by_case"].items()):
            rows.append([oid, record["n_columns"], record["n_missing"],
                         ", ".join(record["missing_from_union"]) or "không", record["source_path"]])
        self.table("Audit schema cột metric", ["Ca", "Số cột", "Vắng so với hợp", "Danh sách cột vắng", "Bản ghi nguồn"],
                   rows, "raw_column_audit.by_case",
                   self.cohort_status("dev30", ["circa_ols_da"]))
        self.add(f'Hợp cột trên cohort có {audit["union_n"]} cột; danh sách đầy đủ ở '
                 f'`{JSON_SOURCE}` → `raw_column_audit.union_columns`. '
                 "Đây là schema gốc trong bản ghi đã chốt, trước tiền xử lý riêng của từng phương pháp. "
                 "Không đưa dấu cột vắng vào phương pháp; chưa kiểm tương quan schema với nhãn ở P4.")
        self.add()

    def published(self):
        source = ROOT / "docs" / "knowledge" / "K4-ho-thuat-toan.md"
        lines = source.read_text(encoding="utf-8").splitlines()
        target = next((i, line) for i, line in enumerate(lines, 1)
                      if "Reported Avg@5 for BARO on RE2-TT by fault type:" in line)
        pubs = {fault.lower(): float(value) for fault, value in re.findall(
            r"\b(CPU|MEM|DISK|SOCKET|DELAY|LOSS)\s+([0-9]+(?:\.[0-9]+)?)", target[1])}
        if len(pubs) != 6:
            raise ValueError("Nguồn knowledge BARO đã đổi; cần đọc lại trước đối chiếu")
        grouped = self.data["methods"]["baro"]["summaries"]["dev30"]["grouped"]["fault"]
        rows = []
        for fault, value in pubs.items():
            own = grouped.get(fault)
            current = own["avg@5"] if own else None
            rows.append([fault, number(value), own["n"] if own else "không có ca trong dev",
                         statuses(own["trang_thai"]) if own else "N/A", number(current),
                         number(current - value) if current is not None else "N/A"])
        self.table("Đối chiếu mốc công bố BARO RE2-TT", ["Loại lỗi", "Avg@5 README", "Ca dev", "Trạng thái dev",
                   "Avg@5 T-024", "T-024 − README"], rows,
                   "methods.baro.summaries.dev30.grouped.fault", "đếm ca dev ở từng dòng")
        self.add(f'Số công bố đọc từ `docs/knowledge/K4-ho-thuat-toan.md:{target[0]}` '
                 "(ghi lại ví dụ RCAEval README). Đây là mốc tham khảo; chưa tái lập toàn bộ bảng công bố. "
                 "Khác tập ca, cửa sổ, bộ cột, quy tắc hòa và cách giữ ca lỗi ở mẫu số có thể giải thích lệch. "
                 "Phân bố loại lỗi và service trong 30 ca dev cũng khác toàn bộ RE2-TT; chưa tách riêng đóng góp của từng nguyên nhân. "
                 "Không chỉnh cấu hình theo độ lệch. Số ASE 2024 trong cùng knowledge dùng corpus Train Ticket khác; "
                 "không dùng làm mốc khớp cho RE2-TT. Knowledge chưa có bảng số đầy đủ cùng giao thức T-024 cho sáu phương pháp.")
        self.add()

    def validation(self):
        checks = self.data["validation"]
        rows = []
        kind_names = {"flat_tie": "khóa đơn có hòa", "flat_other": "ca khóa đơn khác",
                      "torai_blocks": "TORAI dev có khối cùng điểm", "torai_dev": "TORAI dev",
                      "torai_no_equal_blocks": "TORAI dev không hòa khối"}
        for check in checks["rank_checks"]:
            manual = check["manual"]
            rows.append([kind_names.get(check["kind"], check["kind"]),
                         self.data["methods"][check["method"]]["name"], check["seed"], check["opaque_id"],
                         check["root"], compact(check["rank_distribution"]), number(manual["hit@1"]),
                         number(manual["hit@3"]), number(manual["hit@5"]), number(manual["rr"]),
                         number(manual["ndcg@5"]), number(manual["avg@5"]),
                         "khớp" if check["pass"] else "không khớp"])
        self.table("Tính tay ba ca dev khác nhau và đối chiếu evaluator",
                   ["Phép kiểm", "Phương pháp", "Seed", "Ca", "Root", "Phân bố hạng tính độc lập",
                    "Hit@1", "Hit@3", "Hit@5", "RR", "NDCG@5", "Avg@5", "Đối chiếu"], rows,
                   "validation.rank_checks", self.cohort_status("dev30"))
        for check in checks["rank_checks"]:
            self.add(f'Ca `{check["opaque_id"]}`, seed {check["seed"]}: '
                     f'{compact(check["calculation"])}. Nguồn: `{JSON_SOURCE}` → '
                     f'`validation.rank_checks` (phân phối độc lập, giá trị tay và giá trị evaluator cùng lưu).')
        self.add("Theo khóa xếp hạng đã lưu, không có root trong nhóm hòa ở các bản ghi OK, "
                 "nên các cận do hòa bằng kỳ vọng. Ca BARO kiểm tay có hòa ở thực thể khác, root đứng riêng hạng 1. "
                 f'Nguồn: `{JSON_SOURCE}` → `methods.<id>.per_case.<ca>.rank_distribution_by_seed`, '
                 '`validation.rank_checks`. Công thức nhóm hòa được kiểm riêng tại '
                 '`results/T-030/tests/test_buoc2.py` (`test_nhom_hoa`), '
                 '`results/T-024/test-chay-lai/test_buoc2.txt`; fixture TORAI trình riêng bên dưới.')
        self.add()
        ties = checks["torai_cohort_ties"]
        self.table("Kiểm hòa khối TORAI trong cohort thật",
                   ["Bản ghi TORAI A/B đã chốt", "Bản ghi có khối cùng điểm"],
                   [[ties["source_records"], ties["records_with_equal_blocks"]]],
                   "validation.torai_cohort_ties", self.cohort_status("dev30", ["torai_A", "torai_B"]))
        self.add("Cohort thật không có hòa khối TORAI; nhánh hoán vị nhiều khối cùng điểm "
                 "được kiểm bằng fixture riêng theo SPEC đã sửa. Các bản ghi khoa học giữ nguyên.")
        root_rcd = {}
        for mid in ("torai_B", "torai_A"):
            method = self.data["methods"][mid]
            matching = []
            for meta in method["source_records"]:
                record = json.loads((ROOT / meta["path"]).read_text(encoding="utf-8"))
                root = method["per_case"][meta["opaque_id"]]["label"]["root"]
                if record["status"] != "OK":
                    continue
                for i, block in enumerate(record["blocks"]):
                    if any(root in group for group in block["groups"]) and record["extra"]["nhanh_khoi"][i] == "rcd":
                        matching.append(meta["opaque_id"])
            root_rcd[mid] = (len(matching), len(method["source_records"]), len(set(matching)))
        b_count, b_total, _ = root_rcd["torai_B"]
        a_count, a_total, a_cases = root_rcd["torai_A"]
        self.add("Hòa bên trong RCD (bước xếp nhân quả trong cụm của TORAI) chưa kiểm; "
                 "khối RCD hiện chỉ lưu thứ tự, không giữ khóa bên trong. "
                 f'Root TORAI B thuộc khối RCD ở {b_count}/{b_total} lượt; '
                 f'TORAI A ở {a_count}/{a_total} lượt thuộc {a_cases} ca, '
                 "nên chưa loại trừ hòa ẩn ở các lượt này. Số 0 hòa theo khóa đã lưu không chứng minh RCD không hòa. "
                 f'Nguồn: `{MANIFEST}` → bản ghi TORAI `blocks`, `extra.nhanh_khoi`; '
                 f'root nối từ `{JSON_SOURCE}` → `methods.torai_A/torai_B.per_case.<ca>.label.root`. '
                 'Giới hạn đã khai tại `results/T-022/giao-thuc-v2.md` §6.6 và `docs/WHY.md` → WHY-28. '
                 'Chưa có bằng chứng các lượt đó thật sự hòa hoặc số chấm hiện tại sai.')
        self.add()
        fixture = checks["torai_block_fixture"]
        if not fixture["excluded_from_cohort"]:
            raise ValueError("Fixture TORAI phải tách khỏi cohort")
        metric_keys = (("hit@1", "Hit@1"), ("hit@3", "Hit@3"), ("hit@5", "Hit@5"),
                       ("rr", "RR"), ("ndcg@5", "NDCG@5"), ("avg@5", "Avg@5"))
        rows = [[name, number(fixture["manual"][key]), number(fixture["evaluator"][key]),
                 "khớp" if fixture["pass"] else "không khớp"] for key, name in metric_keys]
        self.table("Fixture tổng hợp TORAI: hai khối AB/CD cùng điểm",
                   ["Độ đo", "Tính tay", "Evaluator", "Đối chiếu"], rows,
                   "validation.torai_block_fixture",
                   f'fixture {fixture["record"]["status"]}; đối chiếu '
                   f'{"đạt" if fixture["pass"] else "không đạt"}', scientific_cohort=False)
        self.add(f'Fixture: {compact(fixture["record"])}; root `{fixture["root"]}`; '
                 f'phân bố hạng `{compact(fixture["rank_distribution"])}`. '
                 f'Lý do: {fixture["reason"]}. Nguồn: `{JSON_SOURCE}` → `validation.torai_block_fixture`. '
                 "Đây là dữ liệu tổng hợp để kiểm công thức hòa khối; không thêm ca vào cohort, "
                 "không thay bản ghi đã chốt hoặc số khoa học.")
        self.add()
        rnd = checks["random_check"]
        self.table("Tính tay mức ngẫu nhiên một ca",
                   ["Phương pháp", "Ca", "|O|", "Root trong O", "O Hit@1", "O Hit@3", "O Hit@5", "O Hit@10",
                    "|U|", "U Hit@5", "Đối chiếu"],
                   [[self.data["methods"][rnd["method"]]["name"], rnd["opaque_id"], rnd["O_size"],
                     number(rnd["root_in_O"])] + [number(rnd["manual"][f"O_hit@{k}"]) for k in (1, 3, 5, 10)] +
                    [rnd["U_size"], number(rnd["U_hit@5"]), "khớp" if rnd["pass"] else "không khớp"]],
                   "validation.random_check", self.cohort_status("dev30", [rnd["method"]]))
        self.add(f'Công thức tính tay: {rnd["formula"]}. Nguồn: `{JSON_SOURCE}` → `validation.random_check.formula`.')
        self.add()
        rows = [[f"Bootstrap lặp cùng seed, {cohort}", "giống hệt" if exact else "lệch"]
                for cohort, exact in sorted(checks["bootstrap_same_seed_exact"].items())]
        rows += [["AC@k RCAEval bằng Hit@k khi không hòa",
                  f'{checks["rcaeval_no_tie_parity"]["n_checked"]} bản ghi-ca đã kiểm; khớp'],
                 ["Giữ ca khác OK ở mẫu số", number(checks["non_OK_in_denominator"])]]
        self.table("Các phép kiểm tổng hợp", ["Phép kiểm", "Kết quả"], rows,
                   "validation.bootstrap_same_seed_exact; validation.rcaeval_no_tie_parity; validation.non_OK_in_denominator",
                   self.cohort_status("dev30"))
        fake = checks["shuffled_root_check"]
        rows = []
        for mid in self.ids:
            original = self.data["methods"][mid]["summaries"]["dev30"]["main"]
            shuffled = fake["summaries"][mid]
            rows.append([self.data["methods"][mid]["name"], statuses(original["trang_thai"]),
                         number(original["hit@1"]), number(shuffled["hit@1"]),
                         number(original["avg@5"]), number(shuffled["avg@5"]),
                         number(original["mrr"]), number(shuffled["mrr"])])
        self.table("Phép thử giả: hoán vị root giữa các ca, giữ nguyên đầu ra",
                   ["Phương pháp", "Trạng thái", "Hit@1 thật", "Hit@1 root hoán vị", "Avg@5 thật",
                    "Avg@5 root hoán vị", "MRR thật", "MRR root hoán vị"], rows,
                   "validation.shuffled_root_check.summaries; methods.<id>.summaries.dev30.main",
                   "đầu ra và trạng thái ở từng dòng giữ nguyên")
        self.add(f'Hoán vị dùng seed {fake["seed"]}; root sau hoán vị vẫn trùng root thật ở '
                 f'{fake["root_unchanged_n"]} ca. Nguồn: `{JSON_SOURCE}` → `validation.shuffled_root_check`. '
                 "Phép thử này chỉ đổi nhãn trong evaluator; chưa phân biệt riêng mọi nguyên nhân khả dĩ của điểm cao. "
                 "Không dùng số phép thử giả để chọn cấu hình hoặc chạy lại phương pháp.")
        self.add()

    def build(self):
        self.add("# T-024 — Chấm tầng 1 chế độ (a) trên RE2-TT dev")
        self.add()
        self.add("Báo cáo cho RQ1 và DT18-NV3: xếp root ở mức thực thể trên ca dev, "
                 "theo giao thức V2 và cấu hình đã khóa ở T-031. " + MODE_NOTE)
        self.add()
        self.add(f"Số chấm và khoảng lấy từ `{JSON_SOURCE}`; thống kê root thuộc nhánh RCD "
                 "và đối chiếu thứ tự TraceRCA đếm từ bản ghi đã chốt, nguồn ghi cạnh nhận định. Danh sách bản ghi đã chốt trước evaluator: "
                 f"`{MANIFEST}`. Hash và mã nguồn nằm trong manifest; báo cáo không thay cấu hình đã khóa.")
        self.add()
        self.add("## Phạm vi và cách đọc")
        self.add()
        for cohort in ("dev30", "dev19"):
            c = self.data["cohorts"][cohort]
            self.add(f'- `{cohort}`: {c["n_cases"]} ca, {c["n_cells"]} ô; '
                     f'nguồn `{JSON_SOURCE}` → `cohorts.{cohort}`.')
        self.add()
        self.add("Nhóm 19 loại đúng các ca CIRCA RHT vượt 1e10 đã chốt không dùng nhãn ở T-031 "
                 "(Q-82, WHY-36). Cùng 19 ca được dùng cho mọi phương pháp. "
                 "Nhóm này chọn theo đầu ra CIRCA trên cửa sổ A, không phải mẫu ngẫu nhiên; "
                 "không chứng minh các ca còn lại không có điểm lạ khác.")
        self.add("Các ca bị loại đã được T-031 xác nhận lỗi làm tròn: sai số dự đoán gần 0 "
                 "nhưng phép chuẩn hóa vẫn chia cho số rất nhỏ, làm điểm RHT phình lớn; "
                 "bước DA dùng điểm đó kéo nút cha lên đầu. Nguồn giải thích: "
                 "`docs/WHY.md` → WHY-36; `results/T-031/chan-doan-diem-lon.json`. "
                 "Bảng 30 ca giữ ảnh hưởng lỗi này; bảng 19 ca cho phép xem kết quả khi loại các ca đó.")
        self.add()
        self.dev19_composition()
        excluded = self.data["cohorts"]["dev19"]["excluded_case_ids"]
        self.add("Ca loại khỏi phép so 19: " + ", ".join(excluded) + ". "
                 f"Nguồn: `{JSON_SOURCE}` → `cohorts.dev19.excluded_case_ids`; "
                 "`results/T-031/kiem-11-ca-hashseed.json`.")
        self.add()
        self.add("Sáu dòng chính: BARO, SimpleRCA, MicroRank full, TraceRCA, CIRCA OLS+RHT+DA, TORAI B. "
                 "Dòng phụ giữ CIRCA RHT-only/SVR, TORAI A và MicroRank top11. "
                 "TORAI A dùng bin tác giả lệch lưới và ngưỡng tracets_lat trên toàn file; "
                 "chỉ có kết quả sau cuối file, khác khả năng có kết quả lúc t+300 của dòng chính.")
        self.add()
        self.add("## Bảng gộp và bất định")
        self.add()
        for cohort in ("dev30", "dev19"):
            if cohort == "dev19":
                self.add(self.dev19_note())
                self.add()
            self.summaries(cohort)
            self.rcaeval(cohort)
            self.random(cohort)
            self.bootstrap(cohort)
            self.seeds(cohort)
        self.add("## Phân tầng")
        self.add()
        for cohort in ("dev30", "dev19"):
            self.stratified(cohort)
        self.add("## Từng ca và bốn tập")
        self.add()
        self.per_case()
        self.sets()
        self.add("## Chẩn đoán, audit cột và tự kiểm")
        self.add()
        self.diagnostics()
        self.costs()
        self.columns()
        self.validation()
        self.add("## Đối chiếu và giới hạn")
        self.add()
        self.published()
        self.add(self.tracerca_order_note())
        self.add()
        error_mr = self.data["methods"]["microrank_full"]["summaries"]["dev30"]["main"]["trang_thai"]["ERROR"]
        error_tr = self.data["methods"]["tracerca"]["summaries"]["dev30"]["main"]["trang_thai"]["ERROR"]
        self.add(f'{error_mr} ca MicroRank ERROR và {error_tr} ca TraceRCA ERROR được giữ trong mẫu số. '
                 f'Nguồn: `{JSON_SOURCE}` → `methods.microrank_full.summaries.dev30.main.trang_thai` '
                 'và `methods.tracerca.summaries.dev30.main.trang_thai`. '
                 "MicroRank giữ lỗi operation mới không có nền theo quyết định đã ghi ở LOG T-031; "
                 "thông điệp lỗi TraceRCA và từng ca nằm trong bản ghi nguồn đã chốt, "
                 "nên số đo phản ánh cả giới hạn bản cài. "
                 "Không suy số dev sang 60 ca test, không mở dữ liệu khóa. "
                 "Chế độ phát hiện (b) thuộc T-025; số ở đây không đo chất lượng phát hiện. "
                 "Không kết luận về giá trị đồ thị hoặc chọn phương pháp tốt nhất từ thứ tự điểm trung bình. "
                 "Kết quả mô tả xếp hạng của sáu baseline đã chốt và các khoảng bất định, trước phân tích P4.")
        self.add()
        return "\n".join(self.lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=OUT / "cham-a.json")
    parser.add_argument("--output", type=Path, default=OUT / "cham-a.md")
    args = parser.parse_args()
    # Nguồn JSON và đầu ra phải thuộc đúng task; không cho caller ghi ra ngoài phạm vi.
    args.input = args.input.resolve()
    args.output = args.output.resolve()
    if OUT.resolve() not in args.input.parents or OUT.resolve() not in args.output.parents:
        raise ValueError("Input/output phải trong results/T-024")
    if not (OUT / "ban-ghi-dua-vao-cham.json").is_file():
        raise ValueError("Chưa có manifest chốt bản ghi")
    data = json.loads(args.input.read_text(encoding="utf-8"))
    if data["schema_version"] != 1 or data["mode"] != "a":
        raise ValueError("Schema hoặc chế độ không đúng T-024")
    if set(ORDER) != set(data["methods"]):
        raise ValueError("Thiếu hoặc thêm biến thể ngoài danh sách T-024 đã chốt")
    text = Report(data).build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    print(f"Đã ghi {args.output}; {len(text.splitlines())} dòng")


if __name__ == "__main__":
    main()
