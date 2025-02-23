import speech_recognition as sr
import threading

class KeywordListener:
    def __init__(self, keyword, action):
        self.keyword = keyword.lower()
        self.action = action
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def recognize_speech(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Esperando la frase clave...")
            audio = self.recognizer.listen(source)
        
        try:
            speech = self.recognizer.recognize_google(audio, language="es-ES").lower()
            print(f"Has dicho: {speech}")
            return speech
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
        except sr.RequestError as e:
            print(f"Error al solicitar resultados del servicio de reconocimiento de voz: {e}")
        return None

    def listen_for_keyword(self):
        while True:
            speech = self.recognize_speech()
            if speech and self.keyword in speech:
                self.action()

def keyword_action():
    print("¡Frase clave detectada! Ejecutando acción...")

if __name__ == "__main__":
    keyword = "hola"
    listener = KeywordListener(keyword, keyword_action)
    listener_thread = threading.Thread(target=listener.listen_for_keyword)
    listener_thread.daemon = True
    listener_thread.start()

    print("El programa está en espera de la frase clave.")
    listener_thread.join()
