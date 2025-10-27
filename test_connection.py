"""
Script para probar la conexión con WooCommerce
Ejecuta: python test_connection.py
"""
import os
from dotenv import load_dotenv
from woocommerce import API

load_dotenv()

print("=" * 60)
print("PROBANDO CONEXIÓN CON WOOCOMMERCE")
print("=" * 60)

# Cargar credenciales
url = os.getenv('WOOCOMMERCE_URL')
key = os.getenv('WOOCOMMERCE_CONSUMER_KEY')
secret = os.getenv('WOOCOMMERCE_CONSUMER_SECRET')

print(f"\nURL: {url}")
print(f"Consumer Key: {key[:20]}..." if key else "Consumer Key: NO CONFIGURADA")
print(f"Consumer Secret: {secret[:20]}..." if secret else "Consumer Secret: NO CONFIGURADA")

if not all([url, key, secret]):
    print("\n❌ ERROR: Faltan credenciales en el archivo .env")
    exit(1)

print("\n" + "-" * 60)
print("1. Probando conexión con la API de WooCommerce...")
print("-" * 60)

try:
    # Crear instancia de API
    wcapi = API(
        url=url,
        consumer_key=key,
        consumer_secret=secret,
        version="wc/v3",
        timeout=30
    )

    # Probar obtener productos
    print("\n→ Obteniendo productos...")
    response = wcapi.get("products", params={"per_page": 5})

    print(f"✓ Status Code: {response.status_code}")
    print(f"✓ Content-Type: {response.headers.get('Content-Type', 'N/A')}")

    if response.status_code == 200:
        try:
            data = response.json()
            print(f"✓ Productos encontrados: {len(data)}")

            if len(data) > 0:
                print(f"\n✓ Ejemplo de producto:")
                producto = data[0]
                print(f"  - ID: {producto.get('id')}")
                print(f"  - Nombre: {producto.get('name')}")
                print(f"  - Precio: {producto.get('price')}")
                print(f"  - Estado: {producto.get('status')}")

            print("\n" + "=" * 60)
            print("✓✓✓ CONEXIÓN EXITOSA ✓✓✓")
            print("=" * 60)
            print("\nTus credenciales son correctas.")
            print("Puedes usar Postman con tu backend Flask en:")
            print(f"  → http://localhost:5000/api/products")
            print("\nNo necesitas pasar credenciales en Postman,")
            print("el backend las maneja automáticamente.")

        except ValueError as e:
            print(f"\n❌ Error al parsear JSON: {e}")
            print(f"Respuesta: {response.text[:500]}")

    elif response.status_code == 401:
        print(f"\n❌ ERROR 401: Credenciales incorrectas")
        print("\nVerifica:")
        print("  1. Que el Consumer Key comience con 'ck_'")
        print("  2. Que el Consumer Secret comience con 'cs_'")
        print("  3. Que las credenciales sean correctas en WooCommerce")
        print("\nPara regenerar credenciales:")
        print("  WordPress → WooCommerce → Ajustes → Avanzado → REST API")

    elif response.status_code == 404:
        print(f"\n❌ ERROR 404: API no encontrada")
        print(f"\nLa URL parece incorrecta o WooCommerce no está instalado.")
        print(f"\nVerifica:")
        print(f"  1. URL correcta: {url}")
        print(f"  2. WooCommerce instalado y activado")
        print(f"  3. Permalinks configurados (no 'Simple')")
        print(f"\nPrueba acceder manualmente a:")
        print(f"  → {url}/wp-json/wc/v3")

    else:
        print(f"\n⚠️  Status Code inesperado: {response.status_code}")
        print(f"Respuesta: {response.text[:500]}")

except Exception as e:
    print(f"\n❌ ERROR DE CONEXIÓN: {e}")
    print("\nPosibles causas:")
    print("  1. URL incorrecta o no accesible")
    print("  2. Sin conexión a internet")
    print("  3. Firewall bloqueando la conexión")
    print("  4. La tienda está caída o en mantenimiento")

print("\n" + "=" * 60)
print("FIN DE LA PRUEBA")
print("=" * 60)
