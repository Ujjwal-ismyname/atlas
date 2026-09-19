from dataclasses import FrozenInstanceError
from decimal import Decimal

import pytest

from atlas.domain.portfolio import Portfolio, Position


def make_position(**overrides: object) -> Position:
    values: dict[str, object] = {
        "symbol": "AAPL",
        "quantity": Decimal("10"),
        "average_cost": Decimal("185.50"),
        "currency": "USD",
    }
    values.update(overrides)

    return Position(**values)


def test_position_normalizes_symbol_and_currency() -> None:
    position = make_position(symbol=" aapl ", currency="usd")

    assert position.symbol == "AAPL"
    assert position.currency == "USD"
    assert position.quantity == Decimal("10")
    assert position.average_cost == Decimal("185.50")


def test_position_allows_zero_average_cost() -> None:
    position = make_position(average_cost=Decimal("0"))

    assert position.average_cost == Decimal("0")


@pytest.mark.parametrize("invalid_symbol", ["", "   "])
def test_position_rejects_blank_symbol(invalid_symbol: str) -> None:
    with pytest.raises(ValueError, match="symbol"):
        make_position(symbol=invalid_symbol)


@pytest.mark.parametrize(
    "invalid_currency",
    ["", "US", "USDD", "U5D", "UŚD"],
)
def test_position_rejects_invalid_currency(invalid_currency: str) -> None:
    with pytest.raises(ValueError, match="currency"):
        make_position(currency=invalid_currency)


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
        make_position(quantity=invalid_quantity)


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


def make_portfolio(**overrides: object) -> Portfolio:
    values: dict[str, object] = {
        "identifier": "retirement-core",
        "name": "Retirement Core",
        "positions": (),
    }
    values.update(overrides)

    return Portfolio(**values)


def test_portfolio_stores_its_positions_as_a_tuple() -> None:
    position = make_position()

    portfolio = make_portfolio(positions=[position])

    assert portfolio.identifier == "retirement-core"
    assert portfolio.name == "Retirement Core"
    assert portfolio.positions == (position,)
    assert isinstance(portfolio.positions, tuple)


def test_portfolio_allows_no_positions() -> None:
    portfolio = make_portfolio()
    assert portfolio.positions == ()


def test_portfolio_snapshots_a_mutable_positions_input() -> None:
    source_positions = [make_position(symbol="AAPL")]

    portfolio = make_portfolio(positions=source_positions)

    source_positions.append(make_position(symbol="MSFT"))

    assert portfolio.positions == (make_position(symbol="AAPL"),)


@pytest.mark.parametrize("invalid_identifier", ["", "   "])
def test_portfolio_rejects_blank_identifier(invalid_identifier: str) -> None:
    with pytest.raises(ValueError, match="identifier"):
        make_portfolio(identifier=invalid_identifier)


@pytest.mark.parametrize("invalid_name", ["", "   "])
def test_portfolio_rejects_blank_name(invalid_name: str) -> None:
    with pytest.raises(ValueError, match="name"):
        make_portfolio(name=invalid_name)


def test_portfolio_rejects_duplicate_position_symbols() -> None:
    first = make_position(symbol="AAPL")
    duplicate = make_position(symbol=" aapl ")

    with pytest.raises(ValueError, match="duplicate"):
        make_portfolio(positions=[first, duplicate])


def test_portfolio_is_immutable() -> None:
    portfolio = make_portfolio()

    with pytest.raises(FrozenInstanceError):
        portfolio.name = "Different Name"


def test_portfolio_exposes_symbols_in_position_order() -> None:
    portfolio = make_portfolio(
        positions=[
            make_position(symbol="MSFT"),
            make_position(symbol="AAPL"),
        ],
    )

    assert portfolio.symbols == ("MSFT", "AAPL")
    assert isinstance(portfolio.symbols, tuple)


def test_empty_portfolio_exposes_no_symbols() -> None:
    portfolio = make_portfolio()

    assert portfolio.symbols == ()
