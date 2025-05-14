import smtplib
import os
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from datetime import datetime
import ssl
import base64

# Configurar logging básico
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuración del servidor de correo
SMTP_SERVER = os.getenv('SMTP_SERVER', 'mail.rapanui.com.ar')
SMTP_PORT = int(os.getenv('SMTP_PORT', '465'))
SMTP_USER = os.getenv('SMTP_USER', 'conciliaciones@rapanui.com.ar')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
SENDER_NAME = "Departamento de Sistemas"

def get_destinatarios():
    destinatarios_str = os.getenv('MAIL_RECIPIENTS', '')
    return [email.strip() for email in destinatarios_str.split(',') if email.strip()]

def try_auth_login(server, user, password):
    """Método de autenticación que sabemos que funciona"""
    server.docmd("AUTH LOGIN")
    server.docmd(base64.b64encode(user.encode()).decode())
    server.docmd(base64.b64encode(password.encode()).decode())

def send_files(filepaths, date_str):
    destinatarios = get_destinatarios()
    if not destinatarios:
        print("[ERROR] No hay destinatarios configurados")
        return False

    for filepath in filepaths:
        try:
            # Crear mensaje
            msg = MIMEMultipart()
            msg['From'] = f'{SENDER_NAME} <{SMTP_USER}>'
            msg['To'] = ', '.join(destinatarios)
            msg['Subject'] = f'Conciliación Tarjetas - {date_str}'
            
            # Contenido HTML
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #003366;">Sistema de Conciliaciones Tarjeta</h2>
                <p>Estimados,</p>
                <p>El proceso de conciliación ha finalizado correctamente.</p>
                <p>Fecha de procesamiento: <b>{date_str}</b></p>
                <p>Se adjunta el archivo de conciliación.</p>
                <br>
                <p>Atentamente,<br>{SENDER_NAME}</p>
            </body>
            </html>
            """
            msg.attach(MIMEText(html_content, 'html'))

            # Adjuntar archivo
            with open(filepath, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                filename = os.path.basename(filepath)
                part.add_header('Content-Disposition', 'attachment', filename=filename)
                msg.attach(part)

            # Enviar correo
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
                server.ehlo()
                try_auth_login(server, SMTP_USER, SMTP_PASSWORD)
                
                for dest in destinatarios:
                    try:
                        server.sendmail(SMTP_USER, [dest], msg.as_string())
                        print(f"Correo enviado a: {dest}")
                    except Exception as e:
                        print(f"Error enviando a {dest}: {str(e)}")

            print(f"Proceso completado para: {os.path.basename(filepath)}")
            return True

        except Exception as e:
            print(f"Error en el proceso: {str(e)}")
            return False
