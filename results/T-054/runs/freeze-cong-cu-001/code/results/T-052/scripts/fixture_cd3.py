"""Lỗi/quá giờ đối chứng không làm đổi hạng đã đóng dấu."""
import subprocess
import time
from unittest.mock import patch
from common import ROOT,RUN,digest,read,save,timing
import p7_entry

def main():
    start=time.perf_counter()
    target=ROOT/'results/T-052/fixtures-p7-001'
    source=target/'method-records.json'
    sha=digest(source)
    common=dict(dataset='RE2-TT',timeout_s=15)
    actual=p7_entry.cd3_after_seal(source,sha,target/'cd3-actual.json',**common)
    with patch('p7_entry.subprocess.run',return_value=subprocess.CompletedProcess([],1,'','synthetic failure')):
        failure=p7_entry.cd3_after_seal(source,sha,target/'cd3-error.json',**common)
    with patch('p7_entry.subprocess.run',side_effect=subprocess.TimeoutExpired('synthetic',15)):
        timeout=p7_entry.cd3_after_seal(source,sha,target/'cd3-timeout.json',**common)
    assert failure['trang_thai']=='ERROR' and timeout['trang_thai']=='TIMEOUT'
    assert digest(source)==sha
    save(RUN/'fixture-cd3-001.json',timing('cd3_fixture',start,PASS=True,
         actual_status=actual['trang_thai'],error_isolated=True,timeout_isolated=True,main_hash_unchanged=True))

if __name__=='__main__':main()
