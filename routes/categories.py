from flask import Blueprint, request, jsonify
from services import wc_service
from utils.transformers import transform_categories_minimal

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/', methods=['GET'])
def get_categories():
    """
    Obtiene la lista de categorías
    Query params opcionales:
    - page: número de página (default: 1)
    - per_page: categorías por página (default: 10)
    - search: búsqueda por nombre
    - parent: filtrar por categoría padre
    - hide_empty: ocultar categorías vacías (true/false)
    - orderby: ordenar por (id, name, slug, count)
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
    if request.args.get('parent'):
        params['parent'] = request.args.get('parent')
    if request.args.get('hide_empty'):
        params['hide_empty'] = request.args.get('hide_empty')

    # Ordenamiento
    if request.args.get('orderby'):
        params['orderby'] = request.args.get('orderby')
    if request.args.get('order'):
        params['order'] = request.args.get('order')

    result = wc_service.get('products/categories', params=params)

    if result['success']:
        # Por defecto, devolver versión simplificada (id, name, slug)
        # Usar ?raw=true para obtener datos completos de WooCommerce
        raw = request.args.get('raw', 'false').lower() == 'true'

        if raw:
            data = result['data']
        else:
            data = transform_categories_minimal(result['data'])

        return jsonify(data), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']


@categories_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """
    Obtiene una categoría específica por ID
    Query params opcionales:
    - raw: true para obtener datos completos de WooCommerce
    """
    result = wc_service.get(f'products/categories/{category_id}')

    if result['success']:
        # Por defecto, devolver versión simplificada (id, name, slug)
        raw = request.args.get('raw', 'false').lower() == 'true'

        if raw:
            data = result['data']
        else:
            data = transform_categories_minimal(result['data'])

        return jsonify(data), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']


@categories_bp.route('/', methods=['POST'])
def create_category():
    """
    Crea una nueva categoría
    Body debe incluir:
    - name: nombre de la categoría (requerido)
    - slug: slug de la categoría (opcional)
    - parent: ID de la categoría padre (opcional)
    - description: descripción (opcional)
    - image: objeto de imagen (opcional)
    """
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({'error': 'El nombre de la categoría es requerido'}), 400

    result = wc_service.post('products/categories', data)

    if result['success']:
        return jsonify(result['data']), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']


@categories_bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """Actualiza una categoría existente"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se proporcionaron datos'}), 400

    result = wc_service.put(f'products/categories/{category_id}', data)

    if result['success']:
        return jsonify(result['data']), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']


@categories_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """
    Elimina una categoría
    Query params opcionales:
    - force: true para eliminar permanentemente (default: false)
    """
    params = {}
    if request.args.get('force'):
        params['force'] = request.args.get('force')

    result = wc_service.delete(f'products/categories/{category_id}', params=params)

    if result['success']:
        return jsonify(result['data']), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']


@categories_bp.route('/batch', methods=['POST'])
def batch_categories():
    """
    Operaciones en lote para categorías
    Body debe incluir:
    - create: array de categorías a crear
    - update: array de categorías a actualizar
    - delete: array de IDs de categorías a eliminar
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se proporcionaron datos'}), 400

    result = wc_service.post('products/categories/batch', data)

    if result['success']:
        return jsonify(result['data']), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']
