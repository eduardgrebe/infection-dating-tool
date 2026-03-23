# Copyright (C) 2026 Eduard Grebe Consulting (Pty) Ltd
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Integration tests using ExampleData.csv.

These tests exercise the full pipeline — parse_file → calculate_eddis — against
the canonical example dataset that ships with the tool.  Expected results are
derived analytically from the known test properties so the tests are
self-contained and do not depend on a running server or database.

Test code → test name mappings reflect realistic user choices; the same
mappings would be made in the Streamlit UI's mapping step.

Expected adjusted dates (median/non-CI mode)
--------------------------------------------
All delays are rounded to the nearest integer (matching adjust_test_dates).

Subject A
  ApitmaQualNAT       → Aptima VL, DT=30,   delay = log10(30)/0.35 = 4.2203 → 4 days
  GeeniusIndeterminate → Geenius Indet., delay = 24.8 → 25 days

  EP anchor (latest neg adj):  2017-01-10 − 25 = 2016-12-16
  LP anchor (earliest pos adj): 2017-01-10 −  4 = 2017-01-06
  Interval: 21 days  →  EDDI = 2016-12-16 + 10 = 2016-12-26

Subject B
  UnigoldRT  → Unigold, delay = 25.1 → 25 days
  GeeniusFull → Geenius Full, delay = 28.8 → 29 days

  EP anchor: 2016-09-13 − 25 = 2016-08-19  (only negative)
  LP anchor: earliest of {2017-02-04−25=2017-01-10, 2017-02-04−29=2017-01-06} = 2017-01-06
  Interval: 140 days  →  EDDI = 2016-08-19 + 70 = 2016-10-28

Subject C
  AmplicorPooledx10 (VL, DT=4000): delay = log10(4000)/0.35 = 10.2916 → 10 days
  BioRadWesternBlotIndeterminate: delay = 14.8 → 15 days  (appears as both pos and neg)

  EP anchor (latest neg adj): 2014-09-12 − 15 = 2014-08-28
  LP anchor (earliest pos adj): 2014-09-12 − 10 = 2014-09-02
  Interval: 5 days  →  EDDI = 2014-08-28 + 2 = 2014-08-30
  Flags: discordant date (2014-09-12 in both pos & neg), interval < 10 days
