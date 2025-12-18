from __future__ import annotations
from pathlib import Path
from statistics import mean
from collections import Counter

# Utility Functions 

def is_missing(value: str | None) -> bool:
    """Check if a value should be treated as missing/null."""
    if value is None:
        return True
    cleaned = value.strip().casefold()
    return cleaned in {"", "na", "n/a", "null", "none", "nan"}


def try_float(value: str) -> float | None:
    """Attempt to convert a string to a float, returning None on failure."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def infer_type(values: list[str]) -> str:
    """Infer if a column is numeric or text based on its usable values."""
    usable = [v for v in values if not is_missing(v)]
    if not usable:
        return "text"
    
    for v in usable:
        if try_float(v) is None:
            return "text"
    return "number"


# Main Profiling Logic 

def profile_rows(rows: list[dict[str, str]]) -> dict:
    """
    Main function to profile a list of row dictionaries.
    Calculates metrics for each column and general summary.
    """
    if not rows:
        return {"n_rows": 0, "n_cols": 0, "columns": []}

    n_rows = len(rows)
    columns = list(rows[0].keys())
    col_profiles = []

    for col in columns:
        # Extract all values for this specific column
        values = [r.get(col, "") for r in rows]
        usable = [v for v in values if not is_missing(v)]
        missing = len(values) - len(usable)
        inferred = infer_type(values)
        unique = len(set(usable))

        # Basic profile data
        profile = {
            "name": col,
            "type": inferred,
            "missing": missing,
            "missing_pct": 100.0 * missing / n_rows if n_rows else 0.0,
            "unique": unique,
        }

        # Add numeric statistics if applicable
        if inferred == "number":
            nums = [try_float(v) for v in usable]
            nums = [x for x in nums if x is not None]
            if nums:
                profile.update({
                    "min": min(nums), 
                    "max": max(nums), 
                    "mean": sum(nums) / len(nums)
                })
        
        col_profiles.append(profile)

    return {
        "n_rows": n_rows, 
        "n_cols": len(columns), 
        "columns": col_profiles
    }


# Additional Helper Functions 

def column_values(rows: list[dict[str, str]], col: str) -> list[str]:
    """Helper to extract a list of values for a single column."""
    return [row.get(col, "") for row in rows]


def numeric_stats(values: list[str]) -> dict | None:
    """Calculate detailed numeric statistics for a list of strings."""
    usable_nums = [try_float(v) for v in values if not is_missing(v)]
    nums = [n for n in usable_nums if n is not None]
    
    if not nums:
        return None
    
    return {
        "min": min(nums),
        "max": max(nums),
        "count": len(nums),
        "mean": mean(nums),
        "unique": len(set(nums)),
        "missing": len(values) - len(nums)
    }


def text_stats(values: list[str], top_k: int = 5) -> dict:
    """Calculate frequency stats for text columns."""
    usable = [v for v in values if not is_missing(v)]
    counts = Counter(usable)
    
    return {
        "top": counts.most_common(top_k),
        "unique": len(counts),
        "missing": len(values) - len(usable)
    }