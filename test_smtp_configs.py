import os
from dotenv import load_dotenv
import smtplib
import ssl
import logging
import base64
from time import sleep

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_config(server, port, user, password, use_ssl=True):
    print(f"\nProbando configuración:")
    print(f"Servidor: {server}")
    print(f"Puerto: {port}")
    print(f"Usuario: {user}")
    print(f"SSL/TLS: {'Sí' if use_ssl else 'No'}")
    
    try:
        if use_ssl:
            context = ssl.create_default_context()
            server_conn = smtplib.SMTP_SSL(server, port, context=context)
        else:
            server_conn = smtplib.SMTP(server, port)
            server_conn.starttls()
        
        server_conn.set_debuglevel(1)
        server_conn.ehlo()
        
        # Intentar diferentes métodos de autenticación
        methods = [
            ("LOGIN", lambda: server_conn.login(user, password)),
            ("AUTH LOGIN Manual", lambda: try_auth_login(server_conn, user, password)),
            ("AUTH PLAIN", lambda: try_auth_plain(server_conn, user, password))
        ]
        
        for method_name, auth_method in methods:
            try:
                print(f"\nIntentando método: {method_name}")
                auth_method()
                print(f"✅ Éxito con {method_name}")
                server_conn.quit()
                return True
            except Exception as e:
                print(f"❌ Falló {method_name}: {str(e)}")
                continue
        
        return False
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return False

def try_auth_login(server, user, password):
    server.docmd("AUTH LOGIN")
    server.docmd(base64.b64encode(user.encode()).decode())
    server.docmd(base64.b64encode(password.encode()).decode())

def try_auth_plain(server, user, password):
    auth_string = f"\x00{user}\x00{password}"
    auth_base64 = base64.b64encode(auth_string.encode()).decode()
    server.docmd("AUTH PLAIN", auth_base64)

def main():
    # Cargar variables de entorno
    env_file = os.path.join(os.path.dirname(__file__), 'config', '.env')
    if not os.path.exists(env_file):
        print(f"Error: No se encuentra el archivo .env en {env_file}")
        return

    load_dotenv(env_file)
    
    server = os.getenv('SMTP_SERVER')
    user = os.getenv('SMTP_USER')
    password = os.getenv('SMTP_PASSWORD')
    
    # Probar diferentes configuraciones
    configs = [
        (server, 465, user, password, True),  # SSL
        (server, 587, user, password, True),  # TLS
        ('smtp.office365.com', 587, user, password, True),  # Office 365
        ('smtp.gmail.com', 587, user, password, True),  # Gmail
    ]
    
    for config in configs:
        print("\n" + "="*50)
        test_config(*config)
        print("="*50)
        sleep(2)  # Esperar entre intentos

if __name__ == "__main__":
    main() 