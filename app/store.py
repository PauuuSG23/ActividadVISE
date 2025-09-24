from typing import Dict, TypedDict
from .models import CardType

class Client(TypedDict):
    clientId: int
    name: str
    country: str
    monthlyIncome: float
    viseClub: bool
    cardType: CardType

CLIENTS: Dict[int, Client] = {}
SEQ = 1

def add_client(c: Client) -> None:
    CLIENTS[c["clientId"]] = c

def next_id() -> int:
    global SEQ
    cid = SEQ
    SEQ += 1
    return cid

def get_client(client_id: int) -> Client | None:
    return CLIENTS.get(client_id)

def reset_store():
    global CLIENTS, SEQ
    CLIENTS = {}
    SEQ = 1