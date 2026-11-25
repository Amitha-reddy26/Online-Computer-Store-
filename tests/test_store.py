import pytest
from src.store import validate_quantity

def test_valid_quantity():
    assert validate_quantity(2) == 2

def test_invalid_quantity():
    with pytest.raises(ValueError):
        validate_quantity(0)

def test_negative_quantity():
    with pytest.raises(ValueError):
        validate_quantity(-1)
