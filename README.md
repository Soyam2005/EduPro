# EduPro Learner Intelligence Platform 🎓

A production-grade, evidence-led descriptive analytics dashboard and intelligence platform for EduPro. This system audits, cleans, validates, and visualizes platform user demographics, course catalog dynamics, and transaction histories to empower educational leaders, marketing teams, curriculum planners, and policy stakeholders.

## Live Application

Explore the deployed dashboard: [EduPro Learner Intelligence on Streamlit](https://edupro-ilqcncbfmudr7qqjv8uit3.streamlit.app/)

---

## 🌟 Key Features

- **Relational Data Integrity Engine:** Validates schemas, checks primary key uniqueness, audits foreign key relationships (`Users.UserID → Transactions.UserID ← Courses.CourseID`), and isolates source data as read-only.
- **Dynamic Multi-Dimensional Filtering:** Global sidebar controls for Age Group, Gender, Course Category, and Course Level with instantaneous synchronization across all KPIs, charts, tables, and narrative summaries.
- **Accessible & Responsive Design System:** Custom light-canvas aesthetic (`#F8FAFC`, `#FFFFFF`, `#2563EB`, `#0F766E`, `#D97706`), Inter typography, high-contrast Plotly Express data visualizations, and graceful empty-state handling.
- **Core Analytical Modules:**
  1. *Learner Demographic Overview:* Single-year age distributions and gender parity donuts.
  2. *Enrollment Patterns & Demand:* Standardized age bands, ranked category demand, difficulty levels, and pricing models.
  3. *Demographic × Preference Heatmaps:* Cross-tabulations of age bands vs. categories and gender vs. course levels.
  4. *Behavioral Insights & Depth:* Courses per learner distribution and Pareto concentration metrics.
- **Audit-Ready Documentation:** Includes a full Exploratory Data Analysis research report and an Executive Policy Brief for government and institutional stakeholders.
- **Automated Test Suite:** 100% test coverage with `pytest` for boundary conditions, schema validation, data joins, zero-division safety, and KPI aggregations.

---

## 🏗️ Architecture & Project Structure

```text
EDU PRO/
├── streamlit_app.py              # Streamlit web application & UI layout
├── requirements.txt              # Production and test dependencies
├── README.md                     # Platform overview, setup, and methodology
├── data/
│   ├── raw/                      # Read-only source workbook (EduPro Online Platform.xlsx)
│   └── processed/                # Derived export directory
├── src/
│   ├── __init__.py
│   ├── constants.py              # Design tokens, color palettes, age bands, schemas
│   ├── data_loader.py            # Excel ingestion, schema checks, integrity auditing
│   ├── transforms.py             # Data normalization, age grouping, relational joins
│   ├── metrics.py                # Pure KPI computations, aggregations, behavioral depth
│   └── charts.py                 # Plotly visualizers aligned with Design.md specifications
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Synthetic test datasets and fixtures
│   ├── test_transforms.py        # Transformation, schema, edge-case & join unit tests
│   └── test_metrics.py           # Metric calculations, zero-division safety, filter tests
└── docs/
    ├── project/                  # Product, architecture, design, rules, and delivery plans
    ├── research/                 # EDA research paper and executive summary
    └── development/              # Implementation handoff and session notes
```

---

## 🚀 Quickstart & Installation

### 1. Prerequisites
- Python 3.11+ (Python 3.12 verified)
- `pip` package manager

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Automated Tests
```bash
pytest -v
```
All 14 unit tests will execute, validating schema rules, boundary age groupings, relational integrity, zero-division resilience, and metric outputs.

### 4. Launch the Interactive Dashboard
```bash
streamlit run streamlit_app.py
```
The application will launch locally at `http://localhost:8501`.

---

## 📊 Data Pipeline & Methodology Rules

1. **Source Data Immutability:** Source Excel workbook (`EduPro Online Platform.xlsx`) is treated as read-only.
2. **Standardized Age Bands:** Categorized as `<18`, `18–25`, `26–35`, `36–45`, `45+`.
3. **Foreign Key Integrity:** 10,000 transactions matched with 100% integrity to 3,000 users and 60 courses. Zero orphaned records.
4. **Descriptive Discipline:** No predictive extrapolations, personalized recommendations, or causal claims are introduced without empirical evidence.

---

## 📄 Deliverables Summary

- **Streamlit Interactive Application:** `streamlit_app.py`
- **Exploratory Data Analysis Report:** `docs/research/research_paper.md`
- **Government / Leadership Executive Summary:** `docs/research/executive_summary.md`
- **Engineering Knowledge & Session Record:** `docs/development/Memory.md`
