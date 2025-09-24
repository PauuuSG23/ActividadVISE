from fastapi import APIRouter
from ..schemas import PurchaseInput, PurchaseApproved, RejectResponse
from ..services import process_purchase

router = APIRouter(prefix="/purchase", tags=["purchase"])

@router.post("", responses={200: {"model": PurchaseApproved}, 400: {"model": RejectResponse}})
def post_purchase(payload: PurchaseInput):
    ok, reason, data = process_purchase(**payload.model_dump())
    if not ok:
        return {"status": "Rejected", "error": reason}
    return {"status": "Approved", "purchase": data}