from flask import Blueprint, request, jsonify
from services import wc_service

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/', methods=['GET'])
def get_orders():
    """
    Obtiene la lista de pedidos
    Query params opcionales:
    - page: número de página (default: 1)
    - per_page: pedidos por página (default: 10)
    - search: búsqueda por texto
    - status: filtrar por estado (pending, processing, on-hold, completed, cancelled, refunded, failed)
    - customer: filtrar por ID de cliente
    - product: filtrar por ID de producto
    - after: pedidos después de esta fecha (ISO8601)
    - before: pedidos antes de esta fecha (ISO8601)
    - orderby: ordenar por (date, id, title)
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
    if request.args.get('status'):
        params['status'] = request.args.get('status')
    if request.args.get('customer'):
        params['customer'] = request.args.get('customer')
    if request.args.get('product'):
        params['product'] = request.args.get('product')
    if request.args.get('after'):
        params['after'] = request.args.get('after')
    if request.args.get('before'):
        params['before'] = request.args.get('before')

    # Ordenamiento
    if request.args.get('orderby'):
        params['orderby'] = request.args.get('orderby')
    if request.args.get('order'):
        params['order'] = request.args.get('order')

    result = wc_service.get('orders', params=params)

    if result['success']:
        return jsonify(result['data']), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']


@orders_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Obtiene un pedido específico por ID"""
    result = wc_service.get(f'orders/{order_id}')

    if result['success']:
        return jsonify(result['data']), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']


@orders_bp.route('/', methods=['POST'])
def create_order():
    """
    Crea un nuevo pedido
    Body debe incluir:
    - line_items: array de productos (requerido)
    - billing: información de facturación (opcional)
    - shipping: información de envío (opcional)
    - customer_id: ID del cliente (opcional)
    - payment_method: método de pago (opcional)
    - payment_method_title: título del método de pago (opcional)
    - status: estado del pedido (opcional)
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se proporcionaron datos'}), 400

    result = wc_service.post('orders', data)

    if result['success']:
        return jsonify(result['data']), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']


@orders_bp.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """
    Actualiza un pedido existente
    Útil para cambiar estado, agregar notas, actualizar información
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se proporcionaron datos'}), 400

    result = wc_service.put(f'orders/{order_id}', data)

    if result['success']:
        return jsonify(result['data']), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']


@orders_bp.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """
    Elimina un pedido
    Query params opcionales:
    - force: true para eliminar permanentemente (default: false, envía a papelera)
    """
    params = {}
    if request.args.get('force'):
        params['force'] = request.args.get('force')

    result = wc_service.delete(f'orders/{order_id}', params=params)

    if result['success']:
        return jsonify(result['data']), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']


@orders_bp.route('/<int:order_id>/notes', methods=['GET'])
def get_order_notes(order_id):
    """Obtiene las notas de un pedido"""
    result = wc_service.get(f'orders/{order_id}/notes')

    if result['success']:
        return jsonify(result['data']), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']


@orders_bp.route('/<int:order_id>/notes', methods=['POST'])
def create_order_note(order_id):
    """
    Crea una nota para un pedido
    Body debe incluir:
    - note: texto de la nota (requerido)
    - customer_note: si es visible para el cliente (opcional, default: false)
    """
    data = request.get_json()

    if not data or 'note' not in data:
        return jsonify({'error': 'El texto de la nota es requerido'}), 400

    result = wc_service.post(f'orders/{order_id}/notes', data)

    if result['success']:
        return jsonify(result['data']), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']


@orders_bp.route('/batch', methods=['POST'])
def batch_orders():
    """
    Operaciones en lote para pedidos
    Body debe incluir:
    - create: array de pedidos a crear
    - update: array de pedidos a actualizar
    - delete: array de IDs de pedidos a eliminar
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se proporcionaron datos'}), 400

    result = wc_service.post('orders/batch', data)

    if result['success']:
        return jsonify(result['data']), result['status_code']
    else:
        return jsonify({'error': result['error']}), result['status_code']
