# Guía de Transformadores

Los transformadores te permiten modificar la respuesta de WooCommerce antes de enviarla al frontend, **sin cambiar los datos reales** en WooCommerce.

## Ubicación

Los transformadores están en: `utils/transformers.py`

## Cómo funciona

```
WooCommerce → Backend Flask → Transformador → Next.js
```

1. Backend obtiene datos de WooCommerce
2. Transformador modifica/limpia la respuesta
3. Frontend recibe datos transformados

---

## Uso desde Postman/Frontend

### Obtener productos con transformación (por defecto)
```
GET http://localhost:5000/api/products
```

**Respuesta transformada:**
```json
[
  {
    "id": 123,
    "name": "Producto",
    "price": "29.99",
    "regular_price": "39.99",
    "sale_price": "29.99",
    "is_available": true,
    "has_discount": true,
    "discount_percentage": 25.0,
    "thumbnail": "https://...",
    "gallery": ["https://...", "https://..."],
    "currency": "USD"
  }
]
```

### Obtener datos sin transformar (raw)
```
GET http://localhost:5000/api/products?raw=true
```

Devuelve los datos exactamente como vienen de WooCommerce.

### Obtener versión minimalista
```
GET http://localhost:5000/api/products?minimal=true
```

**Respuesta minimalista (solo campos esenciales):**
```json
[
  {
    "id": 123,
    "name": "Producto",
    "price": "29.99",
    "image": "https://...",
    "on_sale": true
  }
]
```

---

## Personalizar transformaciones

Abre el archivo `utils/transformers.py` y modifica la función `transform_product()`:

### Ejemplo 1: Agregar campos calculados

```python
def transform_product(product):
    transformed = {
        'id': product.get('id'),
        'name': product.get('name'),
        'price': product.get('price'),

        # AGREGAR CAMPO PERSONALIZADO
        'precio_con_iva': calculate_price_with_tax(product.get('price')),
        'es_nuevo': is_new_product(product.get('date_created')),
    }

    return transformed

def calculate_price_with_tax(price):
    """Calcular precio con IVA"""
    try:
        return float(price) * 1.16  # 16% IVA
    except:
        return price

def is_new_product(date_created):
    """Verificar si el producto es nuevo (menos de 30 días)"""
    from datetime import datetime, timedelta
    try:
        created = datetime.fromisoformat(date_created.replace('Z', '+00:00'))
        return (datetime.now() - created).days < 30
    except:
        return False
```

### Ejemplo 2: Renombrar campos

```python
def transform_product(product):
    return {
        'id': product.get('id'),
        'titulo': product.get('name'),  # name → titulo
        'precio': product.get('price'),  # price → precio
        'imagen': product.get('images', [{}])[0].get('src'),  # images → imagen
        'disponible': product.get('stock_status') == 'instock',
    }
```

### Ejemplo 3: Filtrar información sensible

```python
def transform_product(product):
    transformed = {
        'id': product.get('id'),
        'name': product.get('name'),
        'price': product.get('price'),
        # NO incluir costo, proveedor, etc.
    }

    # No enviar meta_data que pueda contener info sensible
    return transformed
```

### Ejemplo 4: Transformar categorías

```python
def transform_product(product):
    transformed = {
        'id': product.get('id'),
        'name': product.get('name'),

        # Simplificar categorías
        'categories': [cat.get('name') for cat in product.get('categories', [])],
        'category_ids': [cat.get('id') for cat in product.get('categories', [])],
    }

    return transformed
```

### Ejemplo 5: Agregar URLs personalizadas

```python
def transform_product(product):
    slug = product.get('slug')

    return {
        'id': product.get('id'),
        'name': product.get('name'),
        'price': product.get('price'),

        # Agregar URL del frontend
        'url': f"https://tu-tienda.com/productos/{slug}",
        'share_url': f"https://tu-tienda.com/share/{product.get('id')}",
    }
```

---

## Crear múltiples versiones

Puedes crear diferentes transformadores para diferentes necesidades:

### En `utils/transformers.py`:

```python
def transform_product_card(product):
    """Para cards/tarjetas en listados"""
    return {
        'id': product.get('id'),
        'name': product.get('name'),
        'price': product.get('price'),
        'image': product.get('images', [{}])[0].get('src'),
        'on_sale': product.get('on_sale'),
    }

def transform_product_detail(product):
    """Para página de detalle completa"""
    return {
        'id': product.get('id'),
        'name': product.get('name'),
        'price': product.get('price'),
        'description': product.get('description'),
        'images': [img.get('src') for img in product.get('images', [])],
        'categories': product.get('categories'),
        'attributes': product.get('attributes'),
        'related_ids': product.get('related_ids'),
    }

def transform_product_search(product):
    """Para resultados de búsqueda"""
    return {
        'id': product.get('id'),
        'name': product.get('name'),
        'price': product.get('price'),
        'image': product.get('images', [{}])[0].get('src'),
    }
```

### Usar en el controlador (`routes/products.py`):

```python
from utils.transformers import (
    transform_product_card,
    transform_product_detail,
    transform_product_search
)

@products_bp.route('/', methods=['GET'])
def get_products():
    # ... código existente ...

    # Elegir transformador según parámetro
    view_type = request.args.get('view', 'default')

    if view_type == 'card':
        data = [transform_product_card(p) for p in result['data']]
    elif view_type == 'detail':
        data = [transform_product_detail(p) for p in result['data']]
    elif view_type == 'search':
        data = [transform_product_search(p) for p in result['data']]
    else:
        data = transform_products(result['data'])

    return jsonify(data), result['status_code']
```

---

## Consejos

1. **No modifiques datos en WooCommerce**: Los transformadores solo cambian la respuesta, no los datos reales
2. **Mantén consistencia**: Usa los mismos campos en todos los transformadores
3. **Documenta cambios**: Comenta qué hace cada transformación
4. **Prueba siempre**: Usa `?raw=true` para comparar con datos originales
5. **Performance**: No hagas operaciones pesadas en transformadores (evita llamadas a DB, APIs, etc.)

---

## Ejemplo completo para Next.js

### En tu API de Next.js:

```javascript
// lib/api.js
export async function getProducts(options = {}) {
  const { minimal = false, ...filters } = options;

  const params = new URLSearchParams({
    ...filters,
    minimal: minimal.toString()
  });

  const response = await fetch(
    `http://localhost:5000/api/products?${params}`
  );

  return response.json();
}

// Usar en componente
const products = await getProducts({ minimal: true, per_page: 10 });
```

---

## Troubleshooting

### Error: "module 'utils.transformers' has no attribute 'transform_product'"

Reinicia el servidor Flask después de modificar transformers.py

### Los cambios no se reflejan

1. Detén el servidor (Ctrl+C)
2. Reinicia: `python app.py`
3. Limpia caché del navegador/Postman

### Quiero datos originales temporalmente

Agrega `?raw=true` a cualquier endpoint:
```
GET /api/products?raw=true
GET /api/products/123?raw=true
```
