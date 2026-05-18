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
  python -X utf8 scripts/validate_repo.py .

  if ($SkillCreatorDir -ne "") {
    $quickValidate = Join-Path $SkillCreatorDir "scripts\quick_validate.py"
    $packageSkill = Join-Path $SkillCreatorDir "scripts\package_skill.py"

    if (Test-Path -LiteralPath $quickValidate) {
      python -X utf8 $quickValidate .
    }

    if (Test-Path -LiteralPath $packageSkill) {
      python -X utf8 $packageSkill . $OutDir
    }
  } else {
    Write-Host "SkillCreatorDir not provided; skipped CodeBuddy quick_validate.py and package_skill.py."
    Write-Host "Example: scripts\package_skill.ps1 -SkillCreatorDir 'C:\path\to\skill-creator'"
  }
} finally {
  Pop-Location
}
