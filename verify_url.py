"""
Script para verificar la URL de WooCommerce
Ejecuta: python verify_url.py
"""
import os
from dotenv import load_dotenv
import requests

load_dotenv()

wc_url = os.getenv('WOOCOMMERCE_URL')
consumer_key = os.getenv('WOOCOMMERCE_CONSUMER_KEY')
consumer_secret = os.getenv('WOOCOMMERCE_CONSUMER_SECRET')

print("=" * 60)
print("VERIFICACIÓN DE CONFIGURACIÓN DE WOOCOMMERCE")
print("=" * 60)

# Verificar que las variables existan
print(f"\n1. Variables de entorno cargadas:")
print(f"   WOOCOMMERCE_URL: {wc_url if wc_url else '❌ NO CONFIGURADA'}")
print(f"   CONSUMER_KEY: {'✓ Configurada' if consumer_key else '❌ NO CONFIGURADA'}")
print(f"   CONSUMER_SECRET: {'✓ Configurada' if consumer_secret else '❌ NO CONFIGURADA'}")

if not all([wc_url, consumer_key, consumer_secret]):
    print("\n⚠️  ERROR: Faltan variables de entorno en el archivo .env")
    exit(1)

# Probar diferentes URLs
print(f"\n2. Probando acceso a la tienda...")
print(f"   URL configurada: {wc_url}")

# Probar URL base
try:
    print(f"\n   Probando: {wc_url}")
    response = requests.get(wc_url, timeout=10, allow_redirects=False)
    print(f"   Status: {response.status_code}")

    if response.status_code in [301, 302, 303, 307, 308]:
        redirect_url = response.headers.get('Location', 'No especificada')
        print(f"   ⚠️  REDIRECCIÓN DETECTADA a: {redirect_url}")

    if 'text/html' in response.headers.get('Content-Type', ''):
        print(f"   ⚠️  Respuesta es HTML (debería ser JSON)")
        if 'lander' in response.text.lower():
            print(f"   ⚠️  Detectada página de landing/inicio")

except Exception as e:
    print(f"   ❌ Error: {e}")

# Probar endpoint de WooCommerce
print(f"\n3. Probando endpoint de WooCommerce API...")
api_urls = [
    f"{wc_url}/wp-json/wc/v3",
    f"{wc_url.rstrip('/')}/wp-json/wc/v3",
]

for url in api_urls:
    try:
        print(f"\n   Probando: {url}")
        response = requests.get(
            url,
            auth=(consumer_key, consumer_secret),
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type', 'No especificado')}")

        if response.status_code == 200:
            print(f"   ✓ CONEXIÓN EXITOSA!")
            try:
                data = response.json()
                print(f"   API encontrada con {len(data.get('routes', {}))} rutas")
                break
            except:
                pass
        elif response.status_code == 401:
            print(f"   ⚠️  Error 401: Credenciales incorrectas")
        elif response.status_code == 404:
            print(f"   ⚠️  Error 404: API no encontrada en esta URL")

        # Mostrar primeros 200 caracteres de la respuesta
        preview = response.text[:200]
        if preview:
            print(f"   Respuesta (primeros 200 chars):")
            print(f"   {preview}...")

    except Exception as e:
        print(f"   ❌ Error: {e}")

# Sugerencias
print(f"\n" + "=" * 60)
print("SUGERENCIAS:")
print("=" * 60)
print("""
1. Verifica que WOOCOMMERCE_URL sea la URL correcta de tu tienda
   - NO debe terminar con /
   - Debe ser algo como: https://mitienda.com
   - NO debe ser: https://mitienda.com/wp-admin o similar

2. Si ves "lander" o redirecciones:
   - Tu URL está apuntando a una página de inicio/landing
   - Verifica cuál es la URL real de tu tienda WooCommerce
   - Posiblemente necesites usar otra URL o subdominio

3. Prueba acceder manualmente en el navegador:
   {}/wp-json/wc/v3

   Deberías ver información JSON de la API, no una página HTML

4. Verifica que WooCommerce esté instalado y activado

5. Verifica los permalinks en WordPress:
   WordPress Admin → Ajustes → Enlaces permanentes
   Selecciona cualquier opción EXCEPTO "Simple"
""".format(wc_url))
