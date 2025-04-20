"""Unit tests for ZIP code extraction utility."""

from app.utils.extract_zip import extract_zip


def test_extract_zip_valid() -> None:
    """Tests extraction of ZIP code from a valid address."""

    assert extract_zip('Street 10, 75001 Paris, France') == '75001'


def test_extract_zip_invalid() -> None:
    """Tests ZIP extraction returns None for invalid addresses."""

    assert extract_zip('No zip here') == ''
