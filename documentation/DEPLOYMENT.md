# Guía de Deployment con Dokploy

## Archivos de configuración creados

- `Procfile` - Define el comando de inicio para Heroku-style deployments
- `nixpacks.toml` - Configuración específica para Nixpacks (Dokploy)
- `start.sh` - Script alternativo de inicio
- `requirements.txt` - Dependencias Python

## Pasos para deployment en Dokploy

### 1. Configurar Variables de Entorno

En la configuración de tu aplicación en Dokploy, agrega las siguientes variables de entorno:

```env
# WooCommerce API Credentials
WOOCOMMERCE_URL=https://backend.dhart1111.com
WOOCOMMERCE_CONSUMER_KEY=ck_effe293765d3d08415285fa188e0861ca831245c
WOOCOMMERCE_CONSUMER_SECRET=cs_442bc44aa467fd1846a1975f3788dce4a4b0837f

# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0

# Puerto (Dokploy lo asigna automáticamente)
PORT=5000

# CORS - Orígenes permitidos
ALLOWED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com

# Security
SECRET_KEY=tu-clave-secreta-super-segura-aqui
```

**IMPORTANTE:**
- NO incluyas `/wp-json/wc/v3` en `WOOCOMMERCE_URL`
- Cambia `SECRET_KEY` por una clave aleatoria y segura
- Actualiza `ALLOWED_ORIGINS` con los dominios de tu frontend

### 2. Configuración del Repositorio

Si aún no has subido el código a GitHub:

```bash
# Inicializar git
git init

# Agregar archivos
git add .

# Crear commit
git commit -m "Initial commit - Flask WooCommerce Backend"

# Agregar remote (reemplaza con tu repo)
git remote add origin https://github.com/Audvis/dhart_flask.git

# Push
git push -u origin main
```

### 3. Deploy en Dokploy

1. **Crear nueva aplicación:**
   - Ve a tu panel de Dokploy
   - Click en "New Application"
   - Selecciona "GitHub" como source

2. **Conectar repositorio:**
   - Selecciona el repositorio: `Audvis/dhart_flask`
   - Branch: `main`

3. **Configurar build:**
   - Build Pack: **Nixpacks** (auto-detectado)
   - Dokploy usará `nixpacks.toml` automáticamente

4. **Variables de entorno:**
   - Click en "Environment Variables"
   - Agrega todas las variables listadas arriba

5. **Deploy:**
   - Click en "Deploy"
   - Espera a que termine el build

### 4. Verificar Deployment

Una vez completado el deployment, verifica:

```bash
# Health check
curl https://tu-app.dokploy.app/health

# Test endpoint
curl https://tu-app.dokploy.app/api/test

# Listar productos
curl https://tu-app.dokploy.app/api/products
```

## Troubleshooting

### Error: "No start command could be found"

**Solución:** Asegúrate de que estos archivos existan:
- ✅ `Procfile`
- ✅ `nixpacks.toml`
- ✅ `requirements.txt` con gunicorn

### Error: "Module not found"

**Solución:** Verifica que `requirements.txt` esté completo:
```bash
Flask==3.0.0
flask-cors==4.0.0
WooCommerce==3.0.0
python-dotenv==1.0.0
requests==2.31.0
gunicorn==21.2.0
```

### Error de conexión con WooCommerce

**Solución:** Verifica las variables de entorno:
- `WOOCOMMERCE_URL` debe ser solo el dominio base
- Las credenciales deben ser válidas
- Los permalinks de WordPress deben estar configurados

### CORS Error

**Solución:** Agrega el dominio de tu frontend a `ALLOWED_ORIGINS`:
```env
ALLOWED_ORIGINS=https://tu-frontend.com,https://www.tu-frontend.com
```

## Logs

Para ver los logs en Dokploy:
1. Ve a tu aplicación
2. Click en "Logs"
3. Selecciona "Application Logs"

## Actualizar la aplicación

Cuando hagas cambios:

```bash
git add .
git commit -m "Descripción del cambio"
git push
```

Dokploy auto-deployará automáticamente (si está configurado) o haz click en "Redeploy".

## Comandos útiles

### Ver estado
```bash
# En el servidor Dokploy
docker ps | grep dhart-backend
```

### Ver logs en tiempo real
```bash
docker logs -f dhart-backend-xxx
```

### Reiniciar aplicación
Desde el panel de Dokploy: Click en "Restart"

## Variables de Entorno Importantes

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `WOOCOMMERCE_URL` | URL base de WooCommerce | `https://backend.dhart1111.com` |
| `WOOCOMMERCE_CONSUMER_KEY` | Consumer Key de WooCommerce | `ck_xxx...` |
| `WOOCOMMERCE_CONSUMER_SECRET` | Consumer Secret de WooCommerce | `cs_xxx...` |
| `PORT` | Puerto de la aplicación | `5000` (auto-asignado) |
| `FLASK_ENV` | Entorno de Flask | `production` |
| `ALLOWED_ORIGINS` | Orígenes permitidos para CORS | `https://tuapp.com` |
| `SECRET_KEY` | Clave secreta de Flask | Una cadena aleatoria segura |

## Seguridad en Producción

✅ **Recomendaciones:**
- Usa HTTPS (Dokploy lo configura automáticamente)
- Cambia `SECRET_KEY` por una aleatoria
- Mantén `FLASK_DEBUG=False` en producción
- Actualiza `ALLOWED_ORIGINS` solo con tus dominios
- No expongas credenciales en logs

## Monitoreo

Dokploy proporciona:
- CPU usage
- Memory usage
- Request metrics
- Application logs

Accede a estas métricas desde el dashboard de tu aplicación.
