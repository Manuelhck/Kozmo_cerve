import speech_recognition as sr

# Crear un reconocedor de voz
recognizer = sr.Recognizer()

# Usar el micrófono como fuente de audio
with sr.Microphone() as source:
    print("Di algo en español...")
    
    # Ajustar el reconocedor al ruido ambiental
    recognizer.adjust_for_ambient_noise(source)
    
    # Escuchar la entrada de audio
    audio = recognizer.listen(source)

    try:
        # Reconocer el audio usando Google Speech Recognition
        texto = recognizer.recognize_google(audio, language="es-ES")
        print("Has dicho: " + texto)
    
    except sr.UnknownValueError:
        print("No se pudo entender el audio")
    
    except sr.RequestError as e:
        print(f"Error al solicitar resultados; {e}")
