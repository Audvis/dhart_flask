import os
from pathlib import Path
from dotenv import load_dotenv

# Obtener el directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / '.env'

# Cargar variables de entorno desde el archivo .env (si existe)
# En producción, las variables vienen del sistema, no del archivo
if ENV_FILE.exists():
    load_dotenv(dotenv_path=ENV_FILE)
else:
    # En producción, las variables ya están en el entorno
    load_dotenv()

class Config:
    """Configuración de la aplicación Flask"""

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 5000))

    # WooCommerce
    WOOCOMMERCE_URL = os.getenv('WOOCOMMERCE_URL', 'https://tu-tienda.com')
    WOOCOMMERCE_CONSUMER_KEY = os.getenv('WOOCOMMERCE_CONSUMER_KEY')
    WOOCOMMERCE_CONSUMER_SECRET = os.getenv('WOOCOMMERCE_CONSUMER_SECRET')

    # CORS
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')

    @staticmethod
    def validate():
        """Valida que las variables de entorno requeridas estén configuradas"""
        required_vars = [
            'WOOCOMMERCE_URL',
            'WOOCOMMERCE_CONSUMER_KEY',
            'WOOCOMMERCE_CONSUMER_SECRET'
        ]

        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)

        if missing_vars:
            raise ValueError(
                f"Faltan las siguientes variables de entorno: {', '.join(missing_vars)}\n"
                f"Por favor, crea un archivo .env basado en .env.example"
            )
