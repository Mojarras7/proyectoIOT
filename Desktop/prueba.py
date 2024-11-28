import cx_Oracle
import datetime

# Configura la conexión
connection = cx_Oracle.connect("usuario", "contraseña", "host:puerto/nombre_bd")

# Datos del producto (por ejemplo, obtenidos mediante un escáner)
codigo_barras = "1234567890"
peso = 500  # peso en gramos

# Fecha y hora actuales
fecha_actual = datetime.datetime.now()

# Inserta los datos
try:
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO tu_tabla (codigo_barras, peso, fecha_ultima_compra, fecha_ultimo_uso)
        VALUES (:codigo_barras, :peso, :fecha_actual, :fecha_actual)
        """,
        codigo_barras=codigo_barras,
        peso=peso,
        fecha_actual=fecha_actual
    )
    connection.commit()
    print("Datos insertados correctamente.")
except cx_Oracle.DatabaseError as e:
    print("Error al insertar datos:", e)
finally:
    cursor.close()
    connection.close()
