import RPi.GPIO as GPIO
import time

# Pines DRV8833
IN1, IN2 = 17, 27
IN3, IN4 = 5, 6

# === Pines de los encoders ===
ENC_A1 = 23
ENC_B1 = 24
ENC_A2 = 25
ENC_B2 = 16

# Configuracion GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for p in (IN1, IN2, IN3, IN4):
    GPIO.setup(p, GPIO.OUT)

# PWM setup
FREQ = 1000  # Frecuencia en Hz
pwm_IN1 = GPIO.PWM(IN1, FREQ)
pwm_IN2 = GPIO.PWM(IN2, FREQ)
pwm_IN3 = GPIO.PWM(IN3, FREQ)
pwm_IN4 = GPIO.PWM(IN4, FREQ)
for pwm in (pwm_IN1, pwm_IN2, pwm_IN3, pwm_IN4):
    pwm.start(0)

duty_cycle = 50  # Duty cycle inicial

# Funciones de movimiento usando PWM
def adelante():
    pwm_IN1.ChangeDutyCycle(0)
    pwm_IN2.ChangeDutyCycle(duty_cycle)
    pwm_IN3.ChangeDutyCycle(duty_cycle)
    pwm_IN4.ChangeDutyCycle(0)

def atras():
    pwm_IN1.ChangeDutyCycle(duty_cycle)
    pwm_IN2.ChangeDutyCycle(0)
    pwm_IN3.ChangeDutyCycle(0)
    pwm_IN4.ChangeDutyCycle(duty_cycle)

def izquierda():
    pwm_IN1.ChangeDutyCycle(duty_cycle)
    pwm_IN2.ChangeDutyCycle(0)
    pwm_IN3.ChangeDutyCycle(duty_cycle)
    pwm_IN4.ChangeDutyCycle(0)

def derecha():
    pwm_IN1.ChangeDutyCycle(0)
    pwm_IN2.ChangeDutyCycle(duty_cycle)
    pwm_IN3.ChangeDutyCycle(0)
    pwm_IN4.ChangeDutyCycle(duty_cycle)

def detener():
    for pwm in (pwm_IN1, pwm_IN2, pwm_IN3, pwm_IN4):
        pwm.ChangeDutyCycle(0)

# Bucle principal de control
print("Comandos: adelante / atras / izquierda / derecha / detener / pwm <valor> / salir")
try:
    while True:
        cmd = input(">> ").strip().lower()
        if cmd == "adelante":
            adelante()
        elif cmd == "atras":
            atras()
        elif cmd == "izquierda":
            izquierda()
        elif cmd == "derecha":
            derecha()
        elif cmd == "detener":
            detener()
        elif cmd.startswith("pwm"):
            try:
                valor = int(cmd.split()[1])
                if 0 <= valor <= 100:
                    duty_cycle = valor
                    print(f"Duty cycle actualizado a {duty_cycle}%")
                else:
                    print("El valor debe estar entre 0 y 100.")
            except (IndexError, ValueError):
                print("Uso: pwm <valor>")
        elif cmd == "salir":
            detener()
            print("Saliendo...")
            break
        else:
            print("Comando no reconocido.")
except KeyboardInterrupt:
    print("\nInterrumpido por el usuario.")
finally:
    detener()
    for pwm in (pwm_IN1, pwm_IN2, pwm_IN3, pwm_IN4):
        pwm.stop()
    GPIO.cleanup()