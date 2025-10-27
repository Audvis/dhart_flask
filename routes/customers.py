from flask import Blueprint, request, jsonify
from services import wc_service

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/', methods=['GET'])
def get_customers():
    """
    Obtiene la lista de clientes
    Query params opcionales:
    - page: número de página (default: 1)
    - per_page: clientes por página (default: 10)
    - search: búsqueda por nombre o email
    - email: filtrar por email específico
    - role: filtrar por rol (all, customer, subscriber, etc)
    - orderby: ordenar por (id, name, email, registered_date)
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
    if request.args.get('email'):
        params['email'] = request.args.get('email')
    if request.args.get('role'):
        params['role'] = request.args.get('role')

    # Ordenamiento
    if request.args.get('orderby'):
        params['orderby'] = request.args.get('orderby')
    if request.args.get('order'):
        params['order'] = request.args.get('order')

    result = wc_service.get('customers', params=params)

    if result['success']:
        return jsonify(result['data']), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']


@customers_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Obtiene un cliente específico por ID"""
    result = wc_service.get(f'customers/{customer_id}')

    if result['success']:
        return jsonify(result['data']), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']


@customers_bp.route('/', methods=['POST'])
def create_customer():
    """
    Crea un nuevo cliente
    Body debe incluir:
    - email: email del cliente (requerido)
    - first_name: nombre (opcional)
    - last_name: apellido (opcional)
    - username: nombre de usuario (opcional)
    - password: contraseña (opcional)
    - billing: información de facturación (opcional)
    - shipping: información de envío (opcional)
    """
    data = request.get_json()

    if not data or 'email' not in data:
        return jsonify({'error': 'El email del cliente es requerido'}), 400

    result = wc_service.post('customers', data)

    if result['success']:
        return jsonify(result['data']), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']


@customers_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """Actualiza un cliente existente"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se proporcionaron datos'}), 400

    result = wc_service.put(f'customers/{customer_id}', data)

    if result['success']:
        return jsonify(result['data']), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']


@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    """
    Elimina un cliente
    Query params opcionales:
    - force: true para eliminar permanentemente (default: false)
    - reassign: ID del usuario al que reasignar los posts (opcional)
    """
    params = {}
    if request.args.get('force'):
        params['force'] = request.args.get('force')
    if request.args.get('reassign'):
        params['reassign'] = request.args.get('reassign')

    result = wc_service.delete(f'customers/{customer_id}', params=params)

    if result['success']:
        return jsonify(result['data']), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']


@customers_bp.route('/<int:customer_id>/downloads', methods=['GET'])
def get_customer_downloads(customer_id):
    """Obtiene las descargas disponibles para un cliente"""
    result = wc_service.get(f'customers/{customer_id}/downloads')

    if result['success']:
        return jsonify(result['data']), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']


@customers_bp.route('/batch', methods=['POST'])
def batch_customers():
    """
    Operaciones en lote para clientes
    Body debe incluir:
    - create: array de clientes a crear
    - update: array de clientes a actualizar
    - delete: array de IDs de clientes a eliminar
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se proporcionaron datos'}), 400

    result = wc_service.post('customers/batch', data)

    if result['success']:
        return jsonify(result['data']), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']
