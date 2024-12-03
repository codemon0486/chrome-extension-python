import pyaudio
import speech_recognition as sr
import threading
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Initialize Speech Recognition
recognizer = sr.Recognizer()

# Start and stop transcribing flags
transcribing = False
transcription_result = ""

# Initialize the microphone (update with correct device index for the virtual microphone)
device_index = 1  # Update this based on the virtual audio cable device
mic = sr.Microphone(device_index=device_index)


# Function to transcribe system audio
def transcribe_system_audio():
    global transcribing, transcription_result
    with mic as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(
            source, duration=1
        )  # Adjust for ambient noise for 1 second
        recognizer.energy_threshold = (
            300  # Lower threshold to make the recognizer more sensitive
        )
        print("Listening for system sounds...")
        while transcribing:
            try:
                audio = recognizer.listen(
                    source, timeout=10
                )  # Increase timeout to 10 seconds
                print("Processing audio...")
                text = recognizer.recognize_google(audio)
                transcription_result += text + " "
                print(f"Transcribed: {text}")
            except sr.UnknownValueError:
                print("Could not understand the audio.")
            except Exception as e:
                print(f"Error: {e}")


# Start transcription route
@app.route("/start", methods=["GET"])
def start_transcription():
    global transcribing
    if not transcribing:
        transcribing = True
        threading.Thread(target=transcribe_system_audio).start()
    return jsonify({"message": "Transcription started"})


# Stop transcription route
@app.route("/stop", methods=["GET"])
def stop_transcription():
    global transcribing
    transcribing = False
    return jsonify({"message": "Transcription stopped", "result": transcription_result})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
