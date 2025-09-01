import RPi.GPIO as GPIO
import time

# === Pines DRV8833 (Motor 1 y Motor 2) ===
IN1 = 17  # Motor 1 A
IN2 = 27  # Motor 1 B
IN3 = 5   # Motor 2 A
IN4 = 6   # Motor 2 B

# === Pines de los encoders ===
ENC_A1 = 23
ENC_B1 = 24
ENC_A2 = 25
ENC_B2 = 16

# Contadores de pulsos
contador1 = 0
contador2 = 0

# === Callbacks para los encoders ===
def encoder1_callback(channel):
    global contador1
    if GPIO.input(ENC_B1):
        contador1 += 1
    else:
        contador1 -= 1

def encoder2_callback(channel):
    global contador2
    if GPIO.input(ENC_B2):
        contador2 += 1
    else:
        contador2 -= 1

# === Configuraci�n de GPIO ===
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motores
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Encoders
GPIO.setup(ENC_A1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ENC_B1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ENC_A2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ENC_B2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Interrupciones
GPIO.add_event_detect(ENC_A1, GPIO.RISING, callback=encoder1_callback)
GPIO.add_event_detect(ENC_A2, GPIO.RISING, callback=encoder2_callback)

try:
    # Mover ambos motores hacia adelante
    print("Motores girando adelante...")
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

    start_time = time.time()
    while time.time() - start_time < 5:  # girar por 5 segundos
        print("Pulsos Motor 1:", contador1, " | Pulsos Motor 2:", contador2)
        time.sleep(0.2)

    # Detener motores
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    print("Motores detenidos.")

except KeyboardInterrupt:
    print("Interrumpido por el usuario")

finally:
    GPIO.cleanup()
