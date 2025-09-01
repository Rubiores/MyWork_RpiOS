import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import RPi.GPIO as GPIO
import time

# Pines del DRV8833
IN1 = 17  # Motor A
IN2 = 27
IN3 = 5   # Motor B
IN4 = 6

# Configuracion de PWM
PWM_FREQ = 1000

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

pwm_A1 = GPIO.PWM(IN1, PWM_FREQ)
pwm_A2 = GPIO.PWM(IN2, PWM_FREQ)
pwm_B1 = GPIO.PWM(IN3, PWM_FREQ)
pwm_B2 = GPIO.PWM(IN4, PWM_FREQ)

pwm_A1.start(0)
pwm_A2.start(0)
pwm_B1.start(0)
pwm_B2.start(0)

class MotorDriver(Node):
    def __init__(self):
        super().__init__('motor_driver')
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )

    def set_motor(self, left_speed, right_speed):
        # Control de motor izquierdo
        if left_speed >= 0:
            pwm_A1.ChangeDutyCycle(left_speed * 100)
            pwm_A2.ChangeDutyCycle(0)
        else:
            pwm_A1.ChangeDutyCycle(0)
            pwm_A2.ChangeDutyCycle(-left_speed * 100)

        # Control de motor derecho
        if right_speed >= 0:
            pwm_B1.ChangeDutyCycle(right_speed * 100)
            pwm_B2.ChangeDutyCycle(0)
        else:
            pwm_B1.ChangeDutyCycle(0)
            pwm_B2.ChangeDutyCycle(-right_speed * 100)

    def cmd_vel_callback(self, msg):
        linear = msg.linear.x      # Movimiento hacia adelante
        angular = msg.angular.z    # Giro izquierda/derecha

        # Algoritmo simple: mezcla diferencial
        left_speed = linear - angular
        right_speed = linear + angular

        # Clip [-1, 1]
        left_speed = max(min(left_speed, 1.0), -1.0)
        right_speed = max(min(right_speed, 1.0), -1.0)

        self.get_logger().info(f'Motores L:{left_speed:.2f} R:{right_speed:.2f}')
        self.set_motor(left_speed, right_speed)

def main(args=None):
    rclpy.init(args=args)
    node = MotorDriver()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        pwm_A1.stop()
        pwm_A2.stop()
        pwm_B1.stop()
        pwm_B2.stop()
        GPIO.cleanup()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
