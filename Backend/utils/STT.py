import speech_recognition as sr
import os
from datetime import datetime

def speech_to_text(data):
    # Check if the user provided an audio file
    audio_file_path = data.get("audio_file", None)

    if audio_file_path:
        # Process the provided audio file
        if not os.path.exists(audio_file_path):
            return {"error": "Audio file does not exist"}
        
        try:
            recognizer = sr.Recognizer()

            with sr.AudioFile(audio_file_path) as source:
                audio = recognizer.record(source)
            
            # Convert speech to text
            print("Processing audio...")
            text = recognizer.recognize_google(audio)
            return {"message": "Audio processed successfully", "text": text, "audio_file": audio_file_path}

        except sr.UnknownValueError:
            return {"message": "Speech recognition could not understand audio"}
        except sr.RequestError as e:
            return {"message": f"Could not request results from speech recognition service: {str(e)}"}
        except Exception as e:
            return {"message": f"Error processing audio: {str(e)}"}

    else:
        # Record audio from the microphone
        try:
            recognizer = sr.Recognizer()

            # Create the directory if it does not exist
            output_dir = "userAudio"
            os.makedirs(output_dir, exist_ok=True)

            # Generate a timestamp
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            output_path = os.path.join(output_dir, f"{timestamp}.wav")

            with sr.Microphone() as source:
                print("Please speak into the microphone...")
                recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
                audio = recognizer.listen(source)

            # Save the recorded audio
            with open(output_path, "wb") as audio_file:
                audio_file.write(audio.get_wav_data())

            # Convert speech to text
            print("Processing recorded audio...")
            text = recognizer.recognize_google(audio)

            # Return success response
            return {"message": "Audio recorded and processed successfully", "text": text, "audio_file": output_path}

        except sr.UnknownValueError:
            return {"message": "Speech recognition could not understand audio"}
        except sr.RequestError as e:
            return {"message": f"Could not request results from speech recognition service: {str(e)}"}
        except Exception as e:
            return {"message": f"Error processing audio: {str(e)}"}
