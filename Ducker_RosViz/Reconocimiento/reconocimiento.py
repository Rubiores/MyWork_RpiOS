import cv2
import numpy as np
from gpiozero import Motor
from time import sleep

# === Pines GPIO para motores ===
motor_izq = Motor(forward=16, backward=12)
motor_der = Motor(forward=6, backward=5)

# === Rangos HSV ===
# Rojo (para avanzar)
lower_red = np.array([0, 120, 70])
upper_red = np.array([10, 255, 255])

# Negro (para retroceder): tiene baja saturación y valor
lower_black = np.array([0, 0, 0])
upper_black = np.array([180, 255, 50])  # Valor máximo bajo

# === Inicia la cámara ===
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("No se pudo abrir la cámara")
    exit()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (320, 240))
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Máscaras de colores
        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        mask_black = cv2.inRange(hsv, lower_black, upper_black)

        detecta_negro = cv2.countNonZero(mask_red) > 500
        detecta_rojo = cv2.countNonZero(mask_black) > 500

        if detecta_rojo:
            print("Negro detectado → ADELANTAR")
            motor_izq.forward()
            motor_der.forward()
        elif detecta_negro:
            print("Rojo detectado → RETROCEDER")
            motor_izq.backward()
            motor_der.backward()
        else:
            print("Nada detectado → DETENER")
            motor_izq.stop()
            motor_der.stop()

        # Mostrar cámaras
        cv2.imshow("Camara", frame)
        cv2.imshow("Mascara Rojo", mask_red)
        cv2.imshow("Mascara Negro", mask_black)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    motor_izq.stop()
    motor_der.stop()
    cap.release()
    cv2.destroyAllWindows()
