"""KPI calculation, demographic aggregations, cross-tabulations, and behavioral metrics."""

import logging
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np

from src.constants import AGE_BAND_ORDER, LEVEL_ORDER, TYPE_ORDER

logger = logging.getLogger(__name__)


def apply_filters(
    df: pd.DataFrame,
    age_groups: Optional[List[str]] = None,
    genders: Optional[List[str]] = None,
    categories: Optional[List[str]] = None,
    levels: Optional[List[str]] = None,
) -> pd.DataFrame:
    """Filter the analytic dataset based on active sidebar selections.
    
    If a filter parameter is None or empty, that filter is not applied.
    """
    if df.empty:
        return df.copy()

    filtered = df.copy()

    if age_groups:
        filtered = filtered[filtered["AgeGroup"].isin(age_groups)]

    if genders:
        filtered = filtered[filtered["Gender"].isin(genders)]

    if categories:
        filtered = filtered[filtered["CourseCategory"].isin(categories)]

    if levels:
        filtered = filtered[filtered["CourseLevel"].isin(levels)]

    return filtered


def compute_kpis(
    filtered_df: pd.DataFrame, total_unfiltered_count: Optional[int] = None
) -> Dict[str, Any]:
    """Compute top-level KPI metrics safely with zero-division protection.
    
    KPIs:
    - Total Enrollments
    - Active Learners
    - Leading Course Category (name, count, share)
    - Leading Course Level (name, count, share)
    - Average Courses per Active Learner
    """
    total_enrollments = len(filtered_df)
    
    if total_enrollments == 0:
        return {
            "total_enrollments": 0,
            "enrollment_share_of_platform": 0.0,
            "active_learners": 0,
            "avg_courses_per_learner": 0.0,
            "leading_category": "N/A",
            "leading_category_count": 0,
            "leading_category_share": 0.0,
            "leading_level": "N/A",
            "leading_level_count": 0,
            "leading_level_share": 0.0,
        }

    active_learners = filtered_df["UserID"].nunique()
    avg_courses = total_enrollments / active_learners if active_learners > 0 else 0.0

    platform_share = (
        (total_enrollments / total_unfiltered_count * 100.0)
        if total_unfiltered_count and total_unfiltered_count > 0
        else 100.0
    )

    # Leading category
    cat_counts = filtered_df["CourseCategory"].value_counts()
    leading_category = cat_counts.index[0] if not cat_counts.empty else "N/A"
    leading_cat_count = int(cat_counts.iloc[0]) if not cat_counts.empty else 0
    leading_cat_share = (leading_cat_count / total_enrollments * 100.0) if total_enrollments > 0 else 0.0

    # Leading level
    lvl_counts = filtered_df["CourseLevel"].value_counts()
    leading_level = lvl_counts.index[0] if not lvl_counts.empty else "N/A"
    leading_lvl_count = int(lvl_counts.iloc[0]) if not lvl_counts.empty else 0
    leading_lvl_share = (leading_lvl_count / total_enrollments * 100.0) if total_enrollments > 0 else 0.0

    return {
        "total_enrollments": total_enrollments,
        "enrollment_share_of_platform": round(platform_share, 1),
        "active_learners": active_learners,
        "avg_courses_per_learner": round(avg_courses, 2),
        "leading_category": leading_category,
        "leading_category_count": leading_cat_count,
        "leading_category_share": round(leading_cat_share, 1),
        "leading_level": leading_level,
        "leading_level_count": leading_lvl_count,
        "leading_level_share": round(leading_lvl_share, 1),
    }


