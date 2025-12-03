import json
import logging
from pathlib import Path
from typing import List, Dict, Any
import threading


class MetadataStore:
    def __init__(self, path: Path):
        """
        Initialize the metadata store with a JSON file path.
        Normally, I would have built a store with SQLITE databases or Postgres for better congruence,
        But this will do for this project.
        Creates parent directories and an empty file if it doesn't exist.
        Still supports thread safety
        """
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()  # Thread safety to avoid race conditions
        if not self.path.exists():
            self._write([])

    def _read(self) -> List[Dict[str, Any]]:
        """Read the JSON list from file, handling errors."""
        try:
            with self.path.open("r") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error while reading {self.path}: {e}.")
            return []

    def _write(self, items: List[Dict[str, Any]]) -> None:
        """Write the JSON list to file."""
        try:
            with self.path.open("w") as fh:
                json.dump(items, fh, indent=2)
        except IOError as e:
            logging.error(f"Error while writing to {self.path}: {e}")
            raise

    def log_file_processed_entry(self, item: Dict[str, Any]) -> None:
        """Log file processed entry to the data store. We only add metadata here"""
        with self._lock:
            items = self._read()
            items.append(item)
            self._write(items)
        logging.info(f"Added metadata for {item.get('filename', 'unknown')}")

    def list_processed_files(self) -> List[Dict[str, Any]]:
        """List all processed files items."""
        return self._read()
