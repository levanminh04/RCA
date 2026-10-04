# Exclusive current-file edit; only the T017 row is replaced/inserted.
$statePath='D:/RCA-flashticket/docs/STATE.md'
$recordPath='D:/RCA-flashticket/results/T-017/runs/state-edit-check.json'
$enc=[System.Text.UTF8Encoding]::new($false,$true)
$newRow='| T-017 | Hồ sơ SimpleRCA M4 và luật Type I/II | P1 | Codex | Claude | chờ phản biện (04/10/2026) | `tasks/T-017-simplerca/` |'
$stream=[System.IO.FileStream]::new($statePath,[System.IO.FileMode]::Open,[System.IO.FileAccess]::ReadWrite,[System.IO.FileShare]::None)
try {
    $beforeBytes=[byte[]]::new($stream.Length)
    if($stream.Read($beforeBytes,0,$beforeBytes.Length) -ne $beforeBytes.Length){throw 'incomplete current read'}
    $before=$enc.GetString($beforeBytes)
    $rowPattern='(?m)^\| T-017 \|[^\r\n]*(?:\r?\n|$)'
    $match=[regex]::Match($before,$rowPattern)
    if($match.Success){
        $index=$match.Index;$old=$match.Value
        $newline=if($old.EndsWith("`r`n")){"`r`n"}else{"`n"}
        $replacement=$newRow+$newline
        $after=$before.Substring(0,$index)+$replacement+$before.Substring($index+$old.Length)
    } else {
        $tableStart=$before.IndexOf('## Mục lục task')
        $tableEnd=$before.IndexOf("`n## ",$tableStart+1)
        if($tableStart -lt 0 -or $tableEnd -lt 0){throw 'task table unavailable'}
        $matches=[regex]::Matches($before.Substring($tableStart,$tableEnd-$tableStart),'(?m)^\| T-\d{3} \|[^\r\n]*(?:\r?\n|$)')
        if($matches.Count -eq 0){throw 'no task table row'}
        $last=$matches[$matches.Count-1]
        $index=$tableStart+$last.Index+$last.Length
        $old='';$newline=if($last.Value.EndsWith("`r`n")){"`r`n"}else{"`n"}
        $replacement=$newRow+$newline
        $after=$before.Substring(0,$index)+$replacement+$before.Substring($index)
    }
    $outsideBefore=[regex]::Replace($before,$rowPattern,'')
    $outsideAfter=[regex]::Replace($after,$rowPattern,'')
    if($outsideBefore -cne $outsideAfter){throw 'unrelated content would change'}
    $offset=$enc.GetByteCount($before.Substring(0,$index))
    $tail=$enc.GetBytes($after.Substring($index))
    $stream.Position=$offset
    $stream.Write($tail,0,$tail.Length)
    $stream.SetLength($offset+$tail.Length)
    $stream.Flush($true)
    $stream.Position=0
    $afterBytes=[byte[]]::new($stream.Length)
    if($stream.Read($afterBytes,0,$afterBytes.Length) -ne $afterBytes.Length){throw 'incomplete reread'}
    if($enc.GetString($afterBytes) -cne $after){throw 'reread mismatch'}
    $record=[ordered]@{status='PASS';old_row=$old.TrimEnd();new_row=$newRow;read_under_exclusive_lock=$true;exact_T017_only=$true;other_content_byte_identical=$true;write_start_byte=$offset;whole_file_rewrite=$false;time=[DateTimeOffset]::Now.ToString('o')}
    [System.IO.File]::WriteAllText($recordPath,($record|ConvertTo-Json),$enc)
    $record|ConvertTo-Json
} finally {$stream.Dispose()}
