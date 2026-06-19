param(
  [string]$SkillPath = ".",
  [string]$OutDir = "dist",
  [string]$SkillCreatorDir = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Resolve-Path -LiteralPath $SkillPath
Push-Location $root
try {
  # Step 1: Validate repository
  python -X utf8 scripts/validate_repo.py .

  # Step 2: Sync platform packages from _shared/
  python -X utf8 scripts/sync-platforms.py --format folders
  python -X utf8 scripts/sync-platforms.py --format plugins

  # Step 3: Optional CodeBuddy skill-creator validation
  if ($SkillCreatorDir -ne "") {
    $quickValidate = Join-Path $SkillCreatorDir "scripts\quick_validate.py"
    $packageSkill = Join-Path $SkillCreatorDir "scripts\package_skill.py"
    $sharedSkillDir = Join-Path $root "_shared\skills\llm-wiki"

    if (Test-Path -LiteralPath $quickValidate) {
      python -X utf8 $quickValidate $sharedSkillDir
    }

    if (Test-Path -LiteralPath $packageSkill) {
      python -X utf8 $packageSkill $sharedSkillDir $OutDir
    }
  } else {
    Write-Host "SkillCreatorDir not provided; skipped CodeBuddy quick_validate.py and package_skill.py."
    Write-Host "Example: scripts\package_skill.ps1 -SkillCreatorDir 'C:\path\to\skill-creator'"
  }
} finally {
  Pop-Location
}
