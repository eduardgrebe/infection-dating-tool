"""
EDDI (Estimated Date of Detectable Infection) calculation pipeline.

The pipeline has three stages:
  1. adjust_test_dates  — apply diagnostic delays to raw test dates
  2. _calculate_subject_eddi — compute EP-DDI/LP-DDI/EDDI for one subject
  3. calculate_eddis    — run the full pipeline over all subjects in a DataFrame

Mappings dict structure (one entry per test code found in the uploaded file):
    {
        "TEST_CODE": {
            "category": str,              # e.g. "Viral Load", "3rd Gen Lab Assay ..."
            "diagnostic_delay": float | None,   # days; None for viral load tests
            "diagnostic_delay_sigma": float | None,
            "detection_threshold": float | None,  # copies/ml; viral load tests only
        }
    }
"""

from __future__ import annotations

import math
from datetime import date, timedelta

import pandas as pd

from .calculations import find_ci_limits, find_delta_scale
from .test_properties import VIRAL_LOAD_CATEGORY

DEFAULT_GROWTH_RATE = 0.35
DEFAULT_ALPHA = 0.05


# ---------------------------------------------------------------------------
# Stage 1: date adjustment
# ---------------------------------------------------------------------------

def adjust_test_dates(
    df: pd.DataFrame,
    mappings: dict[str, dict],
    growth_rate: float = DEFAULT_GROWTH_RATE,
) -> pd.DataFrame:
    """
    Return a copy of df with four new columns:
        adjusted_date    (datetime.date)
        diagnostic_delay (float, days)
        sigma            (float, days)
        warning          (str)

    For viral load tests the diagnostic delay is derived from the detection
    threshold: delay = log10(threshold) / growth_rate.
    If sigma is absent, a relative standard error of 20% is assumed.
    """
    df = df.copy()

    adj_dates: list[date] = []
    delays: list[float] = []
    sigmas: list[float] = []
    warnings: list[str] = []

    for _, row in df.iterrows():
        code = row["Test"]
        props = mappings.get(code, {})
        category = props.get("category", "")

        if category == VIRAL_LOAD_CATEGORY:
            threshold = props.get("detection_threshold")
            if threshold is None or not math.isfinite(threshold) or threshold <= 0:
                raise ValueError(
                    f"Test '{code}' is a Viral Load assay but has no valid "
                    f"detection threshold in its mapping."
                )
            diagnostic_delay = math.log10(threshold) / growth_rate
        else:
            diagnostic_delay = props.get("diagnostic_delay")
            if diagnostic_delay is None or not math.isfinite(diagnostic_delay):
                raise ValueError(
                    f"Test '{code}' has no valid diagnostic delay in its mapping."
                )

        sigma = props.get("diagnostic_delay_sigma")
        warning = ""
        if sigma is None or not math.isfinite(sigma):
            sigma = 0.2 * diagnostic_delay
            warning = (
                f"Sigma unknown. RSE of 20% used "
                f"(d={diagnostic_delay:.2f}, sigma={sigma:.2f})"
            )

        adj_delay = int(round(diagnostic_delay))
        adjusted_date = row["Date"] - timedelta(days=adj_delay)

        adj_dates.append(adjusted_date)
        delays.append(diagnostic_delay)
        sigmas.append(sigma)
        warnings.append(warning)

    df["adjusted_date"] = adj_dates
    df["diagnostic_delay"] = delays
    df["sigma"] = sigmas
    df["warning"] = warnings
    return df


# ---------------------------------------------------------------------------
# Stage 2: per-subject EDDI
# ---------------------------------------------------------------------------

def _check_identical_dates(subject_df: pd.DataFrame) -> str:
    if subject_df["Date"].nunique() == 1:
        return "All tests reported are on same date. "
    return ""


def _check_discordant_dates(subject_df: pd.DataFrame) -> str:
    pos_dates = set(subject_df.loc[subject_df["Result"] == "Positive", "Date"])
    neg_dates = set(subject_df.loc[subject_df["Result"] == "Negative", "Date"])
    if pos_dates & neg_dates:
        return "Subject has a discordant test date. "
    return ""


