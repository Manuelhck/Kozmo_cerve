from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Mostrar una página con instrucciones para el usuario
    return """
    <html>
      <head>
        <title>Reproducir Stream de Video</title>
      </head>
      <body>
        <h1>Reproducir Stream de Video</h1>

        <h2>Instrucciones para Linux</h2>
        <p>Para reproducir el stream de video, ejecuta el siguiente comando en tu terminal:</p>
        <pre>ffplay tcp://192.168.1.151:5001 -vf "setpts=N/30" -fflags nobuffer -flags low_delay -framedrop</pre>
        <p>Asegúrate de tener <code>ffplay</code> instalado en tu sistema. Puedes instalarlo con:</p>
        <pre>sudo apt update && sudo apt install ffmpeg</pre>

        <h2>Instrucciones para Windows</h2>
        <p>Para reproducir el stream de video en Windows, sigue estos pasos:</p>
        <ol>
          <li>Descarga e instala <code>ffmpeg</code> desde <a href="https://ffmpeg.org/download.html" target="_blank">ffmpeg.org</a>.</li>
          <li>Abre una ventana de <code>cmd</code> o <code>PowerShell</code>.</li>
          <li>Navega al directorio donde instalaste <code>ffmpeg</code>. Por ejemplo:</li>
          <pre>cd C:\\ruta\\a\\ffmpeg\\bin</pre>
          <li>Ejecuta el siguiente comando:</li>
          <pre>ffplay tcp://192.168.1.151:5001 -vf "setpts=N/30" -fflags nobuffer -flags low_delay -framedrop</pre>
        </ol>
      </body>
    </html>
    """

if __name__ == '__main__':
    # Ejecutar la aplicación Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
