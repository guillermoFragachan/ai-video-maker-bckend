import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Load the Groq API key from environment variables
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable not set")

# Initialize the Groq client
client = Groq(api_key=groq_api_key)

def send_message_to_groq(user_message):
    # Prepare the messages for the Groq API
    messages = [
        {
            "role": "user",
            "content": user_message
        }
    ]

    # Call the Groq API
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    # Collect the response from the Groq API
    response_text = ""
    for chunk in completion:
        response_text += chunk.choices[0].delta.content or ""

    return response_text
