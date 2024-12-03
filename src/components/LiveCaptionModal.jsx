import React, { useState } from "react";
import axios from "axios";
import {
  modalStyles,
  captionTextStyles,
  recordButtonStyles,
} from "../styles/modalStyles";

function LiveCaptionModal() {
  const [isListening, setIsListening] = useState(false);
  const [transcription, setTranscription] = useState("Click the button");

  const toggleListening = () => {
    if (isListening) {
      // Stop transcription
      axios.get("http://127.0.0.1:5000/stop").then((res) => {
        setIsListening(false);
        setTranscription(res.data.result);
      });
    } else {
      // Start transcription
      axios.get("http://127.0.0.1:5000/start").then(() => {
        setIsListening(true);
        setTranscription("Transcribing system audio...");
      });
    }
  };

  return (
    <div style={modalStyles}>
      <p style={captionTextStyles}>{transcription}</p>
      <button onClick={toggleListening} style={recordButtonStyles}>
        {isListening ? "Stop" : "Start"}
      </button>
    </div>
  );
}

export default LiveCaptionModal;
