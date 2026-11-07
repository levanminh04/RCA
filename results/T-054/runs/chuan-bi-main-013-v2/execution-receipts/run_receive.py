"""Gọi đúng receive_main v2 đã ghim, chỉ nạp trước module T-054 để không bị module trùng tên ở task cũ che khuất.
Không sửa file nào; ghi danh sách module thực nạp và đối chiếu code-pins."""
import json, os, runpy, sys, traceback
ROOT = 'D:/RCA-flashticket'
RUN = ROOT + '/results/T-054/runs/chuan-bi-main-013-v2'
os.chdir(ROOT)
sys.path[:0] = [ROOT + '/results/T-054/scripts', ROOT + '/src', ROOT + '/results/T-052/scripts', RUN]
import cham, dieu_phoi, nguon, bien_nhan  # noqa: E401  pinned T-054 modules
sys.argv = ['receive_main.py'] + sys.argv[1:]
status = 'OK'
try:
    runpy.run_path(RUN + '/receive_main.py', run_name='__main__')
except BaseException:
    status = 'ERROR'
    traceback.print_exc()
finally:
    pins = json.load(open(RUN + '/code-pins.json', encoding='utf-8'))['code_pins']
    loaded = sorted({os.path.relpath(m.__file__, ROOT).replace('\\', '/') for m in list(sys.modules.values())
                     if getattr(m, '__file__', None) and os.path.abspath(m.__file__).startswith(os.path.abspath(ROOT))})
    with open(RUN + '/execution-receipts/receive-002-modules.json', 'x', encoding='utf-8') as f:
        json.dump({'status': status, 'loaded_repo_modules': loaded, 'not_in_code_pins': [p for p in loaded if p not in pins],
                   'wrapper': 'pre-import T-054 cham/dieu_phoi/nguon/bien_nhan, then runpy receive_main.py v2 unchanged'},
                  f, ensure_ascii=False, indent=1)
    if status != 'OK':
        sys.exit(1)
