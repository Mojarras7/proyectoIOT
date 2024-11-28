import requests
import json

# Datos a enviar
data = {
    "codigo_barras": "123456789",
    "estado": "activo",
    "fecha_ultima_compra": "2024-11-01",
    "fecha_ultimo_uso": "2024-11-05",
    "peso": "1.2",
    "producto": "EjemploProducto"
}

# Configuración
repo_owner = "Mojarras7"   # Cambia esto por tu usuario de GitHub
repo_name = "mojarras7.github.io"
file_path = "data.json"
commit_message = "Actualización de datos"
token = "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"  # Reemplaza esto con tu token de acceso personal

# Obtener el contenido SHA del archivo actual
url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
headers = {"Authorization": f"token {token}"}
response = requests.get(url, headers=headers)
file_data = response.json()
sha = file_data["sha"]

# Codificar los nuevos datos a base64
new_content = json.dumps(data).encode("utf-8")
encoded_content = new_content.decode("utf-8")

# Enviar la actualización
update_data = {
    "message": commit_message,
    "content": encoded_content,
    "sha": sha
}
response = requests.put(url, headers=headers, data=json.dumps(update_data))

if response.status_code == 200:
    print("Archivo actualizado exitosamente.")
else:
    print("Error al actualizar el archivo:", response.json())
