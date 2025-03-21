import threading
import time
from playsound import playsound

class BackgroundWavPlayer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.thread = None

    def play(self):
        self.thread = threading.Thread(target=self._play_sound)
        self.thread.start()

    def _play_sound(self):
        playsound(self.file_path)

    def is_playing(self):
        return self.thread.is_alive() if self.thread else False

    def wait_for_completion(self):
        if self.thread:
            self.thread.join()

# Ejemplo de uso
if __name__ == "__main__":
    player = BackgroundWavPlayer("ruta/al/archivo.wav")
    player.play()

    # Esperar un tiempo para demostrar que el sonido se reproduce en segundo plano
    time.sleep(5)

    # Verificar si el sonido sigue reproduciéndose
    if player.is_playing():
        print("El archivo WAV está reproduciéndose.")
    else:
        print("El archivo WAV ha terminado de reproducirse.")

    # Esperar a que la reproducción termine
    player.wait_for_completion()
