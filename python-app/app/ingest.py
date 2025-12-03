import csv
import hashlib
import logging
import shutil
from pathlib import Path
from typing import Tuple, Dict, Any

from .metadata_store import MetadataStore

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Paths relative to python-app/
ROOT_DIR = Path(__file__).parent.parent
INCOMING_DIR = ROOT_DIR / "data" / "incoming"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
REJECTED_DIR = ROOT_DIR / "data" / "rejected"

MAX_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB arbitrary value. better to configure it via an environment variable


def ensure_dirs() -> None:
    """Create required directories if they don't exist."""
    for d in (INCOMING_DIR, PROCESSED_DIR, REJECTED_DIR):
        d.mkdir(parents=True, exist_ok=True)


def compute_sha256(filepath: Path) -> str:
    """Compute SHA256 hash of the file in chunks."""
    h = hashlib.sha256()
    try:
        with filepath.open("rb") as fh:
            for chunk in iter(lambda: fh.read(8192), b""):  # read next byte of data
                h.update(chunk)
    except IOError as e:
        logging.error(f"Error reading {filepath}: {e}")
        raise
    return h.hexdigest()


def is_csv(filepath: Path) -> bool:
    """Check if file is a valid CSV by detecting dialect and sampling rows. For production ready code, this needs a more
    robust solution. A library like DataGristle for example would be much better"""
    if not filepath.exists() or filepath.stat().st_size == 0:
        return False
    try:
        with filepath.open('r', newline='', encoding='utf-8') as csvfile:
            sample = csvfile.read(4096)
            if not sample.strip():
                return False
            csvfile.seek(0)
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=',\t;|')
            except csv.Error:
                logging.warning(f"Could not detect CSV dialect for {filepath}")
                return False

            # Validate it's actually a CSV
            if not csv.Sniffer().has_header(sample):
                # Not fatal, but if there's no header AND very little structure → suspicious
                # We allow it only if there are clear delimiters
                if all(d not in sample for d in dialect.delimiter):
                    return False
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)

            rows = []
            for i, row in enumerate(reader):
                row = [cell.strip() for cell in row if cell.strip() or not row]
                if not row and i == 0:
                    continue  # skip row if empty
                rows.append(row)
                if len(rows) >= 5000:  # won't scale well if file is too big. A dedicated library is recommended.
                    break
            if len(rows) < 1:
                logging.warning(f"CSV has too few rows ({len(rows)}) in {filepath}") # don't process if the rows are
                # only the title of columns
                return False

            # Check column consistency
            column_counts = {len(row) for row in rows}
            if len(column_counts) != 1:
                logging.warning(f"Inconsistent column counts {column_counts} in {filepath}")
                return False
            return True

    except (csv.Error, IOError) as e:
        logging.warning(f"Failed to validate CSV {filepath}: {e}")
        return False


def validate_file(filepath: Path) -> Tuple[bool, str]:
    """Validate file: existence, size, and CSV format."""
    if not filepath.exists():
        return False, "file not found"
    if filepath.stat().st_size > MAX_SIZE_BYTES:
        return False, "file is too large"
    if not is_csv(filepath):
        return False, "invalid file format: (file is not of CSV format)"
    return True, "ok"


def process_file(filepath: Path, metadata_store: MetadataStore) -> Dict[str, Any]:
    """Process a single file: validate, move, compute hash, store metadata."""
    valid, reason = validate_file(filepath)
    sha = compute_sha256(filepath)
    metadata = {
        "filename": filepath.name,
        "size": filepath.stat().st_size,
        "sha256": sha,
        "status": "processed" if valid else "rejected",
        "reason": "" if valid else reason
    }
    try:
        if valid:
            dest = PROCESSED_DIR / filepath.name
            shutil.move(filepath, dest)
            metadata["path"] = str(dest)
        else:
            dest = REJECTED_DIR / filepath.name
            shutil.move(filepath, dest)
            metadata["path"] = str(dest)
    except shutil.Error as e:
        logging.error(f"Error while moving {filepath} to {dest}: {e}")
        raise
    metadata_store.log_file_processed_entry(metadata)
    return metadata


def run() -> None:
    """Run ingestion once: process all files in incoming dir."""
    ensure_dirs()
    store_path = ROOT_DIR / "metadata.json"
    store = MetadataStore(store_path)
    for f in INCOMING_DIR.iterdir():
        if f.is_file():
            logging.info(f"Processing {f.name}...")
            try:
                md = process_file(f, store)
                logging.info(f" -> {md['status']} {md.get('reason', '')}")
            except Exception as e:
                logging.error(f"Failed to process {f.name}: {e}")


if __name__ == "__main__":
    run()
    logging.info(f"Running...")
