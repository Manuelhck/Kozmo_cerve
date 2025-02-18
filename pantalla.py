import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306  # Importar correctamente ssd1306
from PIL import Image

# Configuración de la pantalla OLED
serial = i2c(port=1, address=0x3C)  # Ajusta el puerto y la dirección I2C según tu configuración
device = ssd1306(serial, width=128, height=64)

# Cargar el archivo GIF
gif_path = "./animacion/normal.gif"  # Cambia esto por la ruta de tu archivo GIF
gif = Image.open(gif_path)

# Función para extraer los frames del GIF
def extract_frames(gif):
    frames = []
    try:
        while True:
            frame = gif.copy().convert("1")  # Convertir a modo monocromo (1-bit)
            frames.append(frame)
            gif.seek(len(frames))  # Ir al siguiente frame
    except EOFError:
        pass  # Fin del GIF
    return frames

# Extraer los frames del GIF
frames = extract_frames(gif)

# Mostrar la animación en bucle
try:
    while True:
        for frame in frames:
            device.display(frame)  # Mostrar el frame en la pantalla
            print(gif.info["duration"])
            time.sleep(gif.info["duration"] / 5000)  # Usar el tiempo entre frames del GIF
except KeyboardInterrupt:
    # Limpiar la pantalla al salir
    device.clear()
