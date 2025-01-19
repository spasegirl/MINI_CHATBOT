import os
from dotenv import load_dotenv

load_dotenv()

# Configuration settings
UPLOAD_FOLDER = "static/uploads/"
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
