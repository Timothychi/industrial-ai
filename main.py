from fastapi import FastAPI

from app.api.chat import router as chat_router

app = FastAPI()


@app.get("/")
async def hello():
    return {
        "message": "Industrial AI is running"
    }


app.include_router(chat_router)