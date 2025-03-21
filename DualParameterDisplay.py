from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import ImageFont
import time

class DualParameterDisplay:
    def __init__(self, port=1, address=0x3C, width=128, height=64, font_path=None, font_size=20):
        """
        Inicializa el display OLED SSD1306.
        
        :param port: Puerto I2C (por defecto 1).
        :param address: Dirección I2C del display (por defecto 0x3C).
        :param width: Ancho del display (por defecto 128 píxeles).
        :param height: Alto del display (por defecto 64 píxeles).
        :param font_path: Ruta a un archivo de fuente TrueType (.ttf). Si es None, se usa la fuente predeterminada.
        :param font_size: Tamaño de la fuente (por defecto 20).
        """
        # Configura la interfaz I2C
        self.serial = i2c(port=port, address=address)
        
        # Inicializa el dispositivo SSD1306
        self.device = ssd1306(self.serial, width=width, height=height)
        
        # Carga la fuente
        if font_path:
            self.font = ImageFont.truetype(font_path, font_size)
        else:
            self.font = ImageFont.load_default()

    def clear(self):
        """Limpia la pantalla."""
        with canvas(self.device) as draw:
            draw.rectangle(self.device.bounding_box, outline="black", fill="black")

    def show_parameters(self, param1, param2, duration=3):
        """
        Muestra dos parámetros en el display durante un tiempo específico.
        
        :param param1: Primer parámetro a mostrar (puede ser un número o una cadena).
        :param param2: Segundo parámetro a mostrar (puede ser un número o una cadena).
        :param duration: Duración en segundos para mostrar los parámetros (por defecto 3 segundos).
        """
        # Convierte los parámetros a cadenas si no lo son
        param1_str = str(param1)
        param2_str = str(param2)
        
        # Limpia la pantalla antes de mostrar los parámetros
        self.clear()
        
        # Muestra los parámetros en la pantalla
        with canvas(self.device) as draw:
            # Muestra el primer parámetro en la parte superior
            draw.text((0, 0), f"{param1_str}", font=self.font, fill="white")
            
            # Muestra el segundo parámetro en la parte inferior
            draw.text((0, 30), f"  {param2_str}", font=self.font, fill="white")
        
        # Espera el tiempo especificado
        time.sleep(duration)
        
        # Limpia la pantalla después de mostrar los parámetros
        self.clear()

    def cleanup(self):
        """Limpia y cierra el dispositivo."""
        self.clear()
        self.device.cleanup()

# Ejemplo de uso
if __name__ == "__main__":
    try:
        # Ruta a un archivo de fuente TrueType (.ttf)
        # Puedes descargar una fuente como "arial.ttf" o "Roboto-Regular.ttf"
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # Cambia esta ruta
        
        # Inicializa el display con una fuente más grande
        display = DualParameterDisplay(font_path=font_path, font_size=20)

        # Muestra dos parámetros en el display
        display.show_parameters("25.3°C", "60%", duration=5)

    except KeyboardInterrupt:
        # Limpia el display antes de salir
        display.cleanup()
