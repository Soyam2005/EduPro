"""Tests for KPI metrics, aggregation logic, filters, and behavioral calculations."""

import pandas as pd
import pytest

from src.transforms import build_analytic_dataset
from src.metrics import (
    apply_filters,
    compute_kpis,
    get_age_distribution,
    get_gender_participation,
    get_age_enrollment_breakdown,
    get_category_popularity,
    get_level_demand,
    get_type_distribution,
    get_age_category_crosstab,
    get_gender_level_breakdown,
    get_gender_category_breakdown,
    get_learner_concentration,
)


@pytest.fixture
def analytic_df(sample_users_df, sample_courses_df, sample_transactions_df) -> pd.DataFrame:
    df, _ = build_analytic_dataset(sample_users_df, sample_courses_df, sample_transactions_df)
    return df


def test_apply_filters_none(analytic_df):
    """Empty or None filters should return entire dataset without loss."""
    res = apply_filters(analytic_df, age_groups=None, genders=None, categories=None, levels=None)
    assert len(res) == len(analytic_df)


def test_apply_filters_specific(analytic_df):
    """Filtering by gender should isolate matching rows."""
    females = apply_filters(analytic_df, genders=["Female"])
    assert len(females) == 3
    assert set(females["Gender"]) == {"Female"}


def test_apply_filters_empty_match(analytic_df):
    """Mutually exclusive or non-existent filters should safely return empty DataFrame."""
    res = apply_filters(analytic_df, age_groups=["45+"], categories=["Programming"])
    assert len(res) == 0


def test_compute_kpis_normal(analytic_df):
    """Verify KPIs on populated sample dataset."""
    kpis = compute_kpis(analytic_df, total_unfiltered_count=len(analytic_df))
    assert kpis["total_enrollments"] == 6
    assert kpis["active_learners"] == 5
    assert kpis["avg_courses_per_learner"] == 1.2
    assert kpis["leading_category"] == "Programming"
    assert kpis["leading_category_count"] == 3
    assert kpis["leading_category_share"] == 50.0
    assert kpis["leading_level"] == "Beginner"


def test_compute_kpis_empty():
    """Verify zero-division resilience when filtered DataFrame is empty."""
    empty_df = pd.DataFrame(columns=["UserID", "CourseCategory", "CourseLevel"])
    kpis = compute_kpis(empty_df, total_unfiltered_count=100)
    assert kpis["total_enrollments"] == 0
    assert kpis["active_learners"] == 0
    assert kpis["leading_category"] == "N/A"
    assert kpis["leading_level"] == "N/A"
    assert kpis["avg_courses_per_learner"] == 0.0


def test_demographic_distributions(analytic_df):
    """Verify demographic summary tables and percentages."""
    age_dist = get_age_distribution(analytic_df)
    assert age_dist["Learners"].sum() == 5
    assert round(age_dist["Percentage"].sum(), 0) == 100.0

    gender_dist = get_gender_participation(analytic_df)
    assert gender_dist["Learners"].sum() == 5
    assert gender_dist["Enrollments"].sum() == 6

    age_enroll = get_age_enrollment_breakdown(analytic_df)
    assert age_enroll["Enrollments"].sum() == 6


def test_popularity_distributions(analytic_df):
    """Verify course category, level, and type aggregations."""
    cat_pop = get_category_popularity(analytic_df)
    assert cat_pop["Enrollments"].sum() == 6
    assert cat_pop.iloc[0]["CourseCategory"] == "Programming"

    lvl_demand = get_level_demand(analytic_df)
    assert lvl_demand["Enrollments"].sum() == 6

    type_dist = get_type_distribution(analytic_df)
    assert type_dist["Enrollments"].sum() == 6


def test_learner_concentration(analytic_df):
    """Verify multi-course learner concentration and Pareto calculations."""
    conc = get_learner_concentration(analytic_df)
    assert conc["mean_courses"] == 1.2
    assert "distribution_df" in conc
    assert conc["distribution_df"]["Learners"].sum() == 5


def test_gender_category_breakdown(analytic_df):
    """Verify gender by course category preference calculation."""
    res = get_gender_category_breakdown(analytic_df)
    assert not res.empty
    assert "CourseCategory" in res.columns
    assert "Gender" in res.columns
    assert "Enrollments" in res.columns
    assert res["Enrollments"].sum() == 6

