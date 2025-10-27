import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración de la aplicación Flask"""

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 5000))

    # WooCommerce
    WOOCOMMERCE_URL = os.getenv('WOOCOMMERCE_URL')
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
