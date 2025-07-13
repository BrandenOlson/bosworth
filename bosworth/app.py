from uuid import uuid4
from typing import Literal

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from bosworth.graph import invoke_agent, AgentResponse

app = FastAPI()


class PingResponse(BaseModel):
    ping: Literal["pong"]

@app.get("/ping")
def ping() -> PingResponse:
    return PingResponse(ping="pong")


class ChatRequest(BaseModel):
    query: str
    conversation_id: str = str(uuid4())



@app.post("/chat")
def chat(request: ChatRequest) -> AgentResponse:
    return invoke_agent(
        query=request.query,
        conversation_id=request.conversation_id,
    )


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
