# Requiere ejecutar como administrador
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "Ejecutar como administrador!"
    Break
}

# Configuración del servicio
$serviceName = "FiservConciliacion"
$displayName = "Servicio de Conciliación de Tarjetas"
$description = "Servicio para procesamiento automático de conciliaciones de tarjetas"
$defaultInstallPath = "C:\Program Files\FiservConciliacion"

# Solicitar directorio de instalación
$installPath = Read-Host "Directorio de instalación [$defaultInstallPath]"
if ([string]::IsNullOrWhiteSpace($installPath)) {
    $installPath = $defaultInstallPath
}

# Detener el servicio si existe
if (Get-Service $serviceName -ErrorAction SilentlyContinue) {
    Stop-Service $serviceName
    Write-Host "Servicio detenido para actualización"
}

# Crear directorio de instalación si no existe
if (-not (Test-Path $installPath)) {
    New-Item -ItemType Directory -Path $installPath
}

# Copiar archivos desde la carpeta dist
Write-Host "Copiando archivos..."
Copy-Item "dist\*" -Destination $installPath -Recurse -Force

# Copiar archivos de configuración
Copy-Item "config.py", "service_runner.py", "requirements.txt" -Destination $installPath -Force

# Crear directorios necesarios
$directories = @(
    "$installPath\files\input",
    "$installPath\files\terminado",
    "$installPath\files\excel",
    "$installPath\config"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir
        Write-Host "Creado directorio: $dir"
    }
}

# Configurar archivo .env si no existe
$envFile = "$installPath\config\.env"
if (-not (Test-Path $envFile)) {
    Write-Host "`nConfigurando servidor SMTP..."
    $smtpServer = Read-Host "Servidor SMTP [mail.rapanui.com.ar]"
    if ([string]::IsNullOrWhiteSpace($smtpServer)) { $smtpServer = "mail.rapanui.com.ar" }
    
    $smtpPort = Read-Host "Puerto SMTP [465]"
    if ([string]::IsNullOrWhiteSpace($smtpPort)) { $smtpPort = "465" }
    
    $smtpUser = Read-Host "Usuario SMTP [conciliaciones@rapanui.com.ar]"
    if ([string]::IsNullOrWhiteSpace($smtpUser)) { $smtpUser = "conciliaciones@rapanui.com.ar" }
    
    $smtpPassword = Read-Host "Contraseña SMTP" -AsSecureString
    $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($smtpPassword)
    $smtpPasswordText = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
    
    $recipients = Read-Host "Destinatarios (separados por coma)"
    $senderName = Read-Host "Nombre del remitente [Departamento de Sistemas]"
    if ([string]::IsNullOrWhiteSpace($senderName)) { $senderName = "Departamento de Sistemas" }
    
    $frecuencia = Read-Host "Frecuencia de ejecución (diario/semanal/mensual) [semanal]"
    if ([string]::IsNullOrWhiteSpace($frecuencia)) { $frecuencia = "semanal" }
    
    # Crear archivo .env
    @"
INSTALL_PATH=$installPath

# Configuración del servidor de correo
SMTP_SERVER=$smtpServer
SMTP_PORT=$smtpPort
SMTP_USER=$smtpUser
SMTP_PASSWORD=$smtpPasswordText

# Configuración de correos
MAIL_RECIPIENTS=$recipients
SENDER_NAME=$senderName

# Configuración de ejecución
FRECUENCIA_ENVIO=$frecuencia

# Horarios de ejecución
HORA_EJECUCION_DIARIA=23:00
HORA_EJECUCION_SEMANAL=07:00
HORA_EJECUCION_MENSUAL=06:00
"@ | Out-File -FilePath $envFile -Encoding UTF8
    
    Write-Host "Archivo de configuración creado en: $envFile"
}

# Instalar dependencias adicionales
Write-Host "`nInstalando dependencias..."
Set-Location $installPath
& python -m pip install -r requirements.txt

# Crear o actualizar el servicio
$binaryPath = "$installPath\service_runner.py"
if (Get-Service $serviceName -ErrorAction SilentlyContinue) {
    Write-Host "Actualizando servicio existente..."
    sc.exe config $serviceName binPath= "python $binaryPath"
} else {
    Write-Host "Creando nuevo servicio..."
    New-Service -Name $serviceName `
                -DisplayName $displayName `
                -Description $description `
                -BinaryPathName "python $binaryPath" `
                -StartupType Automatic
}

# Configurar recuperación del servicio
sc.exe failure $serviceName reset= 86400 actions= restart/60000/restart/60000/restart/60000

# Establecer permisos
$acl = Get-Acl $installPath
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule("SYSTEM", "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow")
$acl.SetAccessRule($rule)
Set-Acl $installPath $acl

# Iniciar el servicio
Start-Service $serviceName
Write-Host "`nServicio instalado y configurado correctamente"
Write-Host "Directorio de instalación: $installPath"
Write-Host "Archivo de configuración: $envFile"
Write-Host "Log del servicio: $installPath\service.log"

# Mostrar estado
Get-Service $serviceName 