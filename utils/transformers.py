"""
Transformadores para modificar las respuestas de WooCommerce
antes de enviarlas al frontend
"""

def transform_product(product):
    """
    Transforma un producto individual de WooCommerce
    Aquí puedes agregar, eliminar o modificar campos
    """
    # Ejemplo: extraer solo los campos que necesitas
    transformed = {
        'id': product.get('id'),
        'name': product.get('name'),
        'slug': product.get('slug'),
        'price': product.get('price'),
        'regular_price': product.get('regular_price'),
        'sale_price': product.get('sale_price'),
        'on_sale': product.get('on_sale'),
        'stock_status': product.get('stock_status'),
        'stock_quantity': product.get('stock_quantity'),
        'description': product.get('description'),
        'short_description': product.get('short_description'),
        'categories': product.get('categories', []),
        'images': product.get('images', []),
        'attributes': product.get('attributes', []),

        # Agregar campos calculados o personalizados
        'is_available': product.get('stock_status') == 'instock',
        'has_discount': bool(product.get('sale_price')),
        'discount_percentage': calculate_discount(
            product.get('regular_price'),
            product.get('sale_price')
        ) if product.get('sale_price') else 0,

        # Puedes agregar campos nuevos
        'display_price': product.get('price'),
        'currency': 'USD',  # o desde configuración
    }

    # Transformar imágenes a un formato más simple
    if transformed['images']:
        transformed['thumbnail'] = transformed['images'][0].get('src') if transformed['images'] else None
        transformed['gallery'] = [img.get('src') for img in transformed['images']]

    return transformed


def transform_products(products):
    """
    Transforma una lista de productos
    """
    if isinstance(products, list):
        return [transform_product(product) for product in products]
    return transform_product(products)


def calculate_discount(regular_price, sale_price):
    """
    Calcula el porcentaje de descuento
    """
    try:
        regular = float(regular_price or 0)
        sale = float(sale_price or 0)

        if regular > 0 and sale > 0:
            discount = ((regular - sale) / regular) * 100
            return round(discount, 2)
    except (ValueError, TypeError):
        pass

    return 0


# Puedes crear más transformadores según necesites
def transform_product_minimal(product):
    """
    Versión minimalista del producto (para listados)
    """
    return {
        'id': product.get('id'),
        'name': product.get('name'),
        'price': product.get('price'),
        'image': product.get('images', [{}])[0].get('src') if product.get('images') else None,
        'on_sale': product.get('on_sale'),
    }


def transform_product_detailed(product):
    """
    Versión detallada del producto (para página de producto)
    """
    base = transform_product(product)

    # Agregar información adicional para vista detallada
    base.update({
        'related_ids': product.get('related_ids', []),
        'upsell_ids': product.get('upsell_ids', []),
        'cross_sell_ids': product.get('cross_sell_ids', []),
        'variations': product.get('variations', []),
        'meta_data': product.get('meta_data', []),
    })

    return base
