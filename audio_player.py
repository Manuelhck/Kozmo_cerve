import pygame
import time

class AudioPlayer:
    def __init__(self):
        """
        Inicializa pygame y el mezclador de sonido.
        """
        pygame.init()
        pygame.mixer.init()

    def play(self, file_path):
        """
        Reproduce un archivo de audio.

        :param file_path: Ruta del archivo de audio a reproducir.
        """
        try:
            # Carga el archivo de audio
            pygame.mixer.music.load(file_path)
            print(f"Reproduciendo: {file_path}")

            # Reproduce el archivo de audio
            pygame.mixer.music.play()

            # Espera a que termine la reproducción
            while pygame.mixer.music.get_busy():
                time.sleep(1)

        except pygame.error as e:
            print(f"Error al reproducir el archivo: {e}")
        finally:
            # Detiene y libera los recursos
            pygame.mixer.music.stop()
            pygame.mixer.quit()
