from typing import Literal

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from bosworth.agent import invoke_agent

app = FastAPI()


class PingResponse(BaseModel):
    ping: Literal["pong"]

@app.get("/ping")
def ping() -> PingResponse:
    return PingResponse(ping="pong")


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    content: str


@app.post("/chat")
def chat(request: ChatRequest) -> ChatResponse:
    return ChatResponse(content=invoke_agent(query=request.query))


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)