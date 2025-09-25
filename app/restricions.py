from .models import CardType


# normaliza strings (quita tildes y pone minúsculas)
def _norm(s: str) -> str:
    import unicodedata
    return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().strip().lower()

PROHIBITED_COUNTRIES_NORM = {_norm(x) for x in ["China", "Vietnam", "India", "Irán"]}

def is_eligible_for_card(*, monthlyIncome: float, viseClub: bool, country: str, cardType: CardType):
    """Valida elegibilidad de la tarjeta, según el enunciado."""
    # Classic: sin restricciones
    if cardType == CardType.Classic:
        return True, None
    # Gold: ingreso mínimo 500
    if cardType == CardType.Gold:
        return (monthlyIncome >= 500, "Ingreso mínimo de 500 USD mensuales requerido para Gold") if monthlyIncome < 500 else (True, None)
    # Platinum: ingreso 1000 + VISE CLUB
    if cardType == CardType.Platinum:
        if monthlyIncome < 1000:
            return False, "Ingreso mínimo de 1000 USD mensuales requerido para Platinum"
        if not viseClub:
            return False, "Suscripción VISE CLUB requerida para Platinum"
        return True, None
    # Black / White: ingreso 2000 + VISE CLUB + NO residir en países prohibidos
    if cardType in (CardType.Black, CardType.White):
        if monthlyIncome < 2000:
            return False, f"Ingreso mínimo de 2000 USD mensuales requerido para {cardType.value}"
        if not viseClub:
            return False, f"Suscripción VISE CLUB requerida para {cardType.value}"
        if _norm(country) in PROHIBITED_COUNTRIES_NORM:
            return False, f"Clientes residentes en China, Vietnam, India e Irán no son aptos para {cardType.value}"
        return True, None
    return False, "Tipo de tarjeta no soportado"

def can_purchase_in_country(cardType: CardType, purchaseCountry: str) -> bool:
    """Bloquea compras para Black/White en países prohibidos."""
    if cardType in (CardType.Black, CardType.White) and _norm(purchaseCountry) in PROHIBITED_COUNTRIES_NORM:
        return False
    return True