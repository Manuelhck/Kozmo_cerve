import speech_recognition as sr
from gpiozero import AngularServo
from time import sleep
#from os import system
import pygame

# Inicializa el reconocimiento de voz
reconocedor = sr.Recognizer()

# Inicializa pygame para reproducir sonidos
pygame.mixer.init()

# Inicializa el servo en el pin GPIO 17 (ajusta el número de pin según tu configuración)
servo = AngularServo(9, min_angle=-120, max_angle=120)

def escuchar_palabras_clave():
    # Usa el micrófono como fuente de audio
    with sr.Microphone() as fuente:
        print("Ajustando al ruido ambiental, un momento...")
        reconocedor.adjust_for_ambient_noise(fuente)
        print("Listo, puedes hablar...")
        audio = reconocedor.listen(fuente)

        try:
            texto = reconocedor.recognize_google(audio, language="es-ES")
            print(f"Escuché: {texto}")
            return texto
        except sr.UnknownValueError:
            print("No pude entender lo que dijiste")
        except sr.RequestError:
            print("No se pudo conectar con el servicio de reconocimiento de voz")

    return ""

def mover_servo():
    pygame.mixer.music.load('./sound/aten.wav')
    pygame.mixer.music.play()
    servo.angle = 120
    sleep(1)

palabras_clave = {
    "hola": mover_servo,
    "adios": lambda: print("¡Adiós detectado!"),
    "encender": lambda: print("¡Encender detectado!"),
    "apagar": lambda: print("¡Apagar detectado!"),
}

while True:
    texto_escuchado = escuchar_palabras_clave()
    for palabra, accion in palabras_clave.items():
        if palabra in texto_escuchado.lower():
            accion()
