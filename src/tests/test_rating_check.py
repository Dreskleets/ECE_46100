# tests/test_rating_check.py
import builtins
from src import Admin

def test_rating_check_valid():
    # rating_check currently returns the (string) rating when valid
    assert Admin.rating_check("5") == "5"

def test_rating_check_invalid_then_valid(monkeypatch):
    # Simulate user entering invalid value "11" then valid "3"
    answers = iter(["11", "3"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(answers))
    result = Admin.rating_check("11")
    assert result == "3"
