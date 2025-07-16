from langchain_ollama import ChatOllama

from bosworth.ollama_models import OllamaModel


DEFAULT_MODEL_NAME = OllamaModel.LLAMA3_2

def get_llama(model_name: OllamaModel = DEFAULT_MODEL_NAME) -> ChatOllama:
    return ChatOllama(model=model_name)


DEFAULT_LLM = get_llama()
