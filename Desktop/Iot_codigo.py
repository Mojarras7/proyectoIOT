import requests
import json

# Datos a enviar
peso = 1.5  # Peso del producto, por ejemplo
codigo_barras = '12345'  # Código del producto
fecha_ultima_compra = 'CURRENT_TIMESTAMP'
fecha_ultimo_uso = 'CURRENT_TIMESTAMP'
estado = 'bien'


# URL del Web Service RESTful de APEX
url = 'hhttps://apex.oracle.com/pls/apex/iot_inventario_domestico/productos/peso/'

# Datos a enviar en formato JSON
data = {
    'codigo_barras': codigo_barras,
    'peso': peso,
    'fecha_ultima_compra' : fecha_ultima_compra,
    'fecha_ultimo_uso' : fecha_ultimo_uso,
    'estado' : estado
}

# Encabezados para la solicitud (si es necesario, agrega autenticación)
headers = {
    'Content-Type': 'application/json' 
}

# Realizar la solicitud POST
response = requests.post(url, data=json.dumps(data), headers=headers)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    print("Datos enviados correctamente.")
else:
    print(f"Error al enviar datos: {response.status_code}, {response.text}")
