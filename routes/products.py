from flask import Blueprint, request, jsonify
from services import wc_service
from utils.transformers import transform_products, transform_product_minimal

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
def get_products():
    """
    Obtiene la lista de productos

    Por defecto devuelve solo: id, name, price, images (optimizado)

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
    - _fields: campos específicos a devolver (ej: id,name,price,stock_status)
    - all_fields: true para obtener TODOS los campos de WooCommerce
    - raw: true para obtener datos sin transformar (opcional)
    - minimal: true para obtener versión minimalista (opcional)
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

    # Filtro de campos específicos (WooCommerce _fields)
    # Por defecto, solo traer campos necesarios para mejor performance
    if request.args.get('_fields'):
        params['_fields'] = request.args.get('_fields')
    elif request.args.get('all_fields', 'false').lower() != 'true':
        # Campos por defecto para reducir tamaño de respuesta
        # Usa ?all_fields=true para obtener todos los campos
        params['_fields'] = 'id,name,price,images'

    result = wc_service.get('products', params=params)

    if result['success']:
        # Si se especificó _fields, devolver datos raw por defecto
        # (a menos que se solicite explícitamente transformación)
        raw = request.args.get('raw', 'false').lower() == 'true'
        minimal = request.args.get('minimal', 'false').lower() == 'true'
        transform = request.args.get('transform', 'false').lower() == 'true'

        # Si se usó _fields, devolver raw a menos que se pida transform
        if '_fields' in params and not transform:
            data = result['data']
        elif raw:
            # Devolver datos sin transformar
            data = result['data']
        elif minimal:
            # Versión minimalista
            data = [transform_product_minimal(p) for p in result['data']]
        else:
            # Transformación por defecto solo si no se especificó _fields
            data = result['data'] if '_fields' in params else transform_products(result['data'])

        return jsonify(data), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Obtiene un producto específico por ID
    Query params opcionales:
    - _fields: campos específicos a devolver (ej: id,name,price,images)
    - all_fields: true para obtener todos los campos
    - raw: true para obtener datos sin transformar
    """
    params = {}

    # Filtro de campos específicos
    if request.args.get('_fields'):
        params['_fields'] = request.args.get('_fields')
    elif request.args.get('all_fields', 'false').lower() != 'true':
        # Por defecto, campos básicos para mejor performance
        params['_fields'] = 'id,name,price,images'

    result = wc_service.get(f'products/{product_id}', params=params)

    if result['success']:
        raw = request.args.get('raw', 'false').lower() == 'true'
        transform = request.args.get('transform', 'false').lower() == 'true'

        # Si se usó _fields, devolver raw a menos que se pida transform
        if '_fields' in params and not transform:
            data = result['data']
        elif raw:
            data = result['data']
        else:
            # Transformación por defecto solo si no se especificó _fields
            data = result['data'] if '_fields' in params else transform_products(result['data'])

        return jsonify(data), result['status_code']
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
