. "$PSScriptRoot/remote.ps1"
foreach($role in @('app','obs')) {
    Invoke-Oracle $role "set -e; test -f /home/ubuntu/t058/resources-30m-$role.done; date -u"
    Receive-Oracle $role "/home/ubuntu/t058/resources-30m-$role.jsonl" "$PSScriptRoot/resources-30m-$role.jsonl"
    Receive-Oracle $role "/home/ubuntu/t058/resources-30m-$role-summary.json" "$PSScriptRoot/resources-30m-$role-summary.json"
}
py -3 -X utf8 "$PSScriptRoot/summarize-resources.py"
if($LASTEXITCODE -ne 0){throw 'Resource summary failed'}
