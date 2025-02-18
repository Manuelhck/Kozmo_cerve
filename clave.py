import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306  # Importar correctamente ssd1306
from PIL import Image
import speech_recognition as sr
from gpiozero import AngularServo, Servo
from time import sleep
from gpiozero import Robot
import pygame
pygame.init()
robot = Robot((23, 24), (27, 17))
serial = i2c(port=1, address=0x3C)  # Ajusta el puerto y la dirección I2C según tu configuración
device = ssd1306(serial, width=128, height=64)
gif_path = "./animacion/normal.gif"  # Cambia esto por la ruta de tu archivo GIF
gif = Image.open(gif_path)


# Configuración del servo
SERVOC_PIN = 9  # Pin GPIO donde está conectado el servo
servoCabeza = AngularServo(SERVOC_PIN, min_angle= -120, max_angle=120)  # Configura el servo
servoI = Servo(12)
servoD = Servo(13)
servoI.min()
servoD.max()
sleep(2)
servoI.value =None;
servoD.value =None;

# Ruta al archivo de sonido
SONIDO_WAV =pygame.mixer.Sound("./sound/aten.wav")  # Camba esto por la ruta de tu archivo .wav

# Crear un reconocedor de voz
recognizer = sr.Recognizer()

# Usar el micrófono como fuente de audio
with sr.Microphone() as source:
    print("Di 'hola cosmo' para mover el servo y reproducir sonido...")
    
    # Ajustar el reconocedor al ruido ambiental
    recognizer.adjust_for_ambient_noise(source)
    
    while True:
        print("Escuchando...")
        
        # Escuchar la entrada de audio
        audio = recognizer.listen(source)

        try:
            # Reconocer el audio usando Google Speech Recognition
            texto = recognizer.recognize_google(audio, language="es-ES")
            print("Has dicho: " + texto)
            
            # Verificar si se dijo "hola cosmo"
            if "hola cosmo" in texto.lower():
                print("¡Frase detectada! Moviendo el servo y reproduciendo sonido...")
                
                # Mover el servo a 90 grados
                servoCabeza.angle = 120
                SONIDO_WAV.play()  # Reproducir el sonido
                sleep(2)  # Esperar 2 segundos
                
                # Volver el servo a 0 grados
                servoCabeza.angle = 90
        
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
        
        except sr.RequestError as e:
            print(f"Error al solicitar resultados; {e}")
