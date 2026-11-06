from decimal import Decimal, InvalidOperation

API = "http://127.0.0.1:8001"


def parse_amount(text: str, allow_zero: bool = False) -> Decimal | None:
    try:
        value = Decimal(text.strip().replace(" ", "").replace(",", "."))
    except InvalidOperation:
        return None
    if value < 0 or (value == 0 and not allow_zero):
        return None
    return value

def error_message(r) -> str:
    detail = r.json().get("detail")
    if isinstance(detail, list):
        return "Données invalides : " + "; ".join(d["msg"] for d in detail)
    return str(detail)