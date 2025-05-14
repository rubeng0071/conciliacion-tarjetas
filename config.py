import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        # Cargar variables de entorno
        load_dotenv(os.path.join(self.get_install_dir(), 'config', '.env'))
        
    def get_install_dir(self):
        """Obtener directorio de instalación"""
        return os.getenv('INSTALL_PATH', 'C:\\Program Files\\FiservConciliacion')
        
    @property
    def INSTALL_DIR(self):
        return self.get_install_dir()
        
    @property
    def INPUT_DIR(self):
        return os.path.join(self.INSTALL_DIR, 'files', 'input')
        
    @property
    def TERMINADO_DIR(self):
        return os.path.join(self.INSTALL_DIR, 'files', 'terminado')
        
    @property
    def EXCEL_DIR(self):
        return os.path.join(self.INSTALL_DIR, 'files', 'excel')
        
    @property
    def CONFIG_DIR(self):
        return os.path.join(self.INSTALL_DIR, 'config')
        
    @property
    def LICENSE_FILE(self):
        return os.path.join(self.CONFIG_DIR, 'fiserv_conciliacion.lic')
        
    @property
    def LOG_FILE(self):
        return os.path.join(self.INSTALL_DIR, 'service.log')
        
    @property
    def ENV_FILE(self):
        return os.path.join(self.CONFIG_DIR, '.env')
        
    # Configuración SMTP
    @property
    def SMTP_SERVER(self):
        return os.getenv('SMTP_SERVER', 'mail.rapanui.com.ar')
        
    @property
    def SMTP_PORT(self):
        return int(os.getenv('SMTP_PORT', '465'))
        
    @property
    def SMTP_USER(self):
        return os.getenv('SMTP_USER', 'conciliaciones@rapanui.com.ar')
        
    @property
    def SMTP_PASSWORD(self):
        return os.getenv('SMTP_PASSWORD', '')
        
    @property
    def MAIL_RECIPIENTS(self):
        recipients = os.getenv('MAIL_RECIPIENTS', '')
        return [email.strip() for email in recipients.split(',') if email.strip()]
        
    @property
    def SENDER_NAME(self):
        return os.getenv('SENDER_NAME', 'Departamento de Sistemas')
        
    # Configuración de ejecución
    @property
    def FRECUENCIA_ENVIO(self):
        return os.getenv('FRECUENCIA_ENVIO', 'semanal')
        
    @property
    def HORA_EJECUCION(self):
        return {
            'diario': os.getenv('HORA_EJECUCION_DIARIA', '23:00'),
            'semanal': os.getenv('HORA_EJECUCION_SEMANAL', '07:00'),
            'mensual': os.getenv('HORA_EJECUCION_MENSUAL', '06:00')
        }
        
    def create_directories(self):
        """Crear estructura de directorios necesaria"""
        directories = [
            self.INPUT_DIR,
            self.TERMINADO_DIR,
            self.EXCEL_DIR,
            self.CONFIG_DIR
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            
    def validate_config(self):
        """Validar que la configuración sea correcta"""
        required_vars = [
            'SMTP_SERVER',
            'SMTP_PORT',
            'SMTP_USER',
            'SMTP_PASSWORD',
            'MAIL_RECIPIENTS'
        ]
        
        missing = []
        for var in required_vars:
            if not getattr(self, var):
                missing.append(var)
                
        if missing:
            raise ValueError(f"Faltan variables de configuración requeridas: {', '.join(missing)}")
            
        return True

# Instancia global de configuración
config = Config() 