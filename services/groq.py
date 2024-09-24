import os
from groq import Groq
from dotenv import load_dotenv
import re
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
         {"role": "system", "content": "You are a helpful assistant. Generate 6 segments for a video script based on the user's query. each of the segments should have prompts for images related to the segments in the next paragraph"},
        {
            "role": "user",
            "content": user_message
        }
    ]

    # Call the Groq API
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=0.2,
        seed=10,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None,
    )

    # Collect the response from the Groq API
    response_text = ""
    for chunk in completion:
        response_text += chunk.choices[0].delta.content or ""

    return response_text
    # segments = parse_video_script(response_text)
    # output_dir = "output_images"
    # os.makedirs(output_dir, exist_ok=True)
    # generate_and_save_images(segments, output_dir)



def parse_video_script(response):
    """Parse the video script response into structured segments."""
    segments = []
    segment_pattern = re.compile(r'Segment \d+: (.+?)\nTitle: "(.+?)"\nPrompt: (.+?)\n\n(.+?)(?=\n\n|\$)', re.DOTALL)

    matches = segment_pattern.findall(response)

    for match in matches:
        segment_number, title, prompt, text = match
        segments.append({
            "segment_number": segment_number,
            "title": title,
            "prompt": prompt,
            "text": text.strip()
        })

    return segments






