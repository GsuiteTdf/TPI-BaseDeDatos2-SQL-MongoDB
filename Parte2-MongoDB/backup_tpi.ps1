$ErrorActionPreference = "Stop"

Push-Location $PSScriptRoot

try {
    $config = Get-Content ".\parte2\config.json" -Raw | ConvertFrom-Json
    $fecha = Get-Date -Format "yyyy-MM-dd"
    $destino = ".\resguardos_tpi\$fecha"

    New-Item -ItemType Directory -Force -Path $destino | Out-Null

    mongodump `
        --uri="$($config.mongodb_uri)" `
        --db="$($config.database)" `
        --out="$destino"

    if ($LASTEXITCODE -ne 0) {
        throw "mongodump finalizó con código de error $LASTEXITCODE."
    }

    Write-Host "Resguardo completado correctamente."
    Write-Host "Ubicación: $destino"
}
finally {
    Pop-Location
}