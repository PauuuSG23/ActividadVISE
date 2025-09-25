from pydantic import BaseModel,Field
from typing import Optional

from .models import CardType, Currency


class ClientCreate(BaseModel):
    name: str = Field(min_length=1)
    country: str = Field(min_length=1)
    monthlyIncome: float = Field(ge=0)
    visaClub: bool
    cardType: CardType

class ClientRegistered(BaseModel):
    clientId: int
    name: str
    cardType: CardType
    status: str = "Registered"
    message: str


class RejectResponse(BaseModel):
    status: str = "Rejected"
    error: str


class PurchaseInput(BaseModel):
    clientId: int
    amount: float = Field(gt=0)
    currency: Currency
    purchaseDate: str  # ISO8601, ej "2025-09-20T14:30:00Z"
    purchaseCountry: str


class PurchaseInfo(BaseModel):
    clientId: int
    originalAmount: float
    discountApplied: float
    finalAmount: float
    benefit: str


class PurchaseApproved(BaseModel):
    status: str = "Approved"
    purchase: PurchaseInfo
