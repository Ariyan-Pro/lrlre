# LRLRE Enterprise Grid - PowerShell Launcher
Write-Host "🚀 LRLRE ENTERPRISE GRID - LAUNCH ALL SERVICES" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Cyan

# Function to start a service in new window
function Start-Service {
    param($Name, $Port, $Script)
    
    Write-Host "Starting $Name on port $Port..." -ForegroundColor Yellow
    $powershellPath = "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
    $argumentList = "-NoExit", "-Command", "cd '$pwd'; python $Script"
    
    Start-Process -FilePath $powershellPath -ArgumentList $argumentList
    Start-Sleep -Seconds 2
}

# Start all three services
Start-Service -Name "v7.0 Analysis Grid" -Port 8007 -Script "start_analytics_v7.py"
Start-Service -Name "v8.2 Visual Grid" -Port 8009 -Script "start_analytics_v8_bento_grid.py"
Start-Service -Name "v10.0 Ultimate Grid" -Port 8013 -Script "ultimate_v10_fixed.py"

Write-Host ""
Write-Host "✅ All services launched!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Monitor with: python monitor.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "📌 Quick Access:" -ForegroundColor White
Write-Host "   • Analysis:  http://localhost:8007"
Write-Host "   • Visual:    http://localhost:8009"
Write-Host "   • Ultimate:  http://localhost:8013"
