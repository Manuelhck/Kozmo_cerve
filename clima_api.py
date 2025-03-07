import requests
from DualParameterDisplay import DualParameterDisplay
class ClimaAPI:
    def __init__(self, api_key):
        """
        Inicializa la clase con la API Key de OpenWeatherMap.

        :param api_key: Tu API Key de OpenWeatherMap.
        """
        self.api_key = api_key

    def obtener_clima(self, ciudad):
        """
        Obtiene el clima actual de una ciudad utilizando la API de OpenWeatherMap.

        :param ciudad: Nombre de la ciudad y código del país (ejemplo: "Madrid,ES").
        :return: Diccionario con los datos del clima o None si hay un error.
        """
        url = f'http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={self.api_key}&units=metric&lang=es'
        
        try:
            respuesta = requests.get(url)
            respuesta.raise_for_status()  # Lanza una excepción si la solicitud no fue exitosa
            datos = respuesta.json()
            
            if datos['cod'] != 200:
                print(f"Error: {datos['message']}")
                return None
            
            return datos
        
        except requests.exceptions.RequestException as e:
            print(f"Error al conectarse a la API: {e}")
            return None

    def mostrar_clima(self, datos):
        """
        Muestra los datos del clima en la consola.

        :param datos: Diccionario con los datos del clima.
        """
        if not datos:
            return
        
        print(f"Ciudad: {datos['name']}")
        print(f"Temperatura: {datos['main']['temp']}°C")
        print(f"Condición: {datos['weather'][0]['description'].capitalize()}")
        print(f"Humedad: {datos['main']['humidity']}%")
        print(f"Viento: {datos['wind']['speed']} m/s")
        try:
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            display = DualParameterDisplay(font_path=font_path, font_size=20)
            display.show_parameters( f" {datos['main']['temp']}°C" , f" {datos['main']['humidity']}%", duration=8)
        except KeyboardInterrupt:
            display.cleanup()

    def obtener_y_mostrar_clima(self, ciudad):
        """
        Obtiene y muestra el clima de una ciudad.

        :param ciudad: Nombre de la ciudad y código del país (ejemplo: "Madrid,ES").
        """
        datos_clima = self.obtener_clima(ciudad)
        if datos_clima:
            self.mostrar_clima(datos_clima)

# Ejemplo de uso
if __name__ == "__main__":
    # Reemplaza con tu API Key de OpenWeatherMap
    API_KEY = '24042ef8f3b98cb2da621a3d28c04661'
    
    # Crear una instancia de la clase
    clima = ClimaAPI(API_KEY)
    
    # Obtener y mostrar el clima de una ciudad
    ciudad = "Albacete,ES"  # Cambia esto por la ciudad que desees
    clima.obtener_y_mostrar_clima(ciudad)
