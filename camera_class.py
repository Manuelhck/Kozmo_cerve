import subprocess
import threading
import time

class CameraClass:
    def __init__(self):
        self.process = None
        self.thread = None

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
                "--framerate", "15",  # Tasa de frames reducida
                "-o", "tcp://0.0.0.0:5001"  # Salida a TCP en el puerto 5001
            ]
            self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.process.communicate()  # Espera a que el proceso termine

        # Inicia el comando en un hilo separado
        self.thread = threading.Thread(target=run)
        self.thread.start()
        print("Transmisión de video iniciada en tcp://0.0.0.0:5001")

    def stop_stream(self):
        """
        Detiene la transmisión de video.
        """
        if self.process:
            self.process.terminate()  # Termina el proceso
            self.process = None
        if self.thread:
            self.thread.join()  # Espera a que el hilo termine
            self.thread = None
        print("Transmisión de video detenida")

    def take_photo(self,filename):
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
            print(f"Foto guardada como {filename}")
            
        except subprocess.CalledProcessError as e:
            print(f"Error al tomar la foto: {e}")
 
    def restart_camera(self):
        """
        Reinicia la cámara para asegurarse de que esté disponible.
        """
        try:
            # Detiene cualquier proceso de la cámara que pueda estar en ejecución
            subprocess.run(["sudo", "systemctl", "restart", "rpicam"], check=True)
            time.sleep(1)  # Espera un segundo para asegurarse de que la cámara esté lista
        except subprocess.CalledProcessError as e:
            print(f"Error al reiniciar la cámara: {e}")  

