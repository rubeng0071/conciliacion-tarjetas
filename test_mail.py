import os
from dotenv import load_dotenv
from src.mailer import send_files
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_test_file():
    """Crea un archivo Excel de prueba"""
    import pandas as pd
    
    # Crear un DataFrame simple
    df = pd.DataFrame({
        'Columna1': ['Dato 1', 'Dato 2', 'Dato 3'],
        'Columna2': [100, 200, 300],
        'Fecha': [datetime.now()] * 3
    })
    
    # Guardar como Excel
    test_file = 'files/excel/test_conciliacion.xlsx'
    os.makedirs(os.path.dirname(test_file), exist_ok=True)
    df.to_excel(test_file, index=False)
    
    return test_file

def main():
    # Cargar variables de entorno
    env_file = os.path.join(os.path.dirname(__file__), 'config', '.env')
    if not os.path.exists(env_file):
        print(f"Error: No se encuentra el archivo .env en {env_file}")
        return

    load_dotenv(env_file)
    
    # Crear archivo de prueba
    test_file = create_test_file()
    print(f"\nArchivo de prueba creado: {test_file}")
    
    # Intentar enviar el correo
    print("\nEnviando correo de prueba...")
    success = send_files([test_file], datetime.now().strftime('%d-%m-%Y'))
    
    if success:
        print("\n✅ Correo enviado exitosamente!")
    else:
        print("\n❌ Error al enviar el correo")
        print("Revisa los logs para más detalles")

if __name__ == "__main__":
    main() 