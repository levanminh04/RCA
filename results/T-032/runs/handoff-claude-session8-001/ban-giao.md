# Bàn giao T-032 — cuối phiên8 theo yêu cầu Minh

Minh yêu cầu checkpoint kỹ và bàn giao cho Claude xử lý. Codex dừng mọi khởi chạy mới. Task/gói MicroRank chưa hoàn tất; không nghiệm thu, không đóng RQ2/P4/G2.

## Trạng thái thật

13/52ca PASS exact:2ca cũ hợp lệ và11ca mới phiên8. Còn39ca:38not_run và Nezha-OB/dev-63c30faf34 preparePASS nhưng chưa native/observed. Master/table/segment002 vẫn FAIL_STOP; không đổi FAIL thành PASS. Ca dở chỉ có prepare/check.json, prepare.json, progress.jsonl, hash/fullset đạt, methods_executed=false/stdoutPASS/stderr rỗng. Lỗi attach_child đợi lock rồi lookupPID đã kết thúc, trước gọi phương pháp. Không có so sánh RCA thất bại ở ca này.

Freshrootcheck13ca: native–frozen–observed24fields bit/type/source/capture/T028/order/ties/score/null/closed đầy đủ đạt;3839hashchecks gồm helperpins. Chưa RE2 mới đầu tiên, không có truepeakRE2 để ghi; không dùng peak retrospective thay. Chưa003/004. Mọi kết quả và hashes ở checkpoint.json/manifest, không dựa chat.

Không còn actualcontroller/supervisor/accountant/RAMmonitor do phiên này khởi.137identity đã đóng có proofgốc,139đóng ở lần đọc trước. Lần đọc cuối historicalchildPID3032 accessdenied5, creationtimehiện tại UNKNOWN; không suy PID là worker cũ hoặc kill process khác. Oldidentityabsent proof giữ; xem v3-tool-check/root/handoff-process-read-001.json. Không identity nào được quan sát alive.

## Đã làm và còn thiếu

Đạt: kiểm tiếp nhận/pilot001; v2fullfixtures/forecast5h; launch002 đóng11ca mới; đo overhead thật; giữfailure/kiểm toolabortsource-only; tạo draft3/fixtures/sourcepins; witness khoa học một ca sai pilot.

Chưa đạt:full52/trueRE2peak/operationalv3migration+forecast+budget/A′/coreTrace,CIRCA,TORAI/fullBARO,Simple runtime đối chứng/tổng hợp đủ5đầu raP4. Không coi code/fixturePASS là gói chạy xong.

Bản3 NOT_LAUNCH_ELIGIBLE:
- Controller3 giữPopen kernelhandle/ctime/Windowspeak dù workerngắn và chỉ revisit livePID.19artifactcontroller fullset/hashPASS. Fixtures giữ21exactgate, fake routing reuseprepare/native/observed/audit1lần, không RCA.
- Launcher003/verifier3 có13artifact fullset/hashPASS; readonly13ca+1prepare giữfailedtime. LatestPowerShellarrayfix chưa rerunfake, future003/checkpoint/full52 verifier staticonly. Root chưa đọc/kiểm toànv3diff.
- Controller3 đang resetcase_started khi tiếppreparevalid: phải cộng priorprepareelapsed và giữbytebaseline trong600s/150MiB. Scalar/bound này chưa chốt. Khôngresetcap rồi chạy.
- Fixturemigration làsynthetic/fixture_only, khôngoperationalpermission. Chưafinalmigration3/forecast39/toolledger/pins/freshbudget.
- Recoveryrootreceipt chỉ đúng002/đúngprepare trướcnative; giữallFAIL/oldcases. Không genericFAILresume, không lặpprepare/method, khôngskip/tolerance.

## Chi phí và RAM

