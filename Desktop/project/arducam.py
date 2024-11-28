import cv2
from pyzbar.pyzbar import decode

# Abre la cámara en /dev/video0
cap = cv2.VideoCapture(0)  # '0' corresponde a /dev/video0

if not cap.isOpened():
    print("No se pudo abrir la cámara en /dev/video0.")
    exit()

print("Cámara en /dev/video0 abierta correctamente. Presiona 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo capturar un cuadro.")
        break

    # Decodificar códigos de barras en el cuadro
    barcodes = decode(frame)
    for barcode in barcodes:
        # Decodifica el texto del código de barras
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type

        # Dibuja un rectángulo alrededor del código de barras
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Muestra el texto del código de barras en la ventana
        text = f"{barcode_data} ({barcode_type})"
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Imprime el resultado en la consola
        print(f"Detectado: {text}")

    # Mostrar el cuadro capturado
    cv2.imshow("Vista previa", frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
