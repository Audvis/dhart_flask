# WooCommerce Backend API

Backend Flask que actúa como proxy seguro entre tu aplicación Next.js y la API de WooCommerce. Este backend protege tus credenciales de WooCommerce al no exponerlas en el frontend.

## Características

- Proxy seguro para la API de WooCommerce
- Endpoints RESTful para productos, categorías, pedidos y clientes
- CORS configurado para trabajar con Next.js
- Variables de entorno para proteger credenciales
- Manejo de errores robusto
- Soporte para operaciones CRUD completas
- Operaciones en lote (batch)
- **Servidor MCP (Model Context Protocol)** para integración con asistentes de IA

## Estructura del Proyecto

```
dhart_backend/
├── app.py                  # Aplicación principal Flask
├── mcp_server.py           # Servidor MCP para asistentes de IA
├── config.py               # Configuración de la aplicación
├── requirements.txt        # Dependencias Python
├── .env.example           # Ejemplo de variables de entorno
├── .env.mcp.example       # Ejemplo de variables para MCP
├── .gitignore             # Archivos a ignorar en Git
├── MCP_README.md          # Documentación del servidor MCP
├── services/
│   ├── __init__.py
│   └── woocommerce.py     # Servicio de conexión a WooCommerce
├── routes/
│   ├── __init__.py
│   ├── products.py        # Endpoints de productos
│   ├── categories.py      # Endpoints de categorías
│   ├── orders.py          # Endpoints de pedidos
│   └── customers.py       # Endpoints de clientes
└── documentation/
    ├── DEPLOYMENT.md              # Guía de despliegue
    ├── POSTMAN_GUIDE.md           # Guía de Postman
    ├── TRANSFORMERS_GUIDE.md      # Guía de transformadores
    ├── TROUBLESHOOTING.md         # Solución de problemas
    └── INSTRUCCIONES_WINDOWS.md   # Instrucciones para Windows
```

## Instalación

### 1. Clonar o descargar el proyecto

```bash
cd dhart_backend
```

### 2. Crear un entorno virtual

```bash
python -m venv venv
```

### 3. Activar el entorno virtual

**En Linux/Mac:**
```bash
source venv/bin/activate
```

**En Windows:**
```bash
venv\Scripts\activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno

Copia el archivo `.env.example` a `.env` y configura tus credenciales:

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus datos:

```env
WOOCOMMERCE_URL=https://tu-tienda.com
WOOCOMMERCE_CONSUMER_KEY=ck_tu_consumer_key_aqui
WOOCOMMERCE_CONSUMER_SECRET=cs_tu_consumer_secret_aqui
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
SECRET_KEY=tu-clave-secreta-aqui
```

### 6. Obtener credenciales de WooCommerce

1. Ve a tu panel de WordPress
2. Navega a: **WooCommerce → Ajustes → Avanzado → REST API**
3. Haz clic en **Añadir clave**
4. Configura:
   - Descripción: "Backend Flask"
   - Usuario: Tu usuario administrador
   - Permisos: Lectura/Escritura
5. Copia el **Consumer Key** y **Consumer Secret**

## Uso

### Ejecutar el servidor en desarrollo

```bash
python app.py
```

El servidor estará disponible en: `http://localhost:5000`

### Ejecutar en producción

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Endpoints Disponibles

### Productos

- `GET /api/products` - Listar productos
- `GET /api/products/<id>` - Obtener producto por ID
- `POST /api/products` - Crear producto
- `PUT /api/products/<id>` - Actualizar producto
- `DELETE /api/products/<id>` - Eliminar producto
- `POST /api/products/batch` - Operaciones en lote

**Parámetros de consulta para GET /api/products:**
- `page` - Número de página (default: 1)
- `per_page` - Productos por página (default: 10)
- `search` - Búsqueda por nombre
- `category` - Filtrar por categoría
- `status` - Filtrar por estado (publish, draft, pending)
- `featured` - Filtrar por destacados (true/false)
- `on_sale` - Filtrar por en oferta (true/false)
- `min_price` - Precio mínimo
- `max_price` - Precio máximo
- `orderby` - Ordenar por (date, id, title, price)
- `order` - Orden (asc, desc)

### Categorías

- `GET /api/categories` - Listar categorías
- `GET /api/categories/<id>` - Obtener categoría por ID
- `POST /api/categories` - Crear categoría
- `PUT /api/categories/<id>` - Actualizar categoría
- `DELETE /api/categories/<id>` - Eliminar categoría
- `POST /api/categories/batch` - Operaciones en lote

### Pedidos

- `GET /api/orders` - Listar pedidos
- `GET /api/orders/<id>` - Obtener pedido por ID
- `POST /api/orders` - Crear pedido
- `PUT /api/orders/<id>` - Actualizar pedido
- `DELETE /api/orders/<id>` - Eliminar pedido
- `GET /api/orders/<id>/notes` - Obtener notas del pedido
- `POST /api/orders/<id>/notes` - Crear nota en el pedido
- `POST /api/orders/batch` - Operaciones en lote

**Parámetros de consulta para GET /api/orders:**
- `status` - Filtrar por estado (pending, processing, on-hold, completed, cancelled, refunded, failed)
- `customer` - Filtrar por ID de cliente
- `product` - Filtrar por ID de producto
- `after` - Pedidos después de esta fecha (ISO8601)
- `before` - Pedidos antes de esta fecha (ISO8601)

### Clientes

