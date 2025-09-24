from datetime import datetime, timezone
from .models import CardType

def _parse_utc(iso: str) -> datetime:
    # Acepta "...Z" y lo convierte a offset UTC
    if iso.endswith("Z"):
        iso = iso[:-1] + "+00:00"
    dt = datetime.fromisoformat(iso)
    # asegura tz-aware en UTC
    return dt.astimezone(timezone.utc)

def compute_benefits(*, cardType: CardType, clientCountry: str, purchaseCountry: str, amount: float, purchaseDateISO: str):
    """
    Regresa (discount: float, benefit: str).
    DOW: Monday=0 ... Sunday=6 (datetime.weekday()).
    """
    dt = _parse_utc(purchaseDateISO)
    dow = dt.weekday()  # 0=Mon ... 6=Sun
    is_mon_tue_wed = dow in (0, 1, 2)
    is_weekday = dow <= 4
    is_weekend = dow >= 5
    is_foreign = (purchaseCountry != clientCountry)

    discount = 0.0
    benefit = "Sin beneficio aplicado"

    if cardType == CardType.Classic:
        return discount, benefit

    if cardType == CardType.Gold:
        if is_mon_tue_wed and amount > 100:
            return amount * 0.15, "Lun-Mar-Mié - Descuento 15%"

    elif cardType == CardType.Platinum:
        if is_mon_tue_wed and amount > 100:
            return amount * 0.20, "Lun-Mar-Mié - Descuento 20%"
        elif dow == 5 and amount > 200:  # Saturday
            return amount * 0.30, "Sábado - Descuento 30%"
        elif is_foreign:
            return amount * 0.05, "Compra exterior - Descuento 5%"

    elif cardType == CardType.Black:
        if is_mon_tue_wed and amount > 100:
            return amount * 0.25, "Lun-Mar-Mié - Descuento 25%"
        elif dow == 5 and amount > 200:
            return amount * 0.35, "Sábado - Descuento 35%"
        elif is_foreign:
            return amount * 0.05, "Compra exterior - Descuento 5%"

    elif cardType == CardType.White:
        if is_weekday and amount > 100:
            return amount * 0.25, "Lun-Vie - Descuento 25%"
        elif is_weekend and amount > 200:
            return amount * 0.35, "Sábado-Domingo - Descuento 35%"
        elif is_foreign:
            return amount * 0.05, "Compra exterior - Descuento 5%"

    return discount, benefit