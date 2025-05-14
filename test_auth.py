import os
from dotenv import load_dotenv
import smtplib
import ssl
import base64
import logging

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_auth():
    # Cargar variables de entorno
    env_file = os.path.join(os.path.dirname(__file__), 'config', '.env')
    if not os.path.exists(env_file):
        print(f"Error: No se encuentra el archivo .env en {env_file}")
        return

    load_dotenv(env_file)
    
    # Obtener configuración
    server = os.getenv('SMTP_SERVER')
    port = int(os.getenv('SMTP_PORT', '465'))
    user = os.getenv('SMTP_USER')
    password = os.getenv('SMTP_PASSWORD')
    
    print("\nProbando autenticación SMTP con los siguientes datos:")
    print(f"Servidor: {server}")
    print(f"Puerto: {port}")
    print(f"Usuario: {user}")
    print(f"Contraseña: {'*' * len(password)}")
    
    try:
        # Conectar al servidor
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(server, port, context=context) as server_conn:
            server_conn.set_debuglevel(1)
            server_conn.ehlo()
            
            print("\nIntentando AUTH LOGIN...")
            # Intentar AUTH LOGIN paso a paso
            server_conn.docmd("AUTH LOGIN")
            user_b64 = base64.b64encode(user.encode()).decode()
            print(f"Usuario codificado: {user_b64}")
            server_conn.docmd(user_b64)
            
            pass_b64 = base64.b64encode(password.encode()).decode()
            print(f"Contraseña codificada: {pass_b64}")
            server_conn.docmd(pass_b64)
            
            print("\n✅ Autenticación exitosa!")
            return True
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nPosibles problemas:")
        print("1. Verifica que la contraseña en .env no tenga espacios al inicio o final")
        print("2. Si la contraseña tiene caracteres especiales, asegúrate de que estén correctamente escritos")
        print("3. Prueba a escribir la contraseña entre comillas simples en el .env:")
        print(f"   SMTP_PASSWORD='{password}'")
        return False

if __name__ == "__main__":
    test_auth() 