# EduPro Learner Intelligence Dashboard — Engineering Rules

## 1. Scope boundaries

- Build descriptive analytics only. Do not add predictive models, recommendations, scoring, monetization, or causal claims.
- Analyze only the supplied Users, Courses, and Transactions data unless the product requirements are explicitly updated.
- Do not invent demographic values, missing transactions, or conclusions that data cannot support.

## 2. Required tooling

- Use Streamlit for the application UI.
- Use pandas for tabular data transformation and aggregation.
- Use Plotly Express for dashboard charts where interactive exploration is useful.
- Use `openpyxl` only for Excel reading/writing needs.
- Use `pytest` for unit tests of transformations and metrics.

Avoid adding a database, authentication system, machine-learning framework, or paid API unless explicitly requested.

## 3. Data rules

- Validate all required columns before processing.
- Treat `UserID`, `CourseID`, and `TransactionID` as identifiers, not numerical measures.
- Keep source data immutable; derived columns belong in the analytic dataset.
- Parse `Age` as numeric and `TransactionDate` as datetime with invalid values handled explicitly.
- Normalize categorical strings (trim whitespace and use a documented canonical representation).
- Use a fixed, documented age-band order: `<18`, `18–25`, `26–35`, `36–45`, `45+`.
- Deduplicate only with a documented rule. Never silently remove potentially legitimate repeated enrollments.
- Report invalid rows and unmatched foreign keys in the UI or data-quality summary.

## 4. Metric and visualization rules

- Compute every chart and KPI from the same filtered dataset.
- Label counts, percentages, filters, and denominator choices clearly.
- Do not show a percentage when the denominator is zero.
- Use chronological order for dates and logical category order for age bands and course levels.
- Provide descriptive captions; avoid language such as “causes,” “proves,” or “drives” unless evidence supports it.
- Charts must retain legible labels and useful hover information.

## 5. UI and accessibility rules

- Use color as a supporting cue, never the only way to communicate a category or status.
- Maintain sufficient contrast, readable font sizes, and clear chart titles.
- Use consistent terminology: “learner,” “enrollment,” “course category,” and “course level.”
- Every filter must have an understandable default and reset behavior.
- Empty, loading, and error states must explain what happened and what the user can do.

## 6. Code-quality rules

- Keep business logic out of the Streamlit page; place loading, transformations, metrics, and charts in focused modules.
- Prefer small, pure functions with type hints and docstrings for non-obvious rules.
- Never use bare `except:`. Catch expected exceptions and show contextual user-facing errors.
- Use `logging` for diagnostic details; never expose stack traces or sensitive data by default.
- Add or update tests when changing join logic, age grouping, filtering, or KPI formulas.
- Do not commit secrets, personal exports, or generated caches.

## 7. Privacy and fairness

- Use only the minimum personal data needed for aggregation.
- Do not expose individual learner names in dashboard views unless explicitly required and authorized.
- Present gender analysis as descriptive participation data; do not infer ability, preference, or intent from gender.
- Clearly flag small groups where counts may create privacy or interpretation risk.
