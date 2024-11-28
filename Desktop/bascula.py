from hx711 import HX711
import RPi.GPIO as GPIO
import time

# Configuración de los pines GPIO
DT_PIN = 5  # Pin DATA del HX711
SCK_PIN = 6  # Pin CLOCK del HX711

def cleanAndExit():
    print("Limpiando...") 
    GPIO.cleanup()
    print("Saliendo...")
    exit()

def setup_scale():
    # Crear objeto HX711
    hx = HX711(DT_PIN, SCK_PIN)
    
    # Configurar factor de escala (ajusta según tu celda de carga)
    hx.set_scale(7050)  # Cambia este valor según tu celda de carga
    
    # Calibrar el offset (ajustar a cero)
    hx.tare()
    print("Offset ajustado.")
    
    return hx

def main():
    try:
        hx = setup_scale()
        while True:
            # Leer el peso
            val = hx.get_units(10)  # Promediar 10 lecturas para mayor estabilidad
            print(f"Peso: {val:.2f} g")
            time.sleep(1)
    except KeyboardInterrupt:
        cleanAndExit()

if __name__ == "__main__":
    main()
