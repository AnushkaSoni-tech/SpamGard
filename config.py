import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# API Key
API_key = os.getenv("GEMINI_API_KEY")

# Model Name
gemini_model= "gemini-2.5-flash"

# Temperature
temp = 0

# path

OUTDIR = "\Data"