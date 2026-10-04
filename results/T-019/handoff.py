"""Enumerate the full review scope, append literal template prompt, verify handoff."""
import argparse, ast, csv, hashlib, json, pathlib, re, sys
from acquire import ROOT, OUT, DATA, dump, csvout
TASK=ROOT/'tasks/T-019-the-sock-shop'
HEAD='93f13d4c4a966428177e2acc287d96bc89303e92'

def template():
    text=(ROOT/'docs/review-prompt.md').read_text(encoding='utf-8')
    common=text.split('## Prompt chung',1)[1].split('```text',1)[1].split('```',1)[0].strip('\n')
    g1=text.split('**G1 — phương pháp, dataset, cách chia:**',1)[1].split('```text',1)[1].split('```',1)[0].strip('\n')
    return common,g1

def inventory():
    paths=sorted([p.resolve() for p in OUT.rglob('*') if p.is_file()]+[p.resolve() for p in DATA.rglob('*') if p.is_file()]+[p.resolve() for p in pathlib.Path('D:/RCA-ext/work/T-019').rglob('*') if p.is_file()])
    return [TASK/'SPEC.md',TASK/'LOG.md']+paths

def prompt_for(paths):
    common,g1=template()
    listing='\n'+'\n'.join('- '+p.as_posix() for p in paths)
    filled=common.replace('<T-xxx>','T-019').replace('<T-xxx-tên>','T-019-the-sock-shop').replace('<danh sách>',listing).replace('<commit gốc>',HEAD)
    return filled+'\n\n'+g1

def build():
    for name in ['artifact-manifest.json','handoff-checks.json']:
        if not (OUT/name).exists():dump(OUT/name,{'pending':True})
    if not (OUT/'output-files.csv').exists():csvout(OUT/'output-files.csv',[{'path':'pending','scope':'pending'}])
    paths=inventory();prompt=prompt_for(paths)
    log=TASK/'LOG.md';previous='## Prompt phản biện cho Claude — T-019' in log.read_text(encoding='utf-8')
    report=(OUT/'bao-cao-cuoi.md').read_text(encoding='utf-8')
    append='\n\n'+('## Bổ sung đóng gói bàn giao — 04/10/2026\n\nKiểm đóng gói lượt1 báo trailing spaces ở README nguồn nguyên bản và dòng placeholder của prompt nguyên văn. Giữ source/prompt nguyên trạng, chỉ kiểm whitespace văn bản do T019 viết ngoài code fence; giữ failedchecks trong handoff-checks-001-failed.json. Không thay số liệu hoặc phạm vi. Prompt mới cuối LOG thay bản trước về danh sách file (có thêm record lượt kiểm hỏng); cả hai bản cũ/mới được giữ theo luật append-only.\n\n' if previous else '## Kết thúc phiên — 04/10/2026\n\n')+report.split('\n',1)[1]
    append+='\n**Kết thúc phiên đủ6ý theo mẫu:**\n1. Đã làm: xem A; toàn phần được phép và khả thi đã kiểm, status chờ Claude.\n2. File thay đổi: xem B, output-files.csv và toàn danh sách dưới; nguồn cũ giữ hash trong phạm vi có baseline.\n3. Kiểm tra: xem C/final-checks.json/handoff-checks.json; không chạy RCA/detector.\n4. Điều chưa chắc/cần Minh: xem G/H; chưa chọn dataset/chia hoặc dùng nhãn detail lỗi.\n5. Bước tiếp theo chính xác: Minh mở phiên Claude, dán nguyên prompt cuối này; Claude đọc SPEC/LOG và mọi file liệt kê, ghi đúng tasks/T-019-the-sock-shop/REVIEW.md. Kiểm read-only rẻ: `.venv/Scripts/python.exe -X utf8 -B results/T-019/verify_final.py --read-only`; không chạy runner nguồn.\n6. Lệnh cuối cùng dự kiến sau ghi LOG: `py -3 -X utf8 -B results/T-019/handoff.py verify`; lệnh kiểm diff trước đó: `git diff --check -- docs/STATE.md tasks/T-019-the-sock-shop results/T-019`. Không dùng diff làm phạm vi phản biện; danh sách file dưới đầy đủ cả cache và file ngoài repo.\n'
    append+='\n## Prompt phản biện cho Claude — T-019\n\n```text\n'+prompt+'\n```\n'
    with log.open('a',encoding='utf-8',newline='') as f:f.write(append)
    paths=inventory();records=[]
    mutable={OUT/'artifact-manifest.json',OUT/'handoff-checks.json'}
    for p in paths:
        if p.is_relative_to(DATA):scope='data_inside_repo_outside_git'
        elif not p.is_relative_to(ROOT):scope='outside_repo'
        else:scope='task_output'
        records.append({'path':p.as_posix(),'scope':scope,'bytes':p.stat().st_size,'sha256':None if p in mutable or p.name=='output-files.csv' else hashlib.sha256(p.read_bytes()).hexdigest()})
    csvout(OUT/'output-files.csv',[{k:r[k] for k in ['path','scope']} for r in records])
    # Hash output-files.csv after its complete path list is written; self/check digest excluded.
    for r in records:
        if pathlib.Path(r['path'])==OUT/'output-files.csv':r.update(bytes=(OUT/'output-files.csv').stat().st_size,sha256=hashlib.sha256((OUT/'output-files.csv').read_bytes()).hexdigest())
    dump(OUT/'artifact-manifest.json',{'scope':'all task outputs, SS ignored cache, all outside task files; STATE row audit is separate','files':records,'self_and_handoff_check_hash':'excluded to avoid self-reference; paths are included','counts':{'SS_data_files':sum(r['scope']=='data_inside_repo_outside_git' for r in records),'outside_repo_files':sum(r['scope']=='outside_repo' for r in records),'task_output_files':sum(r['scope']=='task_output' for r in records)}})
    verify()

