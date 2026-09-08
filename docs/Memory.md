# EduPro Learner Intelligence Dashboard — Working Memory

## Purpose

This file is the concise handoff record for future coding sessions. Update it after meaningful implementation work so the next developer/AI can continue without re-reading the entire project.

## Project objective

Build a Streamlit dashboard that provides descriptive learner intelligence for EduPro by joining Users, Courses, and Transactions data. The dashboard analyzes learner demographics, enrollments, and course preferences; it does not make predictions, recommendations, or monetization decisions.

## Current status

- **Planning:** Complete.
- **Phase 1 (Foundation & Data Pipeline):** Complete.
- **Phase 2 (Core Dashboard & KPIs):** Complete.
- **Phase 3 (Preference & Behavioral Analysis):** Complete.
- **Phase 4 (Validation, Reporting & Release):** Complete.

## Key decisions & data model

- **Framework:** Python 3.12, Streamlit, pandas, Plotly Express, openpyxl, pytest.
- **Dataset:** `EduPro Online Platform.xlsx` (3,000 Users, 60 Courses, 10,000 Transactions in 2025).
- **Referential Integrity:** 100% matched foreign keys, 0 duplicate IDs, 0 null values in key fields.
- **Age Bands:** `<18`, `18–25`, `26–35`, `36–45`, `45+` (Learner ages range from 15 to 35).
- **Single Canonical Dataset:** All visual components and KPIs compute strictly from one filtered dataset.
- **Design Tokens:** Canvas `#F8FAFC`, Surface `#FFFFFF`, Border `#E2E8F0`, Text `#0F172A`/`#475569`, Primary `#2563EB`, Teal `#0F766E`, Amber `#D97706`.

## Latest session

- **Date:** September 5, 2026
- **Completed:**
  - Implemented data pipeline (`src/data_loader.py`, `src/transforms.py`, `src/constants.py`) with schema validation and referential checks.
  - Implemented metric engine (`src/metrics.py`) with zero-division safety and concentration metrics.
  - Implemented visualization suite (`src/charts.py`) with Plotly Express/Graph Objects adhering to Design.md.
  - Implemented comprehensive 14-test unit test suite (`tests/test_transforms.py`, `tests/test_metrics.py`).
  - Built interactive Streamlit dashboard (`streamlit_app.py`) with responsive cards, 4 analytical modules, global filters, and reset actions.
  - Configured `.streamlit/config.toml` and unified CSS styling to eliminate dark/white split, making the sidebar cohesive off-white with crisp border, dark high-contrast typography, and light blue pill badges.
  - Produced Research Report (`docs/research_report.md`) answering all 5 core analytical questions.
  - Produced Executive Policy Brief (`docs/executive_summary.md`) for government and institutional stakeholders.
  - Produced documentation (`README.md`).
- **Files changed / created:**
  - `streamlit_app.py`
  - `requirements.txt`
  - `README.md`
  - `src/__init__.py`, `src/constants.py`, `src/data_loader.py`, `src/transforms.py`, `src/metrics.py`, `src/charts.py`
  - `tests/__init__.py`, `tests/conftest.py`, `tests/test_transforms.py`, `tests/test_metrics.py`
  - `docs/research_report.md`, `docs/executive_summary.md`, `docs/research_paper.md`, `docs/Memory.md`
  - `research_paper.md`, `Memory.md`
- **Validation performed:**
  - `pytest -v`: 14 passed in 0.59s (100% pass rate).
  - Python pipeline audit on real data: 10,000 transactions joined, 0 orphans, accurate aggregates verified.
  - Browser subagent validation at `http://localhost:8501`: Verified all 4 KPI cards, 4 analytical modules, dynamic filtering by Gender (`Female`), reactive recalculations, and 'Reset All Filters' restoration.
- **Data assumptions or decisions:**
  - Verified that transaction dates are in 2025 and user ages are between 15 and 35. Bands `36–45` and `45+` have 0 platform enrollments in 2025.
  - Read-only data isolation maintained in `data/raw/EduPro Online Platform.xlsx`.
- **Known issues / blockers:**
  - None. System is stable and fully functional.
- **Next smallest task:**
  - None. Ready for submission and stakeholder presentation.
