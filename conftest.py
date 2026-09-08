"""Pytest fixtures with synthetic and representative datasets for testing."""

import pytest
import pandas as pd


@pytest.fixture
def sample_users_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"UserID": "U001", "UserName": "alice", "Age": 16, "Gender": "Female"},
            {"UserID": "U002", "UserName": "bob", "Age": 22, "Gender": "Male"},
            {"UserID": "U003", "UserName": "carol", "Age": 30, "Gender": " female "},
            {"UserID": "U004", "UserName": "david", "Age": 40, "Gender": "Male"},
            {"UserID": "U005", "UserName": "eve", "Age": 55, "Gender": "Female"},
        ]
    )


@pytest.fixture
def sample_courses_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "CourseID": "C001",
                "CourseName": "Python Basics",
                "CourseCategory": "Programming",
                "CourseType": "Free",
                "CourseLevel": "Beginner",
            },
            {
                "CourseID": "C002",
                "CourseName": "Advanced UI Design",
                "CourseCategory": "Design",
                "CourseType": "Paid",
                "CourseLevel": "Advanced",
            },
            {
                "CourseID": "C003",
                "CourseName": "Business Strategy",
                "CourseCategory": "Business",
                "CourseType": "Paid",
                "CourseLevel": "Intermediate",
            },
        ]
    )


@pytest.fixture
def sample_transactions_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"TransactionID": "T001", "UserID": "U001", "CourseID": "C001", "TransactionDate": "2025-01-10"},
            {"TransactionID": "T002", "UserID": "U002", "CourseID": "C001", "TransactionDate": "2025-01-15"},
            {"TransactionID": "T003", "UserID": "U002", "CourseID": "C002", "TransactionDate": "2025-02-01"},
            {"TransactionID": "T004", "UserID": "U003", "CourseID": "C003", "TransactionDate": "2025-02-10"},
            {"TransactionID": "T005", "UserID": "U004", "CourseID": "C001", "TransactionDate": "2025-03-01"},
            {"TransactionID": "T006", "UserID": "U005", "CourseID": "C002", "TransactionDate": "2025-03-15"},
        ]
    )


@pytest.fixture
def transactions_with_unmatched_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"TransactionID": "T001", "UserID": "U001", "CourseID": "C001", "TransactionDate": "2025-01-10"},
            {"TransactionID": "T002", "UserID": "U999", "CourseID": "C001", "TransactionDate": "2025-01-15"}, # Orphan user
            {"TransactionID": "T003", "UserID": "U002", "CourseID": "C999", "TransactionDate": "2025-02-01"}, # Orphan course
        ]
    )