- `GET /api/customers` - Listar clientes
- `GET /api/customers/<id>` - Obtener cliente por ID
- `POST /api/customers` - Crear cliente
- `PUT /api/customers/<id>` - Actualizar cliente
- `DELETE /api/customers/<id>` - Eliminar cliente
- `GET /api/customers/<id>/downloads` - Obtener descargas del cliente
- `POST /api/customers/batch` - Operaciones en lote

## Uso con Next.js

### Ejemplo de llamada desde Next.js

```javascript
// lib/api.js
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

export async function getProducts(params = {}) {
  const queryString = new URLSearchParams(params).toString();
  const url = `${API_URL}/products${queryString ? `?${queryString}` : ''}`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error('Error al obtener productos');
  }

  return response.json();
}

export async function getProduct(id) {
  const response = await fetch(`${API_URL}/products/${id}`);

  if (!response.ok) {
    throw new Error('Error al obtener producto');
  }

  return response.json();
}

export async function createOrder(orderData) {
  const response = await fetch(`${API_URL}/orders`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(orderData),
  });

  if (!response.ok) {
    throw new Error('Error al crear pedido');
  }

  return response.json();
}
```

### Usar en un componente

```javascript
// app/products/page.js
'use client';

import { useEffect, useState } from 'react';
import { getProducts } from '@/lib/api';

export default function ProductsPage() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchProducts() {
      try {
        const data = await getProducts({ per_page: 20, status: 'publish' });
        setProducts(data);
      } catch (error) {
        console.error('Error:', error);
      } finally {
        setLoading(false);
      }
    }

    fetchProducts();
  }, []);

  if (loading) return <div>Cargando...</div>;

  return (
    <div>
      <h1>Productos</h1>
      <div className="grid grid-cols-3 gap-4">
        {products.map((product) => (
          <div key={product.id}>
            <h2>{product.name}</h2>
            <p>{product.price}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Variables de Entorno en Next.js

Crea un archivo `.env.local` en tu proyecto Next.js:

```env
NEXT_PUBLIC_API_URL=http://localhost:5000/api
```

## Servidor MCP (Model Context Protocol)

Este backend incluye un servidor MCP que permite a asistentes de IA como Claude interactuar con tu tienda WooCommerce de forma segura.

### ¿Qué es MCP?

MCP (Model Context Protocol) es un protocolo estándar que permite a los asistentes de IA conectarse con herramientas y servicios externos. Con el servidor MCP de este backend, puedes:

- Listar y buscar productos con lenguaje natural
- Crear y actualizar productos sin escribir código
- Gestionar pedidos y clientes conversacionalmente
- Automatizar tareas de tu tienda con IA

### Características del Servidor MCP

- **25+ herramientas** para productos, categorías, pedidos y clientes
- Soporte completo para operaciones CRUD
- Filtrado avanzado y búsqueda
- Recursos para verificar salud y configuración del backend
- Integración directa con Claude Desktop y otros clientes MCP

### Inicio Rápido con MCP

1. Instala las dependencias del MCP:
```bash
pip install -r requirements.txt
```

2. Configura tu archivo `.env` con `BACKEND_URL`:
```bash
BACKEND_URL=http://localhost:5000
```

3. Ejecuta el servidor MCP:
```bash
python mcp_server.py
```

4. **Para usar con Claude Desktop**, agrega esta configuración a tu `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "dhart-backend": {
      "command": "python",
      "args": ["/ruta/absoluta/a/mcp_server.py"],
      "env": {
        "BACKEND_URL": "http://localhost:5000"
      }
    }
  }
}
```

### Documentación Completa del MCP

Para más información sobre cómo usar el servidor MCP, consulta **[MCP_README.md](./MCP_README.md)** que incluye:

- Lista completa de herramientas disponibles
- Ejemplos de uso con asistentes de IA
- Configuración avanzada
- Solución de problemas del MCP

## Seguridad

- Las credenciales de WooCommerce NUNCA se exponen al frontend
- CORS está configurado para permitir solo orígenes específicos
- En producción, usa HTTPS
- Cambia la `SECRET_KEY` en producción
- Considera agregar autenticación JWT o API keys para proteger los endpoints

## Despliegue

### En un VPS (Linux)

1. Instala dependencias del sistema:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx
```

2. Clona o sube tu proyecto al servidor

3. Configura el servicio systemd:

Crea `/etc/systemd/system/dhart-backend.service`:

```ini
[Unit]
Description=DHart Backend
After=network.target

[Service]
User=tu-usuario
WorkingDirectory=/ruta/a/dhart_backend
Environment="PATH=/ruta/a/dhart_backend/venv/bin"
ExecStart=/ruta/a/dhart_backend/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

4. Inicia el servicio:
```bash
sudo systemctl enable dhart-backend
sudo systemctl start dhart-backend
```

5. Configura Nginx como proxy inverso:

Crea `/etc/nginx/sites-available/dhart-backend`:

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

6. Habilita el sitio:
```bash
sudo ln -s /etc/nginx/sites-available/dhart-backend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Solución de Problemas

### Error: "Faltan las siguientes variables de entorno"

Asegúrate de que el archivo `.env` existe y contiene todas las variables requeridas.

### Error de CORS

Verifica que el origen de tu aplicación Next.js esté en la variable `ALLOWED_ORIGINS` del archivo `.env`.

### Error de conexión a WooCommerce

Verifica que:
1. La URL de WooCommerce sea correcta (sin barra al final)
2. Las credenciales sean válidas
3. Tu tienda WooCommerce esté accesible desde el servidor

## Licencia

MIT

## Soporte

Para problemas o preguntas, crea un issue en el repositorio del proyecto.
#   d h a r t _ f l a s k  
 