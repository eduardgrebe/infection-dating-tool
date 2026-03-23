# Porting Plan: Infection Dating Tool → Python 3 / Streamlit

## Overview

The original app is a Django 1.9 / Python 2.7 web application with two independent functional
modules. This plan ports the core logic and interface to a modern, lightweight Python 3 stack
using Streamlit, eliminating the database, task queue, and authentication overhead.

Source code to port from: `old/cephia/infection_dating_tool/`
Supporting code referenced: `old/cephia/cephia/` (CephiaUser, csv_helper, excel_helper, lib/)

---

## The Two Modules

### 1. EDDI Calculator
Estimates the date of HIV infection (EDDI — Estimated Date of Diagnosis of Infection) for each
subject in an uploaded dataset.

**Workflow:**
1. User uploads a CSV (columns: Subject, Date, Test, Result)
2. Unique test codes in the file are mapped to diagnostic test properties
   (diagnostic delay, sigma, detection threshold)
3. Global parameters are optionally adjusted (viral load growth rate, credibility interval alpha)
4. Per-subject EDDI is calculated via Bayesian credibility intervals
5. Results (EP-DDI, LP-DDI, EDDI, interval size, flags) are displayed and downloadable as CSV

### 2. Residual Risk Calculator
Estimates the residual risk of HIV transmission via blood donations given a window of infectivity
and donor population characteristics.

**Three input methods** for determining the window of residual risk:
- **Estimates**: User enters viral dynamics (growth rate, origin viral load, detection threshold)
  → infectious period calculated from log10 formula
- **Data**: User uploads inter-donation intervals + transmission count
  → window estimated via chi-squared CI
- **Supply**: User directly enters a point estimate

**Output:** 2D heatmap of risk vs. incidence (%) and donations per year.

---

## Target Architecture

### Phase 1 (EDDI only)
```
infection-dating-tool/
├── app.py                                  # Streamlit entry point
├── core/
│   ├── calculations.py                    # Bayesian CI logic (ported from old app)
│   ├── file_parser.py                     # CSV validation and parsing
│   └── test_properties.py                # Load and query bundled test property data
├── data/
│   └── diagnostic_tests_and_properties.csv   # Bundled reference data (50+ HIV tests)
│                                              # Source: old/cephia/infection_dating_tool/
│                                              #         static/test_and_properties/
├── tests/
│   └── test_calculations.py
├── PLAN.md
└── requirements.txt
```

### Phase 2+ (Residual Risk added)
```
infection-dating-tool/
├── app.py
├── pages/
│   ├── 1_EDDI_Calculator.py               # Extracted from app.py
│   └── 2_Residual_Risk.py                 # Residual risk calculator + heatmaps
├── core/
│   ├── calculations.py
│   ├── residual_risk_calc.py              # Chi2 CI + infectious period calculations
│   ├── file_parser.py
│   └── test_properties.py
├── data/
│   └── diagnostic_tests_and_properties.csv
├── tests/
│   ├── test_calculations.py
│   └── test_residual_risk_calc.py
├── PLAN.md
└── requirements.txt
```

---

## Dependencies

Managed via `pyproject.toml` and locked with `uv.lock`. No separate `requirements.txt` needed.

No database. No task queue. No authentication.

---

## What Ports With Minimal Changes

| Source file | Destination | Phase | Notes |
|---|---|---|---|
| `old/.../calculations.py` | `core/calculations.py` | 1 | Pure Python/scipy — remove Django imports, otherwise unchanged |
| `old/static/.../diagnostic_tests_and_properties.csv` | `data/` | 1 | Copy as-is |
| `old/.../graph_image_generator.py` | `pages/2_Residual_Risk.py` | 2 | Pure matplotlib — trivial port |
| Residual risk math (chi2, viral dynamics) | `core/residual_risk_calc.py` | 2 | Extract from views/forms into standalone functions |

## What Is Replaced or Simplified

| Old | New | Reason |
|---|---|---|
| Django models (IDTSubject, TestHistory, etc.) | Pandas DataFrames in `st.session_state` | No persistence needed across sessions |
| Django file upload + IDTFileInfo state machine | `st.file_uploader` + session state | Simpler, synchronous |
| TestPropertyMapping (database) | Dict in session state, built from selectboxes | Per-session config is sufficient |
| Django auth + CephiaUser | Removed entirely | Single-user tool, no auth needed |
| Django templates + AJAX forms | Streamlit widgets + `st.session_state` step tracking | |
| Celery (async task queue) | Synchronous in-request | Calculations complete in < 1s |
| MySQL | None (SQLite optional in future if custom test configs need persistence) | |
| xlrd / xlwt | pandas + openpyxl | xlrd 2.x dropped .xlsx support; openpyxl handles both |
| unicodecsv | stdlib csv / pandas | Python 3 handles Unicode natively |
| six, enum34, functools32, subprocess32, ipaddress, argparse | Removed | Python 2 backports, all now stdlib |
| django-celery, djcelery | Removed | |
| raven (Sentry) | Removed | Out of scope for initial port |
| pycrypto | Removed | Unmaintained; had CVEs |

---

## EDDI Workflow Design (Streamlit)

Progress tracked via `st.session_state.step` (1–5).

