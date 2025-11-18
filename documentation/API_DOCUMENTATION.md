# Documentación de la API - Backend WooCommerce

Este documento detalla los endpoints y procesos del backend Flask que actúa como proxy para la API de WooCommerce.

## Introducción

Este backend está diseñado para servir como una capa intermedia segura entre una aplicación de frontend (como una aplicación Next.js) y la API de WooCommerce. Su propósito principal es proteger las credenciales de la API de WooCommerce, evitando que se expongan en el lado del cliente. La aplicación maneja todas las solicitudes a WooCommerce, gestiona las credenciales de forma segura en el servidor y devuelve los datos al cliente.

## Arquitectura

La arquitectura de la aplicación se basa en varios componentes clave que trabajan juntos:

- **Aplicación Flask (`app.py`):** Es el punto de entrada principal de la aplicación. Se encarga de inicializar el servidor Flask, configurar CORS para permitir solicitudes desde orígenes autorizados y registrar los blueprints de las rutas.

- **Rutas (Blueprints):** La funcionalidad de la API está organizada en módulos utilizando Blueprints de Flask, uno para cada tipo de recurso (productos, categorías, pedidos y clientes). Cada blueprint define los endpoints específicos para ese recurso, gestionando las solicitudes HTTP y las respuestas.

- **Servicio de WooCommerce (`services/woocommerce.py`):** Este es el núcleo de la lógica de negocio. `WooCommerceService` es una clase singleton que gestiona la conexión con la API de WooCommerce. Se inicializa una única vez con las credenciales de la API y proporciona métodos (`get`, `post`, `put`, `delete`) para interactuar con WooCommerce. También incluye un manejo de errores robusto para gestionar problemas de conexión o respuestas de error de la API.

- **Configuración (`config.py`):** La configuración de la aplicación se gestiona de forma centralizada. `Config` carga las variables de entorno (como las credenciales de la API y la configuración del servidor) desde un archivo `.env`, lo que permite una configuración flexible y segura para diferentes entornos (desarrollo, producción, etc.).

- **Transformadores de Datos (`utils/transformers.py`):** Para optimizar el rendimiento y reducir el tamaño de las respuestas, la aplicación utiliza transformadores de datos. Estas funciones procesan los datos recibidos de WooCommerce para simplificar las estructuras (por ejemplo, en las imágenes de los productos) o para devolver un conjunto mínimo de campos, lo que resulta en respuestas más rápidas y ligeras para el cliente.

## Documentación de Endpoints

A continuación se detallan los endpoints disponibles en la API, agrupados por recurso.

### Productos (`/api/products`)

Endpoints para gestionar los productos de la tienda.

---

#### 1. Obtener la lista de productos

- **Método:** `GET`
- **Endpoint:** `/api/products`
- **Descripción:** Devuelve una lista paginada de productos.
- **Parámetros de consulta (Query Params):**
    - `page` (opcional): Número de página (por defecto: `1`).
    - `per_page` (opcional): Número de productos por página (por defecto: `10`).
    - `search` (opcional): Cadena de texto para buscar productos por nombre.
    - `category` (opcional): ID de la categoría para filtrar los productos.
    - `status` (opcional): Filtra por estado del producto (`publish`, `draft`, `pending`).
    - `featured` (opcional): Filtra productos destacados (`true` o `false`).
    - `on_sale` (opcional): Filtra productos en oferta (`true` o `false`).
    - `min_price` (opcional): Precio mínimo del producto.
    - `max_price` (opcional): Precio máximo del producto.
    - `orderby` (opcional): Campo por el que ordenar (`date`, `id`, `title`, `price`).
    - `order` (opcional): Orden de la lista (`asc` o `desc`).
    - `_fields` (opcional): Campos específicos a devolver, separados por comas (ej: `id,name,price`).
    - `all_fields` (opcional): Si es `true`, devuelve todos los campos de WooCommerce.
    - `raw` (opcional): Si es `true`, devuelve los datos sin ninguna transformación.
    - `minimal` (opcional): Si es `true`, devuelve una versión minimalista de los productos.

---

#### 2. Obtener un producto específico

- **Método:** `GET`
- **Endpoint:** `/api/products/<id>`
- **Descripción:** Devuelve los detalles de un producto específico por su ID.
- **Parámetros de URL:**
    - `id` (requerido): El ID del producto.
