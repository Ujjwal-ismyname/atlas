from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping


def _normalize_non_empty_text(value: object, field_name: str) -> str:
    """Normalize required text while preserving its casing."""
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")

    normalized_value = value.strip()

    if not normalized_value:
        raise ValueError(f"{field_name} must not be blank")

    return normalized_value


def _normalize_required_text(value: object, field_name: str) -> str:
    """Normalize non-empty text input to uppercase."""
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")

    normalized_value = value.strip().upper()

    if not normalized_value:
        raise ValueError(f"{field_name} must not be blank")

    return normalized_value


@dataclass(frozen=True)
class DataSource:
    """An immutable reference to an external document, filing, or knowledge source."""

    identifier: str
    title: str
    uri: str
    content: str
    source_type: str
    metadata: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        normalized_identifier = _normalize_non_empty_text(
            self.identifier,
            "identifier",
        )
        normalized_title = _normalize_non_empty_text(self.title, "title")
        normalized_uri = _normalize_non_empty_text(self.uri, "uri")
        normalized_source_type = _normalize_required_text(
            self.source_type,
            "source_type",
        )

        if not isinstance(self.content, str):
            raise TypeError("content must be a string")

        if not isinstance(self.metadata, Mapping):
            raise TypeError("metadata must be a mapping")

        for key in self.metadata:
            if not isinstance(key, str):
                raise TypeError("metadata keys must be strings")

        object.__setattr__(self, "identifier", normalized_identifier)
        object.__setattr__(self, "title", normalized_title)
        object.__setattr__(self, "uri", normalized_uri)
        object.__setattr__(self, "source_type", normalized_source_type)
        object.__setattr__(self, "content", self.content)
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))
