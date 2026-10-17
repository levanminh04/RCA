"""Chuẩn hóa con trỏ tài liệu; không đổi model, số, phép so hoặc kết luận."""
import datetime as dt
import difflib
from pathlib import Path
from engine import ROOT, OUT, load, save, checksum, canon


def main():
    run=OUT/'runs/chinh-con-tro-tai-lieu-001'
    run.mkdir(exist_ok=False)
    old=load(OUT/'manifest.json')
    (run/'manifest-before.json').write_bytes((OUT/'manifest.json').read_bytes())
    (run/'fix_report_references.py').write_bytes(Path(__file__).read_bytes())
    changed=[]
    for name in ['bao-phu-nguon.md','phan-tich-chenh-lech.md','LICH-SU.md','finish_reports.py']:
        path=OUT/name
        before=path.read_text(encoding='utf-8')
        after=before
        # Chỉ các tham chiếu hiển thị trong tài liệu, không thay đường dẫn input của script.
        for stem in ['mismatch-source-followup.json','incident.json','content-index.json','coverage.json','archive-structures.json']:
            after=after.replace('`coverage/'+stem,'`runs/trien-khai-001/coverage/'+stem)
        after=after.replace('`java-source/','`runs/trien-khai-001/java-source/')
        if after!=before:
            (run/('before-'+name)).write_bytes(path.read_bytes())
            path.write_text(after,encoding='utf-8')
            (run/(name+'.diff')).write_text(''.join(difflib.unified_diff(before.splitlines(keepends=True),after.splitlines(keepends=True),fromfile=name+':before',tofile=name+':after')),encoding='utf-8')
            changed.append(path.relative_to(ROOT).as_posix())
    assert len(changed)==4
    allowed=set(changed)
    unchanged=[r for r in old['files'] if r['path'] not in allowed]
    assert all(checksum(ROOT/r['path'])==r['sha256'] for r in unchanged)
    import ast
    ast.parse((OUT/'finish_reports.py').read_text(encoding='utf-8'))
    log=ROOT/'tasks/T-038-p5b-trainticket/LOG.md'
    log_before=log.read_bytes()
    (run/'LOG-before.md').write_bytes(log_before)
    with log.open('ab') as f:
        f.write(('\n\n**Rà con trỏ tài liệu cuối:** chuẩn hóa các tham chiếu rút gọn coverage/java-source thành đúng runs/trien-khai-001/ trong báo cáo/LICH-SU và script tái tạo. Không đổi số, graph/mapping hoặc kết luận; toàn bộ artifact trước ngoài bốn file văn bản/mã tái tạo giữ hash. Bản trước và diff ở runs/chinh-con-tro-tai-lieu-001/. Kiểm cuối triển khai vẫn28/28đạt; manifest cập nhật theo đúng file đã đổi/thêm. Lệnh cuối: `py -3 -X utf8 -B results/T-038/fix_report_references.py`. Bước tiếp không đổi: Minh chuyển prompt cho Claude, quyết phần thiếu; không tự nghiệm thu/commit/push.\n').encode('utf-8'))
    assert log.read_bytes().startswith(log_before)
    save(run/'verification.json',dict(ok=True,changed=changed,all_other_previous_artifact_hashes_unchanged=True,unchanged_count=len(unchanged),model_comparison_results_changed=False,conclusion_changed=False,log_append_only=True,log_sha256=checksum(log),underlying_checks='runs/ket-phien-002/final-verification.json',current_STATE_sha256=checksum(ROOT/'docs/STATE.md')))
    files=[]
    quarantined={'runs/trien-khai-001/coverage/content-index.json','runs/trien-khai-001/coverage/coverage.json','runs/trien-khai-001/coverage/archive-structures.json'}
    for path in sorted(p for p in OUT.rglob('*') if p.is_file() and p!=OUT/'manifest.json'):
        relative=path.relative_to(OUT).as_posix()
        files.append(dict(path=path.relative_to(ROOT).as_posix(),bytes=path.stat().st_size,sha256=checksum(path),validation='hash-only-source-or-quarantined' if relative.startswith('sources/') or relative in quarantined else 'derived-artifact'))
    old.update(created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),file_count=len(files),files=files,total_artifact_bytes_excluding_manifest=sum(r['bytes'] for r in files),documentation_reference_correction='runs/chinh-con-tro-tai-lieu-001/verification.json',last_external_LOG_sha256=checksum(log))
    save(OUT/'manifest.json',old)
    print(canon(dict(ok=True,changed_documents=4,file_count=len(files),logical_bytes_excluding_manifest=old['total_artifact_bytes_excluding_manifest'],manifest_bytes=(OUT/'manifest.json').stat().st_size,comparison_results_unchanged=True)))


if __name__=='__main__':main()