- **Parámetros de consulta (Query Params):**
    - `_fields`, `all_fields`, `raw`: Mismo uso que en la lista de productos.

---

#### 3. Crear un nuevo producto

- **Método:** `POST`
- **Endpoint:** `/api/products`
- **Descripción:** Crea un nuevo producto en la tienda.
- **Cuerpo de la solicitud (Request Body):**
    - Un objeto JSON con los datos del producto.
    - **Ejemplo mínimo:**
      ```json
      {
        "name": "Nuevo Producto de Prueba",
        "type": "simple",
        "regular_price": "25.00"
      }
      ```

---

#### 4. Actualizar un producto

- **Método:** `PUT`
- **Endpoint:** `/api/products/<id>`
- **Descripción:** Actualiza la información de un producto existente.
- **Parámetros de URL:**
    - `id` (requerido): El ID del producto a actualizar.
- **Cuerpo de la solicitud (Request Body):**
    - Un objeto JSON con los campos a actualizar.

---

#### 5. Eliminar un producto

- **Método:** `DELETE`
- **Endpoint:** `/api/products/<id>`
- **Descripción:** Elimina un producto. Por defecto, lo envía a la papelera.
- **Parámetros de URL:**
    - `id` (requerido): El ID del producto a eliminar.
- **Parámetros de consulta (Query Params):**
    - `force` (opcional): Si es `true`, el producto se elimina permanentemente.

---

#### 6. Operaciones en lote (Batch)

- **Método:** `POST`
- **Endpoint:** `/api/products/batch`
- **Descripción:** Permite crear, actualizar y eliminar múltiples productos en una sola solicitud.
- **Cuerpo de la solicitud (Request Body):**
    - Un objeto JSON que contiene arrays para `create`, `update` y `delete`.
    - **Ejemplo:**
      ```json
      {
        "create": [
          { "name": "Producto A" }
        ],
        "update": [
          { "id": 123, "regular_price": "19.99" }
        ],
        "delete": [ 456, 789 ]
      }
      ```

### Categorías (`/api/categories`)

Endpoints para gestionar las categorías de productos.

---

#### 1. Obtener la lista de categorías

- **Método:** `GET`
- **Endpoint:** `/api/categories`
- **Descripción:** Devuelve una lista de categorías de productos.
- **Parámetros de consulta (Query Params):**
    - `page`, `per_page`, `search`, `orderby`, `order`: Funcionamiento similar a los productos.
    - `parent` (opcional): Filtra por el ID de la categoría padre.
    - `hide_empty` (opcional): Si es `true`, oculta las categorías sin productos.
    - `raw` (opcional): Si es `true`, devuelve los datos completos en lugar de la versión simplificada (id, name, slug).

---

#### 2. Obtener una categoría específica

- **Método:** `GET`
- **Endpoint:** `/api/categories/<id>`
- **Descripción:** Devuelve los detalles de una categoría específica.
- **Parámetros de URL:**
    - `id` (requerido): El ID de la categoría.
- **Parámetros de consulta (Query Params):**
    - `raw`: Mismo uso que en la lista de categorías.

---

#### 3. Crear una nueva categoría

- **Método:** `POST`
- **Endpoint:** `/api/categories`
- **Descripción:** Crea una nueva categoría.
- **Cuerpo de la solicitud (Request Body):**
    - **Ejemplo:**
      ```json
      {
        "name": "Nueva Categoría"
      }
      ```

---

#### 4. Actualizar una categoría

- **Método:** `PUT`
- **Endpoint:** `/api/categories/<id>`
- **Descripción:** Actualiza una categoría existente.
- **Parámetros de URL:**
    - `id` (requerido): El ID de la categoría.
- **Cuerpo de la solicitud (Request Body):**
    - Un objeto JSON con los campos a actualizar.

---

#### 5. Eliminar una categoría

- **Método:** `DELETE`
- **Endpoint:** `/api/categories/<id>`
- **Descripción:** Elimina una categoría.
- **Parámetros de URL:**
    - `id` (requerido): El ID de la categoría.
- **Parámetros de consulta (Query Params):**
    - `force` (opcional): Si es `true`, se elimina permanentemente.

---

#### 6. Operaciones en lote (Batch)

- **Método:** `POST`
- **Endpoint:** `/api/categories/batch`
- **Descripción:** Realiza operaciones en lote para categorías.
- **Cuerpo de la solicitud (Request Body):**
    - Similar al endpoint de batch de productos, con arrays `create`, `update` y `delete`.

