from gpiozero import DistanceSensor
from time import sleep

class DistanceSensorManager:
    def __init__(self, echo_pin, trigger_pin):
        self.sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin)

    def get_distance(self):
        # Devuelve la distancia en metros
        return self.sensor.distance

    def cleanup(self):
        # Limpia los recursos del sensor
        self.sensor.close()
