import json
import pytest
from pathlib import Path

from app.metadata_store import MetadataStore


@pytest.mark.parametrize(
    "items_to_add, expected_count",
    [
        ([], 0),  # Empty array returned when an error occurs while parsing a file
        ([{"filename": "test1.csv", "status": "processed"}], 1),
        ([{"filename": "test1.csv", "status": "processed"}, {"filename": "test2.csv", "status": "rejected"}], 2),
    ],
)
def test_add_and_list(tmp_path: Path, items_to_add: list, expected_count: int) -> None:
    """Test add and list items."""
    p = tmp_path / "metadata.json"
    s = MetadataStore(p)
    for item in items_to_add:
        s.log_file_processed_entry(item)
    out = s.list_processed_files()
    assert isinstance(out, list)
    assert len(out) == expected_count
    if items_to_add:
        assert out[-1] == items_to_add[-1]


def test_list_with_corrupted_file(tmp_path: Path) -> None:
    """Test listing returns empty list on corrupted JSON."""
    p = tmp_path / "metadata.json"
    p.write_text("invalid json")  # Corrupt the file
    s = MetadataStore(p)
    out = s.list_processed_files()
    assert out == []


def test_add_after_corruption(tmp_path: Path) -> None:
    """Test adding after corruption overwrites/recovers."""
    p = tmp_path / "metadata.json"
    p.write_text("invalid json")
    s = MetadataStore(p)
    s.log_file_processed_entry({"filename": "recovered.csv", "status": "processed"})
    out = s.list_processed_files()
    assert len(out) == 1
    assert out[0]["filename"] == "recovered.csv"


def test_file_persistence(tmp_path: Path) -> None:
    """Test data persists in file after add."""
    p = tmp_path / "metadata.json"
    s = MetadataStore(p)
    s.log_file_processed_entry({"filename": "persist.csv", "status": "processed"})
    # Reload from file directly
    with p.open("r") as f:
        data = json.load(f)
    assert len(data) == 1
    assert data[0]["status"] == "processed"
