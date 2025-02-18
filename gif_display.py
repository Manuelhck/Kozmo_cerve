from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageSequence
import threading
import time

class GifDisplay:
    def __init__(self, i2c_port=1, i2c_address=0x3C, width=128, height=64):
        self.width = width
        self.height = height
        self.device = ssd1306(i2c(port=i2c_port, address=i2c_address), width=self.width, height=self.height)
        self.thread = None
        self.stop_thread = threading.Event()

    def extract_frames(self, gif):
        frames = []
        durations = []
        try:
            while True:
                frame = gif.copy().convert("1")  # Convertir a modo monocromo (1-bit)
                frames.append(frame)
                durations.append(gif.info["duration"])  # Obtener la duración del frame
                gif.seek(len(frames)) 
        except EOFError:
            pass
        return frames, durations

    def display_gif(self, gif_path):
        gif = Image.open(gif_path)
        frames, durations = self.extract_frames(gif)
        while not self.stop_thread.is_set():
            for frame, duration in zip(frames, durations):
                if self.stop_thread.is_set():
                    break
                frame = frame.resize((self.width, self.height))
                self.device.display(frame.convert(self.device.mode))
                time.sleep(duration / 2000.0)

    def start(self, gif_path):
        if self.thread is None or not self.thread.is_alive():
            self.stop_thread.clear()
            self.thread = threading.Thread(target=self.display_gif, args=(gif_path,))
            self.thread.daemon = True
            self.thread.start()

    def stop(self):
        if self.thread is not None and self.thread.is_alive():
            self.stop_thread.set()
            self.thread.join()
            self.device.clear()
