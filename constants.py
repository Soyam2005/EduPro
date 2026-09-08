"""Constants, design tokens, and schema definitions for EduPro Learner Intelligence."""

from typing import List, Dict

# Documented fixed age-band order
AGE_BAND_ORDER: List[str] = ["<18", "18–25", "26–35", "36–45", "45+"]

# Categorical orderings
LEVEL_ORDER: List[str] = ["Beginner", "Intermediate", "Advanced"]
TYPE_ORDER: List[str] = ["Free", "Paid"]

# Required fields per table according to PRD
REQUIRED_USER_COLUMNS: List[str] = ["UserID", "UserName", "Age", "Gender"]
REQUIRED_COURSE_COLUMNS: List[str] = [
    "CourseID",
    "CourseName",
    "CourseCategory",
    "CourseType",
    "CourseLevel",
]
REQUIRED_TRANSACTION_COLUMNS: List[str] = [
    "TransactionID",
    "UserID",
    "CourseID",
    "TransactionDate",
]

# Sheet names
SHEET_USERS = "Users"
SHEET_COURSES = "Courses"
SHEET_TRANSACTIONS = "Transactions"

# ──────────────────────────────────────────────────────────
# Design Tokens — Light Theme (Design.md)
# ──────────────────────────────────────────────────────────
_LIGHT: Dict[str, str] = {
    # Layout
    "background": "#F0F4FF",
    "surface": "#FFFFFF",
    "border": "#DDE3F0",
    # Text
    "text_primary": "#0B1437",
    "text_secondary": "#4A5578",
    # Sidebar
    "sidebar_bg": "#FFFFFF",
    "sidebar_border": "#DDE3F0",
    "sidebar_heading": "#0B1437",
    "sidebar_caption": "#64748B",
    # Multiselect tags
    "tag_bg": "#EEF2FF",
    "tag_border": "#C7D2FE",
    "tag_text": "#4338CA",
    # Select input
    "select_bg": "#FFFFFF",
    "select_border": "#C7D2FE",
    "select_text": "#0B1437",
    # Buttons
    "btn_bg": "#F0F4FF",
    "btn_text": "#0B1437",
    "btn_border": "#C7D2FE",
    "btn_hover_bg": "#EEF2FF",
    "btn_hover_border": "#818CF8",
    "btn_hover_text": "#4338CA",
    # Status badge
    "badge_bg": "#ECFDF5",
    "badge_text": "#065F46",
    "badge_border": "#A7F3D0",
    # Observation callout
    "observation_bg": "#F5F3FF",
    # Brand
    "primary": "#4F46E5",
    "indigo": "#6366F1",
    "teal": "#0891B2",
    "amber": "#D97706",
    "red": "#B91C1C",
    "muted_blue": "#818CF8",
    "slate": "#64748B",
    # Charts
    "plot_bg": "rgba(0,0,0,0)",
    "paper_bg": "rgba(0,0,0,0)",
    "grid_color": "#E8EDFA",
    "font_color": "#4A5578",
}

# ──────────────────────────────────────────────────────────
# Design Tokens — Dark Theme
# ──────────────────────────────────────────────────────────
_DARK: Dict[str, str] = {
    # Layout
    "background": "#080D1A",
    "surface": "#111827",
    "border": "#1F2B47",
    # Text
    "text_primary": "#EEF2FF",
    "text_secondary": "#8B9EC7",
    # Sidebar
    "sidebar_bg": "#0D1526",
    "sidebar_border": "#1F2B47",
    "sidebar_heading": "#EEF2FF",
    "sidebar_caption": "#5C6B8A",
    # Multiselect tags
    "tag_bg": "#1A2240",
    "tag_border": "#4F46E5",
    "tag_text": "#A5B4FC",
    # Select input
    "select_bg": "#111827",
    "select_border": "#2E3F63",
    "select_text": "#EEF2FF",
    # Buttons
    "btn_bg": "#1F2B47",
    "btn_text": "#EEF2FF",
    "btn_border": "#2E3F63",
    "btn_hover_bg": "#1A2240",
    "btn_hover_border": "#4F46E5",
    "btn_hover_text": "#A5B4FC",
    # Status badge
    "badge_bg": "#052E16",
    "badge_text": "#6EE7B7",
    "badge_border": "#059669",
    # Observation callout
    "observation_bg": "#111827",
    # Brand (vivid on dark)
    "primary": "#818CF8",
    "indigo": "#6366F1",
    "teal": "#22D3EE",
    "amber": "#FCD34D",
    "red": "#F87171",
    "muted_blue": "#A5B4FC",
    "slate": "#64748B",
    # Charts
    "plot_bg": "rgba(0,0,0,0)",
    "paper_bg": "rgba(0,0,0,0)",
    "grid_color": "#1F2B47",
    "font_color": "#8B9EC7",
}


def get_theme_colors(dark: bool = False) -> Dict[str, str]:
    """Return the active design-token dictionary for the requested theme.

    Args:
        dark: True for dark theme, False (default) for light theme.

    Returns:
        Dictionary of colour tokens keyed by semantic role.
    """
    return _DARK.copy() if dark else _LIGHT.copy()


# Convenience alias for older imports
THEME_COLORS: Dict[str, str] = _LIGHT

# ──────────────────────────────────────────────────────────
# Chart Categorical Color Sequence — Vibrant 12-color
# ──────────────────────────────────────────────────────────
CHART_PALETTE: List[str] = [
    "#6366F1",  # Indigo
    "#06B6D4",  # Cyan
    "#F59E0B",  # Amber
    "#10B981",  # Emerald
    "#F43F5E",  # Rose
    "#8B5CF6",  # Violet
    "#3B82F6",  # Blue
    "#F97316",  # Orange
    "#14B8A6",  # Teal
    "#EC4899",  # Pink
    "#84CC16",  # Lime
    "#A78BFA",  # Soft Violet
]

# ──────────────────────────────────────────────────────────
# Gender Palette — visually distinct, accessible
# Female = coral-rose  |  Male = electric indigo
# ──────────────────────────────────────────────────────────
GENDER_PALETTE: Dict[str, str] = {
    "Female": "#F43F5E",   # Vibrant rose/coral
    "Male": "#6366F1",     # Electric indigo
    "Other": "#F59E0B",    # Warm amber
    "Unknown": "#64748B",  # Slate
}

# Level Palette — difficulty gradient (green→blue→amber)
LEVEL_PALETTE: Dict[str, str] = {
    "Beginner": "#10B981",     # Emerald
    "Intermediate": "#6366F1", # Indigo
    "Advanced": "#F59E0B",     # Amber
}

# Type Palette
TYPE_PALETTE: Dict[str, str] = {
    "Free": "#10B981",   # Emerald
    "Paid": "#6366F1",   # Indigo
}

# ──────────────────────────────────────────────────────────
# Gradient Stop Catalog — for chart fill gradients
# ──────────────────────────────────────────────────────────
GRADIENT_VIOLET_CYAN = [
    "#4F46E5", "#5B52EF", "#6B5EF8",
    "#7B6AF9", "#8B76FA", "#06B6D4",
]

GRADIENT_ROSE_AMBER = [
    "#F43F5E", "#FB7185", "#FBBF24", "#F59E0B",
]

GRADIENT_TEAL_INDIGO = [
    "#0891B2", "#06B6D4", "#22D3EE",
    "#818CF8", "#6366F1", "#4F46E5",
]
