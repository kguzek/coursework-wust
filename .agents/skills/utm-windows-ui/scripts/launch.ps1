param([Parameter(Mandatory=$true)][string]$RunDir)
$ErrorActionPreference = 'Stop'
try {
    $request = Get-Content -Raw -LiteralPath "$RunDir\request.json" | ConvertFrom-Json
    if ($request.process -notmatch '^[A-Za-z0-9_.-]+$') { throw 'Invalid process name.' }
    $processes = @(Get-CimInstance Win32_Process -Filter "Name='$($request.process).exe'" |
        Where-Object { $_.SessionId -gt 0 -and (!$request.pid -or $_.ProcessId -eq $request.pid) })
    if ($processes.Count -ne 1) {
        throw "Expected one matching desktop process, found $($processes.Count). Use --pid to disambiguate."
    }
    $target = $processes[0]
    $owner = Invoke-CimMethod -InputObject $target -MethodName GetOwner
    if ($owner.ReturnValue -ne 0) { throw 'Cannot resolve target process owner.' }
    $account = "$($owner.Domain)\$($owner.User)"
    & "$env:SystemRoot\System32\icacls.exe" $RunDir /grant "${account}:(OI)(CI)M" | Out-Null
    if ($LASTEXITCODE -ne 0) { throw 'Cannot grant the desktop user access to the run directory.' }
    @{ pid = $target.ProcessId; session = $target.SessionId; account = $account } |
        ConvertTo-Json | Set-Content -LiteralPath "$RunDir\target.json" -Encoding UTF8
    $action = New-ScheduledTaskAction -Execute "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe" `
        -Argument "-NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$RunDir\inspect.ps1`" -RunDir `"$RunDir`""
    $principal = New-ScheduledTaskPrincipal -UserId $account -LogonType Interactive -RunLevel Limited
    $settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Minutes 5) `
        -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
    Register-ScheduledTask -TaskName $request.task -Action $action -Principal $principal `
        -Settings $settings | Out-Null
    Start-ScheduledTask -TaskName $request.task
    @{ ok = $true; account = $account; session = $target.SessionId } |
        ConvertTo-Json | Set-Content -LiteralPath "$RunDir\launch.json" -Encoding UTF8
} catch {
    @{ ok = $false; error = ($_ | Out-String) } |
        ConvertTo-Json | Set-Content -LiteralPath "$RunDir\launch.json" -Encoding UTF8
    exit 1
}
