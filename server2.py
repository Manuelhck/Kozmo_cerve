from flask import Flask, render_template, request, redirect, url_for, jsonify
from time  import sleep
from gpiozero import Servo
from PIL import Image
from gif_display import GifDisplay

app = Flask(__name__)

# Note the following are only used with SPI:

gif_display = GifDisplay()

#servokit
servoI = Servo(12)
servoD = Servo(13)
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
       
    servo = request.form.get('servo')

    if servo == 'hi':
        servoI.max()
        servoD.min()
        sleep(2)
        
    elif servo == 'mediun':
        servoI.mid()
        servoD.mid()

    elif servo == 'low':
        servoI.min()
        servoD.max()
        sleep(2)
        servoI.value =None;
        servoD.value =None;

        
    # Aquí puedes añadir la lógica para mover el robot en la dirección indicada
    return redirect(url_for('index'))

@app.route('/start-gif', methods=['POST'])
def start_gif():
    gif_path = request.form.get('gif_path')
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


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8000, debug=False)