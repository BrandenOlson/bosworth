from langchain_ollama import ChatOllama


def get_llama() -> ChatOllama:
    # TODO - auto run `ollama run llama3.2` here rather than in separate shell
    return ChatOllama(
        model="llama3.2",
        temperature=0.2,  # ✅ low temp helps reliability
        top_p=0.9,  # ✅ helps output diversity, lower for more deterministic
        num_predict=512,  # ✅ increase for longer outputs
        stop=["<|eot_id|>"],  # ✅ sometimes needed for Ollama’s internal stopping
    )


DEFAULT_LLM = get_llama()
