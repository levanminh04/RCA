> **LỊCH SỬ — không dùng nữa.** Đề xuất ngày 02/10/2026. Minh bác nhóm cưỡng chế bằng settings/hooks (DX-01 đến DX-05; quyết định Q-14) và bỏ DX-06 đến DX-13. Đã làm DX-14, DX-15, DX-16 (chọn i). Luật hiện hành nằm ở `AGENTS.md`.

# Đề xuất khung làm việc có kiểm soát

- Trạng thái: **ĐỀ XUẤT, chưa áp dụng.** Soạn ngày 02/10/2026 theo yêu cầu của Minh. File này chỉ mô tả; không có thiết lập nào trong file đang chạy.
- Cách duyệt: trả lời theo số, ví dụ "duyệt DX-01, DX-03; sửa DX-05: ...; bỏ DX-07". Mỗi đề xuất được duyệt sẽ làm đúng phạm vi đã ghi, theo Luật 0.

## Phần A — `settings.json` hoạt động thế nào

Nguồn: tài liệu chính thức [Configure permissions](https://code.claude.com/docs/en/permissions) và [Hooks](https://code.claude.com/docs/en/hooks), đọc ngày 02/10/2026.

**1. Ba loại luật.** Mỗi lần agent gọi một công cụ (đọc file, sửa file, chạy lệnh), Claude Code so lời gọi đó với ba danh sách:

- `deny`: chặn hẳn.
- `ask`: bắt buộc hỏi Minh.
- `allow`: cho chạy không hỏi.

Thứ tự xét là deny → ask → allow; khớp danh sách nào trước thì theo danh sách đó. Allow không mở được ngoại lệ cho deny. Nếu một lời gọi khớp cả ask lẫn allow thì vẫn hỏi.

**2. Luật về file.** Chỉ hai loại luật có hiệu lực với file: `Edit(đường dẫn)` cho thao tác ghi và `Read(đường dẫn)` cho thao tác đọc. Luật `Edit` áp dụng cho cả việc sửa lẫn tạo file mới.

- Viết luật cho `Write` thì Claude Code chấp nhận nhưng không bao giờ dùng tới.
- Luật deny và ask cho file cũng áp dụng cho các lệnh Bash mà Claude Code nhận ra là đọc hoặc ghi file: `cat`, `sed`, `tee`, và chuyển hướng `> file`.
- Lệnh `python script.py` tự ghi file bên trong thì **không** bị luật file bắt.
- Cách viết đường dẫn:
  - `/x` tính từ thư mục repo;
  - `//d/...` là đường dẫn tuyệt đối trên ổ D;
  - `~/` tính từ thư mục người dùng.

**3. Chế độ quyền.** Chế độ quyết định những gì **không** khớp luật nào thì xử lý ra sao:

| Chế độ | Ghi file | Lệnh Bash |
|---|---|---|
| `default` (Manual) | Hỏi. Có nút "cho phép đến hết phiên" | Hỏi, trừ lệnh chỉ đọc có sẵn |
| `acceptEdits` | Tự cho phép trong thư mục làm việc | Hỏi, trừ `mkdir`, `touch`, `mv`, `cp` |
| `auto` | Không hỏi; một bộ phân loại tự xét | Không hỏi |
| `bypassPermissions` | Không hỏi gì | Không hỏi gì |

Có thể tắt hẳn hai chế độ `auto` và `bypassPermissions` bằng `disableAutoMode` và `disableBypassPermissionsMode`.

**4. Hook** là một chương trình nhỏ chạy **trước** mỗi lời gọi công cụ.

- Nó nhận tên công cụ, đường dẫn file và chế độ hiện tại.
- Nó trả về một trong bốn kết quả: `deny` (chặn), `ask` (buộc hỏi), `allow`, hoặc không quyết.
- Hook không vượt được luật deny và ask: luật ask vẫn hỏi kể cả khi hook trả về allow.
- Hook có lối thoát mã 2 thì chặn ngay, trước cả các luật.
- Có thêm hai loại hook nhắc việc:
  - `SessionStart`: đưa thông tin vào đầu mỗi phiên.
  - `UserPromptSubmit`: chạy mỗi khi Minh gửi tin.

**5. Nơi đặt file.** Có bốn cấp, ưu tiên từ cao xuống:

1. Cấp tổ chức (managed).
2. Cấp dòng lệnh.
3. `.claude/settings.local.json` của repo (riêng máy, không đưa vào git).
4. `.claude/settings.json` của repo (đưa vào git).
5. `~/.claude/settings.json` của người dùng.

Deny ở bất kỳ cấp nào cũng thắng allow ở cấp khác. Luật allow ở cấp repo chỉ có hiệu lực sau khi Minh chấp nhận hộp thoại "tin tưởng thư mục".

**Trả lời câu "10 file có phải bấm 10 lần không":**

- Ở chế độ `default`, lần ghi đầu tiên có nút "cho phép đến hết phiên". Bấm một lần là xong cho cả phiên, nhưng sau đó **mọi** lần ghi đều được phép, kể cả ngoài phạm vi.
- Ở chế độ `acceptEdits` thì không phải bấm lần nào.
- Vì vậy cần thêm luật ask và hook (DX-04, DX-05) để những file nằm ngoài phạm vi vẫn bị hỏi, dù đang ở chế độ nào.

## Phần B — Các cơ chế người dùng thật khuyên dùng: đã có chưa

| # | Cơ chế (nguồn) | Hiện trạng | Đề xuất |
|---|---|---|---|
| 1 | Cưỡng chế luật bằng công cụ, không chỉ bằng chữ ([dev.to](https://dev.to/krisnamic/stop-telling-claude-code-rules-enforce-them-with-hooks-3po1); HN: agent bỏ qua CLAUDE.md sau 4–5 lượt) | **Chưa có.** Luật 0 mới là chữ, và phiên hiện tại đang chạy chế độ `auto` | DX-01 → DX-05 |
| 2 | File luật luôn nạp phải ngắn, dưới khoảng 100 dòng (Boris; hướng dẫn Codex) | **Chưa đạt.** AGENTS.md có 123 dòng | DX-09 |
| 3 | Nhắc luật giữa phiên, vì luật nạp ở đầu phiên mất dần tác dụng | **Chưa có** | DX-06, DX-07 |
| 4 | Tách lên kế hoạch khỏi thực thi; spec trước khi làm (HN 47106686) | **Có trên giấy** (AGENTS), chưa có mẫu spec | DX-10 |
| 5 | Phiên ngắn, chuyển giao qua file trạng thái 30–50 dòng (HN `mikepurvis`, `roughly`) | **Có.** STATE.md 27 dòng, có mục checkpoint | DX-12 |
| 6 | Vòng tự kiểm: test, so với số công bố (Boris) | **Có trên giấy** (MRP §6), chưa có code | Làm trong từng gói |
| 7 | Phản biện chéo: người phản biện chỉ báo, không sửa (nghiên cứu arXiv 2607.21656: khi được tự sửa, phản biện có thể làm kết quả tệ đi) | **Có trên giấy**, chưa cưỡng chế bằng công cụ | DX-08 |
| 8 | Mỗi khẳng định trỏ về bằng chứng; báo "phép kiểm đã qua", không báo "phương pháp chạy tốt" (ARIS) | **Chưa có** | DX-11 |
| 9 | Commit nhỏ để hoàn tác được (HN `onion2k`) | **Chưa có.** Repo chưa có commit nào | DX-13 |
| 10 | Sổ bài học tích lũy qua các phiên | **Có:** LESSONS.md, bộ nhớ agent | — |

## Phần C — Các đề xuất

### Nhóm 1: Cưỡng chế bằng công cụ

**DX-01. Tắt `auto` và `bypassPermissions`; phiên mặc định ở chế độ `default`.**

- File: tạo `.claude/settings.json` với `defaultMode: "default"`, `disableAutoMode: "disable"`, `disableBypassPermissionsMode: "disable"`.
- Vì sao: ở chế độ `auto`, agent ghi file không cần hỏi. Đây chính là cách lỗi vi phạm Luật 0 hôm nay đã xảy ra.
- Minh cần làm thêm: chuyển chế độ của phiên đang mở trong app về Manual.

**DX-02. Cho phép sẵn các lệnh chỉ đọc của git.**

- Thêm vào `allow`: `git status`, `git diff`, `git log`. Các lệnh chỉ đọc khác vốn đã được Claude Code cho phép sẵn.
- Vì sao: không làm phiền Minh bằng những lệnh không thay đổi gì.

**DX-03. Chặn hẳn (deny).**

- Đọc và ghi repo RCA cũ: `Read(//d/Project/flash-ticket-rca-research/**)`, `Edit(//d/Project/flash-ticket-rca-research/**)`.
  - Vì sao: đây là chốt chống neo bằng công cụ. Agent không còn đọc được kết luận cũ, kể cả khi quên luật.
- Ghi vào repo FlashTicket: `Edit(//d/Project/flash-ticket-platform/**)`. Vẫn cho đọc, vì P9a cần đọc chuẩn B16.
- Đọc và ghi dữ liệu khóa: `Read(/data/locked/**)`, `Edit(/data/locked/**)`.
  - Tập test và dataset giữ ngoài sẽ được đặt trong thư mục này.
  - Chỉ Minh gỡ luật này, ở cổng G3.

**DX-04. Luôn hỏi (ask), dù đang ở chế độ nào.**

- Ghi vào các file luật và quyết định:
  - `AGENTS.md`, `CLAUDE.md`, `.claude/**`;
  - `docs/MRP.md`, `docs/DECISIONS.md`, `docs/WHY.md`, `docs/LESSONS.md`;
  - `docs/specs/**`, `docs/knowledge/**`, `docs/reference/**`;
  - bộ nhớ agent `~/.claude/projects/**/memory/**`.
- Các lệnh: `git commit`, `git push`, `git reset`, `git checkout`, `rm`, `Remove-Item`.
- Vì sao: các file này quyết định hướng đi và luật chơi. Agent không được tự sửa chúng, kể cả khi đang được phép ghi trong một gói việc. Spec cũng nằm trong danh sách này, nên agent không tự nới được phạm vi của mình.

**DX-05. Hook kiểm phạm vi ghi: duyệt một lần cho mỗi gói.**

- Gồm hai file:
  - `.claude/scope.txt`: danh sách thư mục mà gói đang chạy được ghi, chép từ mục "Phạm vi ghi" của spec đã duyệt. File này nằm trong `.claude/`, nên mỗi lần sửa nó đều phải qua Minh (DX-04).
  - `.claude/hooks/scope_guard.py`: chạy trước mỗi lần ghi file.
    - File nằm trong phạm vi: để luồng quyền bình thường xử lý.
    - File ngoài phạm vi, hoặc chưa có phạm vi nào: buộc hỏi Minh.
- Kết quả khi làm một gói:
  - Minh duyệt spec và nội dung `scope.txt` (1 lần bấm).
  - Minh bật `acceptEdits`.
  - Agent ghi 10 file trong phạm vi mà không hỏi thêm.
  - Chạm ra ngoài phạm vi thì bị hỏi.
- Giới hạn: script Python tự ghi file bên trong không đi qua hook. Vì vậy spec phải ghi rõ script ghi vào đâu, và bước tự kiểm phải liệt kê các file mới sinh ra.

**DX-06. Hook đầu phiên (`SessionStart`).** Tự đưa tóm tắt Luật 0 và nội dung STATE.md vào đầu mỗi phiên, kể cả phiên mở lại sau khi hết usage. Vì sao: phiên mới không phụ thuộc vào việc agent tự nhớ đi đọc.

**DX-07. Hook nhắc mỗi lượt (`UserPromptSubmit`).** Thêm đúng một dòng nhắc vào mỗi tin Minh gửi: "Luật 0: câu hỏi không phải lệnh sửa; muốn sửa thì đề xuất rồi chờ duyệt." Vì sao: người dùng thật thấy luật bị quên sau vài lượt. Chi phí: khoảng 30 token mỗi lượt.

**DX-08. Codex phản biện ở chế độ chỉ đọc.**

- Lệnh chuẩn, Minh chạy:

  ```
  codex exec -s read-only -C D:\RCA-flashticket -o docs\reviews\<cổng>-<ngày>.md "<prompt>"
  ```

- Model chạy trong sandbox chỉ đọc, nên không sửa được file nào. Chương trình Codex tự lưu câu trả lời cuối vào file `-o`. Máy đang có codex-cli 0.130.0, đã kiểm có hai tùy chọn `-s` và `-o`.
- Vì sao: người phản biện chỉ báo lỗi kèm bằng chứng, không được sửa.

### Nhóm 2: Quy trình bằng file

**DX-09. Rút gọn AGENTS.md xuống dưới 100 dòng.**

- Giữ lại: vai trò, Luật 0, luật cứng, cách bắt đầu phiên, dấu hiệu đi sai.
- Chuyển phần "cách làm một gói", "phản biện", "văn phong" sang `docs/QUY-TRINH.md`, chỉ đọc khi cần.
- Không đổi nội dung luật, chỉ chuyển chỗ.

**DX-10. Mẫu spec `docs/specs/_MAU.md`.** Các mục:

- mục tiêu (câu nào của cô, DT18, RQ nào);
- đầu vào;
- đầu ra;
- **Phạm vi ghi** (dùng cho DX-05);
- các bước, mỗi bước có lệnh kiểm;
- tiêu chí xong;
- những gì không làm;
- chi phí ước lượng.

**DX-11. Sổ khẳng định `docs/CLAIMS.md`.**

- Mỗi câu kết luận sẽ đưa vào báo cáo cho cô có một dòng: câu khẳng định; file kết quả; lệnh chạy lại; trạng thái (đã kiểm / chưa kiểm / đã bác bỏ).
- Câu không có dòng trong sổ thì không được viết vào báo cáo.
- Vì sao: chống viết số từ trí nhớ (SL17) và nói quá bằng chứng.

**DX-12. Một phiên, một bước.**

- Xong một bước thì cập nhật STATE, rồi Minh mở phiên mới hoặc dùng `/clear`.
- Không làm hai gói trong cùng một phiên.
- Vì sao: ngữ cảnh rối trước cả khi đầy (HN `roughly`).

**DX-13. Commit sau mỗi bước được duyệt.**

- Cuối mỗi bước, agent đề xuất nội dung commit. Minh bấm duyệt; lệnh commit luôn phải hỏi theo DX-04.
- Commit đầu tiên chứa bộ tài liệu hiện có.
- Vì sao: mỗi bước đều hoàn tác được. Thiết kế khóa ở G3 cũng dựa vào commit.

### Nhóm 3: Các việc dọn còn treo

**DX-14.** Trong `docs/WHY.md` và `docs/LESSONS.md`, đổi "Task A §D.3", "Task A §F", "Task A §J" thành "K1 §D.3", "K1 §F", "K1 §J". Đánh số mục trong K1 giữ như cũ.

**DX-15.** Trong MRP P6, đổi "Cách này sai khi…" thành "Quy tắc phân rã theo cây lời gọi sai khi…". Câu cũ không còn rõ nghĩa sau khi bỏ câu về thăm dò 30/30.

**DX-16.** Hai ghi chú `docs/reference/notes/second_dataset_candidates.md` và `advisor_method_families.md`, chọn một trong ba:

- (i) lọc như K1: bỏ các mục "Inferences" và "Takeaway" (đây là phần suy luận), giữ "Cited Findings", gộp vào `docs/knowledge/`;
- (ii) bỏ hẳn;
- (iii) giữ nguyên.

Agent đề nghị (i): phần trích dẫn có đường dẫn nguồn, hữu ích cho P1 và P2; phần suy luận là chỗ dễ neo.

## Phần D — Bản nháp các file (chưa ghi)

`.claude/settings.json`:

```json
{
  "permissions": {
    "defaultMode": "default",
    "disableAutoMode": "disable",
    "disableBypassPermissionsMode": "disable",
    "allow": ["Bash(git status*)", "Bash(git diff*)", "Bash(git log*)"],
    "ask": [
      "Edit(/AGENTS.md)", "Edit(/CLAUDE.md)", "Edit(/.claude/**)",
      "Edit(/docs/MRP.md)", "Edit(/docs/DECISIONS.md)", "Edit(/docs/WHY.md)", "Edit(/docs/LESSONS.md)",
      "Edit(/docs/specs/**)", "Edit(/docs/knowledge/**)", "Edit(/docs/reference/**)",
      "Edit(~/.claude/projects/**/memory/**)",
      "Bash(git commit *)", "Bash(git push *)", "Bash(git reset *)", "Bash(git checkout *)",
      "Bash(rm *)", "PowerShell(Remove-Item *)"
    ],
    "deny": [
      "Read(//d/Project/flash-ticket-rca-research/**)", "Edit(//d/Project/flash-ticket-rca-research/**)",
      "Edit(//d/Project/flash-ticket-platform/**)",
      "Read(/data/locked/**)", "Edit(/data/locked/**)"
    ]
  },
  "hooks": {
    "SessionStart": [{"hooks": [{"type": "command", "command": "py -3 .claude/hooks/session_start.py"}]}],
    "UserPromptSubmit": [{"hooks": [{"type": "command", "command": "py -3 .claude/hooks/remind.py"}]}],
    "PreToolUse": [{"matcher": "Edit|Write|NotebookEdit",
                    "hooks": [{"type": "command", "command": "py -3 .claude/hooks/scope_guard.py"}]}]
  }
}
```

`.claude/hooks/scope_guard.py` (lõi):

```python
import json, sys, fnmatch, pathlib
data = json.load(sys.stdin)
root = pathlib.Path(data["cwd"]).resolve()
target = pathlib.Path(data["tool_input"].get("file_path") or data["tool_input"].get("notebook_path", "")).resolve()
scope_file = root / ".claude" / "scope.txt"
patterns = [l.strip() for l in scope_file.read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.startswith("#")] if scope_file.exists() else []
try:
    rel = target.relative_to(root).as_posix()
except ValueError:
    rel = None
if rel and any(fnmatch.fnmatch(rel, p) for p in patterns):
    sys.exit(0)  # trong phạm vi: để luồng quyền bình thường quyết
print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
      "permissionDecision": "ask",
      "permissionDecisionReason": f"Ngoài phạm vi ghi của gói đang chạy: {rel or target}"}}))
```

## Phần E — Một gói việc chạy thế nào khi khung đã bật

1. Agent viết spec, gồm mục "Phạm vi ghi". Lần ghi spec bị hỏi, vì spec nằm trong danh sách DX-04. Minh đọc rồi duyệt.
2. Agent ghi `.claude/scope.txt` từ mục "Phạm vi ghi". Lần này cũng bị hỏi; Minh kiểm nội dung rồi duyệt.
3. Minh bật `acceptEdits`. Agent làm việc; mọi file trong phạm vi được ghi mà không hỏi.
4. Agent chạm file ngoài phạm vi, hoặc file luật: bị hỏi. Minh chọn cho hay không.
5. Xong bước: agent cập nhật STATE và đề xuất commit. Lệnh commit bị hỏi; Minh duyệt.
6. Minh tắt `acceptEdits`, mở phiên mới cho bước sau. Hook đầu phiên tự đưa STATE vào.

## Phần F — Điều chưa kiểm, sẽ thử trước khi bật thật

Nếu Minh duyệt DX-01 → DX-07, agent sẽ thử từng điểm dưới đây trên file nháp rồi báo kết quả trước khi coi là xong:

1. Luật ask cho `Edit` có còn hỏi khi đang ở `acceptEdits` không. Tài liệu nói luật ask được xét trước allow, nhưng chưa nói rõ trường hợp chế độ tự cho phép.
2. Hook trả về `ask` có buộc hỏi khi đang ở `acceptEdits` không.
3. Lệnh `py -3` của hook có chạy được trong app desktop trên Windows không, và có cần đường dẫn tuyệt đối không.
4. Luật deny đặt ở cấp repo có chặn được việc đọc repo cũ không. Các lệnh đọc qua Bash như `cat` có bị chặn không.
5. Chuyển sang chế độ `default` trong lúc phiên hiện tại đang chạy có cần mở phiên mới không.
