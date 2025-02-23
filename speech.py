import speech_recognition as sr

class SpeechCommands:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.commands = {
            "comando uno": self.action_one,
            "comando dos": self.action_two,
            "comando tres": self.action_three,
            "comando cuatro": self.action_four,
            "comando cinco": self.action_five,
            "comando seis": self.action_six,
            "comando siete": self.action_seven,
            "comando ocho": self.action_eight,
            "comando nueve": self.action_nine,
            "comando diez": self.action_ten,
        }

    def recognize_speech(self):
        with self.microphone as source:
            print("Calibrando micrófono para ruido ambiental...")
            self.recognizer.adjust_for_ambient_noise(source)
            print("Por favor, hable ahora...")
            audio = self.recognizer.listen(source)
        
        try:
            print("Reconociendo discurso...")
            speech = self.recognizer.recognize_google(audio, language="es-ES")
            print(f"Has dicho: {speech}")
            return speech
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
        except sr.RequestError as e:
            print(f"Error al solicitar resultados del servicio de reconocimiento de voz; {e}")
        return None

    def execute_command(self, speech):
        for command, action in self.commands.items():
            if command in speech.lower():
                action()
                return True
        print("Comando no reconocido")
        return False

    def action_one(self):
        print("Ejecutando acción 1")

    def action_two(self):
        print("Ejecutando acción 2")

    def action_three(self):
        print("Ejecutando acción 3")

    def action_four(self):
        print("Ejecutando acción 4")

    def action_five(self):
        print("Ejecutando acción 5")

    def action_six(self):
        print("Ejecutando acción 6")

    def action_seven(self):
        print("Ejecutando acción 7")

    def action_eight(self):
        print("Ejecutando acción 8")

    def action_nine(self):
        print("Ejecutando acción 9")

    def action_ten(self):
        print("Ejecutando acción 10")

if __name__ == "__main__":
    speech_commands = SpeechCommands()
    while True:
        speech = speech_commands.recognize_speech()
        if speech:
            speech_commands.execute_command(speech)
