import schedule
import time
import sys
import os
from datetime import datetime
import logging
import subprocess
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('C:\\Program Files\\FiservConciliacion\\service.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_process(frecuencia, semana_anterior=False, year=None, month=None):
    try:
        cmd = [sys.executable, 'main.py', '--frecuencia', frecuencia]
        
        if semana_anterior:
            cmd.append('--semana-anterior')
        if year is not None:
            cmd.extend(['--year', str(year)])
        if month is not None:
            cmd.extend(['--month', str(month)])
            
        logger.info(f"Ejecutando: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("Proceso completado exitosamente")
            logger.info(result.stdout)
        else:
            logger.error(f"Error en el proceso: {result.stderr}")
            
    except Exception as e:
        logger.error(f"Error ejecutando el proceso: {str(e)}")

def job_diario():
    logger.info("Ejecutando proceso diario")
    run_process('diario')

def job_semanal():
    logger.info("Ejecutando proceso semanal")
    run_process('semanal', semana_anterior=True)

def job_mensual():
    logger.info("Ejecutando proceso mensual")
    # Obtener mes anterior
    now = datetime.now()
    if now.month == 1:
        year = now.year - 1
        month = 12
    else:
        year = now.year
        month = now.month - 1
    run_process('mensual', year=year, month=month)

def main():
    try:
        # Cambiar al directorio de instalación
        os.chdir('C:\\Program Files\\FiservConciliacion')
        logger.info("Iniciando servicio de conciliación")
        
        # Cargar configuración
        load_dotenv('config/.env')
        frecuencia = os.getenv('FRECUENCIA_ENVIO', 'semanal')
        
        # Configurar tareas según frecuencia
        if frecuencia == 'diario':
            # Ejecutar todos los días a las 23:00
            schedule.every().day.at("23:00").do(job_diario)
            logger.info("Configurado para ejecución diaria a las 23:00")
            
        elif frecuencia == 'semanal':
            # Ejecutar todos los lunes a las 07:00
            schedule.every().monday.at("07:00").do(job_semanal)
            logger.info("Configurado para ejecución semanal los lunes a las 07:00")
            
        else:  # mensual
            # Ejecutar el primer día de cada mes a las 06:00
            schedule.every().day.at("06:00").do(lambda: 
                job_mensual() if datetime.now().day == 1 else None
            )
            logger.info("Configurado para ejecución mensual el día 1 a las 06:00")

        # Bucle principal del servicio
        while True:
            schedule.run_pending()
            time.sleep(60)  # Esperar 1 minuto entre verificaciones

    except Exception as e:
        logger.error(f"Error en el servicio: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 