### Pedidos (`/api/orders`)

Endpoints para gestionar los pedidos de la tienda.

---

#### 1. Obtener la lista de pedidos

- **Método:** `GET`
- **Endpoint:** `/api/orders`
- **Descripción:** Devuelve una lista de pedidos.
- **Parámetros de consulta (Query Params):**
    - `page`, `per_page`, `search`, `orderby`, `order`: Funcionamiento similar a los productos.
    - `status` (opcional): Filtra por estado (`pending`, `processing`, `completed`, etc.).
    - `customer` (opcional): Filtra por ID de cliente.
    - `product` (opcional): Filtra por ID de producto incluido en el pedido.
    - `after` (opcional): Pedidos creados después de esta fecha (formato ISO8601).
    - `before` (opcional): Pedidos creados antes de esta fecha (formato ISO8601).

---

#### 2. Obtener un pedido específico

- **Método:** `GET`
- **Endpoint:** `/api/orders/<id>`
- **Descripción:** Devuelve los detalles de un pedido específico.
- **Parámetros de URL:**
    - `id` (requerido): El ID del pedido.

---

#### 3. Crear un nuevo pedido

- **Método:** `POST`
- **Endpoint:** `/api/orders`
- **Descripción:** Crea un nuevo pedido.
- **Cuerpo de la solicitud (Request Body):**
    - Un objeto JSON con los detalles del pedido, incluyendo `line_items`.

---

#### 4. Actualizar un pedido

- **Método:** `PUT`
- **Endpoint:** `/api/orders/<id>`
- **Descripción:** Actualiza un pedido existente (ej: cambiar estado).
- **Parámetros de URL:**
    - `id` (requerido): El ID del pedido.
- **Cuerpo de la solicitud (Request Body):**
    - Un objeto JSON con los campos a actualizar.

---

#### 5. Eliminar un pedido

- **Método:** `DELETE`
- **Endpoint:** `/api/orders/<id>`
- **Descripción:** Elimina un pedido.
- **Parámetros de URL:**
    - `id` (requerido): El ID del pedido.
- **Parámetros de consulta (Query Params):**
    - `force` (opcional): Si es `true`, se elimina permanentemente.

---

#### 6. Obtener y crear notas de un pedido

- **Método:** `GET`, `POST`
- **Endpoint:** `/api/orders/<id>/notes`
- **Descripción:**
    - `GET`: Obtiene todas las notas de un pedido.
    - `POST`: Crea una nueva nota en un pedido.
- **Cuerpo de la solicitud (POST):**
    - **Ejemplo:**
      ```json
      {
        "note": "El cliente ha solicitado un cambio.",
        "customer_note": false
      }
      ```

---

#### 7. Operaciones en lote (Batch)

- **Método:** `POST`
- **Endpoint:** `/api/orders/batch`
- **Descripción:** Realiza operaciones en lote para pedidos.

### Clientes (`/api/customers`)

Endpoints para gestionar los clientes de la tienda.

---

#### 1. Obtener la lista de clientes

- **Método:** `GET`
- **Endpoint:** `/api/customers`
- **Descripción:** Devuelve una lista de clientes.
- **Parámetros de consulta (Query Params):**
    - `page`, `per_page`, `search`, `orderby`, `order`: Funcionamiento similar a los productos.
    - `email` (opcional): Filtra por email exacto.
    - `role` (opcional): Filtra por rol (`customer`, `subscriber`, etc.).

---

#### 2. Obtener un cliente específico

- **Método:** `GET`
- **Endpoint:** `/api/customers/<id>`
- **Descripción:** Devuelve los detalles de un cliente específico.
- **Parámetros de URL:**
    - `id` (requerido): El ID del cliente.

---

#### 3. Crear un nuevo cliente

- **Método:** `POST`
- **Endpoint:** `/api/customers`
- **Descripción:** Crea un nuevo cliente.
- **Cuerpo de la solicitud (Request Body):**
    - **Ejemplo:**
      ```json
      {
        "email": "nuevo.cliente@example.com",
        "first_name": "Juan",
        "last_name": "Pérez"
      }
      ```

---

#### 4. Actualizar un cliente

- **Método:** `PUT`
- **Endpoint:** `/api/customers/<id>`
- **Descripción:** Actualiza un cliente existente.
- **Parámetros de URL:**
    - `id` (requerido): El ID del cliente.
