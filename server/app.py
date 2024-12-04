from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import whisper
import pyaudio
import wave
import os

app = Flask(__name__)
CORS(app)

# Whisper model initialization (base for faster inference)
model = whisper.load_model("base")

# Global variables for managing transcription
is_listening = False
audio_frames = []
audio_thread = None

# PyAudio configurations
FORMAT = pyaudio.paInt16
CHANNELS = 1  # Mono
RATE = 16000  # Whisper works best with 16kHz audio
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "output.wav"


def record_audio():
    """Function to record audio from the system."""
    global is_listening, audio_frames
    audio = pyaudio.PyAudio()

    # Set up stream
    stream = audio.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )
    print("Recording started...")
    audio_frames = []

    # Record until stopped
    while is_listening:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print("Recording stopped...")

    # Save audio to WAV file
    with wave.open(WAVE_OUTPUT_FILENAME, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(audio_frames))


def transcribe_audio():
    """Function to transcribe the recorded audio."""
    if os.path.exists(WAVE_OUTPUT_FILENAME):
        print("Transcribing audio...")
        result = model.transcribe(WAVE_OUTPUT_FILENAME)
        return result.get("text", "No transcription found")
    return "No audio recorded."


@app.route("/start", methods=["GET"])
def start_transcription():
    """Start recording and transcription."""
    global is_listening, audio_thread
    if not is_listening:
        is_listening = True
        audio_thread = threading.Thread(target=record_audio)
        audio_thread.start()
        return jsonify({"status": "started"})
    return jsonify({"status": "already_running"})


@app.route("/stop", methods=["GET"])
def stop_transcription():
    """Stop recording and return transcription."""
    global is_listening, audio_thread
    if is_listening:
        is_listening = False
        audio_thread.join()  # Ensure the thread finishes
        print({"console": "-----------------------"})
        transcription = transcribe_audio()
        return jsonify({"status": "stopped", "transcription": transcription})
    return jsonify({"status": "not_running"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