```
Step 1: Upload CSV
  → st.file_uploader
  → validate headers (Subject, Date, Test, Result)
  → validate date format (YYYY-MM-DD)
  → validate result values (positive/pos/+, negative/neg/-)
  → preview DataFrame

Step 2: Map test codes
  → show unique test codes detected in file
  → for each code: selectbox for test name + selectbox for property estimate
  → loaded from diagnostic_tests_and_properties.csv
  → user can also adjust properties inline

Step 3: Set global parameters
  → viral load growth rate (default: 0.35 log10 cp/ml/day)
  → credibility interval toggle + alpha (default: 0.05)

Step 4: Calculate
  → adjust test dates by diagnostic delay
  → per-subject: find earliest positive / latest negative after adjustment
  → run find_ci_limits() or median-based fallback
  → compute EP-DDI, LP-DDI, EDDI, interval size, flags

Step 5: Results
  → display table (Subject, EP-DDI, LP-DDI, Interval Size, EDDI, Flags)
  → download CSV button
```

---

## Residual Risk Workflow Design (Streamlit)

```
Radio: Choose input method
  ├── Estimates → sidebar inputs (growth_rate, origin_viral_load, viral_load)
  │              → infectious_period = log10(vl / origin) / growth_rate
  ├── Data      → file upload (inter-donation intervals) + n_transmissions input
  │              → residual_risk = n / Σ(1/(interval + d_neg - d_pos))
  │              → CI via chi2 distribution
  └── Supply    → direct numeric input for window estimate

Once window determined:
  → incidence (%) slider/input
  → donations per year input
  → generate 2D heatmap: risk per donation and expected infectious donations
  → display two matplotlib figures inline (st.pyplot)
```

---

## Key Formulas to Preserve (Phase 1)

### EDDI (credibility interval mode)
```python
# Adjust test dates
adjusted_date = test_date - timedelta(days=diagnostic_delay)
# For viral load tests: diagnostic_delay = log10(detection_threshold) / growth_rate

# Per subject (earliest positive after adjustment, latest negative after adjustment)
big_delta = (positive_adjusted_date - negative_adjusted_date).days

find_delta_scale(d_neg, sigma_neg)  ->  delta1, scale1
find_delta_scale(d_pos, sigma_pos)  ->  delta2, scale2
find_ci_limits(0, big_delta, scale1, delta1, scale2, delta2, alpha)  ->  ep_t, lp_t

ep_ddi = negative_adjusted_date + timedelta(days=ep_t)
lp_ddi = negative_adjusted_date + timedelta(days=lp_t)
eddi   = ep_ddi + (lp_ddi - ep_ddi) / 2
```

### EDDI (median mode, credibility intervals disabled)
```python
ep_ddi = negative_adjusted_date + timedelta(days=diagnostic_delay_neg)
lp_ddi = positive_adjusted_date + timedelta(days=diagnostic_delay_pos)
eddi   = ep_ddi + (lp_ddi - ep_ddi) / 2
```

## Key Formulas to Preserve (Phase 2)

### Residual risk (data-based)
```python
total_exposure = sum(1 / (interval + d_neg - d_pos) for interval in intervals)
residual_risk  = n_transmissions / total_exposure
ci_lower = chi2.ppf(0.025, df=2*n)       / (2 * total_exposure)  # 0 if n == 0
ci_upper = chi2.ppf(0.975, df=2*(n + 1)) / (2 * total_exposure)
```

### Infectious period (viral dynamics)
```python
infectious_period = log10(viral_load / origin_viral_load) / viral_growth_rate
```

---

## Build Order

### Phase 1: EDDI Calculator (current focus)

**Step 1.1 — Core calculations**
- Port `core/calculations.py` from `old/.../calculations.py`
- Remove Django imports; no other changes expected
- Write unit tests in `tests/test_calculations.py`

**Step 1.2 — Test property data**
- Copy `diagnostic_tests_and_properties.csv` to `data/`
- Write `core/test_properties.py`: load CSV, expose lookup by test name and category

**Step 1.3 — File parser**
- Write `core/file_parser.py`: validate and parse uploaded subject CSV
- Accepted columns: Subject, Date (YYYY-MM-DD), Test, Result (positive/pos/+, negative/neg/-)
- Returns a clean DataFrame or a list of validation errors

**Step 1.4 — EDDI app**
- Write `app.py` as a single-page Streamlit app with 5-step workflow (see EDDI Workflow Design)
- Step navigation via `st.session_state.step`

**Step 1.5 — Smoke test**
- End-to-end test with `data/ExampleData.csv`

### Phase 2: Residual Risk Calculator

**Step 2.1 — Risk calculations**
- Write `core/residual_risk_calc.py`: extract chi2 CI and infectious period formulas
- Write unit tests in `tests/test_residual_risk_calc.py`

**Step 2.2 — Residual Risk page**
- Add `pages/2_Residual_Risk.py`: risk workflow + heatmap display (matplotlib)
- Refactor `app.py` → `pages/1_EDDI_Calculator.py`; update `app.py` to navigation shell

### Phase 3: Polish
- README with usage instructions
- Review and tighten dependency pins

---

## Data Notes

- The bundled `diagnostic_tests_and_properties.csv` contains ~50 HIV diagnostic tests with
  pre-computed diagnostic delays, sigmas, and detection thresholds. It is the sole reference
  data source — no seeding step needed.
- The original app loaded this via a management command into MySQL. Here it is read directly
  by `core/test_properties.py` at startup.
- `ExampleData.csv` in `data/` serves as the integration test input and can be offered as a download in the UI.

---

## Out of Scope (for this port)

- User authentication / multi-user support
- Persistent custom test configurations across sessions
- Celery / background task processing
- Sentry error tracking
- Email / user registration flow
- The full CEPHIA data management module (specimen tracking, assay results, etc.) —
  this was a separate Django app and is not part of the infection dating tool functionality
