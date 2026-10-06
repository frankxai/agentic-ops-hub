# Registers the 2026-10-06 estate-views tasks in the Starlight Queen inbox.
# Run from any session that may write the shared estate checkout (the Queen, Grok, or Frank). It never overwrites.
#   pwsh ops/queue-proposals/2026-10-06-estate-views/register.ps1            # runnable tasks into queen/inbox, held ones into the hold folder
#   pwsh ops/queue-proposals/2026-10-06-estate-views/register.ps1 -Release 2026-10-06-estate-views-site-wall   # move one held task up
param([string]$Estate = 'C:\Users\frank\starlight', [string]$Release)
$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$inbox = Join-Path $Estate 'queen\inbox'
$holdName = '_hold-estate-views-wave2-20261006'
$holdDir = Join-Path $inbox $holdName
if (-not (Test-Path $inbox)) { throw "no queen inbox at $inbox" }

function Test-Envelope($file) {
  $t = Get-Content $file -Raw | ConvertFrom-Json
  foreach ($k in 'id','class','priority','agent','risk','sandbox','what','why','do','evidence','owner','maxMinutes') { if ($null -eq $t.$k) { throw "$($file): missing $k" } }
  if ($t.priority -isnot [int] -and $t.priority -isnot [long]) { throw "$($file): priority must be an integer" }
  if ($t.agent -ne 'frank' -and -not $t.repo) { throw "$($file): agent task needs repo" }
  if ($t.do -notmatch 'Done when') { throw "$($file): do needs a Done when condition" }
  if ($t.maxMinutes -gt 120) { throw "$($file): maxMinutes must be bounded" }
}

if ($Release) {
  $src = Join-Path $holdDir "$Release.json"
  if (-not (Test-Path $src)) { throw "not held: $Release" }
  $dst = Join-Path $inbox "$Release.json"
  if (Test-Path $dst) { throw "already in inbox: $Release" }
  Move-Item $src $dst; "released $Release"; return
}

foreach ($f in Get-ChildItem (Join-Path $here 'inbox') -Filter *.json) {
  Test-Envelope $f.FullName
  $dst = Join-Path $inbox $f.Name
  if (Test-Path $dst) { "skip (exists): $($f.Name)"; continue }
  Copy-Item $f.FullName $dst; "queued: $($f.Name)"
}
New-Item -ItemType Directory -Force $holdDir | Out-Null
foreach ($f in Get-ChildItem (Join-Path $here $holdName) -File) {
  if ($f.Extension -eq '.json') { Test-Envelope $f.FullName }
  $dst = Join-Path $holdDir $f.Name
  if (Test-Path $dst) { "skip (exists): $holdName/$($f.Name)"; continue }
  Copy-Item $f.FullName $dst; "held: $holdName/$($f.Name)"
}
'done. Nothing was committed; queue files are runtime state.'