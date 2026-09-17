from decimal import Decimal
from dataclasses import FrozenInstanceError

import pytest

from atlas.domain.portfolio import Position

def make_position(**overrides : object) -> Position:
    values: dict[str,object] = {
        "symbol": "AAPL",
        "quantity":Decimal("10"),
        "average_cost":Decimal("185.50"),
        "currency":"USD",
    }
    values.update(overrides)

    return Position(**values)


def test_position_normalizes_symbol_and_currency() -> None:
    position = make_position(symbol = " aapl ", currency = "usd")

    assert position.symbol == "AAPL"
    assert position.currency == "USD"
    assert position.quantity == Decimal("10")
    assert position.average_cost == Decimal("185.50")

def test_position_allows_zero_average_cost()->None:
    position = make_position(average_cost = Decimal("0"))
    assert position.average_cost == Decimal("0")

@pytest.mark.parametrize("invalid_symbol", [""," "])
def test_position_rejects_blank_symbol(invalid_symbol: str) -> None:
    with pytest.raises(ValueError, match="symbol"):
        make_position(symbol=invalid_symbol)

@pytest.mark.parametrize("invalid_currency",["","US","USDD","U5D","UŚD"])
def test_position_rejects_invalid_currency(invalid_currency: str) -> None:
    with pytest.raises(ValueError, match = "currency"):
        make_position(currency = invalid_currency)

@pytest.mark.parametrize(
    "invalid_quantity",
    [
        Decimal("0"),
        Decimal("-1"),
        Decimal("NaN"),
        Decimal("Infinity"),
    ],
)
def test_position_rejects_invalid_quantity(invalid_quantity: Decimal) -> None:
    with pytest.raises(ValueError, match="quantity"):
        make_position(quantity = invalid_quantity)

@pytest.mark.parametrize(
    "invalid_average_cost",
    [
        Decimal("-0.01"),
        Decimal("NaN"),
        Decimal("Infinity"),
    ],
)
def test_position_rejects_invalid_average_cost(
    invalid_average_cost: Decimal,
) -> None:
    with pytest.raises(ValueError, match="average_cost"):
        make_position(average_cost=invalid_average_cost)


def test_position_rejects_non_decimal_quantity() -> None:
    with pytest.raises(TypeError, match="quantity"):
        make_position(quantity=10)


def test_position_rejects_non_decimal_average_cost() -> None:
    with pytest.raises(TypeError, match="average_cost"):
        make_position(average_cost=185.50)


def test_position_is_immutable() -> None:
    position = make_position()

    with pytest.raises(FrozenInstanceError):
        position.symbol = "MSFT"