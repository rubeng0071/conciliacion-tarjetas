import os
from dotenv import load_dotenv
from src.mailer import test_smtp_connection
import logging

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    # Cargar variables de entorno
    env_file = os.path.join(os.path.dirname(__file__), 'config', '.env')
    if not os.path.exists(env_file):
        print(f"Error: No se encuentra el archivo .env en {env_file}")
        return

    load_dotenv(env_file)
    
    # Mostrar configuración actual
    print("\nConfiguración SMTP actual:")
    print(f"Servidor: {os.getenv('SMTP_SERVER')}")
    print(f"Puerto: {os.getenv('SMTP_PORT')}")
    print(f"Usuario: {os.getenv('SMTP_USER')}")
    print(f"Contraseña: {'*' * len(os.getenv('SMTP_PASSWORD', ''))}")
    print(f"Destinatarios: {os.getenv('MAIL_RECIPIENTS')}\n")
    
    # Probar conexión
    print("Probando conexión SMTP...")
    success, message = test_smtp_connection()
    
    if success:
        print("\n✅ Conexión SMTP exitosa!")
    else:
        print(f"\n❌ Error en la conexión SMTP: {message}")
        print("\nPosibles soluciones:")
        print("1. Verificar que la contraseña sea correcta")
        print("2. Confirmar que el servidor SMTP esté configurado para SSL/TLS")
        print("3. Verificar que la cuenta tenga permisos para envío SMTP")
        print("4. Comprobar si hay restricciones de seguridad o firewall")
        print("5. Intentar con el puerto 587 (TLS) en lugar de 465 (SSL)")

if __name__ == "__main__":
    main() 