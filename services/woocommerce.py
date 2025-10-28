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
        try:
            Config.validate()

            self.wcapi = API(
                url=Config.WOOCOMMERCE_URL,
                consumer_key=Config.WOOCOMMERCE_CONSUMER_KEY,
                consumer_secret=Config.WOOCOMMERCE_CONSUMER_SECRET,
                version="wc/v3",
                timeout=30
            )
            print(f"[WooCommerce] Conectado a: {Config.WOOCOMMERCE_URL}")
        except Exception as e:
            print(f"[WooCommerce] Error al inicializar: {e}")
            # No lanzar error, permitir que la app inicie
            # Los endpoints devolverán error cuando se usen
            self.wcapi = None

    def get(self, endpoint, params=None):
        """Realiza una petición GET a la API de WooCommerce"""
        if self.wcapi is None:
            return {
                'success': False,
                'error': 'WooCommerce no está configurado. Verifica las variables de entorno.',
                'status_code': 500
            }

        try:
            response = self.wcapi.get(endpoint, params=params)

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
