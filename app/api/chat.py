from fastapi import APIRouter
from pydantic import BaseModel

from app.agent.process_agent import ProcessAgent

router = APIRouter()

agent = ProcessAgent()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
async def chat(request: ChatRequest):

    answer = await agent.run(request.message)

    return {
        "message": answer
    }