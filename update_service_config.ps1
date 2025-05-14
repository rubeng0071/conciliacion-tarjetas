param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('diario', 'semanal', 'mensual')]
    [string]$Frecuencia,
    
    [int]$Year,
    [int]$Month,
    [switch]$SemanaAnterior
)

# Requiere ejecutar como administrador
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "Ejecutar como administrador!"
    Break
}

$serviceName = "FiservConciliacion"
$installPath = "C:\Program Files\FiservConciliacion"
$exePath = "$installPath\FiservConciliacion.exe"

# Detener el servicio
Stop-Service $serviceName

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

# Actualizar el servicio
$service = Get-WmiObject -Class Win32_Service -Filter "Name='$serviceName'"
$service.Change($null, $null, $null, $null, $null, $null, $null, $null, $null, $null, $command)

# Iniciar el servicio
Start-Service $serviceName

Write-Host "Configuración del servicio actualizada y reiniciado"
Write-Host "Nueva configuración: $command" 