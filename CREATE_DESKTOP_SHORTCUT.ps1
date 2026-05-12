$WScriptShell = New-Object -ComObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$Shortcut = $WScriptShell.CreateShortcut("$DesktopPath\LRLRE Enterprise Grid.lnk")
$Shortcut.TargetPath = "C:\Users\dell\Projects\LRLRE-Enterprise\LAUNCH_LRLRE.bat"
$Shortcut.WorkingDirectory = "C:\Users\dell\Projects\LRLRE-Enterprise"
$Shortcut.Description = "Launch LRLRE Enterprise Grid (3 versions)"
$Shortcut.Save()
Write-Host "✅ Desktop shortcut created!" -ForegroundColor Green
