import streamlit as st
import speech_recognition as sr
import requests
from gtts import gTTS
import io

# Speech-to-text function
def transcribe_audio():
    recognizer = sr.Recognizer()
    audio = st.audio_input("Record a voice message")
    if audio is not None:
            print("Audio coming")
            st.audio(audio)
            audio_bytes = audio.read()
            audio_file = io.BytesIO(audio_bytes)  # Create a BytesIO object from the audio bytes
            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data,language='ne-NP')
                return text
            except sr.UnknownValueError:
                return "Sorry, I could not understand that."
            except sr.RequestError as e:
                return f"Error: {e}"
    else:
        print("audio-data is not coming")
        
#translate question to english
def translate(question,src,target):
    translate_api="http://127.0.0.1:5000/translate"
    data= {
        "text": question,
        "source_language": src,
        "target_language": target
    }  
    try:
        response = requests.post(translate_api, json=data)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx responses
        return response.json()  # Return the JSON response from the API
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}
    
#translate question to english
def chat(question_eng):
    translate_api="http://127.0.0.1:5000/qa"
    data = {
    "question": question_eng
    }   
    try:
        response = requests.post(translate_api, json=data)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx responses
        return response.json()  # Return the JSON response from the API
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}

# Function to generate audio
def generate_audio(text):
    lang='ne'
    tts = gTTS(text=text, lang=lang)
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer

# Streamlit UI
st.title("तपाइँको साथी")
st.write("तपाईंको प्रश्न तलको माइक्रोफोन बटन प्रयोग गरेर सोध्नुहोस्।")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input: Voice button
question = transcribe_audio()
if question:
    st.session_state.messages.append({"user": True, "text": question})
    answer = chat(question)
    print(answer)
    response = f"{answer['answer']}"
    st.session_state.messages.append({"user": False, "text": response})

    # Play the audio file
    # audio_file = generate_audio(answer_org['data'])
    # st.audio(audio_file, format="audio/mp3")

for msg in st.session_state.messages:
    if msg["user"]:
        # Display user messages on the left side with a unique color
        st.markdown(f"""
            <div style="background-color: #E1F5FE; padding: 10px; margin: 5px; border-radius: 10px; max-width: 70%; float: left;">
                <strong>You:</strong> {msg['text']}
            </div>
            """, unsafe_allow_html=True)
    else:
        # Display bot messages on the right side with a different color
        st.markdown(f"""
            <div style="background-color: #FFEBEE; padding: 10px; margin: 5px; border-radius: 10px; max-width: 70%; float: right;">
                <strong>Bot:</strong> {msg['text']}
            </div>
            """, unsafe_allow_html=True)

# Audio Play Button for Bot Response
if "messages" in st.session_state and len(st.session_state.messages) > 0:
    last_message = st.session_state.messages[-1]
    if not last_message["user"]:  # If last message is from the bot
        audio_buffer = generate_audio(last_message["text"])
        st.audio(audio_buffer, format="audio/mp3")
