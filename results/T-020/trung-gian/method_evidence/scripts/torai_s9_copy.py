"""T-016 R1: tính lại tỉ lệ ô trùng logts trên TOÀN BẢNG (SPEC S9) từ so-sanh đã lưu, không chạy lại Drain.
Mẫu số = 96 dòng × Σ_service max(cột mẫu, cột dựng); tử số = số ô trùng sau phép gán (đã lưu)."""
import json
for f in ("results/T-016/runs/s9/so-sanh-lan1.json", "results/T-016/runs/s9/so-sanh-lan2.json"):
    k = json.load(open(f, encoding="utf-8"))
    print(f)
    for key, v in k["logts"].items():
        ms = 96 * sum(max(s["cot_mau"], s["cot_dung"]) for s in v["theo_service"].values())
        print(f"  {key}: ô trùng {v['o_trung']}; toàn bảng {v['o_trung']}/{ms} = {v['o_trung'] / ms:.4f}; "
              f"độ phủ bảng mẫu {v['o_trung']}/{v['so_o']} = {v['o_trung'] / v['so_o']:.4f}")
