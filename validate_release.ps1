Write-Host "=== Git Status ==="
git status

Write-Host ""
Write-Host "=== Latest Render ==="

$file = Get-ChildItem output\final_*.mp4 |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $file) {
    Write-Error "No generated video found"
    exit 1
}

Write-Host "Testing:"
Write-Host $file.FullName

ffprobe $file.FullName

Write-Host ""
Write-Host "=== Python Compile Check ==="

python -m py_compile app.py

if ($LASTEXITCODE -ne 0) {
    Write-Error "Python syntax check failed"
    exit 1
}

Write-Host ""
Write-Host "=== Validation Complete ==="
