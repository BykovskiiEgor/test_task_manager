from fastapi import APIRouter

index_router = APIRouter()


@index_router.get("/")
def healthcheck() -> dict:
    return {"status": "ok"}