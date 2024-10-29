from fastapi import APIRouter

router_v1 = APIRouter(prefix="/v1/health")


@router_v1.get("/")
async def status():
    return {"status": "ok"}