"""

from __future__ import annotations

import io
from datetime import date
from pathlib import Path

import pytest

from core.file_parser import get_test_codes, parse_file
from core.eddi import calculate_eddis
from core.test_properties import get_test_properties, VIRAL_LOAD_CATEGORY

EXAMPLE_DATA = Path(__file__).parent.parent / "data" / "ExampleData.csv"

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

# Maps each test code in ExampleData.csv to the canonical test name
TEST_CODE_TO_NAME: dict[str, str] = {
    "ApitmaQualNAT":                  "Aptima HIV-1 RNA Qualitative Assay",
    "GeeniusIndeterminate":           "BioRad Geenius Indeterminate",
    "UnigoldRT":                      "Trinity Biotech Unigold Rapid HIV Test",
    "GeeniusFull":                    "BioRad Geenius Fully Reactive",
    "OraQuickRT-Blood":               "OraSure OraQuick ADVANCE whole blood",
    "CoulterP24":                     "Coulter p24 HIV-1 Antigen Assay",
    "GenscreenV2":                    "BioRad Genscreen HIV-1/2 Version 2 Assay",
    "AmplicorPooledx10":              "Pooled Roche Amplicor Monitor v1.5 (standard sensitivity) (Pool of 10)",
    "BioRadWesternBlotIndeterminate": "BioRad GS HIV-1 Western blot Indeterminate",
    "ARCHITECT":                      "Abbott ARCHITECT HIV Ag/Ab Combo",
    "BioRadWesternBlotFull":          "BioRad GS HIV-1 Western blot Fully Reactive",
}


@pytest.fixture(scope="module")
def mappings() -> dict[str, dict]:
    """Build the mappings dict from test_properties for each code in the example file."""
    result = {}
    for code, name in TEST_CODE_TO_NAME.items():
        props = get_test_properties(name)
        assert props is not None, f"Test '{name}' not found in bundled properties"
        result[code] = {
            "category":               props["category"],
            "diagnostic_delay":       props["diagnostic_delay"],
            "diagnostic_delay_sigma": props["diagnostic_delay_sigma"],
            "detection_threshold":    props["detection_threshold"],
        }
    return result


@pytest.fixture(scope="module")
def parsed_df():
    df, errors = parse_file(EXAMPLE_DATA)
    assert not errors, f"Unexpected parse errors: {errors}"
    return df


@pytest.fixture(scope="module")
def results_median(parsed_df, mappings):
    """EDDI results with credibility intervals disabled (deterministic, median-based)."""
    return calculate_eddis(parsed_df, mappings, calculate_ci=False)


@pytest.fixture(scope="module")
def results_ci(parsed_df, mappings):
    """EDDI results with credibility intervals enabled."""
    return calculate_eddis(parsed_df, mappings, calculate_ci=True, alpha=0.05)


# ---------------------------------------------------------------------------
# 1. File parsing
# ---------------------------------------------------------------------------

class TestFileParsing:
    def test_parses_without_errors(self):
        df, errors = parse_file(EXAMPLE_DATA)
        assert errors == []
        assert df is not None

    def test_row_count(self, parsed_df):
        # 14 data rows in the file (excluding header and trailing blank line)
        assert len(parsed_df) == 14

    def test_subjects(self, parsed_df):
        assert set(parsed_df["Subject"]) == {"Subject A", "Subject B", "Subject C"}

    def test_subject_order_preserved(self, parsed_df):
        assert list(dict.fromkeys(parsed_df["Subject"])) == [
            "Subject A", "Subject B", "Subject C"
        ]

    def test_result_normalisation(self, parsed_df):
        assert set(parsed_df["Result"]) == {"Positive", "Negative"}

    def test_date_types(self, parsed_df):
        assert all(isinstance(d, date) for d in parsed_df["Date"])

    def test_test_codes(self, parsed_df):
        expected_codes = set(TEST_CODE_TO_NAME.keys())
        assert set(parsed_df["Test"]) == expected_codes

    def test_bytesio_input(self):
        """parse_file should accept a BytesIO as returned by st.file_uploader."""
        raw = EXAMPLE_DATA.read_bytes()
        df, errors = parse_file(io.BytesIO(raw))
        assert not errors
        assert len(df) == 14


# ---------------------------------------------------------------------------
# 2. Output structure
# ---------------------------------------------------------------------------

class TestOutputStructure:
    def test_one_row_per_subject(self, results_median):
        assert len(results_median) == 3

    def test_subject_order(self, results_median):
        assert list(results_median["Subject"]) == ["Subject A", "Subject B", "Subject C"]

    def test_required_columns(self, results_median):
        for col in ("Subject", "EP_DDI", "LP_DDI", "Interval_Size", "EDDI", "Flag"):
            assert col in results_median.columns


# ---------------------------------------------------------------------------
# 3. Subject A — median mode (exact dates)
# ---------------------------------------------------------------------------

class TestSubjectAMedian:
    @pytest.fixture(autouse=True)
    def row(self, results_median):
        self.row = results_median[results_median["Subject"] == "Subject A"].iloc[0]

    def test_ep_ddi(self):
        assert self.row["EP_DDI"] == date(2016, 12, 16)

    def test_lp_ddi(self):
        assert self.row["LP_DDI"] == date(2017, 1, 6)

    def test_interval_size(self):
        assert self.row["Interval_Size"] == 21

    def test_eddi(self):
        assert self.row["EDDI"] == date(2016, 12, 26)


# ---------------------------------------------------------------------------
# 4. Subject B — median mode (exact dates)
# ---------------------------------------------------------------------------

class TestSubjectBMedian:
    @pytest.fixture(autouse=True)
    def row(self, results_median):
        self.row = results_median[results_median["Subject"] == "Subject B"].iloc[0]

    def test_ep_ddi(self):
        assert self.row["EP_DDI"] == date(2016, 8, 19)

    def test_lp_ddi(self):
        # Earliest positive adjusted: GeeniusFull wins (2017-01-06 < Unigold's 2017-01-10)
        assert self.row["LP_DDI"] == date(2017, 1, 6)

    def test_interval_size(self):
        assert self.row["Interval_Size"] == 140

    def test_eddi(self):
        assert self.row["EDDI"] == date(2016, 10, 28)


# ---------------------------------------------------------------------------
# 5. Subject C — median mode (exact dates + flags)
# ---------------------------------------------------------------------------

class TestSubjectCMedian:
    @pytest.fixture(autouse=True)
    def row(self, results_median):
        self.row = results_median[results_median["Subject"] == "Subject C"].iloc[0]

    def test_ep_ddi(self):
        # Latest negative adjusted: BioRadWesternBlotIndeterminate neg on 2014-09-12 − 15
        assert self.row["EP_DDI"] == date(2014, 8, 28)

    def test_lp_ddi(self):
        # Earliest positive adjusted: AmplicorPooledx10 on 2014-09-12 − 10
        assert self.row["LP_DDI"] == date(2014, 9, 2)

    def test_interval_size(self):
        assert self.row["Interval_Size"] == 5

    def test_eddi(self):
        assert self.row["EDDI"] == date(2014, 8, 30)

    def test_discordant_date_flag(self):
        # 2014-09-12 appears as both positive (AmplicorPooledx10) and negative
        # (BioRadWesternBlotIndeterminate)
        assert "discordant" in self.row["Flag"].lower()

    def test_small_interval_flag(self):
        assert "less than 10 days" in self.row["Flag"].lower()


# ---------------------------------------------------------------------------
# 6. CI mode — structural properties
# ---------------------------------------------------------------------------

class TestCIMode:
    def test_eddi_between_ep_and_lp(self, results_ci):
        for _, row in results_ci.iterrows():
            if row["EP_DDI"] and row["LP_DDI"] and row["EDDI"]:
                assert row["EP_DDI"] <= row["EDDI"] <= row["LP_DDI"], (
                    f"Subject {row['Subject']}: EDDI {row['EDDI']} not in "
                    f"[{row['EP_DDI']}, {row['LP_DDI']}]"
                )

    def test_ci_flag_present_for_subject_a(self, results_ci):
        row = results_ci[results_ci["Subject"] == "Subject A"].iloc[0]
        assert "credibility interval" in row["Flag"].lower()

    def test_ci_flag_present_for_subject_b(self, results_ci):
        row = results_ci[results_ci["Subject"] == "Subject B"].iloc[0]
        assert "credibility interval" in row["Flag"].lower()

    def test_subject_c_discordant_flag_preserved_under_ci(self, results_ci):
        row = results_ci[results_ci["Subject"] == "Subject C"].iloc[0]
        assert "discordant" in row["Flag"].lower()

    def test_subject_c_ci_widens_narrow_window(self, results_median, results_ci):
        """For Subject C (big_delta = 5 days) CI should produce a wider interval
        than the raw median anchors, because sigma is large relative to the window."""
        med = results_median[results_median["Subject"] == "Subject C"].iloc[0]
        ci  = results_ci[results_ci["Subject"] == "Subject C"].iloc[0]
        assert ci["Interval_Size"] > med["Interval_Size"], (
            f"CI interval ({ci['Interval_Size']}) should be wider than "
            f"median interval ({med['Interval_Size']}) for the 5-day window"
        )

    def test_subject_b_ci_narrows_wide_window(self, results_median, results_ci):
        """For Subject B (big_delta = 140 days) the likelihood peaks well inside
        the window, so the 95% CI should be narrower than the full test-date span."""
        med = results_median[results_median["Subject"] == "Subject B"].iloc[0]
        ci  = results_ci[results_ci["Subject"] == "Subject B"].iloc[0]
        assert ci["Interval_Size"] < med["Interval_Size"], (
            f"CI interval ({ci['Interval_Size']}) should be narrower than "
            f"median interval ({med['Interval_Size']}) for the 140-day window"
        )

    def test_ci_regression_subject_a(self, results_ci):
        """Regression: exact 95% CI dates for Subject A."""
        row = results_ci[results_ci["Subject"] == "Subject A"].iloc[0]
        assert row["EP_DDI"] == date(2016, 12, 12)
        assert row["LP_DDI"] == date(2017, 1, 6)
        assert row["Interval_Size"] == 25

    def test_ci_regression_subject_b(self, results_ci):
        """Regression: exact 95% CI dates for Subject B."""
        row = results_ci[results_ci["Subject"] == "Subject B"].iloc[0]
        assert row["EP_DDI"] == date(2016, 8, 22)
        assert row["LP_DDI"] == date(2017, 1, 4)
        assert row["Interval_Size"] == 135

    def test_ci_regression_subject_c(self, results_ci):
        """Regression: exact 95% CI dates for Subject C."""
        row = results_ci[results_ci["Subject"] == "Subject C"].iloc[0]
        assert row["EP_DDI"] == date(2014, 8, 24)
        assert row["LP_DDI"] == date(2014, 9, 5)
        assert row["Interval_Size"] == 12