def _calculate_subject_eddi(
    subject_df: pd.DataFrame,
    calculate_ci: bool = True,
    alpha: float = DEFAULT_ALPHA,
) -> dict:
    """
    Compute EP-DDI, LP-DDI, EDDI and diagnostic flags for a single subject.

    subject_df must already have adjusted_date, diagnostic_delay, sigma columns
    (i.e. the output of adjust_test_dates filtered to one subject).

    Returns a dict with keys: ep_ddi, lp_ddi, eddi, interval_size, flag.
    """
    flag = _check_identical_dates(subject_df)

    positives = subject_df[subject_df["Result"] == "Positive"].sort_values("adjusted_date")
    negatives = subject_df[subject_df["Result"] == "Negative"].sort_values("adjusted_date")

    has_pos = not positives.empty
    has_neg = not negatives.empty

    # EP-DDI anchor: latest negative; LP-DDI anchor: earliest positive
    lp_row = positives.iloc[0] if has_pos else None
    ep_row = negatives.iloc[-1] if has_neg else None

    ep_ddi: date | None = None
    lp_ddi: date | None = None
    eddi: date | None = None
    interval_size: int | None = None
    ci_failed = False

    # --- Cannot calculate EDDI without both positive and negative results ---
    if not has_pos or not has_neg:
        if not has_pos:
            flag += "Only negative tests reported. "
            ep_ddi = ep_row["adjusted_date"]
        if not has_neg:
            flag += "Only positive tests reported. "
            lp_ddi = lp_row["adjusted_date"]
        return {
            "ep_ddi": ep_ddi, "lp_ddi": lp_ddi,
            "eddi": None, "interval_size": None,
            "flag": flag.strip(),
        }

    neg_adjusted: date = ep_row["adjusted_date"]
    neg_delay: float = ep_row["diagnostic_delay"]
    neg_sigma: float = ep_row["sigma"]

    pos_adjusted: date = lp_row["adjusted_date"]
    pos_delay: float = lp_row["diagnostic_delay"]
    pos_sigma: float = lp_row["sigma"]

    big_delta = (pos_adjusted - neg_adjusted).days

    use_ci = calculate_ci
    if use_ci and big_delta <= 0:
        use_ci = False
        flag += (
            "Credibility interval cannot be calculated if results are "
            "in unexpected order. "
        )

    # --- Credibility interval path ---
    if use_ci:
        delta1, scale1, error = find_delta_scale(neg_delay, neg_sigma)
        delta2, scale2, error2 = find_delta_scale(pos_delay, pos_sigma)
        error = error or error2

        if not error:
            ep_ddi_t, lp_ddi_t, error = find_ci_limits(
                0, big_delta, scale1, delta1, scale2, delta2, alpha
            )
            if not error:
                ep_ddi = neg_adjusted + timedelta(days=round(ep_ddi_t))
                lp_ddi = neg_adjusted + timedelta(days=round(lp_ddi_t))
                flag += (
                    f"EP-DDI & LP-DDI represent "
                    f"{int(round((1 - alpha) * 100))}% Credibility Interval. "
                )

        if error:
            ci_failed = True
            flag += error

    # --- Median (fallback or default) path ---
    if not use_ci or ci_failed:
        ep_ddi = neg_adjusted
        lp_ddi = pos_adjusted
        if ci_failed:
            flag += (
                "Credibility interval could not be calculated. "
                "EP-DDI & LP-DDI based on median diagnostic delays. "
            )
        else:
            flag += "EP-DDI & LP-DDI based on median diagnostic delays. "

    # --- Derive EDDI from the interval ---
    if ep_ddi is not None and lp_ddi is not None:
        flag += _check_discordant_dates(subject_df)
        interval_size = (lp_ddi - ep_ddi).days

        if interval_size < 0:
            flag += "Unexpected ordering of EP-DDI and LP-DDI. "
        if abs(interval_size) < 10:
            flag += "EP-DDI and LP-DDI less than 10 days apart. "

        eddi = ep_ddi + timedelta(days=abs(interval_size) // 2)
        interval_size = abs(interval_size)

    return {
        "ep_ddi": ep_ddi,
        "lp_ddi": lp_ddi,
        "eddi": eddi,
        "interval_size": interval_size,
        "flag": flag.strip(),
    }


# ---------------------------------------------------------------------------
# Stage 3: full pipeline
# ---------------------------------------------------------------------------

def calculate_eddis(
    df: pd.DataFrame,
    mappings: dict[str, dict],
    growth_rate: float = DEFAULT_GROWTH_RATE,
    calculate_ci: bool = True,
    alpha: float = DEFAULT_ALPHA,
) -> pd.DataFrame:
    """
    Run the full EDDI calculation pipeline over all subjects.

    Parameters
    ----------
    df : parsed test history DataFrame (columns: Subject, Date, Test, Result)
    mappings : {test_code: properties_dict} — see module docstring for structure
    growth_rate : viral load growth rate in log10 copies/ml/day
    calculate_ci : use Bayesian credibility intervals when True; medians when False
    alpha : significance level for credibility intervals (default 0.05 → 95% CI)

    Returns
    -------
    DataFrame with columns:
        Subject, EP_DDI, LP_DDI, Interval_Size, EDDI, Flag
    Subjects are returned in order of first appearance in the input.
    """
    adjusted = adjust_test_dates(df, mappings, growth_rate)

    # Preserve subject order from the input file
    subject_order = list(dict.fromkeys(df["Subject"]))

    rows = []
    for subject in subject_order:
        group = adjusted[adjusted["Subject"] == subject]
        result = _calculate_subject_eddi(group, calculate_ci, alpha)
        rows.append({
            "Subject": subject,
            "EP_DDI": result["ep_ddi"],
            "LP_DDI": result["lp_ddi"],
            "Interval_Size": result["interval_size"],
            "EDDI": result["eddi"],
            "Flag": result["flag"],
        })

    return pd.DataFrame(rows)
