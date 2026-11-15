$ErrorActionPreference='Stop'
$name='FlashTicket-L1-Tunnel-Probe'
try {
 $service=New-Object -ComObject Schedule.Service
 $service.Connect()
 $folder=$service.GetFolder('\')
 $definition=$service.NewTask(0)
 $definition.RegistrationInfo.Description='L1 authorized tunnel durability probe; writes only in tai-2/bo-sung-1'
 $definition.Principal.UserId=[Security.Principal.WindowsIdentity]::GetCurrent().Name
 $definition.Principal.LogonType=3
 $definition.Settings.Enabled=$true
 $definition.Settings.AllowDemandStart=$true
 $definition.Settings.ExecutionTimeLimit='PT2M'
 $action=$definition.Actions.Create(0)
 $action.Path=(Join-Path $PSHOME 'powershell.exe')
 $action.Arguments='-NoProfile -NonInteractive -WindowStyle Hidden -File "'+$PSScriptRoot+'\scheduler-probe.ps1"'
 $action.WorkingDirectory=$PSScriptRoot
 $task=$folder.RegisterTaskDefinition($name,$definition,6,$null,$null,3,$null)
 $null=$task.Run($null)
 $record=@{utc=[DateTime]::UtcNow.ToString('o');registered=$true;name=$name;independentLauncher='Windows Task Scheduler';rollback='Delete only task FlashTicket-L1-Tunnel-Probe when probe complete'}
} catch {
 $record=@{utc=[DateTime]::UtcNow.ToString('o');registered=$false;name=$name;error=$_.Exception.Message;hresult=$_.Exception.HResult;action='Do not bypass; preserve restriction and continue independent load code'}
}
[IO.File]::WriteAllText("$PSScriptRoot/scheduler-register.json",($record|ConvertTo-Json),(New-Object System.Text.UTF8Encoding($false)))
$record|ConvertTo-Json
