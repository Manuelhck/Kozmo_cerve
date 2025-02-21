<<<<<<< Updated upstream
apNOTA IMPORTANTE: baja y Quema una imagen del sistema operativo
=======
NOTA IMPORTANTE: baja y Quema una imagen del sistema operativo
>>>>>>> Stashed changes

Raspberry Pi OS Lite

    Release date: November 19th 2024
    System: 64-bit
    Kernel version: 6.6
    Debian version: 12 (bookworm)

con RPI_IMAGE no olvides de poner tu contrasena y tu red wifi...no cambies el usuario deja Raspberry

para encontrar la ip de tu raspi:
arp-scan -l
conectate a ella con ssh raspberry@ "la ip de la raspi" 
ejemplo:
ssh raspberry@192.168.1.143

 


# Kozmo_cerve

Setup Raspberry pi zero 2w:
Preparar Rasberry pi zero 2w:

sudo raspi-config

    enable camera, i2c, spi, and disable serial.

enable i2s amp(speaker)

	sudo nano /boo/firmware/config.txt

	## add "dtoverlay=googlevoicehat-soundcard"  
	example:
		 "[all]
		  
		  dtoverlay=googlevoicehat-soundcard
	          
	sudo reboot

	## test max98357a
	speaker-test -c2
	speaker-test -c2 --test=wav -w /usr/share/sounds/alsa/Front_Center.wav

	## test micro
	arecord -l
	arecord -D plughw:0 -c1 -r 48000 -f S32_LE -t wav -V mono -v file.wav
        		
#instalar librerias raspdebian

sudo apt install -y python3-dev
sudo apt install -y python3-smbus i2c-tools
sudo apt install -y python3-pil
sudo apt install -y python3-pip
sudo apt install -y python3-setuptools
sudo apt install -y python3-rpi.gpio
sudo apt install -y python3-venv
sudo apt install -y git
<<<<<<< Updated upstream
apt install gcc-arm-linux-gnueabihf
=======
sudo apt-get install portaudio19-dev
sudo apt install build-essential libfreetype6-dev libjpeg-dev libopenjp2-7-dev libtiff5-dev
sudo apt-get install python3 python3-pip python3-pil libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7 libtiff5 flac -y


>>>>>>> Stashed changes




python3 -m venv Kozmo
source kozmo/bin/activate
cd kozmo/
python3 -m pip install pyproject.toml
python3 -m pip install --upgrade luma.oled
sudo apt install build-essential libfreetype6-dev libjpeg-dev libopenjp2-7-dev libtiff5-dev
sudo apt-get install python3 python3-pip python3-pil libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7 libtiff5 -y
<<<<<<< Updated upstream

python3 -m pip install lgpio gpiozero flask
=======
python3 -m pip install lgpio gpiozero flask speechrecognition pyaudio opencv-python

>>>>>>> Stashed changes


