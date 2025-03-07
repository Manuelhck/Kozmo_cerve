from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import ImageFont
import time

class TemperatureDisplay:
    def __init__(self, port=1, address=0x3C, width=128, height=64):
        """
        Inicializa el display OLED SSD1306.
        
        :param port: Puerto I2C (por defecto 1).
        :param address: Dirección I2C del display (por defecto 0x3C).
        :param width: Ancho del display (por defecto 128 píxeles).
        :param height: Alto del display (por defecto 64 píxeles).
        """
        # Configura la interfaz I2C
        self.serial = i2c(port=port, address=address)
        
        # Inicializa el dispositivo SSD1306
        self.device = ssd1306(self.serial, width=width, height=height)
        
        # Carga una fuente por defecto (puedes cambiar la ruta a otra fuente)
        self.font = ImageFont.load_default()

    def clear(self):
        """Limpia la pantalla."""
        with canvas(self.device) as draw:
            draw.rectangle(self.device.bounding_box, outline="black", fill="black")

    def show_temperature(self, temperature):
        """
        Muestra la temperatura en el display durante 3 segundos.
        
        :param temperature: Temperatura a mostrar (puede ser un número o una cadena).
        """
        # Convierte la temperatura a cadena si no lo es
        temperature_str = str(temperature)
        
        # Limpia la pantalla antes de mostrar la temperatura
        self.clear()
        
        # Muestra la temperatura en el centro de la pantalla
        with canvas(self.device) as draw:
            text_width, text_height = draw.textsize(temperature_str, font=self.font)
            x = (self.device.width - text_width) // 2
            y = (self.device.height - text_height) // 2
            draw.text((x, y), temperature_str, font=self.font, fill="white")
        
        # Espera 3 segundos
        time.sleep(3)
        
        # Limpia la pantalla después de mostrar la temperatura
        self.clear()

    def cleanup(self):
        """Limpia y cierra el dispositivo."""
        self.clear()
        self.device.cleanup()

# Ejemplo de uso
if __name__ == "__main__":
    try:
        # Inicializa el display
        display = TemperatureDisplay()

        # Muestra una temperatura en el display
        display.show_temperature("25.3°C")

    except KeyboardInterrupt:
        # Limpia el display antes de salir
        display.cleanup()
