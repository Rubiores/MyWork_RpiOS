# control_robot.py
import sys
import RPi.GPIO as GPIO
import time

# Pines de control
IN1, IN2, IN3, IN4 = 17, 27, 5, 6

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup([IN1, IN2, IN3, IN4], GPIO.OUT)

def adelante():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def atras():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def izquierda():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def derecha():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def detener():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 control_robot.py [forward|backward|left|right|stop]")
        sys.exit(1)

    action = sys.argv[1]

    if action == "forward":
        adelante()
    elif action == "backward":
        atras()
    elif action == "left":
        izquierda()
    elif action == "right":
        derecha()
    else:
        detener()
