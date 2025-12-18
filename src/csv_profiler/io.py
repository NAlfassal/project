from __future__ import annotations
from csv import DictReader
from pathlib import Path
import csv

# Basic implementation of reading CSV rows
def read_csv_rows_v1(path: str | Path) -> list[dict[str, str]]:
    path = Path(path)
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = DictReader(f)
        return [dict(row) for row in reader]

# Improved implementation with error handling
def read_csv_rows(path: Path) -> list[dict[str, str]]:
    # Check if the file exists before opening
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")
    
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        # Raise an error if the CSV file is empty
        if not rows:
            raise ValueError("CSV has no data rows")
            
        return rows
