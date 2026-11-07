# T-054 — checkpoint008: OB source-native và phần chuẩn bị còn chặn

Codex người làm; Claude phản biện. Nguồn quyền có điều kiện tại checkpoint.json và DECISIONS; SPEC/WHY đã cập nhật trước code. Đã triển khai ứng viên đã trình, không suy quyềnG3/main.

## Thay đổi và căn cứ
Nămfilecode đúngscope được sửa: p3/nezha.py thêm source_native opt-in, mặcđịnhlegacy; m1/adapter.py biểu diễn mẫu thật vớiindexnguồn; m1/chuoi.py kiểmmapping vàchấm đúngsource; p3/adapters/nezha.py BAROtheosource vàghépkhóa, SimpleRCA/tracegiữpipeline; workerT054 bậtlayoutrõchoOB. Khônggiảtimestamp, đệm, dịchmốc, bỏca haygán0. Bản5N5A giữđườngcũ. Code diff đầyđủ: code-diff.patch. Đây là sửa biểu diễn input/adapter, không chứng minh cơ chế hoặc hiệuquảRCA.

## Kiểm và giới hạn
43kiểm OBtổnghợpPASS trongsynthetic002;1TTmặcđịnhfullrecord exactPASS ở003;92kiểm tíchhợpdữliệugiảPASS. SixconfigM1/bỏE1/E2/E5/C-a0/a1 trên5N5A cho toànrecord trùngcoretrướcpatch. BAROforcedsourcewise↔rectangular giữitems/keys/hòa/hạng;2N5A/3N5A/6N5A/5N6A giữsốmẫu/timestampthật. Năm loại mapping sai bịbác; nguồnrỗng giữERRORgốcBARO, khôngbịépOK. Hai giảđịnh test sai giữlượt001/002vàstderr; chỉsửatest, khôngđổicoređểlàmđẹp.1DEVOBdev-607751ac0a chạyworker thật trênlaptop cho rawrecord vànormalizedinputexact với receipt005 được007kếthừa, đãkiểm pin006. Laptop đượcdùngchoexactparity với thamchiếu cùngmáy; cloudkhôngtruycậpđược. Khôngruncác4testOBhoặcchấmnhãn;khôngRCAtelemetryRE3. Các kiểm này không làfullcohort, bảnđánhgiáđộhiệuquả hoặcparity trêncloud.

## Bước3 và4
Đãchuẩnbịcandidate35/25mới tại prepared/: EC2_1=523job+2C-einsufficient;EC2_2=817jobgồm68UNSUPPORTED;laptop300job.1640job+2dònghỗtrợ=1642vịtrí, tốiđa1572lượtđượchỗtrợ; C-d3códependencychađúngpin/thứtự. Đãkiểmschema/slot/union/phụthuộc vàthửauthorizechặncả3hostbằngWAIT_G3. KhôngfakeLOCKEDpolicy/attestation đểqua validator. Protocol/contract/placement/sourcebundlemới cópinriêng;rootmetadatachỉcậpnhậtsaukhifilecandidatecóthật. Khôngsửa006/007hoặcdùngactivate006choplan35/25.

Hai SSHendpointđềutimeout. SauđóMinhbáotàikhoảnAWSbịtạmkhóa vàcho tạm dừngphầncloud; đãdừngSSH/sync/staging/kiểmmáy. Chưachuyển5TTthêm,OBhoặccode008; chưaxácnhậnidentity/env/RAM/đĩahiệntại. Khôngtựchạyfullmaintrênlaptop/cấpmáykhác. ChưađủG3: actualcomputehost/source/staging/parity/bindings vàdựtoánđĩađầyđủcònthiếu. Cócandidate vàhồsơđiểmchặn, khôngcóđềnghịkhóaG3hoặcnghiệmthutoàntask.

## RE3 và công việc local tiếp
90schema007giữhợp lệ; khônglấy lại. Đãlấycardtĩnh7887byteđúngGitblobHFrevisionđãpin: xácnhậnmetric.timeunixseconds vàpublishermôtảuniontimestamp/nullatrest. Khôngsuyđơnvịint64trace/duration/log từđó. re3-contract-008.json tách phầnxácnhận vàOPEN: đơnvịtrace/log,inventory/frontend-external,profiles5schema,cadence/severity/coverage/support/adapter/bảngriêng. ChưaH2adapter; khôngmởtelemetryđểtune. Đây là thiếu hợpdồngđầuvàoRE3, khôngtựbỏRE3khỏinghiêncứu.

## AWS và bảo toàn kết quả
Theo lệnhMinh, đãlàmkiểm kêlocal vàbáohệquảnếumấtEC2: aws-loss-report.md; chi tiết/aws-loss-local-audit.json vàaws-loss-main-source-presence.json. Khôngcoitàikhoảnkhóalàmấtdata. PhầnrawintermediateT048khôngcótạicácđườnglocaltrongmanifestlàrủirocụthể; cácgóilocalđãkiểmkhôngcầnchạylạivìđổimáy. Ghiđúnggiớihạnkiểm, khôngtuyênbốmọiremoteđãbackup.

## Tiếp nhận
Đọccheckpoint.json,báocáonày,code-diff.patch,dev-ob-001/parity.json,prepared-validation.json,aws-loss-report.md vàre3-contract-008.json. Kiểmmanifest008 trước dùng. Giữvai trò/phạmvi vàquyềnAWSpauseriêng; tiếpnhữngphầnlocalđãđượcduyệt, khônglặpkiểmđãhợp lệ vìđổiphiên. NếuMinhchoresumecloud: kiểmidentity/env/source/codebyte008 rồi chỉbổsungphầnthiếu. Candidate008cònWAIT_G3vàthẩmquyềnmainriêng; khôngrun/resume/activate từcheckpointnày. Khôngcommit/push. Bất kỳ replayfullrawmấtphải làrunmớivàtrìnhlýdo/quyềnđúngphần, khôngtựmởtaskđãđóng.
