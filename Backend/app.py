from flask import Flask, request, jsonify
from utils.TTS import text_to_speech
from utils.STT import speech_to_text
from utils.translate import translate_text
from utils.chat import question_answering_service

app = Flask(__name__)

# API for Text to Speech (TTS)
@app.route('/tts', methods=['POST'])
def text_to_speech_api():
    data = request.get_json()
    result = text_to_speech(data)
    return jsonify(result)

# API for Speech to Text (STT)
@app.route('/stt', methods=['POST'])
def speech_to_text_api():
    data = request.get_json()
    result = speech_to_text(data)
    return jsonify(result)

# API for Translation
@app.route('/translate', methods=['POST'])
def translate_api():
    data = request.get_json()
    result = translate_text(data)
    return jsonify(result)

SERPAPI_KEY = "bd81357e3619736d57c9d72882111f8265f1119be015648baf2ca6dae299ba8c"
@app.route('/qa', methods=["POST"])
def qa_api():
    try:
        data = request.get_json()

        # Validate input
        if "question" not in data:
            return jsonify({"error": "Missing 'question' parameter"}), 400

        question = data["question"]
        
        # Call the service function
        result = question_answering_service(question, SERPAPI_KEY)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
