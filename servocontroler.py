from gpiozero import AngularServo
from time import sleep

class ServoController:
    def __init__(self, pin_servo1=17, pin_servo2=27, pin_servo3=22):
        # Inicializa los servos con los pines especificados
        self.servo1 = AngularServo(pin_servo1, min_angle=-90, max_angle=90)
        self.servo2 = AngularServo(pin_servo2, min_angle=-90, max_angle=90)
        self.servo3 = AngularServo(pin_servo3, min_angle=-90, max_angle=90)

    def move_servo(self, servo, angle):
        """Mueve un servo a un ángulo específico."""
        if servo == 1:
            self.servo1.angle = angle
        elif servo == 2:
            self.servo2.angle = angle
        elif servo == 3:
            self.servo3.angle = angle
        else:
            raise ValueError("Servo no válido. Usa 1, 2 o 3.")

    def move_all_servos(self, angle1, angle2, angle3):
        """Mueve todos los servos a ángulos específicos."""
        self.move_servo(1, angle1)
        self.move_servo(2, angle2)
        self.move_servo(3, angle3)

    def sweep_servos(self):
        """Realiza un barrido de 0 a 180 grados en todos los servos."""
        for angle in range(-90, 91, 10):
            self.move_all_servos(angle, angle, angle)
            sleep(0.5)

    def detach_servos(self):
        """Desconecta los servos para liberar los pines GPIO."""
        self.servo1.detach()
        self.servo2.detach()
        self.servo3.detach()

# Ejemplo de uso
if __name__ == "__main__":
    controller = ServoController()

    try:
        # Mueve todos los servos a 0 grados
        controller.move_all_servos(0, 0, 0)
        sleep(1)

        # Realiza un barrido de 0 a 180 grados
        controller.sweep_servos()

        # Mueve los servos a posiciones específicas
        controller.move_servo(1, 45)
        controller.move_servo(2, -30)
        controller.move_servo(3, 60)
        sleep(1)

    finally:
        # Desconecta los servos al finalizar
        controller.detach_servos()
