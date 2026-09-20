from dataclasses import FrozenInstanceError

import pytest

from atlas.domain.data_source import DataSource


def make_data_source(**overrides: object) -> DataSource:
    values: dict[str, object] = {
        "identifier": "sec-10k-aapl-2023",
        "title": "Apple Inc. FY2023 Form 10-K",
        "uri": "https://www.sec.gov/edgar/data/320193/000032019323000106/aapl-20230930.htm",
        "content": "Item 1. Business... Apple designs, manufactures and markets smartphones...",
        "source_type": "sec_edgar",
    }
    values.update(overrides)

    return DataSource(**values)  # type: ignore[arg-type]


def test_data_source_initialization_and_normalization() -> None:
    source = make_data_source(
        identifier="  sec-10k-aapl-2023  ",
        title="  Apple Inc. FY2023 Form 10-K  ",
        uri="  https://example.com/filing  ",
        source_type="  sec_edgar  ",
    )

    assert source.identifier == "sec-10k-aapl-2023"
    assert source.title == "Apple Inc. FY2023 Form 10-K"
    assert source.uri == "https://example.com/filing"
    assert source.source_type == "SEC_EDGAR"
    assert source.metadata == {}


def test_data_source_with_custom_metadata() -> None:
    source = make_data_source(metadata={"cik": "0000320193", "year": 2023})

    assert source.metadata["cik"] == "0000320193"
    assert source.metadata["year"] == 2023


def test_data_source_is_immutable() -> None:
    source = make_data_source()

    with pytest.raises(FrozenInstanceError):
        source.title = "New Title"  # type: ignore[misc]

    with pytest.raises(TypeError):
        source.metadata["new_key"] = "value"  # type: ignore[index]


@pytest.mark.parametrize("invalid_id", ["", "   "])
def test_data_source_rejects_blank_identifier(invalid_id: str) -> None:
    with pytest.raises(ValueError, match="identifier"):
        make_data_source(identifier=invalid_id)


def test_data_source_rejects_non_string_identifier() -> None:
    with pytest.raises(TypeError, match="identifier"):
        make_data_source(identifier=12345)


@pytest.mark.parametrize("invalid_title", ["", "   "])
def test_data_source_rejects_blank_title(invalid_title: str) -> None:
    with pytest.raises(ValueError, match="title"):
        make_data_source(title=invalid_title)


def test_data_source_rejects_non_string_title() -> None:
    with pytest.raises(TypeError, match="title"):
        make_data_source(title=None)


@pytest.mark.parametrize("invalid_uri", ["", "   "])
def test_data_source_rejects_blank_uri(invalid_uri: str) -> None:
    with pytest.raises(ValueError, match="uri"):
        make_data_source(uri=invalid_uri)


def test_data_source_rejects_non_string_uri() -> None:
    with pytest.raises(TypeError, match="uri"):
        make_data_source(uri=100)


@pytest.mark.parametrize("invalid_type", ["", "   "])
def test_data_source_rejects_blank_source_type(invalid_type: str) -> None:
    with pytest.raises(ValueError, match="source_type"):
        make_data_source(source_type=invalid_type)


def test_data_source_rejects_non_string_source_type() -> None:
    with pytest.raises(TypeError, match="source_type"):
        make_data_source(source_type=False)


def test_data_source_rejects_non_string_content() -> None:
    with pytest.raises(TypeError, match="content"):
        make_data_source(content=12345)


def test_data_source_rejects_non_mapping_metadata() -> None:
    with pytest.raises(TypeError, match="metadata"):
        make_data_source(metadata=["not", "a", "mapping"])


def test_data_source_rejects_non_string_metadata_keys() -> None:
    with pytest.raises(TypeError, match="metadata keys"):
        make_data_source(metadata={123: "invalid_key"})
