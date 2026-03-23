"""
Infection Dating Tool — Streamlit app (Phase 1: EDDI Calculator)

Five-step workflow:
  1. Upload subject test history CSV
  2. Map test codes → diagnostic test properties
  3. Set calculation parameters
  4. Run EDDI calculation
  5. View and download results
"""

from __future__ import annotations

import io
from pathlib import Path

import pandas as pd
import streamlit as st

from core.eddi import calculate_eddis
from core.file_parser import get_test_codes, parse_file
from core.test_properties import (
    VIRAL_LOAD_CATEGORY,
    get_default_growth_rate,
    get_test_names,
    get_test_properties,
    get_tests_by_category,
)

DATA_DIR = Path(__file__).parent / "data"
EXAMPLE_DATA = DATA_DIR / "ExampleData.csv"

STEP_LABELS = ["Upload", "Map Tests", "Parameters", "Calculate", "Results"]


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

def _init_state() -> None:
    defaults: dict = {
        "step": 1,
        "df": None,
        "filename": "",
        "growth_rate": get_default_growth_rate(),
        "calculate_ci": True,
        "alpha": 0.05,
        "results": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def _go(step: int) -> None:
    st.session_state.step = step
    st.rerun()


def _build_mappings(codes: list[str]) -> dict[str, dict]:
    """Assemble the properties dict from each code's selectbox value."""
    mappings = {}
    for code in codes:
        name = st.session_state.get(f"sel_{code}", "— select —")
        if name and name != "— select —":
            props = get_test_properties(name)
            mappings[code] = {
                "category":               props["category"],
                "diagnostic_delay":       props["diagnostic_delay"],
                "diagnostic_delay_sigma": props["diagnostic_delay_sigma"],
                "detection_threshold":    props["detection_threshold"],
            }
        else:
            mappings[code] = {}
    return mappings


def _all_mapped(codes: list[str]) -> bool:
    return all(
        st.session_state.get(f"sel_{code}", "— select —") != "— select —"
        for code in codes
    )


# ---------------------------------------------------------------------------
# Step indicator
# ---------------------------------------------------------------------------

def _render_step_indicator() -> None:
    step = st.session_state.step
    cols = st.columns(len(STEP_LABELS))
    for i, (col, label) in enumerate(zip(cols, STEP_LABELS), 1):
        if i == step:
            col.markdown(f"**{i}. {label}**")
        elif i < step:
            col.markdown(
                f"<span style='color: #888'>{i}. {label}</span>",
                unsafe_allow_html=True,
            )
        else:
            col.markdown(
                f"<span style='color: #ccc'>{i}. {label}</span>",
                unsafe_allow_html=True,
            )
    st.divider()


# ---------------------------------------------------------------------------
# Step 1: Upload
# ---------------------------------------------------------------------------

def _step_upload() -> None:
    st.subheader("Upload subject test history")
    st.markdown(
        "Provide a CSV with four columns: **Subject**, **Date** (YYYY-MM-DD), "
        "**Test** (test code), **Result** (positive / negative)."
    )

    st.download_button(
        "Download example file",
        data=EXAMPLE_DATA.read_bytes(),
        file_name="ExampleData.csv",
        mime="text/csv",
    )

    uploaded = st.file_uploader("Choose a CSV file", type=["csv"])
    if not uploaded:
        return

    df, errors = parse_file(uploaded)

    if errors:
        for err in errors:
            st.error(err)
        return

    n_sub = df["Subject"].nunique()
    n_cod = df["Test"].nunique()
    st.success(
        f"{len(df)} rows · "
        f"{n_sub} subject{'s' if n_sub != 1 else ''} · "
        f"{n_cod} unique test code{'s' if n_cod != 1 else ''}"
    )
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Clear any mapping keys left over from a previous upload
    for key in [k for k in st.session_state if k.startswith("sel_")]:
        del st.session_state[key]

    # Pre-select codes that exactly match a known test name
    known = set(get_test_names())
    for code in get_test_codes(df):
        st.session_state[f"sel_{code}"] = code if code in known else "— select —"

    st.session_state.df = df
    st.session_state.filename = uploaded.name

    if st.button("Next →", type="primary"):
        _go(2)


# ---------------------------------------------------------------------------
# Step 2: Map test codes
# ---------------------------------------------------------------------------

def _step_map() -> None:
    df: pd.DataFrame = st.session_state.df
    codes = get_test_codes(df)

    st.subheader("Map test codes to diagnostic tests")
    st.markdown(
        "Assign each test code in your file to a known diagnostic test. "
        "Codes that exactly match a test name are pre-selected."
    )

    # Flat option list ordered by category then name
    by_cat = get_tests_by_category()
    options: list[str] = ["— select —"]
    for cat in sorted(by_cat):
        options.extend(by_cat[cat])

    for code in codes:
        with st.container(border=True):
            left, right = st.columns([1, 2])
            left.markdown(f"**`{code}`**")
            selected: str = right.selectbox(
                "Test",
                options=options,
                key=f"sel_{code}",
                label_visibility="collapsed",
            )
            if selected != "— select —":
                props = get_test_properties(selected)
                if props["category"] == VIRAL_LOAD_CATEGORY:
                    st.caption(
                        f"Viral Load · detection threshold: "
                        f"**{props['detection_threshold']:.0f}** copies/ml"
                    )
                else:
                    sigma = props["diagnostic_delay_sigma"]
                    sigma_str = f"{sigma:.2f} days" if sigma else "20% RSE (default)"
                    st.caption(
                        f"{props['category']} · "
                        f"diagnostic delay: **{props['diagnostic_delay']:.1f}** days · "
                        f"σ = {sigma_str}"
                    )

    st.divider()
    left, right = st.columns([1, 5])
    with left:
        if st.button("← Back"):
            _go(1)
    with right:
        if not _all_mapped(codes):
            st.warning("All test codes must be mapped before continuing.")
        elif st.button("Next →", type="primary"):
            _go(3)


# ---------------------------------------------------------------------------
# Step 3: Parameters
# ---------------------------------------------------------------------------

def _step_params() -> None:
    st.subheader("Calculation parameters")

    st.number_input(
        "Viral load growth rate (log₁₀ copies/ml/day)",
        min_value=0.01,
        max_value=2.0,
        step=0.01,
        format="%.3f",
        key="growth_rate",
        help="Default: 0.35 (Fiebig et al. 2003). Used only for viral load assays.",
    )

    st.checkbox(
        "Use Bayesian credibility intervals for EP-DDI / LP-DDI",
        key="calculate_ci",
        help=(
            "When enabled, EP-DDI and LP-DDI are the bounds of a posterior credibility "
            "interval for the infection date. When disabled, they are the adjusted dates "
            "of the latest negative and earliest positive tests (median diagnostic delay)."
        ),
    )

    if st.session_state.calculate_ci:
        st.number_input(
            "Significance level (α)",
            min_value=0.01,
            max_value=0.50,
            step=0.01,
            format="%.2f",
            key="alpha",
            help="α = 0.05 → 95% credibility interval (default).",
        )

    st.divider()
    left, right = st.columns([1, 5])
    with left:
        if st.button("← Back"):
            _go(2)
    with right:
        if st.button("Next →", type="primary"):
            _go(4)


# ---------------------------------------------------------------------------
# Step 4: Calculate
# ---------------------------------------------------------------------------

def _step_calculate() -> None:
    df: pd.DataFrame = st.session_state.df
    codes = get_test_codes(df)
    n_sub = df["Subject"].nunique()

    ci_label = (
        f"{int(round((1 - st.session_state.alpha) * 100))}% credibility intervals"
        if st.session_state.calculate_ci
        else "median diagnostic delays"
    )

    st.subheader("Ready to calculate")
    st.markdown(
        f"**{n_sub}** subject{'s' if n_sub != 1 else ''} · "
        f"EP-DDI / LP-DDI via **{ci_label}**"
    )

    left, right = st.columns([1, 5])
    with left:
        if st.button("← Back"):
            _go(3)
    with right:
        if st.button("Calculate →", type="primary"):
            mappings = _build_mappings(codes)
            with st.spinner("Calculating…"):
                try:
                    results = calculate_eddis(
                        df,
                        mappings,
                        growth_rate=st.session_state.growth_rate,
                        calculate_ci=st.session_state.calculate_ci,
                        alpha=st.session_state.alpha,
                    )
                    st.session_state.results = results
                    _go(5)
                except Exception as exc:
                    st.error(f"Calculation failed: {exc}")


# ---------------------------------------------------------------------------
# Step 5: Results
# ---------------------------------------------------------------------------

def _step_results() -> None:
    results: pd.DataFrame = st.session_state.results

    st.subheader("Results")
    st.dataframe(results, use_container_width=True, hide_index=True)

    stem = Path(st.session_state.filename).stem
    st.download_button(
        "Download results (CSV)",
        data=results.to_csv(index=False).encode(),
        file_name=f"{stem}_eddi_results.csv",
        mime="text/csv",
        type="primary",
    )

    st.divider()
    if st.button("← Start over"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Infection Dating Tool",
    layout="centered",
)

_init_state()

st.title("Infection Dating Tool")
st.caption(
    "Estimates plausible HIV infection intervals (EP-DDI, LP-DDI, EDDI) "
    "from diagnostic test histories."
)

_render_step_indicator()

{
    1: _step_upload,
    2: _step_map,
    3: _step_params,
    4: _step_calculate,
    5: _step_results,
}[st.session_state.step]()
