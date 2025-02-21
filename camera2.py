from flask import Flask, Response
import subprocess

app = Flask(__name__)

def generate_frames():
    # Comando para recibir el stream TCP y convertirlo a MJPEG
    command = [
        'ffmpeg',
        '-i', 'tcp://192.168.1.151:5001',  # Recibir el stream TCP
        '-f', 'mjpeg',  # Convertir a MJPEG
        '-',  # Salida en stdout
    ]

    # Iniciar el proceso de ffmpeg
    process = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=0)

    # Leer la salida del proceso y enviarla como frames
    try:
        while True:
            frame = process.stdout.read(1024)
            if not frame:
                break
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    finally:
        # Detener el proceso cuando se interrumpe la transmisión
        process.terminate()
        process.wait()

@app.route('/video_feed')
def video_feed():
    # Transmitir los frames al navegador
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    # Página HTML para mostrar el video
    return """
    <html>
      <head>
        <title>Video Streaming</title>
      </head>
      <body>
        <h1>Video Streaming</h1>
        <img src="/video_feed">
      </body>
    </html>
    """

if __name__ == '__main__':
    # Ejecutar la aplicación Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