def get_age_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Compute distinct learner age distribution from filtered enrollments."""
    if df.empty:
        return pd.DataFrame(columns=["Age", "Learners", "Percentage"])
    
    learners = df.drop_duplicates(subset=["UserID"])
    counts = learners["Age"].value_counts().sort_index().reset_index()
    counts.columns = ["Age", "Learners"]
    total = len(learners)
    counts["Percentage"] = (counts["Learners"] / total * 100.0).round(1) if total > 0 else 0.0
    return counts


def get_gender_participation(df: pd.DataFrame) -> pd.DataFrame:
    """Compute distinct learner counts and enrollment counts by gender."""
    if df.empty:
        return pd.DataFrame(columns=["Gender", "Learners", "LearnerShare", "Enrollments", "EnrollmentShare"])

    learners = df.drop_duplicates(subset=["UserID"])
    learner_counts = learners["Gender"].value_counts()
    enrollment_counts = df["Gender"].value_counts()

    total_learners = len(learners)
    total_enrollments = len(df)

    genders = sorted(list(set(learner_counts.index).union(set(enrollment_counts.index))))
    rows = []
    for g in genders:
        l_cnt = int(learner_counts.get(g, 0))
        e_cnt = int(enrollment_counts.get(g, 0))
        l_pct = round((l_cnt / total_learners * 100.0), 1) if total_learners > 0 else 0.0
        e_pct = round((e_cnt / total_enrollments * 100.0), 1) if total_enrollments > 0 else 0.0
        rows.append({
            "Gender": g,
            "Learners": l_cnt,
            "LearnerShare": l_pct,
            "Enrollments": e_cnt,
            "EnrollmentShare": e_pct,
        })
    return pd.DataFrame(rows)


def get_age_enrollment_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Compute total enrollment counts and shares across standardized age bands."""
    if df.empty:
        return pd.DataFrame(columns=["AgeGroup", "Enrollments", "Percentage"])

    counts = df["AgeGroup"].value_counts()
    total = len(df)
    
    rows = []
    for band in AGE_BAND_ORDER:
        cnt = int(counts.get(band, 0))
        pct = round((cnt / total * 100.0), 1) if total > 0 else 0.0
        rows.append({"AgeGroup": band, "Enrollments": cnt, "Percentage": pct})
    
    # Check for any unexpected or Unknown band
    for band in counts.index:
        if band not in AGE_BAND_ORDER:
            cnt = int(counts[band])
            pct = round((cnt / total * 100.0), 1) if total > 0 else 0.0
            rows.append({"AgeGroup": str(band), "Enrollments": cnt, "Percentage": pct})

    return pd.DataFrame(rows)


def get_category_popularity(df: pd.DataFrame) -> pd.DataFrame:
    """Compute enrollments, distinct learners, and shares by course category."""
    if df.empty:
        return pd.DataFrame(columns=["CourseCategory", "Enrollments", "Percentage", "ActiveLearners"])

    total = len(df)
    grouped = df.groupby("CourseCategory").agg(
        Enrollments=("TransactionID", "count"),
        ActiveLearners=("UserID", "nunique")
    ).reset_index()

    grouped["Percentage"] = (grouped["Enrollments"] / total * 100.0).round(1) if total > 0 else 0.0
    grouped = grouped.sort_values(by="Enrollments", ascending=False).reset_index(drop=True)
    return grouped


def get_level_demand(df: pd.DataFrame) -> pd.DataFrame:
    """Compute enrollments and shares by course level in logical progression order."""
    if df.empty:
        return pd.DataFrame(columns=["CourseLevel", "Enrollments", "Percentage"])

    total = len(df)
    counts = df["CourseLevel"].value_counts()

    rows = []
    for lvl in LEVEL_ORDER:
        cnt = int(counts.get(lvl, 0))
        pct = round((cnt / total * 100.0), 1) if total > 0 else 0.0
        rows.append({"CourseLevel": lvl, "Enrollments": cnt, "Percentage": pct})

    for lvl in counts.index:
        if lvl not in LEVEL_ORDER:
            cnt = int(counts[lvl])
            pct = round((cnt / total * 100.0), 1) if total > 0 else 0.0
            rows.append({"CourseLevel": str(lvl), "Enrollments": cnt, "Percentage": pct})

    return pd.DataFrame(rows)


