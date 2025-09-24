from app.store import add_client, get_client, next_id
from app.models import CardType
from app.restrictions import is_eligible_for_card, can_purchase_in_country
from app.benefits import compute_benefits

def register_client(*, name: str, country: str, monthlyIncome: float, viseClub: bool, cardType: CardType):
    ok, reason = is_eligible_for_card(
        monthlyIncome=monthlyIncome, viseClub=viseClub, country=country, cardType=cardType
    )
    if not ok:
        return False, reason, None
    cid = next_id()
    add_client({
        "clientId": cid, "name": name, "country": country,
        "monthlyIncome": monthlyIncome, "viseClub": viseClub, "cardType": cardType
    })
    return True, None, {"clientId": cid, "name": name, "cardType": cardType}

def process_purchase(*, clientId: int, amount: float, currency: str, purchaseDate: str, purchaseCountry: str):
    client = get_client(clientId)
    if not client:
        return False, "Cliente no registrado", None

    if not can_purchase_in_country(client["cardType"], purchaseCountry):
        return False, f"El cliente con tarjeta {client['cardType'].value} no puede realizar compras desde {purchaseCountry}", None

    discount, benefit = compute_benefits(
        cardType=client["cardType"],
        clientCountry=client["country"],
        purchaseCountry=purchaseCountry,
        amount=amount,
        purchaseDateISO=purchaseDate
    )
    final_amount = round(amount - discount, 2)
    return True, None, {
        "clientId": clientId,
        "originalAmount": amount,
        "discountApplied": round(discount, 2),
        "finalAmount": final_amount,
        "benefit": benefit
    }