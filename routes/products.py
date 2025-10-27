from flask import Blueprint, request, jsonify
from services import wc_service

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
def get_products():
    """
    Obtiene la lista de productos
    Query params opcionales:
    - page: número de página (default: 1)
    - per_page: productos por página (default: 10)
    - search: búsqueda por nombre
    - category: filtrar por categoría
    - status: filtrar por estado (publish, draft, pending)
    - featured: filtrar por destacados (true/false)
    - on_sale: filtrar por en oferta (true/false)
    - min_price: precio mínimo
    - max_price: precio máximo
    - orderby: ordenar por (date, id, title, price)
    - order: orden (asc, desc)
    """
    params = {}

    # Paginación
    if request.args.get('page'):
        params['page'] = request.args.get('page')
    if request.args.get('per_page'):
        params['per_page'] = request.args.get('per_page')

    # Filtros
    if request.args.get('search'):
        params['search'] = request.args.get('search')
    if request.args.get('category'):
        params['category'] = request.args.get('category')
    if request.args.get('status'):
        params['status'] = request.args.get('status')
    if request.args.get('featured'):
        params['featured'] = request.args.get('featured')
    if request.args.get('on_sale'):
        params['on_sale'] = request.args.get('on_sale')
    if request.args.get('min_price'):
        params['min_price'] = request.args.get('min_price')
    if request.args.get('max_price'):
        params['max_price'] = request.args.get('max_price')

    # Ordenamiento
    if request.args.get('orderby'):
        params['orderby'] = request.args.get('orderby')
    if request.args.get('order'):
        params['order'] = request.args.get('order')

    result = wc_service.get('products', params=params)

    if result['success']:
        return jsonify(result['data']), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Obtiene un producto específico por ID"""
    result = wc_service.get(f'products/{product_id}')

    if result['success']:
        return jsonify(result['data']), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']


@products_bp.route('/', methods=['POST'])
def create_product():
    """
    Crea un nuevo producto
    Body debe incluir datos del producto según la API de WooCommerce
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se proporcionaron datos'}), 400

    result = wc_service.post('products', data)

    if result['success']:
        return jsonify(result['data']), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']


@products_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Actualiza un producto existente"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se proporcionaron datos'}), 400

    result = wc_service.put(f'products/{product_id}', data)

    if result['success']:
        return jsonify(result['data']), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']


@products_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """
    Elimina un producto
    Query params opcionales:
    - force: true para eliminar permanentemente (default: false, envía a papelera)
    """
    params = {}
    if request.args.get('force'):
        params['force'] = request.args.get('force')

    result = wc_service.delete(f'products/{product_id}', params=params)

    if result['success']:
        return jsonify(result['data']), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']


@products_bp.route('/batch', methods=['POST'])
def batch_products():
    """
    Operaciones en lote para productos
    Body debe incluir:
    - create: array de productos a crear
    - update: array de productos a actualizar
    - delete: array de IDs de productos a eliminar
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se proporcionaron datos'}), 400

    result = wc_service.post('products/batch', data)

    if result['success']:
        return jsonify(result['data']), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']