Chargedprior trước v3tools2163,835252s:toolv2charge213,235439 (táchactual/allocation120),001actual423,893617+20reserve,002failedactual1486,706197+20reserve. Không bỏfailedtime hoặc resetwholepackage.
Measuredtools3controller4,887440s/launcher9,903740s/rootfailureaudit4,203913s. Rootreads/checkpoint/prelaunch/closing chưachốtledger; cộng hostactual/explicitallowance, không cộngtimercon hayoverlap2lần.

39rows oldslowmodel còn10982,210237s/987.794.404B trướcnewclosing/toolsallowance; chỉ draft/notupperbound/notlaunchforecast. Cần chốt freshforecast đủactualhistory+failedcost+tools+metadata/reused/ERRORroutes.

TrầnMicro giữ5h toàngói/new2,5GiB/local4GiB/combined12GiB/case600s150MiB/oneworker/allchecks/exact. RAM chỉ thiếuworkerRAM hoặc system>=95%, khôngfixed4,55GBfreegate. Q125TraceRAM riêng, không ápMicrothreshold.

Actual002inventory213call931,458034s trêncontroller1477,431870s (~63%), nguồn overhead chính trong đoạn đãđo; maxscan20,996447s. Không biết tỷtrọngv1pilot chưainstrument. V2RAMsamplemaxgap3,515369s; standalone50ms1124samples/67,114809s/maxgap0,120473s. Guardpeak88,5%; standalone71%chỉtừstartnó. Chưa95%. Sumindividualpeaks không simultaneoustreepeak; sampledRAM không Windowslifetimeworkerpeak.

## Tiếp nhận và bước kế chính xác

1. ĐọcAGENTS/STATE/SPEC/LOGmục cuối; checkpoint.json và hashmanifest trên filethật. Đọcold002failure/table/prepare/rootproof, không tin notes làm bằng chứng.
2. Vai trò:SPECkhóaCodexngườilàm/Claudengườiphảnbiện. Minh yêu cầubàn giaoClaude xửlý. Đềxuất tối thiểu đổi đúng2dòngSPEC thànhClaudengườilàm/Codexngườiphảnbiện, giữnội dungkhác. Codex chưa sửaSPEC/DECISIONSđổivai vì chưa trình đúnghaidòngfileđó. Trước khi sửaSPEC cầnMinhduyệt đúngđềxuất theoLuật0; chưa có thì đọc/soáttrongchat. Không tựmởreview hoặc suy promptcấpquyền ngoàiSPEC.
3. Đọc toàncurrentv3/diff/fixtures; xửlýprior600s/bytecap từtimestamps/log/precedingcaseclosure vàbaseline cócăn cứ. Newversion nếu sửa, giữdrafts/failures. Rerunpurefake sauarrayfix và kiểmfuture/checkpoint/full52; không rerunnative.
4. Chốt cumulativetoolledger/migrationnewghimpreviousv2+rootrecovery+currentpins, forecast39. Freshlocal+EC2bytes/RAM/disk/jobs<=300s; snapshot002stale. Không cólệnhlaunch003 đãđược rootkiểm: KHÔNG chạy launch-command002 hoặcfixturemigration.
5. Khiđủkiểm/budget,003remaining39 StopAfterFirstRe2, reusepreparevalid. Nezha còn10rồiRE2mớiđầu. Đóng/accountantseal/fullhash/exact/PID/byte/wall; ghi trueWindowspeaknative/observedRE2LOG, freshbudget/resume004remaining28 tựtiếp trongQ126. Sameplace3fails/caps/RAM/exactdiff đúngđiềukiệnstop.
6. Full52 rồiverifyexpectfull/allsources/checks/nonOK/NAs/scoretie/order/budget. Q124 yêu cầuWHYbổ sung trước dùngMicro nhánhlaptoptrongbáocáo; WHY42 chưa được tựghi. SauMicro tiếpLog trongquyềnthật, không đóngRQ2 vìexact.