def verify():
    manifest=json.loads((OUT/'artifact-manifest.json').read_text(encoding='utf-8'));paths=inventory();log=(TASK/'LOG.md').read_text(encoding='utf-8')
    prompt=log.rsplit('## Prompt phản biện cho Claude — T-019',1)[1].split('```text\n',1)[1].split('\n```',1)[0]
    rows=manifest['files']; checks={}
    checks['full_file_set_matches_inventory']=set(r['path'] for r in rows)==set(p.as_posix() for p in paths)
    checks['recorded_output_hashes_still_match']=all(hashlib.sha256(pathlib.Path(r['path']).read_bytes()).hexdigest()==r['sha256'] for r in rows if r['sha256'])
    checks['prompt_literal_common_plus_G1_and_full_list']=prompt==prompt_for(paths)
    checks['no_unfilled_prompt_placeholders']=not bool(re.search(r'<(?:T-|danh sách|commit gốc)',prompt))
    checks['six_end_items_present']=all('\n'+str(i)+'. ' in log.split('**Kết thúc phiên đủ6ý theo mẫu:**',1)[1].split('## Prompt phản biện',1)[0] for i in range(1,7))
    checks['A_through_H_report_present']=all('**'+x+'. ' in log for x in 'ABCDEFGH')
    checks['all_python_sources_parse']=True
    for p in OUT.rglob('*.py'):ast.parse(p.read_text(encoding='utf-8-sig'))
    def prose_clean(p):
        if p.is_relative_to(OUT/'sources-audit/snapshots'):return True # Preserve third-party source bytes.
        in_fence=False
        for line in p.read_text(encoding='utf-8').splitlines():
            if line.startswith('```'):in_fence=not in_fence;continue
            if not in_fence and line!=line.rstrip():return False
        return True
    checks['own_markdown_prose_no_trailing_whitespace']=all(prose_clean(p) for p in list(OUT.rglob('*.md'))+[TASK/'SPEC.md',TASK/'LOG.md'])
    checks['STATE_row_waiting_review']=any(x.startswith('| T-019 |') and 'chờ phản biện (04/10/2026)' in x for x in (ROOT/'docs/STATE.md').read_text(encoding='utf-8').splitlines())
    checks['both_STATE_splices_preserved_other_bytes']=all(json.loads((OUT/f).read_text(encoding='utf-8'))['other_bytes_preserved'] for f in ['state-start.json','state-finish.json'])
    checks['scientific_final_checks_pass']=json.loads((OUT/'final-checks.json').read_text(encoding='utf-8'))['all_pass']
    result={'checks':checks,'all_pass':all(checks.values()),'counts':manifest['counts'],'source_of_prompt':'docs/review-prompt.md common and G1, exact except neutral substitutions','git_diff_used_as_scope':False}
    dump(OUT/'handoff-checks.json',result);print(json.dumps(result,ensure_ascii=False,indent=2));assert result['all_pass']

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['build','verify']);args=parser.parse_args();build() if args.mode=='build' else verify()
