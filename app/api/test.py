from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/test", tags=["test"])


@router.get("/ping")
def ping():
    return {
        "status": "ok",
        "message": "API is working"
    }


class EchoRequest(BaseModel):
    name: str
    age: int


@router.post("/echo")
def echo(data: EchoRequest):
    return {
        "received": data,
        "message": "POST test success"
    }
