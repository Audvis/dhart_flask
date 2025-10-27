# Solución de Problemas

## Error: "Expecting value: line 1 column 1 (char 0)"

Este error ocurre cuando la API de WooCommerce devuelve una respuesta vacía o no válida.

### Causas comunes:

1. **URL de WooCommerce incorrecta**
   - Verifica que la URL en `.env` sea correcta
   - No debe terminar con `/`
   - Debe incluir `https://` o `http://`
   - Ejemplo correcto: `https://tu-tienda.com`
   - Ejemplo incorrecto: `https://tu-tienda.com/`

2. **Credenciales incorrectas**
   - Verifica que `WOOCOMMERCE_CONSUMER_KEY` y `WOOCOMMERCE_CONSUMER_SECRET` sean correctos
   - Deben empezar con `ck_` y `cs_` respectivamente

3. **WooCommerce no está instalado o activado**
   - Asegúrate de que WooCommerce esté instalado y activado en tu WordPress

4. **Permalinks no configurados**
   - Ve a WordPress: Ajustes → Enlaces permanentes
   - Selecciona cualquier opción excepto "Simple"
   - Guarda los cambios

5. **SSL/HTTPS**
   - Si tu sitio usa HTTPS, asegúrate de que el certificado SSL sea válido

### Cómo diagnosticar:

1. **Prueba el endpoint de diagnóstico:**
```bash
# Con el servidor corriendo
curl http://localhost:5000/api/test
```

Esto te dará información específica sobre el error.

2. **Verifica tus credenciales en WooCommerce:**
   - Ve a: WooCommerce → Ajustes → Avanzado → REST API
   - Verifica que las credenciales existan y tengan permisos de Lectura/Escritura

3. **Prueba la conexión directa desde el navegador:**
```
https://tu-tienda.com/wp-json/wc/v3/products?consumer_key=ck_xxx&consumer_secret=cs_xxx
```

Reemplaza `tu-tienda.com` y las credenciales con tus valores.

## Error de CORS

### Síntoma:
```
Access to fetch at 'http://localhost:5000/api/products' from origin 'http://localhost:3000'
has been blocked by CORS policy
```

### Solución:
Agrega el origen de tu aplicación Next.js en el archivo `.env`:

```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001,https://tu-dominio.com
```

## Error: "Faltan las siguientes variables de entorno"

### Solución:
1. Verifica que exista el archivo `.env` en la raíz del proyecto
2. Asegúrate de que contenga todas las variables requeridas:
   - `WOOCOMMERCE_URL`
   - `WOOCOMMERCE_CONSUMER_KEY`
   - `WOOCOMMERCE_CONSUMER_SECRET`

## Error 401: Unauthorized

### Causas:
- Credenciales incorrectas
- Usuario sin permisos suficientes
- Claves expiradas o eliminadas

### Solución:
1. Regenera las credenciales en WooCommerce
2. Actualiza el archivo `.env` con las nuevas credenciales
3. Reinicia el servidor Flask

## Error 404: Not Found

### Causas:
- El endpoint de WooCommerce no existe
- URL base incorrecta
- WordPress no está accesible

### Solución:
1. Verifica que tu sitio WordPress esté accesible
2. Prueba acceder a: `https://tu-tienda.com/wp-json/wc/v3`
3. Deberías ver información sobre la API

## Error de Timeout

### Síntoma:
El servidor tarda mucho y finalmente falla con timeout.

### Solución:
1. Verifica tu conexión a internet
2. Verifica que el sitio WooCommerce esté funcionando
3. Aumenta el timeout en `services/woocommerce.py` línea 24:
```python
timeout=60  # Aumentar de 30 a 60 segundos
```

## Verificar configuración

Puedes verificar tu configuración con estos pasos:

### 1. Verificar Python y dependencias
```powershell
python --version
pip list | findstr Flask
pip list | findstr WooCommerce
```

### 2. Verificar archivo .env
```powershell
Get-Content .env
```

### 3. Probar conexión con WooCommerce
```powershell
# Inicia el servidor
python app.py

# En otra terminal
curl http://localhost:5000/api/test
```

## Logs y Debug

Para obtener más información sobre errores, el servidor mostrará mensajes detallados en la consola cuando `FLASK_DEBUG=True` esté configurado en `.env`.

Los errores ahora incluyen:
- Código de estado HTTP
- Mensaje de error específico
- Primeros 200 caracteres de la respuesta si hay error de parseo JSON

## Contacto

Si el problema persiste después de seguir estos pasos, verifica:
1. Los logs del servidor Flask en la consola
2. Los logs de errores de WordPress (si tienes acceso)
3. Que no haya un firewall bloqueando las conexiones
