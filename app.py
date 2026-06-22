from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.predict import (
    router as predict_router
)

from api.recommend import router

from api.chat_completions import (
    router as chat_router
)


app = FastAPI(
    title="Lead Intelligence API",
    version="1.0"
)

app.include_router(router)
app.include_router(chat_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(predict_router)


@app.get("/")
def home():

    return {
        "status": "running"
    }


@app.get("/health")
def health():

    return {
        "status": "ok",
        "version": "1.0"
    }