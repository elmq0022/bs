from fastapi import FastAPI

from contextlib import asynccontextmanager

from bs.routers import articles, health
from bs.db import run_async_upgrade


@asynccontextmanager
async def lifespan(app: FastAPI):
    await run_async_upgrade()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router=articles.router_v1)
app.include_router(router=health.router_v1)
