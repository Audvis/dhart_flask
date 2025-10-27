from woocommerce import API
from config import Config

class WooCommerceService:
    """Servicio para interactuar con la API de WooCommerce"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WooCommerceService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Inicializa la conexión con WooCommerce"""
        Config.validate()

        self.wcapi = API(
            url=Config.WOOCOMMERCE_URL,
            consumer_key=Config.WOOCOMMERCE_CONSUMER_KEY,
            consumer_secret=Config.WOOCOMMERCE_CONSUMER_SECRET,
            version="wc/v3",
            timeout=30
        )

    def get(self, endpoint, params=None):
        """Realiza una petición GET a la API de WooCommerce"""
        try:
            response = self.wcapi.get(endpoint, params=params)
            return {
                'success': True,
                'data': response.json(),
                'status_code': response.status_code
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'status_code': 500
            }

    def post(self, endpoint, data):
        """Realiza una petición POST a la API de WooCommerce"""
        try:
            response = self.wcapi.post(endpoint, data)
            return {
                'success': True,
                'data': response.json(),
                'status_code': response.status_code
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'status_code': 500
            }

    def put(self, endpoint, data):
        """Realiza una petición PUT a la API de WooCommerce"""
        try:
            response = self.wcapi.put(endpoint, data)
            return {
                'success': True,
                'data': response.json(),
                'status_code': response.status_code
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'status_code': 500
            }

    def delete(self, endpoint, params=None):
        """Realiza una petición DELETE a la API de WooCommerce"""
        try:
            response = self.wcapi.delete(endpoint, params=params)
            return {
                'success': True,
                'data': response.json(),
                'status_code': response.status_code
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'status_code': 500
            }

# Instancia única del servicio
wc_service = WooCommerceService()
