import pytest
from pathlib import Path

from app.ingest import compute_sha256, validate_file, process_file
from app.metadata_store import MetadataStore


def create_csv(path: Path, content: str = "col1,col2\n1,2\n3,4\n") -> None:
    """Utility function to create a CSV file"""
    path.write_text(content)


def test_compute_sha256(tmp_path: Path) -> None:
    """Test SHA256 computation on a simple file."""
    f = tmp_path / "temp.csv"
    f.write_text("a")
    s = compute_sha256(f)
    assert isinstance(s, str)
    assert len(s) == 64
    # exact hash value for the char "a" do not touch
    assert s == "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb"


@pytest.mark.parametrize(
    "file_content, expected_valid, expected_reason",
    [
        ("col1,col2\n1,2\n", True, "ok"),  # valid CSV file
        ("invalid text", False, "invalid file format: (file is not of CSV format)"),  # invalid CSV file
        ("", False, "invalid file format: (file is not of CSV format)"),  # empty file
    ],
)
def test_validate_file(tmp_path: Path, file_content: str, expected_valid: bool, expected_reason: str) -> None:
    """Test file validation for various cases."""
    f = tmp_path / "test.csv"
    f.write_text(file_content)
    valid, reason = validate_file(f)
    assert valid == expected_valid
    assert reason == expected_reason


def test_validate_file_not_found(tmp_path: Path) -> None:
    """Test validation for non-existent file."""
    f = tmp_path / "missing.csv"
    valid, reason = validate_file(f)
    assert not valid
    assert reason == "file not found"


def test_validate_file_too_large(tmp_path: Path, monkeypatch) -> None:
    """Test validation for oversized file."""
    from app import ingest
    monkeypatch.setattr(ingest, "MAX_SIZE_BYTES", 5)  # patch max size
    f = tmp_path / "large.csv"
    f.write_text("a" * 10)  # > 5 bytes supported this will no longer fail if we set a different convention of course
    valid, reason = validate_file(f)
    assert not valid
    assert reason == "file is too large"


def test_process_file_valid(monkeypatch, tmp_path: Path) -> None:
    """Test processing a valid file with mocked dirs."""
    base = tmp_path / "proj"
    incoming_dir = base / "data" / "incoming"
    processed_dir = base / "data" / "processed"
    rejected_dir = base / "data" / "rejected"
    incoming_dir.mkdir(parents=True)  # recursive path creation, didn't know that
    processed_dir.mkdir(parents=True)
    rejected_dir.mkdir(parents=True)

    # Patch globals in ingest.py to use temp dirs
    from app import ingest
    monkeypatch.setattr(ingest, "INCOMING_DIR", incoming_dir)
    monkeypatch.setattr(ingest, "PROCESSED_DIR", processed_dir)
    monkeypatch.setattr(ingest, "REJECTED_DIR", rejected_dir)

    # Create valid CSV
    incoming = incoming_dir / "valid.csv"
    create_csv(incoming)
    store_path = base / "metadata.json"
    store = MetadataStore(store_path)
    metadata = process_file(incoming, store)

    assert metadata["status"] == "processed"
    assert "sha256" in metadata and len(metadata["sha256"]) == 64
    assert (processed_dir / "valid.csv").exists()
    assert not incoming.exists()  # File has been moved so we expect this to fail

    processed_files = store.list_processed_files()
    assert len(processed_files) == 1
    assert processed_files[0]["filename"] == "valid.csv"
    assert processed_files[0]["status"] == "processed"


def test_process_invalid_file(monkeypatch, tmp_path: Path) -> None:
    """Test processing an invalid file, with patched dirs."""
    base = tmp_path / "proj"
    incoming_dir = base / "data" / "incoming"
    processed_dir = base / "data" / "processed"
    rejected_dir = base / "data" / "rejected"
    incoming_dir.mkdir(parents=True)
    processed_dir.mkdir(parents=True)
    rejected_dir.mkdir(parents=True)

    # Patch globals
    from app import ingest
    monkeypatch.setattr(ingest, "INCOMING_DIR", incoming_dir)
    monkeypatch.setattr(ingest, "PROCESSED_DIR", processed_dir)
    monkeypatch.setattr(ingest, "REJECTED_DIR", rejected_dir)

    # Create an invalid file
    incoming = incoming_dir / "bad_file.txt"
    incoming.write_text("invalid")
    store_path = base / "metadata.json"
    store = MetadataStore(store_path)
    metadata = process_file(incoming, store)

    assert metadata["status"] == "rejected"
    assert metadata["reason"] == "invalid file format: (file is not of CSV format)"
    assert (rejected_dir / "bad_file.txt").exists()
    assert not incoming.exists()  # File has been moved so we expect this to fail

    processed_files = store.list_processed_files()
    assert len(processed_files) == 1
    assert processed_files[0]["status"] == "rejected"
