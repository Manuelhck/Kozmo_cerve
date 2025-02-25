import speech_recognition as sr
import threading
import time
from servocontroler import ServoController
from time import sleep

class SpeechRecognitionService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.commands = {
            "cosmo manos arriba": self.encender_luz,
            "cosmo baja las manos": self.apagar_luz,
            "abrir puerta": self.abrir_puerta,
            "cerrar puerta": self.cerrar_puerta,
            "reproducir música": self.reproducir_musica,
            "detener música": self.detener_musica,
            "contar chiste": self.contar_chiste,
            "hora actual": self.decir_hora,
            "temperatura": self.decir_temperatura,
            "detener servicio": self.detener_servicio,
        }

    def start_listening(self):
        """Inicia el servicio de reconocimiento de voz en segundo plano."""
        self.is_listening = True
        self.thread = threading.Thread(target=self._listen_loop)
        self.thread.start()
        print("Servicio de reconocimiento de voz iniciado. Escuchando...")

    def stop_listening(self):
        """Detiene el servicio de reconocimiento de voz."""
        self.is_listening = False
        print("Servicio de reconocimiento de voz detenido.")

    def _listen_loop(self):
        """Bucle principal que escucha y procesa comandos."""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)  # Calibra el micrófono
            while self.is_listening:
                print("Escuchando...")
                try:
                    audio = self.recognizer.listen(source, timeout=5)
                    command = self.recognizer.recognize_google(audio, language="es-ES").lower()
                    print(f"Comando detectado: {command}")
                    self._process_command(command)
                except sr.UnknownValueError:
                    print("No se entendió el comando")
                except sr.RequestError:
                    print("Error al conectar con el servicio de reconocimiento de voz")
                except sr.WaitTimeoutError:
                    continue  # Si no se detecta voz, continúa escuchando

    def _process_command(self, command):
        """Procesa el comando detectado."""
        for cmd, action in self.commands.items():
            if cmd in command:
                action()
                break
        else:
            print("Comando no reconocido")

    # Funciones asociadas a los comandos
    def encender_luz(self):
        print("OK")
        controller = ServoController()
        controller.move_servo(1, 100)
        sleep(1)
        
        


    def apagar_luz(self):
        
        print("OK")
        controller = ServoController()
        controller.move_servo(1, 0)
        sleep(1)

    def abrir_puerta(self):
        print("Abriendo la puerta...")

    def cerrar_puerta(self):
        print("Cerrando la puerta...")

    def reproducir_musica(self):
        print("Reproduciendo música...")

    def detener_musica(self):
        print("Deteniendo la música...")

    def contar_chiste(self):
        print("¿Por qué los programadores prefieren el modo oscuro? ¡Porque la luz atrae a los bugs!")

    def decir_hora(self):
        from datetime import datetime
        now = datetime.now()
        print(f"La hora actual es: {now.strftime('%H:%M:%S')}")

    def decir_temperatura(self):
        print("La temperatura es de 25°C (simulado).")

    def detener_servicio(self):
        """Detiene el servicio de reconocimiento de voz."""
        self.stop_listening()

# Ejemplo de uso
if __name__ == "__main__":
    service = SpeechRecognitionService()
    service.start_listening()

    # Mantén el programa principal en ejecución
    try:
        while service.is_listening:
            time.sleep(1)
    except KeyboardInterrupt:
        service.stop_listening()
