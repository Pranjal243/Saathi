import cohere
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Set your Cohere API key
COHERE_API_KEY = os.environ.get("COHERE_API_KEY")

# Initialize the Cohere client
co = cohere.Client(COHERE_API_KEY)

# Set the model to use
MODEL = "command-r-08-2024"

PROMPT_PREAMBLE = "You are a Nepali AI agent to assist people who knows Nepali only. Use transliteration english unless specified otherwise. Answer very briefly and crisply, do not provide unnecessary informations. Always answer in 2-3 lines max. "

# Function to send a message and save chat history
def send_message(message):  
    # Send the message to the Cohere model
    response = co.chat(
        model=MODEL,
        message= PROMPT_PREAMBLE+ message,
        temperature=0.7,
        connectors=[{"id": "web-search"}],
        conversation_id='test3',
    )
    return response.text

# Start the conversation
print("Chatbot: Namastey!! Tapaiko Kasari madad garna sakchhu?")
while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("Chatbot: Goodbye!")
        break
    assistant_response = send_message(user_input)
    print("Chatbot:", assistant_response)

print("Conversation ended.")
