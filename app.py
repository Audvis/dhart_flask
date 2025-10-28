from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from routes.products import products_bp
from routes.categories import categories_bp
from routes.orders import orders_bp
from routes.customers import customers_bp
from services import wc_service

app = Flask(__name__)
app.config.from_object(Config)

# Configurar CORS para permitir requests desde Next.js
CORS(app, resources={
    r"/api/*": {
        "origins": app.config['ALLOWED_ORIGINS'],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Registrar blueprints
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(categories_bp, url_prefix='/api/categories')
app.register_blueprint(orders_bp, url_prefix='/api/orders')
app.register_blueprint(customers_bp, url_prefix='/api/customers')

@app.route('/')
def index():
    return {
        'message': 'WooCommerce Backend API',
        'version': '1.0.0',
        'endpoints': {
            'products': '/api/products',
            'categories': '/api/categories',
            'orders': '/api/orders',
            'customers': '/api/customers',
            'test': '/api/test'
        }
    }

@app.route('/health')
def health():
    """Health check básico"""
    import os
    return {
        'status': 'healthy',
        'env': os.getenv('FLASK_ENV', 'not set'),
        'woocommerce_configured': wc_service.wcapi is not None
    }

@app.route('/api/config')
def check_config():
    """Verifica el estado de la configuración"""
    import os
    return jsonify({
        'flask_env': os.getenv('FLASK_ENV', 'not set'),
        'woocommerce_url': os.getenv('WOOCOMMERCE_URL', 'not set'),
        'consumer_key_set': bool(os.getenv('WOOCOMMERCE_CONSUMER_KEY')),
        'consumer_secret_set': bool(os.getenv('WOOCOMMERCE_CONSUMER_SECRET')),
        'allowed_origins': os.getenv('ALLOWED_ORIGINS', 'not set'),
        'port': os.getenv('PORT', 'not set'),
        'woocommerce_service_initialized': wc_service.wcapi is not None
    })

@app.route('/api/test')
def test_woocommerce():
    """Endpoint para probar la conexión con WooCommerce"""
    result = wc_service.test_connection()
    status_code = result.pop('status_code', 200)
    return jsonify(result), status_code

if __name__ == '__main__':
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
