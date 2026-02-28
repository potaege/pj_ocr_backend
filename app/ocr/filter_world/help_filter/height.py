import re

def check_height(text: str):
    if not isinstance(text, str):
        return "", False

    t = text.upper().strip()

    # Fix OCR common errors
    t = t.replace(",", ".")
    t = t.replace("I", "1")

    t = re.sub(r'[^0-9]', '', t)

    test = int(t)

    if 50 <= test <= 250:
        return str(test) , True

    return str(test), False
