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
    return {'status': 'healthy'}

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
