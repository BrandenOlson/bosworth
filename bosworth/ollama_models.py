from enum import Enum

class OllamaModel(str, Enum):
    LLAMA3_2 = "llama3.2"
    MISTRAL = "mistral"

if __name__ == "__main__":
    for model in OllamaModel:
        print(model.value)
