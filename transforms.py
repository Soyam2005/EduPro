"""Data transformation, normalization, age band derivation, and relational joining."""

import logging
from typing import Tuple, Dict, Any, Union
import pandas as pd
import numpy as np

from src.constants import AGE_BAND_ORDER

logger = logging.getLogger(__name__)


def derive_age_group(
    age: Union[float, int, pd.Series]
) -> Union[str, pd.Series]:
    """Map numeric age to standardized age bands:
    - '<18': age < 18
    - '18–25': 18 <= age <= 25
    - '26–35': 26 <= age <= 35
    - '36–45': 36 <= age <= 45
    - '45+': age > 45
    
    Returns 'Unknown' for null or non-numeric values.
    """
    def _assign_single(val):
        if pd.isna(val):
            return "Unknown"
        try:
            num = float(val)
        except (ValueError, TypeError):
            return "Unknown"
            
        if num < 18:
            return "<18"
        elif 18 <= num <= 25:
            return "18–25"
        elif 26 <= num <= 35:
            return "26–35"
        elif 36 <= num <= 45:
            return "36–45"
        else:
            return "45+"

    if isinstance(age, pd.Series):
        return age.apply(_assign_single)
    return _assign_single(age)


def clean_and_normalize(
    users_df: pd.DataFrame, courses_df: pd.DataFrame, transactions_df: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Normalize strings, cast identifiers to string, and parse numeric and date types.
    Source DataFrames are treated as immutable and never modified in place.
    """
    u_clean = users_df.copy()
    c_clean = courses_df.copy()
    t_clean = transactions_df.copy()

    # Cast identifiers as stripped strings
    u_clean["UserID"] = u_clean["UserID"].astype(str).str.strip()
    c_clean["CourseID"] = c_clean["CourseID"].astype(str).str.strip()
    t_clean["TransactionID"] = t_clean["TransactionID"].astype(str).str.strip()
    t_clean["UserID"] = t_clean["UserID"].astype(str).str.strip()
    t_clean["CourseID"] = t_clean["CourseID"].astype(str).str.strip()

    # Clean Users
    if "UserName" in u_clean.columns:
        u_clean["UserName"] = u_clean["UserName"].astype(str).str.strip()
    if "Gender" in u_clean.columns:
        u_clean["Gender"] = u_clean["Gender"].astype(str).str.strip().str.capitalize()
    u_clean["Age"] = pd.to_numeric(u_clean["Age"], errors="coerce")
    u_clean["AgeGroup"] = derive_age_group(u_clean["Age"])

    # Clean Courses
    str_course_cols = ["CourseName", "CourseCategory", "CourseType", "CourseLevel"]
    for col in str_course_cols:
        if col in c_clean.columns:
            c_clean[col] = c_clean[col].astype(str).str.strip()
            if col in ["CourseType", "CourseLevel"]:
                c_clean[col] = c_clean[col].str.capitalize()

    # Clean Transactions
    t_clean["TransactionDate"] = pd.to_datetime(t_clean["TransactionDate"], errors="coerce")
    if "PaymentMethod" in t_clean.columns:
        t_clean["PaymentMethod"] = t_clean["PaymentMethod"].astype(str).str.strip()

    return u_clean, c_clean, t_clean


def build_analytic_dataset(
    users_df: pd.DataFrame, courses_df: pd.DataFrame, transactions_df: pd.DataFrame
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Clean tables, validate foreign keys, and perform relational join.
    
    Join path: Users.UserID -> Transactions.UserID <- Courses.CourseID.
    
    Returns:
        analytic_df: Canonical joined DataFrame for metrics and visualizations.
        stats: Dictionary containing join audit metadata.
    """
    u_clean, c_clean, t_clean = clean_and_normalize(users_df, courses_df, transactions_df)

    # Referential check
    valid_u_ids = set(u_clean["UserID"])
    valid_c_ids = set(c_clean["CourseID"])

    initial_tx_count = len(t_clean)
    valid_tx = t_clean[
        t_clean["UserID"].isin(valid_u_ids) & t_clean["CourseID"].isin(valid_c_ids)
    ].copy()
    
    dropped_tx_count = initial_tx_count - len(valid_tx)

    # Relational Join
    joined = valid_tx.merge(
        u_clean, on="UserID", how="inner", suffixes=("", "_user")
    ).merge(
        c_clean, on="CourseID", how="inner", suffixes=("", "_course")
    )

    # Ensure AgeGroup has category type ordered according to constants
    existing_bands = [b for b in AGE_BAND_ORDER if b in joined["AgeGroup"].values]
    if "Unknown" in joined["AgeGroup"].values:
        existing_bands.append("Unknown")
    joined["AgeGroup"] = pd.Categorical(
        joined["AgeGroup"], categories=existing_bands, ordered=True
    )

    stats = {
        "raw_user_count": len(users_df),
        "raw_course_count": len(courses_df),
        "raw_transaction_count": len(transactions_df),
        "joined_transaction_count": len(joined),
        "excluded_transactions": dropped_tx_count,
        "unique_active_learners": joined["UserID"].nunique(),
        "unique_enrolled_courses": joined["CourseID"].nunique(),
        "min_transaction_date": joined["TransactionDate"].min(),
        "max_transaction_date": joined["TransactionDate"].max(),
    }

    logger.info(
        f"Analytic dataset created: {len(joined)} records from {stats['unique_active_learners']} active learners."
    )
    return joined, stats
