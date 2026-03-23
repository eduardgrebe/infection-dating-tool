"""
Parse and validate subject test history CSV files.

Expected columns (case-insensitive, order-independent):
    Subject, Date, Test, Result

Date format: YYYY-MM-DD
Result values: positive / pos / +  →  'Positive'
               negative / neg / -  →  'Negative'
"""

from __future__ import annotations

import io
from datetime import date, datetime

import pandas as pd

REQUIRED_COLUMNS = {"Subject", "Date", "Test", "Result"}

POSITIVE_VALUES = {"positive", "pos", "+"}
NEGATIVE_VALUES = {"negative", "neg", "-"}


def _normalise_result(value: str) -> str | None:
    v = str(value).strip().lower()
    if v in POSITIVE_VALUES:
        return "Positive"
    if v in NEGATIVE_VALUES:
        return "Negative"
    return None


def _parse_date(value: str) -> date | None:
    try:
        return datetime.strptime(str(value).strip(), "%Y-%m-%d").date()
    except ValueError:
        return None


def parse_file(
    file_obj: io.BytesIO | io.StringIO | str,
) -> tuple[pd.DataFrame | None, list[str]]:
    """
    Parse an uploaded subject test history file.

    Parameters
    ----------
    file_obj : file-like object (BytesIO from st.file_uploader, path string, etc.)

    Returns
    -------
    (df, errors)
        df     : DataFrame with columns Subject (str), Date (datetime.date),
                 Test (str), Result ('Positive'|'Negative') — or None on failure.
        errors : list of human-readable error strings (empty on full success).
    """
    errors: list[str] = []

    # --- Read raw CSV ---
    try:
        raw = pd.read_csv(file_obj, dtype=str, skip_blank_lines=True)
    except Exception as exc:
        return None, [f"Could not read file: {exc}"]

    # Strip whitespace from column names and handle UTF-8 BOM
    raw.columns = [c.strip().lstrip("\ufeff") for c in raw.columns]

    # --- Check required columns ---
    missing = REQUIRED_COLUMNS - set(raw.columns)
    if missing:
        return None, [
            f"Missing required column(s): {', '.join(sorted(missing))}. "
            f"File must contain: Subject, Date, Test, Result."
        ]

    # Drop rows that are entirely empty
    raw = raw.dropna(how="all").reset_index(drop=True)

    if raw.empty:
        return None, ["File contains no data rows."]

    # --- Validate and transform row by row ---
    subjects = []
    dates = []
    tests = []
    results = []

    for i, row in raw.iterrows():
        row_num = i + 2  # 1-based, accounting for header row

        # Skip rows where all four fields are blank
        if all(pd.isna(row.get(c, None)) or str(row.get(c, "")).strip() == ""
               for c in REQUIRED_COLUMNS):
            continue

        # Date
        date_val = _parse_date(row["Date"]) if pd.notna(row["Date"]) else None
        if date_val is None:
            errors.append(
                f"Row {row_num}: invalid date '{row['Date']}' — expected YYYY-MM-DD."
            )

        # Result
        result_val = _normalise_result(row["Result"]) if pd.notna(row["Result"]) else None
        if result_val is None:
            errors.append(
                f"Row {row_num}: invalid result '{row['Result']}' — "
                f"expected positive/pos/+ or negative/neg/-."
            )

        subjects.append(str(row["Subject"]).strip())
        dates.append(date_val)
        tests.append(str(row["Test"]).strip())
        results.append(result_val)

    if errors:
        return None, errors

    df = pd.DataFrame({
        "Subject": subjects,
        "Date": dates,
        "Test": tests,
        "Result": results,
    })

    return df, []


def get_test_codes(df: pd.DataFrame) -> list[str]:
    """Return the unique test codes present in a parsed DataFrame, in order of first appearance."""
    seen: set[str] = set()
    codes: list[str] = []
    for code in df["Test"]:
        if code not in seen:
            seen.add(code)
            codes.append(code)
    return codes
