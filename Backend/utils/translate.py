from translatepy import Translator

def translate_text(data):
    text = data.get("text", "")
    source_lang = data.get("source_language", "auto")  # Default is "auto" (auto-detect)
    target_lang = data.get("target_language", "en")  # Default is English
    
    if not text:
        return {"error": "No text provided"}
    
    translator = Translator()
    
    try:
        # Translate text to the target language
        translation = translator.translate(text, source_lang, target_lang)
        return {"data": translation.result}
    
    except Exception as e:
        return {"data": f"Error translating text: {str(e)}"}

