# LRLRE Enterprise Grid - PowerShell Launcher
Write-Host "🚀 LRLRE ENTERPRISE GRID - LAUNCHER" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

# Kill existing processes
Write-Host "Stopping any existing services..." -ForegroundColor Yellow
$ports = @(8007, 8009, 8013)
foreach ($port in $ports) {
    $connections = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    foreach ($conn in $connections) {
        Stop-Process -Id $conn.OwningProcess -Force -ErrorAction SilentlyContinue
    }
}
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "Starting all services..." -ForegroundColor Yellow
Write-Host ""

# Launch each version
$scripts = @(
    @{Name="v7.0 Analysis Grid"; Port=8007; File="start_analytics_v7.py"},
    @{Name="v8.2 Visual Grid"; Port=8009; File="start_analytics_v8_bento_grid.py"},
    @{Name="v10.0 Ultimate Grid"; Port=8013; File="ultimate_v10_fixed.py"}
)

foreach ($script in $scripts) {
    Write-Host "  Starting $($script.Name) on port $($script.Port)..." -ForegroundColor Yellow
    $argumentList = "-NoExit", "-Command", "cd '$pwd'; Write-Host '='*60 -ForegroundColor Green; Write-Host '$($script.Name)' -ForegroundColor Cyan; Write-Host '='*60 -ForegroundColor Green; Write-Host 'Port: $($script.Port)' -ForegroundColor Yellow; Write-Host ''; python $($script.File)"
    Start-Process powershell -ArgumentList $argumentList
    Start-Sleep -Seconds 2
}

Write-Host ""
Write-Host "✅ All services launched!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Monitor with: python bin\monitor.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "📌 Quick Access:" -ForegroundColor White
Write-Host "   • Analysis:  http://localhost:8007"
Write-Host "   • Visual:    http://localhost:8009"
Write-Host "   • Ultimate:  http://localhost:8013"
