import json
import hashlib
from datetime import datetime, timedelta
import argparse
from cryptography.fernet import Fernet
import base64
import os

def generate_encryption_key():
    """Genera una clave de encriptación única basada en el hardware"""
    # Obtener información única del sistema
    system_info = os.getenv('COMPUTERNAME', '') + os.getenv('USERNAME', '')
    # Generar una clave basada en esta información
    key = hashlib.sha256(system_info.encode()).digest()
    return base64.urlsafe_b64encode(key)

def generate_license(license_key, expiration_date):
    # Generar hash de la licencia
    license_hash = hashlib.sha256(license_key.encode()).hexdigest()
    
    # Crear objeto de licencia
    license_data = {
        'license_key': license_key,
        'expiration_date': expiration_date.strftime('%Y-%m-%d'),
        'hash': license_hash,
        'system_id': os.getenv('COMPUTERNAME', ''),
        'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Encriptar los datos
    f = Fernet(generate_encryption_key())
    encrypted_data = f.encrypt(json.dumps(license_data).encode())
    
    return encrypted_data

def main():
    parser = argparse.ArgumentParser(description='Generar archivo de licencia')
    parser.add_argument('--key', required=True, help='Clave de licencia')
    parser.add_argument('--days', type=int, default=365, help='Días de validez de la licencia')
    parser.add_argument('--output', default='config/fiserv_conciliacion.lic', help='Archivo de salida')
    args = parser.parse_args()
    
    # Calcular fecha de vencimiento
    expiration_date = datetime.now() + timedelta(days=args.days)
    
    # Generar licencia encriptada
    encrypted_license = generate_license(args.key, expiration_date)
    
    # Asegurar que el directorio config existe
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Guardar licencia encriptada
    with open(args.output, 'wb') as f:
        f.write(encrypted_license)
    
    print(f"Licencia generada exitosamente en: {args.output}")
    print(f"Fecha de vencimiento: {expiration_date.strftime('%Y-%m-%d')}")
    print("IMPORTANTE: Esta licencia solo funcionará en este equipo específico.")

if __name__ == "__main__":
    main() 