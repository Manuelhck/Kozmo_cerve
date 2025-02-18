import os
from time import sleep
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image

# Configuración de la pantalla OLED
serial = i2c(port=1, address=0x3C)  # Ajusta el puerto y la dirección I2C según tu configuración
device = ssd1306(serial, width=128, height=64)

# Ruta a la carpeta con los frames del GIF
FRAMES_DIR = "./animacion/normal/"  # Cambia esto por la ruta de tu carpeta de frames

# Cargar los frames del GIF
frames = []
for frame_file in sorted(os.listdir(FRAMES_DIR)):
    if frame_file.endswith(".png") or frame_file.endswith(".bmp"):  # Asegúrate de que sean imágenes
        frame_path = os.path.join(FRAMES_DIR, frame_file)
        frame = Image.open(frame_path).convert("1")  # Convertir a modo monocromo (1-bit)
        frames.append(frame)

# Mostrar la animación en bucle
try:
    while True:
        for frame in frames:
            device.display(frame)  # Mostrar el frame en la pantalla
            sleep(0.1)  # Ajusta el tiempo entre frames para la velocidad de la animación
except KeyboardInterrupt:
    # Limpiar la pantalla al salir
    device.clear()
