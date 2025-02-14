from gpiozero import InputDevice
from time import sleep

# Initialize the sensor as a digital input device on GPIO 17
#sensorI = InputDevice(5)
sensorD = InputDevice(0) #en reslidad sersord
while True:
   if sensorD.is_active: #  or sensorD.is_active:
      print("No obstacle detected")  # Prints when no obstacle is detected
   else:
      print("Obstacle detected")     # Prints when an obstacle is detected
   sleep(0.5)
