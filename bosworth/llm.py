from langchain_ollama import ChatOllama

from bosworth.ollama_models import OllamaModel


DEFAULT_MODEL_NAME = OllamaModel.LLAMA3_2

def get_llama(model_name: OllamaModel = DEFAULT_MODEL_NAME) -> ChatOllama:
    # TODO - auto run `ollama run llama3.2` here rather than in separate shell
    return ChatOllama(
        model=model_name,
        temperature=0.2,  # low temp helps reliability
        top_p=0.9,  # helps output diversity, lower for more deterministic
        num_predict=512,
        stop=["<|eot_id|>"],  # sometimes needed for Ollama’s internal stopping
    )


DEFAULT_LLM = get_llama()
