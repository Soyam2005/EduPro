"""Tests for data transformations, cleaning, schema validation, and relational joining."""

import pandas as pd
import numpy as np
import pytest

from src.transforms import (
    derive_age_group,
    clean_and_normalize,
    build_analytic_dataset,
)
from src.data_loader import (
    validate_schemas,
    check_referential_integrity,
)


def test_derive_age_group_boundaries():
    """Verify exact boundary behavior for age bands per PRD & Architecture."""
    assert derive_age_group(15) == "<18"
    assert derive_age_group(17.9) == "<18"
    assert derive_age_group(18) == "18–25"
    assert derive_age_group(25) == "18–25"
    assert derive_age_group(26) == "26–35"
    assert derive_age_group(35) == "26–35"
    assert derive_age_group(36) == "36–45"
    assert derive_age_group(45) == "36–45"
    assert derive_age_group(46) == "45+"
    assert derive_age_group(65) == "45+"
    assert derive_age_group(None) == "Unknown"
    assert derive_age_group(np.nan) == "Unknown"
    assert derive_age_group("invalid") == "Unknown"


def test_derive_age_group_series():
    """Verify derive_age_group operates correctly over a pandas Series."""
    s = pd.Series([16, 18, 30, 42, 60, None])
    res = derive_age_group(s)
    expected = ["<18", "18–25", "26–35", "36–45", "45+", "Unknown"]
    assert list(res) == expected


def test_clean_and_normalize_immutability(sample_users_df, sample_courses_df, sample_transactions_df):
    """Ensure source dataframes are not modified in-place and strings are trimmed."""
    original_gender = sample_users_df["Gender"].copy()
    u_clean, c_clean, t_clean = clean_and_normalize(
        sample_users_df, sample_courses_df, sample_transactions_df
    )

    # Source must remain untouched
    pd.testing.assert_series_equal(sample_users_df["Gender"], original_gender)

    # Cleaned dataframe must normalize ' female ' to 'Female'
    assert u_clean.loc[u_clean["UserID"] == "U003", "Gender"].values[0] == "Female"
    assert "AgeGroup" in u_clean.columns
    assert pd.api.types.is_datetime64_any_dtype(t_clean["TransactionDate"])


def test_validate_schemas():
    """Ensure missing columns in any table are caught."""
    valid_u = pd.DataFrame({"UserID": [1], "UserName": ["a"], "Age": [20], "Gender": ["M"]})
    valid_c = pd.DataFrame({
        "CourseID": [1], "CourseName": ["a"], "CourseCategory": ["c"],
        "CourseType": ["Free"], "CourseLevel": ["Beginner"]
    })
    valid_t = pd.DataFrame({
        "TransactionID": [1], "UserID": [1], "CourseID": [1], "TransactionDate": ["2025-01-01"]
    })

    # All valid
    assert len(validate_schemas(valid_u, valid_c, valid_t)) == 0

    # Missing User column
    invalid_u = valid_u.drop(columns=["Age"])
    errors = validate_schemas(invalid_u, valid_c, valid_t)
    assert len(errors) == 1
    assert "Age" in errors[0]


def test_check_referential_integrity(sample_users_df, sample_courses_df, transactions_with_unmatched_df):
    """Ensure orphaned foreign keys are flagged."""
    report = check_referential_integrity(
        sample_users_df, sample_courses_df, transactions_with_unmatched_df
    )
    assert not report["is_healthy"]
    assert report["unmatched_user_transactions"] == 1
    assert "U999" in report["unmatched_user_ids_sample"]
    assert report["unmatched_course_transactions"] == 1
    assert "C999" in report["unmatched_course_ids_sample"]


def test_build_analytic_dataset(sample_users_df, sample_courses_df, sample_transactions_df):
    """Ensure clean relational join with expected columns and metrics."""
    analytic_df, stats = build_analytic_dataset(
        sample_users_df, sample_courses_df, sample_transactions_df
    )
    assert len(analytic_df) == len(sample_transactions_df)
    assert stats["excluded_transactions"] == 0
    assert stats["unique_active_learners"] == 5
    assert "AgeGroup" in analytic_df.columns
    assert "CourseCategory" in analytic_df.columns
    assert "CourseLevel" in analytic_df.columns
