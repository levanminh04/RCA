# Codex giả cho phép thử mô phỏng: lần đầu báo hết hạn mức (giờ hồi = phút kế tiếp theo giờ máy), lần resume trả OK.
import sys, datetime as dt, uuid, pathlib
args = sys.argv[1:]
data = sys.stdin.buffer.read()
out = args[args.index('-o') + 1]
if 'resume' in args:
    sid = args[args.index('resume') + 1]
    print(f'session id: {sid}'); print('resume bytes', len(data)); print('tokens used\n10')
    pathlib.Path(out).write_text('OK sau resume\n', encoding='utf-8'); sys.exit(0)
sid = str(uuid.uuid4())
hoi = (dt.datetime.now() + dt.timedelta(minutes=1)).strftime('%I:%M %p').lstrip('0')
print(f'session id: {sid}'); print('brief bytes', len(data))
print(f"ERROR: You've hit your usage limit. Upgrade to Pro, visit https://chatgpt.com/settings/usage to purchase more credits or try again at {hoi}.")
sys.exit(1)
