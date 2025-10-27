# Guía de Postman para el Backend Flask

## Opción 1: Llamar a tu Backend Flask (Más simple y recomendado)

Tu backend Flask maneja la autenticación automáticamente. **NO necesitas pasar credenciales**.

### Configuración en Postman:

#### 1. Listar productos
```
Método: GET
URL: http://localhost:5000/api/products
Authorization: No Auth
Headers: (ninguno necesario)
Query Params (opcionales):
  - per_page: 10
  - status: publish
  - search: camiseta
```

#### 2. Obtener un producto
```
Método: GET
URL: http://localhost:5000/api/products/123
Authorization: No Auth
```

#### 3. Crear producto
```
Método: POST
URL: http://localhost:5000/api/products
Authorization: No Auth
Headers:
  - Content-Type: application/json
Body (raw JSON):
{
  "name": "Producto de Prueba",
  "type": "simple",
  "regular_price": "29.99",
  "description": "Descripción del producto",
  "short_description": "Descripción corta"
}
```

#### 4. Actualizar producto
```
Método: PUT
URL: http://localhost:5000/api/products/123
Authorization: No Auth
Headers:
  - Content-Type: application/json
Body (raw JSON):
{
  "regular_price": "24.99",
  "sale_price": "19.99"
}
```

#### 5. Eliminar producto
```
Método: DELETE
URL: http://localhost:5000/api/products/123?force=true
Authorization: No Auth
```

---

## Opción 2: Llamar directamente a WooCommerce (Para verificar credenciales)

Si quieres probar que tus credenciales de WooCommerce funcionan directamente:

### Método 1: Basic Authentication (Recomendado)

```
Método: GET
URL: https://tu-tienda.com/wp-json/wc/v3/products

Authorization:
  Type: Basic Auth
  Username: ck_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  Password: cs_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Pasos en Postman:**
1. Ve a la pestaña "Authorization"
2. Selecciona "Basic Auth" en el dropdown
3. En "Username" pega tu `WOOCOMMERCE_CONSUMER_KEY`
4. En "Password" pega tu `WOOCOMMERCE_CONSUMER_SECRET`
5. Click en "Send"

### Método 2: Query Parameters

```
Método: GET
URL: https://tu-tienda.com/wp-json/wc/v3/products?consumer_key=ck_xxx&consumer_secret=cs_xxx

Authorization: No Auth
```

**Pasos en Postman:**
1. Ve a la pestaña "Params"
2. Agrega:
   - Key: `consumer_key` → Value: tu consumer key
   - Key: `consumer_secret` → Value: tu consumer secret
3. Click en "Send"

---

## Colección de Postman

Puedes importar esta colección en Postman:

### Crear Collection:

1. Abre Postman
2. Click en "New" → "Collection"
3. Nombre: "WooCommerce Backend"

### Agregar requests:

**Request 1: Listar Productos**
```
GET http://localhost:5000/api/products
```

**Request 2: Obtener Producto**
```
GET http://localhost:5000/api/products/{{product_id}}
```

**Request 3: Crear Producto**
```
POST http://localhost:5000/api/products
Body:
{
  "name": "Producto Nuevo",
  "type": "simple",
  "regular_price": "29.99"
}
```

**Request 4: Listar Categorías**
```
GET http://localhost:5000/api/categories
```

**Request 5: Listar Pedidos**
```
GET http://localhost:5000/api/orders
```

**Request 6: Test de Conexión**
```
GET http://localhost:5000/api/test
```

---

## Variables de entorno en Postman (Opcional pero útil)

1. Click en el ícono de ojo (👁️) en la esquina superior derecha
2. Click en "Add" para crear un nuevo environment
3. Nombre: "Local Development"
4. Agrega variables:
   - `base_url`: `http://localhost:5000`
   - `wc_url`: `https://tu-tienda.com`
   - `consumer_key`: tu consumer key
   - `consumer_secret`: tu consumer secret

Luego usa en tus requests:
```
GET {{base_url}}/api/products
```

---

## Troubleshooting

### Error: "Could not get any response"
- Verifica que el servidor Flask esté corriendo
- Verifica que el puerto sea 5000
- Prueba con: `http://localhost:5000/health`

### Error 500: Internal Server Error
- Revisa la consola de Flask para ver el error específico
- Verifica que el archivo `.env` esté configurado correctamente

### Error: "Expecting value: line 1 column 1 (char 0)"
- Tu URL de WooCommerce es incorrecta
- Ejecuta: `python test_connection.py` para verificar

### Error 401: Unauthorized
- Las credenciales de WooCommerce son incorrectas
- Regenera las credenciales en WooCommerce

### Error 404: Not Found
- Verifica que el endpoint exista
- Para tu backend Flask: `/api/products`
- Para WooCommerce directo: `/wp-json/wc/v3/products`

---

## Ejemplos con respuestas

### Ejemplo exitoso:
```json
[
  {
    "id": 123,
    "name": "Camiseta",
    "slug": "camiseta",
    "price": "29.99",
    "regular_price": "29.99",
    "sale_price": "",
    "status": "publish",
    "stock_status": "instock"
  }
]
```

### Ejemplo de error:
```json
{
  "error": "Error 401: Invalid signature"
}
```
