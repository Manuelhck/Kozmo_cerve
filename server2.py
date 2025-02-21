from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
import os
from time  import sleep
from gpiozero import Servo, AngularServo
from PIL import Image
from gif_display import GifDisplay
from camera_class import CameraClass
import time
from audio_player import AudioPlayer
from servocontroler import ServoController
app = Flask(__name__)
IMAGE_FOLDER = "./images"
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
# Note the following are only used with SPI:
angulo=0
gif_display = GifDisplay()
camera = CameraClass()
player = AudioPlayer()

#servokit
servoI = Servo(12)
servoD = Servo(13)
servoCZ = AngularServo(9, min_angle=-120, max_angle=120)

servoI.min()
servoD.max()
sleep(2)
servoI.value =None;
servoD.value =None;

from gpiozero import Robot
robot = Robot((23, 24), (27, 17))

# Clear display.

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/gallery')

def gallery():
    # List all files in the image folder
    images = os.listdir(app.config['IMAGE_FOLDER'])
    return render_template('gallery.html', images=images)

@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory(app.config['IMAGE_FOLDER'], filename)

@app.route('/download/<filename>')
def download_image(filename):
    return send_from_directory(app.config['IMAGE_FOLDER'], filename, as_attachment=True)





@app.route('/move', methods=['POST'])
def move():
       
    direction = request.form.get('direction')
    velocidad = request.form.get('velocidad')
    speed=1.0
    print (direction)
    print (velocidad)
    if velocidad =='slow':
        speed=0.4
    elif direction == 'mediun':
        speed=1
    elif direction == 'fast':
        speed=2
    if direction == 'up':
        robot.forward(speed)
        
        print("go go GO!")
    elif direction == 'left':
        print("hacia la izquierda!")
        robot.left(speed)
    elif direction == 'right':
        print("hacia la derecha!")
        robot.right(speed)
    elif direction == 'down':
        print("Patras!!")
        robot.backward(speed)
    # Aquí puedes añadir la lógica para mover el robot en la dirección indicada
    return redirect(url_for('index'))

@app.route('/speed', methods=['POST'])
def speed():
    speed_action = request.form.get('emotion')
    cara=request.form.get('emotion')
    
# Aquí puedes añadir la lógica para ajustar la velocidad del robot
    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop():
    print("Detener el robot")
    robot.stop()
    # Aquí puedes añadir la lógica para detener el robot
    return redirect(url_for('index'))
@app.route('/arms', methods=['POST'])

def arms():
    global angulo
    servo = request.form.get('servo')
    if servo == 'hi':
        servoI.max()
        servoD.min()
        sleep(2)
        servoI.value =None;
        servoD.value =None;
        
        
    elif servo == 'mediun':
         servoI.mid()
         servoD.mid()
         sleep(2)
         servoI.value =None;
         servoD.value =None;
    elif servo == 'low':
         servoI.min()
         servoD.max()
         sleep(2)
         servoI.value =None;
         servoD.value =None; 
    elif servo == 'HU': 
         servoCZ.angle =120
         
         angulo  = 120
         sleep(2)
         print(angulo)
         servoCZ.value =None
    elif servo == 'H-':
         
         angulo -=30
         print(angulo)
         servoCZ.angle = angulo 
         
         sleep(2)
         servoCZ.value =None
    elif servo == 'HD':
         servoCZ.angle = -60

         angulo  = -60
         sleep(2)
         print(angulo)
         servoCZ.value =None
    elif servo == 'H+':

         angulo +=30
         print(angulo)
         servoCZ.angle = angulo

         sleep(2)
         servoCZ.value =None
        
    # Aquí puedes añadir la lógica para mover el robot en la dirección indicada
    return redirect(url_for('index'))

@app.route('/start-gif', methods=['POST'])
def start_gif():
    gif_path = request.form.get('gif_path')
    print (gif_path)
    if gif_path:
        gif_display.start(gif_path)
        return redirect(url_for('index'))
    else:
        return "No gif_path provided", 400

@app.route('/stop-gif', methods=['POST'])
def stop_gif():
    gif_display.stop()
    return redirect(url_for('index'))


    # Aquí puedes añadir la lógica para mover el robot en la dirección indicada
    return redirect(url_for('index'))

@app.route('/start_stream')
def start_stream():
    camera.start_stream()
    return redirect(url_for('index'))

@app.route('/stop_stream')
def stop_stream():
    camera.stop_stream()
    return redirect(url_for('index'))

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/back_to_home')
def back_to_home():
    return redirect(url_for('index'))


@app.route('/take_photo')
def take_photo():
    filename="./animacion/foto.gif"
    filename2="./animacion/normal.gif"
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


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8000, debug=False)
