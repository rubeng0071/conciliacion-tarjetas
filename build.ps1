# Requiere ejecutar como administrador
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "Ejecutar como administrador!"
    Break
}

# Crear entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Compilar el proyecto
pyinstaller --noconfirm --onefile --windowed `
    --add-data "src;src" `
    --add-data "config;config" `
    --icon "config/icon.ico" `
    --name "FiservConciliacion" `
    main.py

# Crear directorios necesarios en la carpeta dist
New-Item -ItemType Directory -Force -Path "dist\files\input"
New-Item -ItemType Directory -Force -Path "dist\files\excel"
New-Item -ItemType Directory -Force -Path "dist\files\terminado"
New-Item -ItemType Directory -Force -Path "dist\config"

# Copiar archivo .env de ejemplo si existe
if (Test-Path "config\.env.example") {
    Copy-Item "config\.env.example" -Destination "dist\config\.env"
}

Write-Host "Compilación completada. El ejecutable se encuentra en la carpeta 'dist'" 