Lệnh mở đầu chỉ đọc:
Get-Content -LiteralPath AGENTS.md
Get-Content -LiteralPath docs/STATE.md
Get-Content -LiteralPath tasks/T-032-g2-nguyen-nhan-xep-hang/SPEC.md
Get-Content -LiteralPath tasks/T-032-g2-nguyen-nhan-xep-hang/LOG.md -Tail 180
Get-Content -LiteralPath results/T-032/runs/handoff-claude-session8-001/checkpoint.json -Raw
Get-Content -LiteralPath results/T-032/runs/microrank-laptop-cohort-001-v3-tool-check/root/tool-abort-recovery-001.json -Raw
Get-Content -LiteralPath results/T-032/runs/microrank-laptop-cohort-001-v3-tool-check/controller/summary.json -Raw
Get-Content -LiteralPath results/T-032/runs/microrank-laptop-cohort-001-v3-tool-check/launcher/handoff-notes-001.md

Laptopmainenv D:/RCA-ext/envs/T-014-main/Scripts/python.exe, -B -X utf8/PYTHONDONTWRITEBYTECODE=1/hashseed0/five threadunset Q124. No installs/envchanges. EC2ubuntu@3.26.62.217/key2.pem, /home/ubuntu/rca/T-032, mainenv /home/ubuntu/rca/T-025/envs/main/bin/python. OnlyT032writes. Codexdefaulttools lỗihelper_unknown_error; require_escalated scopedjustification đọc/sửaT032 đãhoạtđộng. Không nhầm lỗi hosttool với methodfailure.

## Mục tiêu khoa học và phần còn mở

Micro witness001 caNezhasai: wholetraceA→operationcoverage→weightedcells→entitymax; frontendmaxcurrency vượtshipping. Không chứng minh frontendchờshipping. Cần tất cảlockedcorrectcontrols/fullpreferred/runtimeconditions; đặc tính chung không nguyênnhânriêngmọicasai. Witness002 KHÔNGtạo: draft dùng nhầm graphoperation_trace(operationkey). Codegraph.py operation_trace maps trace→operations, trace_operation maps operation→traceIDs. Readingerrors giữ trongreading-attempt-failure.json; chưacorrectedrerun. Pairpilotk5index166, không1668; k1index146khôngcorrectcontrol.

BAROnewruntime-witness001 chỉcheckpoint3file6887B/501links369pairs52endpoint chưa runtimefull. Rawlocal66.542.465B;14preparedtablesdedup vềadapter-input theoactualcalls, khôngfilemất. Simple331linksactualrowwitness ở396.191.713BrawEC2chưalocal; readingview cốýbỏrowwitness. KhôngremoteT032write/download khiMicroactive fixedremotegrowth0, tránhcasebytecap.

Tracev2 có33purefake/66artifact/sourcepins; rootfullcode/EC2runtime/transfer/firstcasecheckpoint/49newchưalàm. Q1254,5h2,5GiB/RAM6GiBtree+1GiBavailable/7GiBstartup giữ. CIRCAv4draftrootreview/pilotpending; TORAI_Bnotcorecaptured. A′notrun/coreJ0nativeunitshaminvariantsrequired. Physicalwait/instrumentationsemantics/P9a/graphbenefitOPEN. FullcohortexactvẫnphảichỉstepYlàmmất/đánhgiásaiZ trongX/cảcađúngsai; táchobservation/inference/candidate/decided/open.

## Files và quyền

Phiên này nốiQ126DECISIONS/LOG, chỉT032STATErow, newT032tools/runs cùngMicroliveoutputs/witness001/Tracev2/BAROcheckpoint. Giữallversions/failures. Gitdirtykhácpreexisting; khôngclaimowned/xóa/commit. KhôngSPEC/WHY/MRP/shared/rawdata/test/locked/T033/archivechanges. Khôngcommit/push.

Promptsoátđộc lập nguyênmẫuriêng ởprompt-kiem-doc-lap.md; khôngtựcấpquyềnđổi vai/chạy. Minhchọncopy; Codexkhôngtựgửimessage/mởphiênClaude.
