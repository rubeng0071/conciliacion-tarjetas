# Verificar que estamos en el directorio correcto
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "1. Verificando estructura de directorios..." -ForegroundColor Green
$directories = @(
    ".\files\input",
    ".\files\terminado",
    ".\files\excel",
    ".\config"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force
        Write-Host "Creado directorio: $dir"
    }
}

Write-Host "`n2. Verificando archivo .env..." -ForegroundColor Green
if (-not (Test-Path ".\config\.env")) {
    Write-Host "ATENCIÓN: No se encuentra el archivo .env en config/" -ForegroundColor Yellow
    Write-Host "Por favor, crea el archivo config/.env con las siguientes variables:"
    @"
# Configuración del servidor de correo (Configuración verificada y funcional)
SMTP_SERVER=mail.rapanui.com.ar
SMTP_PORT=465
SMTP_USER=conciliaciones@rapanui.com.ar
SMTP_PASSWORD=rPn7412@@

# Destinatarios de las conciliaciones
MAIL_RECIPIENTS=finanzas@rapanui.com.ar,rubeng0071@gmail.com

# Configuración del procesamiento
FRECUENCIA_ENVIO=semanal
DIA_INICIO_SEMANA=0
SEMANA_ANTERIOR=true
"@ | Out-Host
    exit 1
}

Write-Host "`n3. Generando licencia de prueba..." -ForegroundColor Green
python generate_license.py --key "LICENCIA_PRUEBA" --days 30
if (-not (Test-Path ".\config\fiserv_conciliacion.lic")) {
    Write-Host "Error: No se pudo generar la licencia" -ForegroundColor Red
    exit 1
}

Write-Host "`n4. Probando diferentes modos de ejecución..." -ForegroundColor Green

Write-Host "`nProbando procesamiento diario:" -ForegroundColor Cyan
python main.py --frecuencia diario
Write-Host "Presiona cualquier tecla para continuar..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host "`nProbando procesamiento semanal:" -ForegroundColor Cyan
python main.py --frecuencia semanal
Write-Host "Presiona cualquier tecla para continuar..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host "`nProbando procesamiento mensual:" -ForegroundColor Cyan
python main.py --frecuencia mensual
Write-Host "Presiona cualquier tecla para continuar..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host "`n5. Compilando el proyecto..." -ForegroundColor Green
if (Test-Path ".\build.ps1") {
    .\build.ps1
} else {
    Write-Host "ATENCIÓN: No se encuentra build.ps1" -ForegroundColor Yellow
}

Write-Host "`n6. Instalando el servicio..." -ForegroundColor Green
if (Test-Path ".\install_service.ps1") {
    .\install_service.ps1
} else {
    Write-Host "ATENCIÓN: No se encuentra install_service.ps1" -ForegroundColor Yellow
}

Write-Host "`n7. Verificando el servicio..." -ForegroundColor Green
$service = Get-Service -Name "FiservConciliacion" -ErrorAction SilentlyContinue
if ($service) {
    Write-Host "Estado del servicio: $($service.Status)"
    Write-Host "Para iniciar el servicio: Start-Service FiservConciliacion"
    Write-Host "Para detener el servicio: Stop-Service FiservConciliacion"
} else {
    Write-Host "ATENCIÓN: El servicio no está instalado" -ForegroundColor Yellow
}

Write-Host "`nPruebas completadas!" -ForegroundColor Green
Write-Host "Revisa los mensajes anteriores para verificar que todo esté correcto." 