# EduPro Learner Intelligence Dashboard — Architecture

## 1. Technical stack

- **Python 3.11+**
- **Streamlit** for the web application and interactive controls
- **pandas** for loading, cleaning, joining, and aggregation
- **Plotly Express** for responsive charts and heatmaps
- **openpyxl** for Excel workbook input (when source data is `.xlsx`)
- **pytest** for transformation and KPI tests

## 2. System flow

```text
Users sheet ────────┐
                    ├─> validation & cleaning ─> relational join ─> analytic dataset
Courses sheet ──────┤                                         │
                    │                                         ├─> KPI calculations
Transactions sheet ─┘                                         ├─> filtered charts/tables
                                                              └─> Streamlit dashboard
```

### Data-processing sequence

1. Load Users, Courses, and Transactions from the configured workbook or CSV files.
2. Validate required columns, data types, non-empty IDs, and duplicate primary IDs.
3. Standardize text values such as gender, category, and level; convert `Age` to numeric and `TransactionDate` to datetime.
4. Validate foreign keys in transactions. Report unmatched user/course IDs.
5. Join `Transactions` to `Users` using `UserID`, then to `Courses` using `CourseID`.
6. Derive `AgeGroup`: `<18`, `18–25`, `26–35`, `36–45`, and `45+`.
7. Apply sidebar filters to the analytic dataset.
8. Compute KPIs and build visualizations from the same filtered dataset.

## 3. Application layout

```text
page
├── Header: title, scope, data freshness/status
├── Sidebar: age group, gender, category, and level filters
├── KPI row: total enrollments, active learners, leading category, leading level
├── Demographics
│   ├── age distribution
│   └── gender participation
├── Enrollment patterns
│   ├── enrollments by age group
│   └── category/type/level popularity
├── Preferences
│   ├── age group × category heatmap
│   └── gender × level comparison
├── Behavioral insights
│   ├── courses per learner
│   └── enrollment concentration
└── Data quality / methodology notes
```

## 4. Recommended project structure

```text
project-root/
├── streamlit_app.py              # Streamlit entry point and page composition
├── requirements.txt
├── README.md
├── data/
│   ├── raw/                      # source workbook/CSVs; never edited by the app
│   └── processed/                # optional derived exports, gitignored
├── src/
│   ├── __init__.py
│   ├── data_loader.py             # file loading and schema checks
│   ├── transforms.py              # cleaning, joins, and age bands
│   ├── metrics.py                 # KPI and aggregation functions
│   ├── charts.py                  # Plotly figure builders
│   └── constants.py               # labels, age-band order, required schemas
├── tests/
│   ├── test_transforms.py
│   └── test_metrics.py
└── docs/
    ├── PRD.md
    ├── Architecture.md
    ├── Rules.md
    ├── 4.Phases.md
    ├── Design.md
    └── Memory.md                  # created only once implementation begins
```

## 5. State and performance

- Use `st.cache_data` for file loading and deterministic transformations.
- Treat uploaded/source data as read-only; do not mutate raw source files.
- Keep computations in pure functions so KPIs can be unit-tested.
- Recalculate all visuals from one canonical filtered data frame to prevent inconsistent totals.

## 6. Error and empty states

- Missing or malformed source files: show a concise blocking message with expected fields.
- Invalid rows: exclude only when necessary, count them, and state why they were excluded.
- Unmatched foreign keys: display count and do not include those records in joined metrics.
- No data after filtering: render an informative empty state rather than blank charts or errors.
