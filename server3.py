from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
import os
from gpiozero import Robot
from time import sleep
from gpiozero import Servo, AngularServo
from PIL import Image
from gif_display import GifDisplay
from camera_class import CameraClass
import time
from audio_player import AudioPlayer
import socket
from ipoled import OLEDDisplay
from distance_sensor_manager import DistanceSensorManager

app = Flask(__name__)
IMAGE_FOLDER = "./images"
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER

# Note the following are only used with SPI:
angulo = 0
gif_display = GifDisplay()
camera = CameraClass()
player = AudioPlayer()

# servokit
try:
    servoI = Servo(12)
    servoD = Servo(13)
    servoCZ = AngularServo(9, min_angle=-120, max_angle=120)

    servoI.min()
    servoD.max()
    sleep(1)
    servoI.value = None
    servoD.value = None
except Exception as e:
    print(f"Error initializing servos: {e}")

robot = Robot((23, 24), (27, 17))
servoCZ.angle = None

# eco sensor
echo_pin = 26
trigger_pin = 6
sensor_manager = DistanceSensorManager(echo_pin, trigger_pin)

def get_server_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception as e:
        ip = "No se pudo obtener la IP"
        print(f"Error getting server IP: {e}")
    finally:
        s.close()
    return ip

ips = get_server_ip()
display = OLEDDisplay(font_size=22)
display.display_text(ips)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    try:
        images = os.listdir(app.config['IMAGE_FOLDER'])
        return render_template('gallery.html', images=images)
    except Exception as e:
        print(f"Error loading gallery: {e}")
        return render_template('gallery.html', images=[])

@app.route('/images/<filename>')
def get_image(filename):
    try:
        return send_from_directory(app.config['IMAGE_FOLDER'], filename)
    except Exception as e:
        print(f"Error getting image: {e}")
        return "Image not found", 404

@app.route('/download/<filename>')
def download_image(filename):
    try:
        return send_from_directory(app.config['IMAGE_FOLDER'], filename, as_attachment=True)
    except Exception as e:
        print(f"Error downloading image: {e}")
        return "File not found", 404

@app.route('/move', methods=['POST'])
def move():
    try:
        direction = request.form.get('direction')
        velocidad = request.form.get('velocidad')
        speed = 1.0

        if velocidad == 'slow':
            speed = 0.4
        elif velocidad == 'medium':
            speed = 1
        elif velocidad == 'fast':
            speed = 2

        if direction == 'up':
            robot.forward(speed)
        elif direction == 'left':
            robot.left(speed)
        elif direction == 'right':
            robot.right(speed)
        elif direction == 'down':
            robot.backward(speed)

        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error moving robot: {e}")
        return redirect(url_for('index'))

@app.route('/speed', methods=['POST'])
def speed():
    try:
        speed_action = request.form.get('emotion')
        cara = request.form.get('emotion')
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error adjusting speed: {e}")
        return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop():
    try:
        robot.stop()
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error stopping robot: {e}")
        return redirect(url_for('index'))

@app.route('/arms', methods=['POST'])
def arms():
    global angulo
    try:
        servo = request.form.get('servo')

        if servo == 'hi':
            servoI.max()
            servoD.min()
            sleep(1)
            servoI.value = None
            servoD.value = None
        elif servo == 'medium':
            servoI.mid()
            
            sleep(1)
            servoI.value = None
            servoD.value = None
        elif servo == 'low':
            servoI.min()
            servoD.max()
            sleep(1)
            servoI.value = None
            servoD.value = None
        elif servo == 'HU':
            servoCZ.angle = 120
            angulo = 120
            sleep(0.5)
            servoCZ.value = None
        elif servo == 'H-':
            angulo -= 30
            servoCZ.angle = angulo
            sleep(0.5)
            servoCZ.value = None
        elif servo == 'HD':
            servoCZ.angle = -60
            angulo = -60
            sleep(0.5)
            servoCZ.value = None
        elif servo == 'H+':
            angulo += 30
            servoCZ.angle = angulo
            sleep(0.5)
            servoCZ.value = None

        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error moving arms: {e}")
        return redirect(url_for('index'))

@app.route('/start-gif', methods=['POST'])
def start_gif():
    try:
        gif_path = request.form.get('gif_path')
        if gif_path:
            gif_display.start(gif_path)
            return redirect(url_for('index'))
        else:
            return "No gif_path provided", 400
    except Exception as e:
        print(f"Error starting GIF: {e}")
        return redirect(url_for('index'))

@app.route('/stop-gif', methods=['POST'])
def stop_gif():
    try:
        gif_display.stop()
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error stopping GIF: {e}")
        return redirect(url_for('index'))

@app.route('/start_stream')
def start_stream():
    try:
        camera.start_stream()
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error starting stream: {e}")
        return redirect(url_for('index'))

@app.route('/stop_stream')
def stop_stream():
    try:
        camera.stop_stream()
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error stopping stream: {e}")
        return redirect(url_for('index'))

@app.route('/instructions')
def instructions():
    try:
        server_ip = get_server_ip()
        return render_template('instructions.html', server_ip=server_ip)
    except Exception as e:
        print(f"Error loading instructions: {e}")
        return redirect(url_for('index'))

@app.route('/back_to_home')
def back_to_home():
    return redirect(url_for('index'))

@app.route('/take_photo')
def take_photo():
    try:
        filename = "./animacion/foto.gif"
        filename2 = "./animacion/normal.gif"
        camera.stop_stream()
        gif_display.stop()
        gif_display.start(filename)
        player = AudioPlayer()
        sleep(2)
        gif_display.stop()
        filename = f"./images/photo_{int(time.time())}.png"
        camera.take_photo(filename)
        player.play("./sound/photo.wav")
        gif_display.start(filename2)
        camera.start_stream()
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error taking photo: {e}")
        return redirect(url_for('index'))

@app.route('/distance', methods=['GET'])
def get_distance():
    try:
        distance = sensor_manager.get_distance()
        return jsonify({"distance": distance})
    except Exception as e:
        print(f"Error getting distance: {e}")
        return jsonify({"distance": -1})

@app.route('/cleanup', methods=['POST'])
def cleanup():
    try:
        sensor_manager.cleanup()
        return jsonify({"status": "sensor cleaned up"})
    except Exception as e:
        print(f"Error cleaning up sensor: {e}")
        return jsonify({"status": "error"})

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8000, debug=False)
    except Exception as e:
        print(f"Error running server: {e}")
    finally:
        try:
            sensor_manager.cleanup()
        except Exception as e:
            print(f"Error during cleanup: {e}")