def get_type_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Compute enrollments and shares by course type (Free vs Paid)."""
    if df.empty:
        return pd.DataFrame(columns=["CourseType", "Enrollments", "Percentage"])

    total = len(df)
    counts = df["CourseType"].value_counts()
    
    rows = []
    for t in TYPE_ORDER:
        cnt = int(counts.get(t, 0))
        pct = round((cnt / total * 100.0), 1) if total > 0 else 0.0
        rows.append({"CourseType": t, "Enrollments": cnt, "Percentage": pct})

    for t in counts.index:
        if t not in TYPE_ORDER:
            cnt = int(counts[t])
            pct = round((cnt / total * 100.0), 1) if total > 0 else 0.0
            rows.append({"CourseType": str(t), "Enrollments": cnt, "Percentage": pct})

    return pd.DataFrame(rows)


def get_age_category_crosstab(df: pd.DataFrame) -> pd.DataFrame:
    """Produce pivot table of AgeGroup vs CourseCategory for heatmap visualization."""
    if df.empty:
        return pd.DataFrame()

    ct = pd.crosstab(df["AgeGroup"], df["CourseCategory"])
    # Reindex rows to match AGE_BAND_ORDER where present
    existing_rows = [b for b in AGE_BAND_ORDER if b in ct.index]
    ct = ct.reindex(existing_rows)
    return ct


def get_gender_level_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Compute cross-tabulation of Gender and CourseLevel."""
    if df.empty:
        return pd.DataFrame(columns=["Gender", "CourseLevel", "Enrollments", "PercentageWithinGender"])

    ct = df.groupby(["Gender", "CourseLevel"])["TransactionID"].count().reset_index()
    ct.columns = ["Gender", "CourseLevel", "Enrollments"]

    # Calculate percentage within gender
    gender_totals = df.groupby("Gender")["TransactionID"].count().to_dict()
    ct["PercentageWithinGender"] = ct.apply(
        lambda r: round(r["Enrollments"] / gender_totals.get(r["Gender"], 1) * 100.0, 1),
        axis=1
    )
    return ct


def get_gender_category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Compute cross-tabulation of Gender and CourseCategory for preference analysis."""
    if df.empty or "Gender" not in df.columns or "CourseCategory" not in df.columns:
        return pd.DataFrame(columns=["CourseCategory", "Gender", "Enrollments", "PercentageWithinGender"])

    ct = df.groupby(["CourseCategory", "Gender"])["TransactionID"].count().reset_index()
    ct.columns = ["CourseCategory", "Gender", "Enrollments"]

    gender_totals = df.groupby("Gender")["TransactionID"].count().to_dict()
    ct["PercentageWithinGender"] = ct.apply(
        lambda r: round(r["Enrollments"] / max(gender_totals.get(r["Gender"], 1), 1) * 100.0, 1),
        axis=1,
    )
    return ct


def get_learner_concentration(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze learner engagement depth and enrollment concentration.
    
    Returns:
    - Distribution of courses per user (1 course, 2-3 courses, 4+ courses)
    - Mean and median courses per learner
    - Pareto metric: Top 20% most active learners share of total enrollments
    """
    if df.empty:
        return {
            "mean_courses": 0.0,
            "median_courses": 0.0,
            "top_20_share": 0.0,
            "distribution_df": pd.DataFrame(columns=["CourseCountBucket", "Learners", "Percentage"]),
        }

    courses_per_user = df.groupby("UserID")["CourseID"].count()
    mean_courses = float(courses_per_user.mean())
    median_courses = float(courses_per_user.median())

    # Pareto top 20% calculation
    n_top = max(1, int(len(courses_per_user) * 0.2))
    top_20_enrollments = courses_per_user.sort_values(ascending=False).iloc[:n_top].sum()
    top_20_share = round((top_20_enrollments / len(df) * 100.0), 1)

    # Bucketing
    def _bucket(n):
        if n == 1:
            return "1 course"
        elif 2 <= n <= 3:
            return "2–3 courses"
        else:
            return "4+ courses"

    buckets = courses_per_user.apply(_bucket).value_counts()
    bucket_order = ["1 course", "2–3 courses", "4+ courses"]
    total_learners = len(courses_per_user)

    bucket_rows = []
    for b in bucket_order:
        cnt = int(buckets.get(b, 0))
        pct = round((cnt / total_learners * 100.0), 1) if total_learners > 0 else 0.0
        bucket_rows.append({"CourseCountBucket": b, "Learners": cnt, "Percentage": pct})

    return {
        "mean_courses": round(mean_courses, 2),
        "median_courses": round(median_courses, 1),
        "top_20_share": top_20_share,
        "distribution_df": pd.DataFrame(bucket_rows),
    }
