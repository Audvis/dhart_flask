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
            # Log para debug
            full_url = f"{Config.WOOCOMMERCE_URL}/wp-json/wc/v3/{endpoint}"
            print(f"[DEBUG] Llamando a: {full_url}")
            print(f"[DEBUG] Params: {params}")

            response = self.wcapi.get(endpoint, params=params)

            print(f"[DEBUG] Status Code: {response.status_code}")
            print(f"[DEBUG] URL final: {response.url}")
            print(f"[DEBUG] Content-Type: {response.headers.get('Content-Type', 'N/A')}")

            # Verificar si la respuesta es exitosa
            if response.status_code >= 400:
                error_msg = f"Error {response.status_code}: {response.text}"
                return {
                    'success': False,
                    'error': error_msg,
                    'status_code': response.status_code,
                    'url_called': response.url
                }

            # Intentar parsear JSON
            try:
                data = response.json()
            except ValueError as json_error:
                return {
                    'success': False,
                    'error': f"Error al parsear JSON: {str(json_error)}. Respuesta: {response.text[:200]}",
                    'status_code': response.status_code,
                    'url_called': response.url
                }

            return {
                'success': True,
                'data': data,
                'status_code': response.status_code
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Error de conexión: {str(e)}",
                'status_code': 500
            }

    def post(self, endpoint, data):
        """Realiza una petición POST a la API de WooCommerce"""
        try:
            response = self.wcapi.post(endpoint, data)

            if response.status_code >= 400:
                error_msg = f"Error {response.status_code}: {response.text}"
                return {
                    'success': False,
                    'error': error_msg,
                    'status_code': response.status_code
                }

            try:
                data = response.json()
            except ValueError as json_error:
                return {
                    'success': False,
                    'error': f"Error al parsear JSON: {str(json_error)}. Respuesta: {response.text[:200]}",
                    'status_code': response.status_code
                }

            return {
                'success': True,
                'data': data,
                'status_code': response.status_code
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Error de conexión: {str(e)}",
                'status_code': 500
            }

    def put(self, endpoint, data):
        """Realiza una petición PUT a la API de WooCommerce"""
        try:
            response = self.wcapi.put(endpoint, data)

            if response.status_code >= 400:
                error_msg = f"Error {response.status_code}: {response.text}"
                return {
                    'success': False,
                    'error': error_msg,
                    'status_code': response.status_code
                }

            try:
                data = response.json()
            except ValueError as json_error:
                return {
                    'success': False,
                    'error': f"Error al parsear JSON: {str(json_error)}. Respuesta: {response.text[:200]}",
                    'status_code': response.status_code
                }

            return {
                'success': True,
                'data': data,
                'status_code': response.status_code
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Error de conexión: {str(e)}",
                'status_code': 500
            }

    def delete(self, endpoint, params=None):
        """Realiza una petición DELETE a la API de WooCommerce"""
        try:
            response = self.wcapi.delete(endpoint, params=params)

            if response.status_code >= 400:
                error_msg = f"Error {response.status_code}: {response.text}"
                return {
                    'success': False,
                    'error': error_msg,
                    'status_code': response.status_code
                }

            try:
                data = response.json()
            except ValueError as json_error:
                return {
                    'success': False,
                    'error': f"Error al parsear JSON: {str(json_error)}. Respuesta: {response.text[:200]}",
                    'status_code': response.status_code
                }

            return {
                'success': True,
                'data': data,
                'status_code': response.status_code
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Error de conexión: {str(e)}",
                'status_code': 500
            }

    def test_connection(self):
        """Prueba la conexión con la API de WooCommerce"""
        try:
            # Intenta obtener información básica de la tienda
            response = self.wcapi.get("")
            return {
                'success': True,
                'message': 'Conexión exitosa con WooCommerce',
                'status_code': response.status_code,
                'store_info': response.json() if response.status_code == 200 else None
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Error de conexión: {str(e)}",
                'message': 'No se pudo conectar con WooCommerce. Verifica tus credenciales y URL.',
                'status_code': 500
            }

# Instancia única del servicio
wc_service = WooCommerceService()
