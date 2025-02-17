# Kozmo_cerve

Setup Raspberry pi zero 2w:

apt-get update

sudo raspi-config

    enable ssh, i2c, spi, camera, and disable serial.

enable i2s amp(speaker)

	sudo apt install -y wget
	pip3 install adafruit-python-shell
	wget https://github.com/adafruit/Raspberry-Pi-Installer-Scripts/raw/main/i2samp.py
	sudo -E env PATH=$PATH python3 i2samp.py 
	##say 'N' to playback service.

enable microphone 
	sudo nano /boo/firmware/config.txt
	##add "dtoverlay=googlevoicehat-soundcard" over "max98357a" 
	example:
		 "[all]
		  enable_uart=0
		  dtoverlay=googlevoicehat-soundcard
	          dtoverlay=max98357a"