- **Cuerpo de la solicitud (Request Body):**
    - Un objeto JSON con los campos a actualizar.

---

#### 5. Eliminar un cliente

- **Método:** `DELETE`
- **Endpoint:** `/api/customers/<id>`
- **Descripción:** Elimina un cliente.
- **Parámetros de URL:**
    - `id` (requerido): El ID del cliente.
- **Parámetros de consulta (Query Params):**
    - `force` (opcional): Si es `true`, se elimina permanentemente.
    - `reassign` (opcional): ID de usuario al que se le reasignarán los pedidos del cliente eliminado.

---

#### 6. Obtener descargas de un cliente

- **Método:** `GET`
- **Endpoint:** `/api/customers/<id>/downloads`
- **Descripción:** Devuelve las descargas disponibles para un cliente.
- **Parámetros de URL:**
    - `id` (requerido): El ID del cliente.

---

#### 7. Operaciones en lote (Batch)

- **Método:** `POST`
- **Endpoint:** `/api/customers/batch`
- **Descripción:** Realiza operaciones en lote para clientes.

### Endpoints de Utilidad y Diagnóstico

Estos endpoints proporcionan información sobre el estado y la configuración del servidor.

---

#### 1. Endpoint Raíz

- **Método:** `GET`
- **Endpoint:** `/`
- **Descripción:** Muestra un mensaje de bienvenida y una lista de los principales endpoints de la API.

---

#### 2. Health Check

- **Método:** `GET`
- **Endpoint:** `/health`
- **Descripción:** Realiza una comprobación básica del estado del servidor. Devuelve el estado de salud y si el servicio de WooCommerce está configurado.
- **Respuesta de ejemplo:**
  ```json
  {
    "status": "healthy",
    "env": "development",
    "woocommerce_configured": true
  }
  ```

---

#### 3. Verificación de Configuración

- **Método:** `GET`
- **Endpoint:** `/api/config`
- **Descripción:** Devuelve el estado de la configuración del entorno, indicando qué variables se han establecido. No expone valores sensibles.
- **Respuesta de ejemplo:**
  ```json
  {
    "flask_env": "development",
    "woocommerce_url": "https://tu-tienda.com",
    "consumer_key_set": true,
    "consumer_secret_set": true,
    "allowed_origins": "http://localhost:3000",
    "woocommerce_service_initialized": true
  }
  ```

---

#### 4. Test de Conexión con WooCommerce

- **Método:** `GET`
- **Endpoint:** `/api/test`
- **Descripción:** Realiza una prueba de conexión activa con la API de WooCommerce para verificar si las credenciales y la URL son correctas.
- **Respuesta de ejemplo (éxito):**
  ```json
  {
    "success": true,
    "message": "Conexión exitosa con WooCommerce",
    "store_info": { ... }
  }
  ```
- **Respuesta de ejemplo (error):**
  ```json
  {
    "success": false,
    "error": "Error de conexión: ...",
    "message": "No se pudo conectar con WooCommerce."
  }
  ```

## Procesos Adicionales

### Transformación de Datos

Para mejorar el rendimiento y la eficiencia, la API realiza transformaciones en los datos devueltos por WooCommerce.

- **Comportamiento por defecto:** Por defecto, la API devuelve una versión optimizada de los datos. Por ejemplo, en el endpoint de productos, solo se devuelven los campos más comunes (`id`, `name`, `price`, etc.) y la estructura de las imágenes se simplifica para reducir el tamaño de la respuesta. De manera similar, para las categorías, solo se devuelven `id`, `name` y `slug`.

- **Control de la transformación:** Puedes controlar cómo se devuelven los datos mediante los siguientes parámetros de consulta en los endpoints `GET`:
    - `raw=true`: Devuelve los datos originales de WooCommerce sin ninguna modificación.
    - `minimal=true`: Devuelve una versión aún más reducida de los datos, ideal para vistas de lista con información básica.
    - `all_fields=true`: Solicita todos los campos disponibles de la API de WooCommerce, en lugar del subconjunto predeterminado.
    - `_fields=<campos>`: Permite especificar exactamente qué campos se desean, separados por comas.

Este enfoque permite adaptar la respuesta de la API a las necesidades específicas del cliente, solicitando solo la información necesaria y mejorando así los tiempos de carga y la experiencia del usuario.
