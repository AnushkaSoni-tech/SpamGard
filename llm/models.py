from langchain_google_genai import ChatGoogleGenerativeAI
from config import gemini_model, API_key , temp

def get_model():
    if not API_key:
        raise RuntimeError("API Key is missing")
    return ChatGoogleGenerativeAI(
        model=gemini_model,
        api_key=API_key,
        temperature=temp)
