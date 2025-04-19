import re


def extract_zip(address: str) -> str:
    match = re.search(r"\b(\d{4,5})\b", address)
    return match.group(1) if match else ""
