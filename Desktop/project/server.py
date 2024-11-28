import paho.mqtt.client as mqtt
import mysql.connector
import json

# Configuración de la base de datos
DB_CONFIG = {
    'host': '10.43.102.36',
    'user': 'root',
    'password': '',
    'database': 'productos'
}

# Configuración del broker
BROKER = "localhost"
TOPIC_CONTROL = "control/send_data"
TOPIC_DATA = "data/live_view"  # Tópico para enviar datos en tiempo real

# Variables globales
codigo_barras = "123"
peso = 10.0

def enviar_datos_a_db(codigo_barras, peso):
    """Función para insertar datos en la base de datos."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        sql = "INSERT INTO productos (product_name, codigo_barras, peso, status, date_added, date_updated) VALUES (NULL, %s, %s, NULL, NULL, NULL);"
        cursor.execute(sql, (codigo_barras, peso))
        conn.commit()
        print("Datos enviados a la base de datos.")
    except Exception as e:
        print(f"Error al enviar datos: {e}")
    finally:
        conn.close()

# Callback para recibir mensajes
def on_message(client, userdata, msg):
    global codigo_barras, peso

    if msg.topic == TOPIC_DATA:
        # Se reciben los datos en tiempo real
        datos = json.loads(msg.payload.decode())
        codigo_barras = datos["codigo_barras"]
        peso = datos["peso"]
        print(f"Datos recibidos: Código de Barras: {codigo_barras}, Peso: {peso} kg")

    elif msg.topic == TOPIC_CONTROL:
        # Se recibe la confirmación de la página web
        if codigo_barras and peso:
            print("Confirmación recibida. Guardando datos en la base de datos...")
            enviar_datos_a_db(codigo_barras, peso)
        else:
            print("No se han recibido datos válidos para guardar.")

# Configuración del cliente MQTT
client = mqtt.Client()
client.on_message = on_message

# Conectar al broker MQTT y suscribirse a los tópicos
client.connect(BROKER)
client.subscribe(TOPIC_DATA)  # Para recibir los datos en tiempo real
client.subscribe(TOPIC_CONTROL)  # Para recibir la confirmación

print("Escuchando mensajes...")
enviar_datos_a_db(codigo_barras, peso)
client.loop_forever()
