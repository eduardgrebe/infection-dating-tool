# Plan: Infection Dating Tool — Python 3 / Streamlit rewrite

## Overview

Rewrite of the original Django 1.9 / Python 2.7 application as a modern, lightweight Python 3
Streamlit app, eliminating the database, task queue, and authentication overhead.

Source code ported from: `old/cephia/infection_dating_tool/`
Supporting code referenced: `old/cephia/cephia/` (csv_helper, excel_helper, lib/)

---

## Current scope: EDDI Calculator

The EDDI Calculator is the core module of this rewrite. It estimates the date of HIV infection
for each subject in an uploaded dataset.

**Workflow:**
1. User uploads a CSV (columns: Subject, Date, Test, Result)
2. Unique test codes in the file are mapped to diagnostic test properties
   (diagnostic delay, sigma, detection threshold)
3. Global parameters are optionally adjusted (viral load growth rate, credibility interval alpha)
4. Per-subject EDDI is calculated via Bayesian credibility intervals
5. Results (EP-DDI, LP-DDI, EDDI, interval size, flags) are displayed and downloadable as CSV

The residual risk module is out of scope for this rewrite; it is being developed separately.

---

## Architecture

```
infection-dating-tool/
├── app.py                                  # Streamlit entry point (single-page, 5-step workflow)
├── core/
│   ├── calculations.py                    # Bayesian CI logic (ported from old app)
│   ├── eddi.py                            # EDDI calculation pipeline
│   ├── file_parser.py                     # CSV validation and parsing
│   └── test_properties.py                # Load and query bundled test property data
├── data/
│   ├── diagnostic_tests_and_properties.csv   # Bundled reference data (50+ HIV tests)
│   └── ExampleData.csv                       # Example input file
├── tests/
│   ├── test_calculations.py               # Unit tests for Bayesian CI functions
│   └── test_integration_example_data.py   # Integration tests using ExampleData.csv
├── old/                                   # Original Django/Python 2.7 source (reference only)
├── PLAN.md
├── README.md
├── pyproject.toml                         # Dependencies managed by uv
└── uv.lock
```

---

## Dependencies

Managed via `pyproject.toml` and locked with `uv.lock`. No separate `requirements.txt` needed.

No database. No task queue. No authentication.

---

## What was ported

| Source | Destination | Notes |
|---|---|---|
| `old/.../calculations.py` | `core/calculations.py` | Pure Python/scipy — Django imports removed, logic unchanged |
| `old/.../models.py` (calculate_eddi) | `core/eddi.py` | Extracted from Django model method |
| `old/.../views.py` (update_adjusted_dates) | `core/eddi.py` | Extracted from Django view function |
| `old/.../file_handlers/` | `core/file_parser.py` | Rewritten without Django/xlrd |
| `old/static/.../diagnostic_tests_and_properties.csv` | `data/` | Copied as-is |

## What was replaced or removed

| Old | New | Reason |
|---|---|---|
| Django models (IDTSubject, TestHistory, etc.) | Pandas DataFrames in `st.session_state` | No persistence needed across sessions |
| Django file upload + IDTFileInfo state machine | `st.file_uploader` + session state | Simpler, synchronous |
| TestPropertyMapping (database) | Dict in session state, built from selectboxes | Per-session config is sufficient |
| Django auth + CephiaUser | Removed entirely | Single-user tool, no auth needed |
| Django templates + AJAX forms | Streamlit widgets + `st.session_state` step tracking | |
| Celery (async task queue) | Synchronous | Calculations complete in < 1s |
| MySQL | None | |
| xlrd / xlwt | pandas + openpyxl | xlrd 2.x dropped .xlsx; openpyxl covers both |
| unicodecsv | stdlib csv / pandas | Python 3 handles Unicode natively |
| six, enum34, functools32, subprocess32, ipaddress, argparse | Removed | Python 2 backports, now all stdlib |
| raven (Sentry) | Removed | Out of scope |
| pycrypto | Removed | Unmaintained, CVEs |

---

## Key formulas

### EDDI (credibility interval mode)
```python
# Adjust test dates
adjusted_date = test_date - timedelta(days=round(diagnostic_delay))
# For viral load tests: diagnostic_delay = log10(detection_threshold) / growth_rate

# Per subject: latest negative adjusted → EP anchor; earliest positive adjusted → LP anchor
big_delta = (lp_anchor - ep_anchor).days

find_delta_scale(d_neg, sigma_neg)  ->  delta1, scale1
find_delta_scale(d_pos, sigma_pos)  ->  delta2, scale2
find_ci_limits(0, big_delta, scale1, delta1, scale2, delta2, alpha)  ->  ep_t, lp_t

ep_ddi = ep_anchor + timedelta(days=round(ep_t))
lp_ddi = ep_anchor + timedelta(days=round(lp_t))
eddi   = ep_ddi + timedelta(days=abs(interval_size) // 2)
```

### EDDI (median mode, credibility intervals disabled)
```python
ep_ddi = ep_anchor   # adjusted date of latest negative test
lp_ddi = lp_anchor   # adjusted date of earliest positive test
eddi   = ep_ddi + timedelta(days=abs(interval_size) // 2)
```

---

## Build status

### Phase 1: EDDI Calculator ✓ Complete
- [x] `core/calculations.py` — Bayesian CI functions, unit tests
- [x] `core/test_properties.py` — bundled test property data loader
- [x] `core/file_parser.py` — CSV validation and parsing
- [x] `core/eddi.py` — full EDDI pipeline
- [x] `app.py` — 5-step Streamlit workflow
- [x] Integration tests against `data/ExampleData.csv`

### Phase 2: Polish (current focus)
- [ ] Review and improve app UX (mapping step, results display)
- [ ] README — update to reflect current app, retain scientific description and credits
- [ ] Consider edge cases and error handling improvements

---

## Data notes

- `diagnostic_tests_and_properties.csv` contains ~50 HIV diagnostic tests with pre-computed
  diagnostic delays, sigmas, and detection thresholds. It is the sole reference data source —
  no seeding step needed. Read directly by `core/test_properties.py` at startup.
- `ExampleData.csv` serves as both the integration test input and a downloadable example in the UI.

---

## Out of scope

- Residual risk module — being developed in a separate application
- User authentication / multi-user support
- Persistent custom test configurations across sessions
- The CEPHIA data management module (specimen tracking, assay results, etc.)
