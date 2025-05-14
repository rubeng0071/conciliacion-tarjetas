param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('diario', 'semanal', 'mensual')]
    [string]$Frecuencia,
    
    [int]$Year,
    [int]$Month,
    [switch]$SemanaAnterior
)

$exePath = "C:\Program Files\FiservConciliacion\FiservConciliacion.exe"

# Construir el comando base
$command = "$exePath --frecuencia $Frecuencia"

# Agregar parámetros según la frecuencia
switch ($Frecuencia) {
    'mensual' {
        if ($Year -and $Month) {
            $command += " --year $Year --month $Month"
        }
    }
    'semanal' {
        if ($SemanaAnterior) {
            $command += " --semana-anterior"
        }
    }
}

# Ejecutar el comando
Write-Host "Ejecutando: $command"
Invoke-Expression $command 