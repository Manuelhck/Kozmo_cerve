from datetime import datetime
from DualParameterDisplay import DualParameterDisplay
class HoraYDia:
    def obtener_hora_actual(self, formato="%H:%M:%S"):
        """
        Obtiene la hora actual en el formato especificado.
        
        :param formato: Formato de la hora (por defecto "%H:%M:%S").
        :return: Hora actual como cadena.
        """
        ahora = datetime.now()
        return ahora.strftime(formato)

    def obtener_dia_actual(self, formato="%A"):
        """
        Obtiene el día de la semana actual en el formato especificado.
        
        :param formato: Formato del día (por defecto "%A" para el nombre completo del día).
        :return: Día de la semana como cadena.
        """
        ahora = datetime.now()
        return ahora.strftime(formato)

    def mostrar_hora_y_dia(self, formato_hora="%H:%M:%S", formato_dia="%A"):
        """
        Muestra la hora actual y el día de la semana en la consola.
        
        :param formato_hora: Formato de la hora (por defecto "%H:%M:%S").
        :param formato_dia: Formato del día (por defecto "%A").
        """
        hora_actual = self.obtener_hora_actual(formato_hora)
        dia_actual = self.obtener_dia_actual(formato_dia)
        print(f"Hora actual: {hora_actual}")
        print(f"Día actual: {dia_actual}")
        try:
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            display = DualParameterDisplay(font_path=font_path, font_size=20)    
            display.show_parameters( f" {hora_actual}",f" {dia_actual}" , duration=5)
        except KeyboardInterrupt:
            display.cleanup()


# Ejemplo de uso
if __name__ == "__main__":
    reloj = HoraYDia()
    #reloj.mostrar_hora_y_dia()  # Muestra la hora y el día en formato predeterminado
    reloj.mostrar_hora_y_dia("%d/%m/%Y","%H:%M:%S")  # Formato personalizado
