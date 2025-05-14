# Conciliación Tarjetas Fiserv

Sistema automatizado para procesar archivos de liquidación de tarjetas Fiserv.

## Requisitos

- Windows Server 2019 o superior
- Python 3.11 o superior
- PowerShell 5.1 o superior

## Instalación

### Desarrollo

1. Clonar el repositorio:
```bash
git clone <url-del-repo>
cd Concilacion_Tarjetas
```

2. Crear entorno virtual e instalar dependencias:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```powershell
# Copiar el archivo de ejemplo
Copy-Item config\.env.example config\.env

# Editar el archivo .env con tus configuraciones
notepad config\.env
```

### Instalación del Servicio

1. Ejecutar como administrador:
```powershell
# Instalar el servicio
.\install_service.ps1
```

El script de instalación:
- Solicitará el directorio de instalación
- Configurará el servidor SMTP
- Configurará los destinatarios de correo
- Configurará la frecuencia de ejecución
- Creará la estructura de directorios
- Instalará el servicio de Windows

## Configuración

### Variables de Entorno (.env)
```ini
# Ruta de instalación
INSTALL_PATH=C:\Program Files\FiservConciliacion

# Configuración del servidor de correo
SMTP_SERVER=mail.rapanui.com.ar
SMTP_PORT=465
SMTP_USER=conciliaciones@rapanui.com.ar
SMTP_PASSWORD=tu_contraseña

# Configuración de correos
MAIL_RECIPIENTS=correo1@ejemplo.com,correo2@ejemplo.com
SENDER_NAME=Departamento de Sistemas

# Configuración de ejecución
FRECUENCIA_ENVIO=semanal    # Opciones: diario, semanal, mensual

# Horarios de ejecución
HORA_EJECUCION_DIARIA=23:00
HORA_EJECUCION_SEMANAL=07:00
HORA_EJECUCION_MENSUAL=06:00
```

### Frecuencias de Ejecución

1. **Diario**:
   - Ejecuta todos los días a las 23:00
   - Procesa archivos del día actual

2. **Semanal**:
   - Ejecuta los lunes a las 07:00
   - Procesa archivos de la semana anterior

3. **Mensual**:
   - Ejecuta el primer día de cada mes a las 06:00
   - Procesa archivos del mes anterior

## Uso

### Ejecución Manual

```powershell
# Procesar semana actual
python main.py --frecuencia semanal

# Procesar semana anterior
python main.py --frecuencia semanal --semana-anterior

# Procesar mes específico
python main.py --frecuencia mensual --year 2024 --month 3

# Procesar diariamente
python main.py --frecuencia diario
```

### Gestión del Servicio

```powershell
# Iniciar servicio
Start-Service FiservConciliacion

# Detener servicio
Stop-Service FiservConciliacion

# Ver estado
Get-Service FiservConciliacion

# Ver logs
Get-EventLog -LogName Application -Source FiservConciliacion
```

### Estructura de Directorios
```
FiservConciliacion/
├── files/
│   ├── input/      # Archivos TXT a procesar
│   ├── terminado/  # Archivos procesados
│   └── excel/      # Archivos Excel generados
├── config/
│   ├── .env        # Configuración
│   └── fiserv_conciliacion.lic  # Licencia
└── service.log     # Log del servicio
```

## Mantenimiento

### Actualización del Servicio
1. Detener el servicio:
```powershell
Stop-Service FiservConciliacion
```

2. Reinstalar:
```powershell
.\install_service.ps1
```

### Desinstalación
```powershell
# Ejecutar como administrador
.\uninstall_service.ps1
```

## Solución de Problemas

### Problemas Comunes

1. **Servicio no inicia**:
   - Verificar permisos en el directorio de instalación
   - Revisar logs en `service.log`
   - Verificar que la licencia sea válida

2. **Archivos no se procesan**:
   - Verificar que los archivos estén en `files/input/`
   - Verificar el formato de los nombres de archivo
   - Revisar los logs del servicio

3. **Correos no se envían**:
   - Verificar configuración SMTP en `.env`
   - Verificar conexión al servidor SMTP
   - Revisar logs del servicio

### Logs
Los logs se pueden encontrar en:
- `C:\Program Files\FiservConciliacion\service.log`
- Event Viewer > Windows Logs > Application
  - Filtro: Source = "FiservConciliacion"

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

- **main.py**: Punto de entrada principal. Busca archivos TXT en `files/input/` que contengan `CL586D`, extrae la fecha del nombre, procesa los archivos, genera un Excel, envía un mail con el Excel adjunto y mueve los archivos procesados a `files/terminado/`.
- **src/fiserv_parser.py**: Módulo encargado de parsear los archivos TXT. Extrae y convierte los campos según las especificaciones, aplicando conversiones de decimales, signos y traducciones de códigos.
- **src/excel_generator.py**: Genera un archivo Excel a partir de los registros parseados, creando una hoja por tipo de registro y ajustando automáticamente los anchos de columna.
- **src/mailer.py**: Envía correos electrónicos con el Excel adjunto, utilizando las credenciales y destinatarios configurados en el archivo `.env`.
- **config.py**: Clase de configuración que centraliza rutas y variables de entorno. Actualmente, el flujo principal (`main.py`) define las rutas directamente, pero se recomienda unificar su uso para mayor mantenibilidad.
- **requirements.txt**: Lista de dependencias necesarias para el proyecto.
- **.gitignore**: Configurado para ignorar archivos sensibles (como `config/.env`) y archivos temporales.

## Flujo de Procesamiento

1. **Búsqueda de Archivos**: El script busca en `files/input/` archivos cuyo nombre contenga `CL586D` y terminen en `.TXT`.
2. **Extracción de Fecha**: Extrae la fecha del nombre del archivo (formato: `TRONA001.20250403051234777.CL586D.I0403253.TXT`, donde la fecha es `20250403`).
3. **Procesamiento**: Para cada archivo encontrado, se parsea su contenido utilizando `fiserv_parser.py`, que extrae y convierte los campos según las especificaciones.
4. **Generación de Excel**: Se genera un archivo Excel con los registros procesados, utilizando `excel_generator.py`.
5. **Envío de Mail**: Se envía un correo electrónico con el Excel adjunto, utilizando `mailer.py`. El asunto del correo incluye la fecha extraída.
6. **Movimiento de Archivos**: Los archivos procesados se mueven a la carpeta `files/terminado/` para evitar reprocesos.
