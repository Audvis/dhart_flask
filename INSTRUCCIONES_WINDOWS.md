# Instrucciones para Windows PowerShell

## Pasos rápidos para levantar la aplicación

### 1. Abrir PowerShell en este directorio

Abre PowerShell en la carpeta del proyecto:
```powershell
cd C:\Users\USER\Documents\VPS\dhart_backend
```

### 2. Permitir ejecución de scripts (solo primera vez)

Si es la primera vez que ejecutas scripts de PowerShell, necesitas habilitar la ejecución:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Ejecutar setup (solo primera vez)

```powershell
.\setup.ps1
```

Este script:
- Verifica que Python esté instalado
- Crea el entorno virtual
- Instala todas las dependencias

### 4. Configurar credenciales

Edita el archivo `.env` (se crea automáticamente) con tus credenciales de WooCommerce:

```env
WOOCOMMERCE_URL=https://tu-tienda.com
WOOCOMMERCE_CONSUMER_KEY=ck_tu_consumer_key_aqui
WOOCOMMERCE_CONSUMER_SECRET=cs_tu_consumer_secret_aqui
```

### 5. Iniciar el servidor

```powershell
.\start.ps1
```

El servidor estará disponible en: `http://localhost:5000`

---

## Comandos manuales (alternativa)

Si prefieres hacerlo manualmente:

### Crear entorno virtual
```powershell
python -m venv venv
```

### Activar entorno virtual
```powershell
.\venv\Scripts\Activate.ps1
```

### Instalar dependencias
```powershell
pip install -r requirements.txt
```

### Copiar archivo de configuración
```powershell
Copy-Item .env.example .env
```

Luego edita `.env` con tus credenciales.

### Ejecutar la aplicación
```powershell
python app.py
```

---

## Solución de problemas

### Error: "no se puede cargar el archivo ... porque la ejecución de scripts está deshabilitada"

Ejecuta:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Python no se reconoce como comando

Instala Python desde: https://www.python.org/downloads/

Asegúrate de marcar "Add Python to PATH" durante la instalación.

### Error de módulo no encontrado

Asegúrate de tener el entorno virtual activado:
```powershell
.\venv\Scripts\Activate.ps1
```

Luego reinstala las dependencias:
```powershell
pip install -r requirements.txt
```

---

## Detener el servidor

Presiona `Ctrl + C` en la terminal donde está corriendo el servidor.

---

## Desactivar entorno virtual

Cuando termines de trabajar:
```powershell
deactivate
```
