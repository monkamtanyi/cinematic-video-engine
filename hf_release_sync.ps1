Write-Host "========================================="
Write-Host " Cinematic Engine v1.9 HF Sync Release"
Write-Host "========================================="

$ErrorActionPreference = "Stop"

$BASE_BRANCH = "main"
$SYNC_BRANCH = "hf-v1.9-production-sync"
$SOURCE_TAG = "v1.8-audio-persistence"
$RELEASE_TAG = "v1.9-hf-production-sync"

$HF_REMOTE = "hf"

Write-Host ""
Write-Host "=== Current Branch ==="

$current = git branch --show-current
Write-Host $current


Write-Host ""
Write-Host "=== Checking Git Status ==="

$status = git status --porcelain

if ($status) {

    Write-Error "Working tree is not clean"
    git status
    exit 1

}

Write-Host "Working tree clean"


Write-Host ""
Write-Host "=== Checking Release Tag ==="

$tagExists = git tag --list $SOURCE_TAG

if (-not $tagExists) {

    Write-Error "$SOURCE_TAG not found"
    exit 1

}

Write-Host "$SOURCE_TAG exists"


Write-Host ""
Write-Host "=== Updating Main ==="

git checkout $BASE_BRANCH
git pull origin $BASE_BRANCH


Write-Host ""
Write-Host "=== Creating HF Sync Branch ==="

$branchExists = git branch --list $SYNC_BRANCH

if (-not $branchExists) {

    git checkout -b $SYNC_BRANCH

}
else {

    git checkout $SYNC_BRANCH
}


Write-Host ""
Write-Host "=== Checking HF Remote ==="

$hf = git remote get-url $HF_REMOTE 2>$null


if (-not $hf) {

    Write-Error "HF remote not configured"

    Write-Host ""
    Write-Host "Add it with:"
    Write-Host "git remote add hf https://huggingface.co/spaces/monkamtanyi/cinematic-engine-v5"

    exit 1

}

Write-Host "HF Remote:"
Write-Host $hf



Write-Host ""
Write-Host "=== Running Python Validation ==="

python -m py_compile app.py

if ($LASTEXITCODE -ne 0) {

    Write-Error "Python validation failed"
    exit 1

}


Write-Host ""
Write-Host "=== Running Release Validation ==="


if (Test-Path ".\validate_release.ps1") {

    .\validate_release.ps1

}
else {

    Write-Warning "validate_release.ps1 missing"

}



Write-Host ""
Write-Host "=== Pushing To Hugging Face ==="


git push $HF_REMOTE $SYNC_BRANCH:main


if ($LASTEXITCODE -ne 0) {

    Write-Error "HF push failed"
    exit 1

}


Write-Host ""
Write-Host "=== Merging HF Sync Branch ==="


git checkout $BASE_BRANCH

git merge $SYNC_BRANCH



Write-Host ""
Write-Host "=== Creating v1.9 Release Tag ==="


git tag -a $RELEASE_TAG `
-m "HF Space production synchronization"



Write-Host ""
Write-Host "=== Pushing GitHub Release ==="


git push origin $BASE_BRANCH

git push origin $RELEASE_TAG



Write-Host ""
Write-Host "========================================="
Write-Host " v1.9 HF Production Sync Complete"
Write-Host "========================================="

Write-Host ""

Write-Host "Verify HF Space:"
Write-Host "https://huggingface.co/spaces/monkamtanyi/cinematic-engine-v5"

Write-Host ""

Write-Host "Manual Tests:"
Write-Host "[ ] Upload images"
Write-Host "[ ] Upload MP3"
Write-Host "[ ] Generate video"
Write-Host "[ ] Confirm audio"
Write-Host "[ ] Refresh browser"
Write-Host "[ ] Test Android playback"
