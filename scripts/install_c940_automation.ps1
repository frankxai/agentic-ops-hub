# Idempotent C940 deterministic automation installer.
[CmdletBinding()]
param(
    [switch]$ValidateOnly
)

$ErrorActionPreference = 'Stop'
$PwshAlias = Join-Path $env:LOCALAPPDATA 'Microsoft\WindowsApps\pwsh.exe'
$Pwsh = if (Test-Path -LiteralPath $PwshAlias -PathType Leaf) { $PwshAlias } else { (Get-Command pwsh -ErrorAction Stop).Source }
$UserId = if ($env:USERDOMAIN) { "$env:USERDOMAIN\$env:USERNAME" } else { $env:USERNAME }

$Definitions = @(
    [pscustomobject]@{
        Name = 'StarlightAgentWatchdog'
        Script = Join-Path $HOME 'Starlight-Intelligence-System\scripts\agent-watchdog.ps1'
        Trigger = 'two-hourly'
        At = $null
        LimitMinutes = 10
        Arguments = ''
        Description = 'Bounded resource and orphan-process watchdog; no worktree deletion.'
        Enabled = $true
    },
    [pscustomobject]@{
        Name = 'StarlightSecretScan'
        Script = Join-Path $HOME 'Starlight-Intelligence-System\scripts\api-secret-scan.ps1'
        Trigger = 'daily'
        At = '04:45'
        LimitMinutes = 45
        Arguments = ''
        Description = 'Fail-closed secret scan across validated active repositories.'
        Enabled = $true
    },
    [pscustomobject]@{
        Name = 'StarlightSubstrateBackup'
        Script = Join-Path $HOME 'Starlight-Intelligence-System\scripts\run-restic-backup.ps1'
        Trigger = 'daily'
        At = '01:15'
        LimitMinutes = 120
        Arguments = ''
        Description = 'SIS/restic backup with repository self-exclusion and snapshot verification.'
        Enabled = $true
    },
    [pscustomobject]@{
        Name = 'StarlightMorningBrief'
        Script = Join-Path $HOME 'starlight-voice\scripts\morning-brief.ps1'
        Trigger = 'daily'
        At = '04:30'
        LimitMinutes = 15
        Arguments = ''
        Description = 'Daily local Starlight voice brief.'
        Enabled = $true
    },
    [pscustomobject]@{
        Name = 'StarlightCrossRepoIndexer'
        Script = Join-Path $HOME 'Starlight-Intelligence-System\scripts\run-cross-repo-indexer.ps1'
        Trigger = 'daily'
        At = '03:00'
        LimitMinutes = 30
        Arguments = ''
        Description = 'Disabled: canonical private/memory-bus indexer implementation is absent.'
        Enabled = $false
    },
    [pscustomobject]@{
        Name = 'ArcaneaAgentSurface'
        Script = Join-Path $HOME 'Arcanea\scripts\agent-surface-watch.ps1'
        Trigger = 'hourly'
        At = $null
        LimitMinutes = 10
        Arguments = '-Quiet'
        Description = 'Hourly Arcanea agent-surface snapshot; no permanent watcher process.'
        Enabled = $true
    }
)

$missing = @($Definitions | Where-Object { -not (Test-Path -LiteralPath $_.Script -PathType Leaf) })
if ($missing.Count -gt 0) {
    $missing | ForEach-Object { Write-Error "Missing task script for $($_.Name): $($_.Script)" }
    exit 2
}

if ($ValidateOnly) {
    [pscustomobject]@{
        valid = $true
        pwsh = $Pwsh
        user = $UserId
        definitions = $Definitions
    } | ConvertTo-Json -Depth 5
    exit 0
}

function New-HourlyTrigger([int]$Hours) {
    return New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(5) -RepetitionInterval (New-TimeSpan -Hours $Hours) -RepetitionDuration (New-TimeSpan -Days 3650)
}

function Register-BoundedTask($Definition) {
    $trigger = switch ($Definition.Trigger) {
        'daily' { New-ScheduledTaskTrigger -Daily -At ([datetime]::ParseExact($Definition.At, 'HH:mm', $null)) }
        'hourly' { New-HourlyTrigger -Hours 1 }
        'two-hourly' { New-HourlyTrigger -Hours 2 }
        default { throw "Unsupported trigger kind: $($Definition.Trigger)" }
    }

    $scriptArgs = "-NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$($Definition.Script)`""
    if ($Definition.Arguments) { $scriptArgs += " $($Definition.Arguments)" }
    $action = New-ScheduledTaskAction -Execute $Pwsh -Argument $scriptArgs -WorkingDirectory (Split-Path $Definition.Script)
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes $Definition.LimitMinutes)
    $principal = New-ScheduledTaskPrincipal -UserId $UserId -LogonType Interactive -RunLevel Limited

    Register-ScheduledTask -TaskName $Definition.Name -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description $Definition.Description -Force | Out-Null
    if ($Definition.Enabled) {
        Enable-ScheduledTask -TaskName $Definition.Name | Out-Null
    } else {
        Disable-ScheduledTask -TaskName $Definition.Name | Out-Null
    }
    Write-Host "Installed $($Definition.Name) [$($Definition.Trigger), enabled=$($Definition.Enabled)] -> $($Definition.Script)"
}

foreach ($definition in $Definitions) {
    Register-BoundedTask $definition
}

Write-Host "Installed $($Definitions.Count) bounded C940 automations." -ForegroundColor Green
