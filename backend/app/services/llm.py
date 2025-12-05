from langchain_groq import ChatGroq
from app.core.config import settings


def get_llm(model_name: str, temperature: float = 0.7):
    return ChatGroq(
        model=model_name,
        temperature=temperature,
        api_key=settings.GROQ_API_KEY,
        max_retries=2
    )