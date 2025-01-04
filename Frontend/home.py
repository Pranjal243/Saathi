import streamlit as st
import speech_recognition as sr
import requests
from gtts import gTTS
import io
import cohere

# Speech-to-text function
def transcribe_audio():
    recognizer = sr.Recognizer()
    audio = st.audio_input("Press recorder icon below to ask your question")
    if audio is not None:
            print("Audio coming")
            audio_bytes = audio.read()
            audio_file = io.BytesIO(audio_bytes)  # Create a BytesIO object from the audio bytes
            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data,language='ne-NP')
                return text
            except sr.UnknownValueError:
                return "Sorry, I could not understand that. Please record voice again."
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
    
def chat(question):
    # translate_api="http://127.0.0.1:5000/qa"
    # data = {
    # "question": question_eng
    # }   
    # try:
    #     response = requests.post(translate_api, json=data)
    #     response.raise_for_status()  # Raise an exception for 4xx or 5xx responses
    #     return response.json()  # Return the JSON response from the API
    # except requests.exceptions.RequestException as e:
    #     return {"answer": f"API request failed: {e}"}
    cohere_api_key = "8eNnHvBCvhU4E2im58t5AKQUcXrgcHqMzZ4Oxvmc"
    co = cohere.ClientV2(cohere_api_key)

    # Function to generate an answer using Cohere
    # PROMPT_PREAMBLE = """
    # तपाईं एक बुद्धिमान र मैत्री प्रयोगकर्ता सहायक हुनुहुन्छ। तपाईं प्रयोगकर्ताको सोधिएको प्रश्नहरूको जवाफ दिनुहुन्छ। तपाईं स्पष्ट, सटीक र उपयोगी जानकारी दिन खोज्नुहुन्छ। तपाईंले सधैं नेपालीमा जवाफ दिनुहुन्छ। कृपया उपयोगकर्ताको प्रश्नलाई बुझेर राम्रोसँग उत्तर दिनुहोस्।

    # प्रश्न: 
    # """
    try:
        # Generate answer using Cohere's language model
        response = co.chat(
            model="command-r",
            messages=[
                {"role": "system", "content": "You are assisting Nepali people, always answer in Nepali. Translate english to nepali and return the result"},
                {"role": "user", "content": question}
            ],
        )
        answer = response.message.content[0].text
        return answer
    except Exception as e:
        return f"Error generating answer with Cohere: {e}"

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
    answer = chat(question)
    print(answer)
    response = f"{answer}"
    st.session_state.messages.append({"user": False, "text": response})
    st.session_state.messages.append({"user": True, "text": question})
    audio_buffer = generate_audio(answer)
    st.audio(audio_buffer, format="audio/mp3")

for msg in reversed(st.session_state.messages):
    if msg["user"]:
        st.markdown(f"""
            <div style="background-color: #E1F5FE; padding: 10px; margin: 5px; border-radius: 10px; max-width: 70%; float: leftt;">
                <strong>You:</strong> {msg['text']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="background-color: #FFEBEE; padding: 10px; margin: 5px; border-radius: 10px; max-width: 70%; float: right;">
                <strong>Bot:</strong> {msg['text']}
            </div>
            """, unsafe_allow_html=True)

# # Audio Play Button for Bot Response
# if "messages" in st.session_state and len(st.session_state.messages) > 0:
#     last_message = st.session_state.messages[0]
#     if last_message["user"]:  # If last message is from the bot
        
