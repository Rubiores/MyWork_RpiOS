import cv2
import numpy as np
import RPi.GPIO as GPIO

# Pines GPIO para motores
IN1 = 5
IN2 = 6
IN3 = 12
IN4 = 16

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
    detener()

def avanzar():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    print("🔴 AVANZANDO")

def retroceder():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    print("🔵 RETROCEDIENDO")

def girar_derecha():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    print("🟢 GIRANDO DERECHA")

def girar_izquierda():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    print("⚫ GIRANDO IZQUIERDA")

def detener():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    print("⚪ DETENIDO")

def es_rojo(color_bgr):
    b, g, r = color_bgr
    pixel = np.uint8([[[b, g, r]]])
    hsv = cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)
    h = hsv[0][0][0]
    return (h >= 0 and h <= 10) or (h >= 160 and h <= 180)

def es_azul(color_bgr):
    b, g, r = color_bgr
    pixel = np.uint8([[[b, g, r]]])
    hsv = cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)
    h = hsv[0][0][0]
    return h >= 100 and h <= 130

def es_verde(color_bgr):
    b, g, r = color_bgr
    pixel = np.uint8([[[b, g, r]]])
    hsv = cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[0][0]
    return 35 <= h <= 85 and s > 50 and v > 50

def es_negro(color_bgr):
    b, g, r = color_bgr
    pixel = np.uint8([[[b, g, r]]])
    hsv = cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)
    _, s, v = hsv[0][0]
    return v < 50 and s < 50  # muy oscuro y poca saturación

def decidir_movimiento(color_bgr):
    if es_rojo(color_bgr):
        avanzar()
    elif es_azul(color_bgr):
        retroceder()
    elif es_verde(color_bgr):
        girar_derecha()
    elif es_negro(color_bgr):
        girar_izquierda()
    else:
        detener()

def detectar_color_promedio(frame, contour):
    mask = np.zeros(frame.shape[:2], dtype="uint8")
    cv2.drawContours(mask, [contour], -1, 255, -1)
    mean = cv2.mean(frame, mask=mask)[:3]  # BGR
    return mean

def main():
    setup_gpio()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ No se pudo acceder a la cámara.")
        return

    print("✅ Cámara activa. Pulsa 'q' para salir.")
    cv2.namedWindow("Detección de figuras", cv2.WINDOW_NORMAL)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (640, 480))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY)

            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            movimiento_decidido = False

            for cnt in contours:
                approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
                if len(approx) == 4 and cv2.contourArea(cnt) > 1000:
                    x, y, w, h = cv2.boundingRect(approx)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    color_bgr = detectar_color_promedio(frame, cnt)
                    decidir_movimiento(color_bgr)
                    movimiento_decidido = True

                    color_texto = f"Color BGR: ({int(color_bgr[0])}, {int(color_bgr[1])}, {int(color_bgr[2])})"
                    cv2.putText(frame, "Cuadrado", (x, y - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    cv2.putText(frame, color_texto, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

                    break  # Solo reacciona al primer cuadrado detectado

            if not movimiento_decidido:
                detener()

            cv2.imshow("Detección de figuras", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        detener()
        GPIO.cleanup()
        cap.release()
        cv2.destroyAllWindows()
        print("🛑 Cámara cerrada y GPIO limpiado.")

if __name__ == "__main__":
    main()
