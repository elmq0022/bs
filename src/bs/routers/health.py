from fastapi import APIRouter

router = APIRouter(prefix="/health")


@router.get("/v1")
async def status():
    return {"status": "ok"}
