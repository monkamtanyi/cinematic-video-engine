Write-Host "================================="
Write-Host " Cinematic Engine Release Check"
Write-Host "================================="

Write-Host ""
Write-Host "=== Current Branch ==="
$branch = git branch --show-current
Write-Host $branch

if ($branch -ne "feature/audio-normalization") {
    Write-Error "Wrong branch. Expected feature/audio-normalization"
    exit 1
}

Write-Host ""
Write-Host "=== Git Status ==="
$status = git status --porcelain

if ($status) {
    Write-Error "Working tree is not clean:"
    git status
    exit 1
}

Write-Host "Working tree clean"

Write-Host ""
Write-Host "=== Latest Commit ==="
git log -1 --oneline

Write-Host ""
Write-Host "=== Running Release Validation ==="

if (Test-Path ".\validate_release.ps1") {
    .\validate_release.ps1
}
else {
    Write-Error "validate_release.ps1 not found"
    exit 1
}

Write-Host ""
Write-Host "=== Pushing Branch ==="

git push origin feature/audio-normalization

if ($LASTEXITCODE -ne 0) {
    Write-Error "Git push failed"
    exit 1
}

Write-Host ""
Write-Host "================================="
Write-Host " Release Ready For Pull Request"
Write-Host "================================="

Write-Host ""
Write-Host "PR URL:"
Write-Host "https://github.com/monkamtanyi/cinematic-video-engine/pull/new/feature/audio-normalization"

