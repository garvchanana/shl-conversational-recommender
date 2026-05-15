import os

from groq import Groq
from dotenv import load_dotenv


# -----------------------------------
# Load Environment Variables
# -----------------------------------

load_dotenv()


# -----------------------------------
# Initialize Groq Client
# -----------------------------------

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# -----------------------------------
# Default Model
# -----------------------------------

MODEL_NAME = "llama-3.3-70b-versatile"


# -----------------------------------
# Generate LLM Response
# -----------------------------------

def generate_response(prompt):

    try:

        response = client.chat.completions.create(

            model=MODEL_NAME,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an SHL assessment recommendation assistant. "
                        "Recommend only from provided assessment context."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.3,
            max_tokens=500
        )

        content = response.choices[0].message.content

        if not content:

            return (
                "Unable to generate recommendations "
                "at the moment."
            )

        return content.strip()

    except Exception as e:

        print(f"[ERROR] Groq API Error: {e}")

        return (
            "An internal recommendation error occurred. "
            "Please try again."
        )