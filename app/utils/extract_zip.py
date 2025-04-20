"""Utility functions for extracting ZIP codes from addresses."""

import re


def extract_zip(address: str) -> str:
    """Extracts ZIP code from a given address string."""
    match = re.search(r'\b(\d{4,5})\b', address)
    return match.group(1) if match else ''
