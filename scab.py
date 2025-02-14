
from gpiozero import AngularServo
from time import sleep

servo = AngularServo(9, min_angle=-120, max_angle=120)

while True:
    servo.angle = 120
    sleep(2)
    servo.angle = -100

    sleep(2)
