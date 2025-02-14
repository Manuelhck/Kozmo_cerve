import speech_recognition as sr
from os import system
from gpiozero import AngularServo
from time import sleep

servo = AngularServo(9, min_angle=-120, max_angle=120)
# Crear un reconocedor
recognizer = sr.Recognizer()

# Palabra clave a detectar
PALABRA_CLAVE = "oye cosmo"

# Usar el micrófono como fuente de audio
with sr.Microphone() as source:
    print("Escuchando...")
    while True:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="es-ES")
            print("Has dicho: " + text)

            if PALABRA_CLAVE.lower() in text.lower():
                print(f"¡Palabra clave '{PALABRA_CLAVE}' detectada!")
                servo.angle = 120
                system("aplay ./sound/aten.wav")
                sleep(2)
                break  # Salir del bucle si se detecta la palabra clave
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
        except sr.RequestError as e:
            print(f"Error al solicitar resultados: {e}")

