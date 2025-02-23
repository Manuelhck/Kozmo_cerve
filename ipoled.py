from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont
import time

class OLEDDisplay:
    def __init__(self, i2c_port=1, i2c_address=0x3C,font_size=12):
        # Configuración de la interfaz y el dispositivo OLED
        self.serial = i2c(port=i2c_port, address=i2c_address)
        self.device = ssd1306(self.serial)
        self.font = ImageFont.load_default()

    def display_text(self, text):
        with canvas(self.device) as draw:
            # Dibujar texto en la pantalla OLED
            draw.text((30, 20), text, font=self.font, fill=255)
        # Mostrar el texto durante 10 segundos
        time.sleep(10)
        # Apagar la pantalla después de 10 segundos
        self.clear_display()

    def clear_display(self):
        # Limpiar la pantalla OLED
        self.device.clear()

if __name__ == "__main__":
    text_to_display = "IP!"
    oled_display = OLEDDisplay()
    oled_display.display_text(text_to_display) 
