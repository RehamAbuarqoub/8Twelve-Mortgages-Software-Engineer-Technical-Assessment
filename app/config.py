import os
from dotenv import load_dotenv

# Load values from the .env file
load_dotenv()

# Get the Groq API key from the environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Get the model name from the environment
# If it is missing, use this default model
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")