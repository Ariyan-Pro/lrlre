# LRLRE ENTERPRISE GRID - POWERSHELL LAUNCHER
Clear-Host
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "    🚀 LRLRE ENTERPRISE GRID - ONE CLICK LAUNCHER" -ForegroundColor Yellow
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""
Write-Host "This will launch ALL THREE versions:" -ForegroundColor White
Write-Host "  📊 v7.0 Analysis Grid  (port 8007)" -ForegroundColor Green
Write-Host "  🎯 v8.2 Visual Grid    (port 8009)" -ForegroundColor Green
Write-Host "  💎 v10.0 Ultimate Grid (port 8013)" -ForegroundColor Green
Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Kill existing processes
Write-Host "🔍 Checking for existing processes..." -ForegroundColor Yellow
$ports = @(8007, 8009, 8013)
foreach ($port in $ports) {
    $connections = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    foreach ($conn in $connections) {
        Stop-Process -Id $conn.OwningProcess -Force -ErrorAction SilentlyContinue
    }
}
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "🚀 Launching services..." -ForegroundColor Yellow
Write-Host ""

# Launch v7.0
$arg1 = "-NoExit", "-Command", "cd '$pwd'; Write-Host '='*60 -ForegroundColor Green; Write-Host '📊 v7.0 ANALYSIS GRID' -ForegroundColor Cyan; Write-Host '='*60 -ForegroundColor Green; Write-Host 'Port: 8007' -ForegroundColor Yellow; Write-Host ''; python start_analytics_v7.py"
Start-Process powershell -ArgumentList $arg1
Write-Host "  ✅ v7.0 Analysis Grid started on port 8007" -ForegroundColor Green
Start-Sleep -Seconds 2

# Launch v8.2
$arg2 = "-NoExit", "-Command", "cd '$pwd'; Write-Host '='*60 -ForegroundColor Green; Write-Host '🎯 v8.2 VISUAL GRID' -ForegroundColor Cyan; Write-Host '='*60 -ForegroundColor Green; Write-Host 'Port: 8009' -ForegroundColor Yellow; Write-Host ''; python start_analytics_v8_bento_grid.py"
Start-Process powershell -ArgumentList $arg2
Write-Host "  ✅ v8.2 Visual Grid started on port 8009" -ForegroundColor Green
Start-Sleep -Seconds 2

# Launch v10.0
$arg3 = "-NoExit", "-Command", "cd '$pwd'; Write-Host '='*60 -ForegroundColor Green; Write-Host '💎 v10.0 ULTIMATE GRID' -ForegroundColor Cyan; Write-Host '='*60 -ForegroundColor Green; Write-Host 'Port: 8013' -ForegroundColor Yellow; Write-Host ''; python ultimate_v10_fixed.py"
Start-Process powershell -ArgumentList $arg3
Write-Host "  ✅ v10.0 Ultimate Grid started on port 8013" -ForegroundColor Green

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "✅ ALL SERVICES LAUNCHED SUCCESSFULLY!" -ForegroundColor Yellow
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Monitor with: python bin\monitor.py" -ForegroundColor White
Write-Host ""
Write-Host "📌 ACCESS AT:" -ForegroundColor Cyan
Write-Host "   📍 Analysis:  http://localhost:8007" -ForegroundColor White
Write-Host "   📍 Visual:    http://localhost:8009" -ForegroundColor White
Write-Host "   📍 Ultimate:  http://localhost:8013" -ForegroundColor White
Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
