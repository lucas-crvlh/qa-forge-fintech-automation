param(
  [Parameter(Position=0)]
  [string]$Action = "test",

  [Parameter(Position=1)]
  [string]$Target = ""
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $root "venv\Scripts\python.exe"

if (-not (Test-Path $python)) {
  Write-Error "Python do venv não encontrado em: $python. Crie/ative o venv primeiro."
}

function Invoke-Python {
  param([string]$Args)
  & $python $Args
}

switch ($Action) {
  'setup' {
    Invoke-Python -Args "-m pip install -r requirements.txt"
    Invoke-Python -Args "-m playwright install chromium"
  }
  'install-browsers' {
    Invoke-Python -Args "-m playwright install chromium"
  }
  'test' {
    $testTarget = if ($Target -ne "") { $Target } else { "tests" }
    Invoke-Python -Args "-m pytest -s -q `"$testTarget`""
  }
  Default {
    Write-Host "Uso:" -ForegroundColor Yellow
    Write-Host "  .\task.ps1 setup                      # instala deps e browsers"
    Write-Host "  .\task.ps1 install-browsers           # instala browsers do Playwright"
    Write-Host "  .\task.ps1 test                        # roda toda a suíte"
    Write-Host "  .\task.ps1 test tests\\ui\\test_navegacao_simples.py  # roda teste específico"
    exit 1
  }
}


