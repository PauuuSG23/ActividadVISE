from fastapi import APIRouter
from ..schemas import ClientCreate, ClientRegistered, RejectResponse
from ..services import register_client

router = APIRouter(prefix="/client", tags=["client"])

@router.post("", responses={200: {"model": ClientRegistered}, 400: {"model": RejectResponse}})
def post_client(payload: ClientCreate):
    ok, reason, data = register_client(**payload.model_dump())
    if not ok:
        return {"status": "Rejected", "error": reason}
    return {
        "clientId": data["clientId"],
        "name": data["name"],
        "cardType": data["cardType"],
        "status": "Registered",
        "message": f"Cliente apto para tarjeta {data['cardType'].value}"
    }