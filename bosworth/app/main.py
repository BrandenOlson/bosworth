import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from bosworth.agent import invoke_agent

app = FastAPI()


@app.get("/ping")
def ping():
    return {"Hello": "World"}


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    content: str


@app.post("/chat")
def chat(request: ChatRequest) -> ChatResponse:
    return ChatResponse(content=invoke_agent(query=request.query))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)