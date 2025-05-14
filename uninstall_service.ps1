# Requiere ejecutar como administrador
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "Ejecutar como administrador!"
    Break
}

$serviceName = "FiservConciliacion"
$installPath = "C:\Program Files\FiservConciliacion"

# Detener y eliminar el servicio
if (Get-Service $serviceName -ErrorAction SilentlyContinue) {
    Stop-Service $serviceName
    Remove-Service $serviceName
}

# Eliminar archivos de instalación
if (Test-Path $installPath) {
    Remove-Item $installPath -Recurse -Force
}

Write-Host "Servicio desinstalado exitosamente" 