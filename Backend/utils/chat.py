import cohere
from serpapi import GoogleSearch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Initialize Cohere client
cohere_api_key = "8eNnHvBCvhU4E2im58t5AKQUcXrgcHqMzZ4Oxvmc"
co = cohere.Client(cohere_api_key)

# Function to generate an answer using Cohere
PROMPT_PREAMBLE = """
तपाईं एक बुद्धिमान र मैत्री प्रयोगकर्ता सहायक हुनुहुन्छ। तपाईं प्रयोगकर्ताको सोधिएको प्रश्नहरूको जवाफ दिनुहुन्छ। तपाईं स्पष्ट, सटीक र उपयोगी जानकारी दिन खोज्नुहुन्छ। तपाईंले सधैं नेपालीमा जवाफ दिनुहुन्छ। कृपया उपयोगकर्ताको प्रश्नलाई बुझेर राम्रोसँग उत्तर दिनुहोस्।

प्रश्न: 
"""
def generate_answer_cohere(question):
    try:
        # Generate answer using Cohere's language model
        response = co.chat(
            model="command-r",
            message= PROMPT_PREAMBLE+ question,
            temperature=0.7,
            connectors=[{"id": "web-search"}],
            conversation_id='test3',
        )
        answer = response.text
        return answer
    except Exception as e:
        return f"Error generating answer with Cohere: {e}"

# Function to perform a web search using SerpAPI
def search_web(question, api_key):
    try:
        search = GoogleSearch({"q": question, "api_key": api_key})
        results = search.get_dict()
        if "organic_results" in results:
            snippet = results["organic_results"][0].get("snippet", "No snippet available.")
            return snippet
        return "No results found."
    except Exception as e:
        return f"Error during web search: {e}"

# Combined function for question answering
def question_answering_service(question, api_key=None):
    if not question:
        return {"error": "No question provided"}
    # Attempt to generate an answer using Cohere
    cohere_answer = generate_answer_cohere(question)
    if cohere_answer:
        if "Sorry, I couldn't find" in cohere_answer or not cohere_answer.strip():
            web_answer = search_web(question, api_key)
            if web_answer:
                return {"source": "Web Search", "answer": web_answer}
        return {"source": "Cohere Model", "answer": cohere_answer}

    # Final fallback if everything fails
    return {"source": "None", "answer": "Could not generate an answer."}
