from fastapi import FastAPI

from bs import articles

app = FastAPI()
app.include_router(router=articles.router)
