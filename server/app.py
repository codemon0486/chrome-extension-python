from flask import Flask, jsonify
from flask_cors import CORS
import threading
import speech_recognition as sr
import pyaudio

app = Flask(__name__)
CORS(app)

transcribing = False
transcription_result = ""


def transcribe_system_audio():
    global transcribing, transcription_result
    recognizer = sr.Recognizer()
    with sr.AudioFile(
        "VB-Audio Output"
    ) as source:  # Replace with your system audio source
        while transcribing:
            try:
                print("Listening to system sounds...")
                audio = recognizer.record(
                    source, duration=5
                )  # Capture 5 seconds of audio
                text = recognizer.recognize_google(audio)
                transcription_result += text + "\n"
                print(f"Transcribed: {text}")
            except sr.UnknownValueError:
                print("Could not understand the audio.")
            except Exception as e:
                print(f"Error: {e}")


@app.route("/start", methods=["GET"])
def start_transcription():
    global transcribing
    if not transcribing:
        transcribing = True
        threading.Thread(target=transcribe_system_audio).start()
    return jsonify({"message": "Transcription started"})


@app.route("/stop", methods=["GET"])
def stop_transcription():
    global transcribing
    transcribing = False
    return jsonify({"message": "Transcription stopped", "result": transcription_result})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
