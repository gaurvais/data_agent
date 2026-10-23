from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

def pick_llm(Level : str):
    """
    Pick the appropriate LLM based on the level of complexity.

    Args:
        Level (str): The level of complexity ('basic', 'intermediate', 'advanced').

    Returns:
        str: The name of the selected LLM.
    """
    if Level.lower() == "low":
        llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0)
    elif Level.lower() == "medium":
        llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash", temperature=0)
    elif Level.lower() == "high":
        llm = ChatGoogleGenerativeAI(model="gemini-3.1-pro-preview", temperature=0)
    else:
        raise ValueError(f"Unsupported level: {Level}")

    return llm
