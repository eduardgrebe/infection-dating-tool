"""
Load and query the bundled HIV diagnostic test properties.

The CSV has a non-standard structure:
  Row 0: viral_load_growth_rate metadata (default growth rate value)
  Row 1: column headers
  Row 2+: one test per row
"""

import math
from functools import lru_cache
from pathlib import Path

import pandas as pd

DATA_FILE = Path(__file__).parent.parent / "data" / "diagnostic_tests_and_properties.csv"

VIRAL_LOAD_CATEGORY = "Viral Load"
DEFAULT_GROWTH_RATE = 0.35


@lru_cache(maxsize=1)
def _load() -> tuple[float, pd.DataFrame]:
    """
    Parse the bundled CSV and return (growth_rate, tests_df).

    tests_df columns:
        test_id, test_name, category, diagnostic_delay,
        diagnostic_delay_sigma, detection_threshold
    """
    # Growth rate is in the second field of the first row
    with open(DATA_FILE) as fh:
        first_line = fh.readline()
    growth_rate_str = first_line.split(",")[1].strip()
    growth_rate = float(growth_rate_str) if growth_rate_str else DEFAULT_GROWTH_RATE

    df = pd.read_csv(DATA_FILE, skiprows=1)

    df = df.rename(columns={
        "viral_load_detection_threshold": "detection_threshold",
    })

    keep = [
        "test_id",
        "test_name",
        "test_category",
        "diagnostic_delay",
        "diagnostic_delay_sigma",
        "detection_threshold",
    ]
    df = df[keep].copy()
    df = df.rename(columns={"test_category": "category"})

    # Coerce numeric columns; invalid parses become NaN
    for col in ("diagnostic_delay", "diagnostic_delay_sigma", "detection_threshold"):
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return growth_rate, df


def get_default_growth_rate() -> float:
    """Return the default viral load growth rate (log10 copies/ml/day)."""
    growth_rate, _ = _load()
    return growth_rate


def get_tests_df() -> pd.DataFrame:
    """Return the full test properties DataFrame."""
    _, df = _load()
    return df.copy()


def get_test_names() -> list[str]:
    """Return a sorted list of all test names."""
    _, df = _load()
    return sorted(df["test_name"].tolist())


def get_categories() -> list[str]:
    """Return a sorted list of unique test categories."""
    _, df = _load()
    return sorted(df["category"].dropna().unique().tolist())


def get_tests_by_category() -> dict[str, list[str]]:
    """Return {category: [test_name, ...]} mapping, each list sorted."""
    _, df = _load()
    result: dict[str, list[str]] = {}
    for cat, group in df.groupby("category"):
        result[str(cat)] = sorted(group["test_name"].tolist())
    return result


def get_test_properties(test_name: str) -> dict | None:
    """
    Return the properties dict for a named test, or None if not found.

    Keys: test_id, test_name, category, diagnostic_delay,
          diagnostic_delay_sigma, detection_threshold
    """
    _, df = _load()
    matches = df[df["test_name"] == test_name]
    if matches.empty:
        return None
    row = matches.iloc[0].to_dict()
    # Replace NaN with None for cleaner downstream handling
    return {k: (None if isinstance(v, float) and math.isnan(v) else v)
            for k, v in row.items()}


def is_viral_load(test_name: str) -> bool:
    """Return True if the named test is a Viral Load assay."""
    props = get_test_properties(test_name)
    return props is not None and props.get("category") == VIRAL_LOAD_CATEGORY
