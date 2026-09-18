from dataclasses import dataclass
from decimal import Decimal


def _normalize_required_text(value: object, field_name: str) -> str:
    """Normalize non-empty text input to uppercase."""
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")

    normalized_value = value.strip().upper()

    if not normalized_value:
        raise ValueError(f"{field_name} must not be blank")

    return normalized_value


def _validate_decimal(
    value: object,
    field_name: str,
    *,
    must_be_positive: bool,
) -> Decimal:
    """Validate a finite Decimal financial value."""
    if not isinstance(value, Decimal):
        raise TypeError(f"{field_name} must be a Decimal")

    if not value.is_finite():
        raise ValueError(f"{field_name} must be finite")

    if must_be_positive and value <= Decimal("0"):
        raise ValueError(f"{field_name} must be greater than zero")

    if not must_be_positive and value < Decimal("0"):
        raise ValueError(f"{field_name} must not be negative")

    return value


@dataclass(frozen=True)
class Position:
    """A long-only holding in a portfolio."""

    symbol: str
    quantity: Decimal
    average_cost: Decimal
    currency: str

    def __post_init__(self) -> None:
        normalized_symbol = _normalize_required_text(self.symbol, "symbol")
        normalized_currency = _normalize_required_text(self.currency, "currency")

        if (
            len(normalized_currency) != 3
            or not normalized_currency.isascii()
            or not normalized_currency.isalpha()
        ):
            raise ValueError("currency must be a three-letter ASCII alphabetic code")

        validated_quantity = _validate_decimal(
            self.quantity,
            "quantity",
            must_be_positive=True,
        )
        validated_average_cost = _validate_decimal(
            self.average_cost,
            "average_cost",
            must_be_positive=False,
        )

        object.__setattr__(self, "symbol", normalized_symbol)
        object.__setattr__(self, "currency", normalized_currency)
        object.__setattr__(self, "quantity", validated_quantity)
        object.__setattr__(self, "average_cost", validated_average_cost)
