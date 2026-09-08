"""Data loading, schema verification, and referential integrity auditing for EduPro."""

import os
import logging
from typing import Tuple, Dict, Any, List, Optional
import pandas as pd

from src.constants import (
    REQUIRED_USER_COLUMNS,
    REQUIRED_COURSE_COLUMNS,
    REQUIRED_TRANSACTION_COLUMNS,
    SHEET_USERS,
    SHEET_COURSES,
    SHEET_TRANSACTIONS,
)

logger = logging.getLogger(__name__)


def validate_schemas(
    users_df: pd.DataFrame, courses_df: pd.DataFrame, transactions_df: pd.DataFrame
) -> List[str]:
    """Validate that all required columns are present in the loaded DataFrames.
    
    Returns:
        List of validation error messages (empty if all valid).
    """
    errors: List[str] = []
    
    missing_users = [col for col in REQUIRED_USER_COLUMNS if col not in users_df.columns]
    if missing_users:
        errors.append(f"Users table is missing required columns: {', '.join(missing_users)}")
        
    missing_courses = [col for col in REQUIRED_COURSE_COLUMNS if col not in courses_df.columns]
    if missing_courses:
        errors.append(f"Courses table is missing required columns: {', '.join(missing_courses)}")
        
    missing_tx = [col for col in REQUIRED_TRANSACTION_COLUMNS if col not in transactions_df.columns]
    if missing_tx:
        errors.append(f"Transactions table is missing required columns: {', '.join(missing_tx)}")
        
    return errors


def check_referential_integrity(
    users_df: pd.DataFrame, courses_df: pd.DataFrame, transactions_df: pd.DataFrame
) -> Dict[str, Any]:
    """Audit primary key uniqueness, foreign key relationships, and null values."""
    # Ensure ID columns are cast as string identifiers
    user_ids = set(users_df["UserID"].dropna().astype(str))
    course_ids = set(courses_df["CourseID"].dropna().astype(str))
    
    tx_user_ids = transactions_df["UserID"].dropna().astype(str)
    tx_course_ids = transactions_df["CourseID"].dropna().astype(str)
    
    unmatched_users = tx_user_ids[~tx_user_ids.isin(user_ids)]
    unmatched_courses = tx_course_ids[~tx_course_ids.isin(course_ids)]
    
    user_duplicates = users_df["UserID"].duplicated().sum()
    course_duplicates = courses_df["CourseID"].duplicated().sum()
    tx_duplicates = transactions_df["TransactionID"].duplicated().sum()
    
    null_users = users_df[REQUIRED_USER_COLUMNS].isnull().sum().to_dict()
    null_courses = courses_df[REQUIRED_COURSE_COLUMNS].isnull().sum().to_dict()
    null_tx = transactions_df[REQUIRED_TRANSACTION_COLUMNS].isnull().sum().to_dict()
    
    return {
        "total_users": len(users_df),
        "total_courses": len(courses_df),
        "total_transactions": len(transactions_df),
        "duplicate_user_ids": int(user_duplicates),
        "duplicate_course_ids": int(course_duplicates),
        "duplicate_transaction_ids": int(tx_duplicates),
        "unmatched_user_transactions": int(len(unmatched_users)),
        "unmatched_course_transactions": int(len(unmatched_courses)),
        "unmatched_user_ids_sample": list(unmatched_users.unique()[:5]),
        "unmatched_course_ids_sample": list(unmatched_courses.unique()[:5]),
        "null_counts": {
            "users": null_users,
            "courses": null_courses,
            "transactions": null_tx,
        },
        "is_healthy": (
            len(unmatched_users) == 0
            and len(unmatched_courses) == 0
            and user_duplicates == 0
            and course_duplicates == 0
            and tx_duplicates == 0
        ),
    }


def load_raw_data(
    file_path: str,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """Load Users, Courses, and Transactions from an Excel workbook and audit quality.
    
    Raises:
        FileNotFoundError: If file does not exist.
        ValueError: If sheets or required columns are missing.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Source file not found at: {file_path}")

    try:
        excel_file = pd.ExcelFile(file_path)
    except Exception as e:
        logger.error(f"Failed to read Excel file at {file_path}: {e}")
        raise ValueError(f"Failed to parse Excel workbook: {str(e)}")

    sheet_names = excel_file.sheet_names
    for required_sheet in [SHEET_USERS, SHEET_COURSES, SHEET_TRANSACTIONS]:
        if required_sheet not in sheet_names:
            raise ValueError(
                f"Missing required sheet '{required_sheet}'. Available sheets: {', '.join(sheet_names)}"
            )

    users_df = pd.read_excel(excel_file, sheet_name=SHEET_USERS)
    courses_df = pd.read_excel(excel_file, sheet_name=SHEET_COURSES)
    transactions_df = pd.read_excel(excel_file, sheet_name=SHEET_TRANSACTIONS)

    # Schema validation
    schema_errors = validate_schemas(users_df, courses_df, transactions_df)
    if schema_errors:
        raise ValueError(" | ".join(schema_errors))

    # Audit referential integrity
    integrity_report = check_referential_integrity(users_df, courses_df, transactions_df)

    return users_df, courses_df, transactions_df, integrity_report
