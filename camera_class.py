import subprocess
import threading
import time
import logging

class CameraClass:
    def __init__(self):
        self.process = None
        self.thread = None
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """
        Configura un logger para registrar eventos y errores.
        """
        logger = logging.getLogger("CameraClass")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def start_stream(self):
        """
        Inicia la transmisión de video en un hilo separado usando el comando rpicam-vid.
        """
        def run():
            command = [
                "rpicam-vid",
                "-t", "0",          # Transmitir indefinidamente
                "--inline",         # Habilita el modo inline (necesario para transmisión TCP)
                "--listen",         # Escuchar en el puerto TCP
                "--framerate", "10",  # Tasa de frames reducida a 10 FPS
                "-o", "tcp://0.0.0.0:5001"  # Salida a TCP en el puerto 5001
            ]
            try:
                self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.logger.info("Transmisión de video iniciada en tcp://0.0.0.0:5001")
                self.process.communicate()  # Espera a que el proceso termine
            except Exception as e:
                self.logger.error(f"Error al iniciar la transmisión de video: {e}")
                if self.process:
                    self.process.terminate()
                    self.process = None

        # Inicia el comando en un hilo separado con baja prioridad
        self.thread = threading.Thread(target=run)
        self.thread.start()

    def stop_stream(self):
        """
        Detiene la transmisión de video.
        """
        try:
            if self.process:
                self.process.terminate()  # Termina el proceso
                self.process = None
                self.logger.info("Proceso de transmisión terminado.")
            if self.thread:
                self.thread.join()  # Espera a que el hilo termine
                self.thread = None
                self.logger.info("Hilo de transmisión finalizado.")
            self.logger.info("Transmisión de video detenida.")
        except Exception as e:
            self.logger.error(f"Error al detener la transmisión de video: {e}")

    def take_photo(self, filename="./images/photo.png"):
        """
        Toma una foto y la guarda en un archivo.

        :param filename: Nombre del archivo donde se guardará la foto (por defecto: "./images/photo.png").
        """
        command = [
            "rpicam-still",
            "-o", filename,  # Guarda la foto en el archivo especificado
            "--nopreview"    # Desactiva la vista previa para ahorrar recursos
        ]
        try:
            subprocess.run(command, check=True)
            self.logger.info(f"Foto guardada como {filename}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error al tomar la foto: {e}")
        except Exception as e:
            self.logger.error(f"Error inesperado al tomar la foto: {e}")

    def restart_camera(self):
        """
        Reinicia la cámara para asegurarse de que esté disponible.
        """
        try:
            # Detiene cualquier proceso de la cámara que pueda estar en ejecución
            subprocess.run(["sudo", "systemctl", "restart", "rpicam"], check=True)
            time.sleep(1)  # Espera un segundo para asegurarse de que la cámara esté lista
            self.logger.info("Cámara reiniciada correctamente.")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error al reiniciar la cámara: {e}")
        except Exception as e:
            self.logger.error(f"Error inesperado al reiniciar la cámara: {e}")

    def __del__(self):
        """
        Asegura que los recursos se liberen correctamente al destruir la instancia.
        """
        self.stop_stream()
