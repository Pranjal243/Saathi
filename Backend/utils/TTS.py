from gtts import gTTS
import os
from datetime import datetime

def text_to_speech(data):
    text = data.get("text", "")
    lang = data.get("lang", "en")  # Default language is English

    if not text:
        return {"error": "No text provided"}

    try:
        # Create the directory if it does not exist
        output_dir = "ChatAudio"
        os.makedirs(output_dir, exist_ok=True)

        # Generate a timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_path = os.path.join(output_dir, f"{timestamp}.wav")

        # Generate TTS audio
        tts = gTTS(text=text, lang=lang)
        tts.save(output_path)

        # Return success response with the file name
        return {"message": "Audio generated successfully", "audio_file": output_path}

    except Exception as e:
        return {"message": f"Error generating audio: {str(e)}"}
