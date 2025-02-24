import requests
import sys

# Verifica si se proporcionó la ciudad como argumento
if len(sys.argv) != 2:
    print("Uso: python3 tiempo.py <ciudad>")
    print("Ejemplo: python3 tiempo.py Madrid,ES")
    sys.exit(1)

# Tu API Key de OpenWeatherMap
API_KEY = '24042ef8f3b98cb2da621a3d28c04661'  # Reemplaza con tu API Key
CIUDAD = sys.argv[1]  # Obtiene la ciudad desde el argumento

# URL de la API para el tiempo actual
url = f'http://api.openweathermap.org/data/2.5/weather?q={CIUDAD}&appid={API_KEY}&units=metric&lang=es'

# Hacer la solicitud
respuesta = requests.get(url)
datos = respuesta.json()

# Mostrar datos
if datos['cod'] == 200:
    print(f"Ciudad: {datos['name']}")
    print(f"Temperatura: {datos['main']['temp']}°C")
    print(f"Condición: {datos['weather'][0]['description']}")
    print(f"Humedad: {datos['main']['humidity']}%")
    print(f"Viento: {datos['wind']['speed']} m/s")
else:
    print(f"Error: {datos['message']}")
