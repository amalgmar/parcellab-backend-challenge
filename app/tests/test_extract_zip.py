from app.utils.extract_zip import extract_zip


def test_extract_zip_valid():
    assert extract_zip("Street 10, 75001 Paris, France") == "75001"


def test_extract_zip_invalid():
    assert extract_zip("No zip here") == ""
