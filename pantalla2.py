import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image

# Configuración de la pantalla OLED
serial = i2c(port=1, address=0x3C)  # Ajusta el puerto y la dirección I2C según tu configuración
device = ssd1306(serial, width=128, height=64)  # Crear el dispositivo OLED

# Cargar el archivo GIF
gif_path = "./animacion/normal.gif"  # Cambia esto por la ruta de tu archivo GIF
gif = Image.open(gif_path)

# Función para extraer los frames y sus duraciones
def extract_frames(gif):
    frames = []
    durations = []
    try:
        while True:
            frame = gif.copy().convert("1")  # Convertir a modo monocromo (1-bit)
            frames.append(frame)
            durations.append(gif.info["duration"])  # Obtener la duración del frame
            gif.seek(len(frames))  # Ir al siguiente frame
    except EOFError:
        pass  # Fin del GIF
    return frames, durations

# Extraer los frames y sus duraciones
frames, durations = extract_frames(gif)

# Mostrar la animación en bucle
try:
    while True:
        for frame, duration in zip(frames, durations):
            device.display(frame)  # Mostrar el frame en la pantalla
            time.sleep(duration / 2500)  # Usar el tiempo entre frames del GIF (en milisegundos)
except KeyboardInterrupt:
    # Limpiar la pantalla al salir
    device.clear()
