Write-Host "========================================="
Write-Host " Cinematic Engine v1.9.2 Audio Duration Fix"
Write-Host "========================================="

$branch = git branch --show-current

Write-Host ""
Write-Host "Branch:"
Write-Host $branch

if ($branch -ne "feature/audio-duration-fix") {
    Write-Error "Run this only on feature/audio-duration-fix"
    exit 1
}


$file = "engine/core/video_renderer.py"

$text = Get-Content $file -Raw


Write-Host ""
Write-Host "Patching audio loop..."


$text = $text.Replace(
    'cmd += ["-i", music_path]',
    @"
cmd += [
    "-stream_loop",
    "-1",
    "-i",
    music_path
]
"@
)


Write-Host ""
Write-Host "Removing shortest flag..."

$text = $text.Replace(
    '"-shortest"',
    ''
)


Set-Content $file $text


Write-Host ""
Write-Host "Python validation..."

python -m py_compile `
app.py `
engine/core/video_renderer.py


if ($LASTEXITCODE -ne 0) {

    Write-Error "Python compile failed"
    exit 1

}


Write-Host ""
Write-Host "Staging..."

git add engine/core/video_renderer.py


Write-Host ""
Write-Host "Staged files:"
git diff --cached --name-only


Write-Host ""
Write-Host "Review:"
Write-Host "git diff --cached"

