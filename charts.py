"""Plotly Express and Graph Objects chart builders — creative, ultra-premium theme-aware designs."""

from typing import Optional, Dict, Any, List
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.constants import (
    GENDER_PALETTE,
    LEVEL_PALETTE,
    TYPE_PALETTE,
    CHART_PALETTE,
    get_theme_colors,
)

FONT_FAMILY = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
_DEFAULT_TC = get_theme_colors(dark=False)


def _apply_common_layout(
    fig: go.Figure,
    title: str,
    tc: Dict[str, str],
    x_title: Optional[str] = None,
    y_title: Optional[str] = None,
    height: int = 390,
) -> go.Figure:
    """Apply consistent, ultra-clean typography, colors, and margins."""
    fig.update_layout(
        title={
            "text": f"<span style='font-size:15px; font-weight:800; letter-spacing:-0.2px; color:{tc['text_primary']};'>{title}</span>",
            "font": {"family": FONT_FAMILY, "color": tc["text_primary"]},
            "x": 0.015,
            "xanchor": "left",
            "y": 0.96,
        },
        font={"family": FONT_FAMILY, "color": tc["font_color"], "size": 12},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin={"l": 45, "r": 25, "t": 60, "b": 45},
        modebar={
            "bgcolor": "rgba(0,0,0,0)",
            "color": tc["text_secondary"],
            "activecolor": tc["primary"],
        },
        xaxis={
            "title": {"text": x_title, "font": {"size": 11, "weight": 600, "color": tc["text_secondary"]}} if x_title else None,
            "showgrid": True,
            "gridcolor": tc["grid_color"],
            "gridwidth": 1,
            "zeroline": False,
            "tickfont": {"size": 11, "color": tc["text_secondary"], "family": FONT_FAMILY},
        },
        yaxis={
            "title": {"text": y_title, "font": {"size": 11, "weight": 600, "color": tc["text_secondary"]}} if y_title else None,
            "showgrid": True,
            "gridcolor": tc["grid_color"],
            "gridwidth": 1,
            "zeroline": False,
            "tickfont": {"size": 11, "color": tc["text_secondary"], "family": FONT_FAMILY},
        },
        legend={
            "font": {"size": 11, "weight": 600, "color": tc["text_secondary"], "family": FONT_FAMILY},
            "bgcolor": "rgba(0,0,0,0)",
            "bordercolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1.0,
        },
        hoverlabel={
            "bgcolor": tc["surface"],
            "font": {"family": FONT_FAMILY, "size": 12, "color": tc["text_primary"]},
            "bordercolor": tc["border"],
            "namelength": -1,
        },
    )
    return fig


def create_empty_state_figure(
    message: str = "No data available for the selected filters.",
    theme: Optional[Dict[str, str]] = None,
) -> go.Figure:
    """Generate a clean, centered empty-state placeholder figure."""
    tc = theme or _DEFAULT_TC
    fig = go.Figure()
    fig.add_annotation(
        text=f"<b>✨ No Data Found</b><br><span style='font-size:12px;color:{tc['text_secondary']};'>{message}</span>",
        xref="paper", yref="paper", x=0.5, y=0.5,
        showarrow=False,
        font={"family": FONT_FAMILY, "size": 14, "color": tc["text_primary"]},
        align="center",
    )
    _apply_common_layout(fig, title="", tc=tc, height=280)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
    return fig


# ---------------------------------------------------------
# 1. Age Distribution Chart (Spline Curve + Sleek Gradient Bars)
# ---------------------------------------------------------
def create_age_distribution_chart(
    df: pd.DataFrame,
    theme: Optional[Dict[str, str]] = None,
) -> go.Figure:
    """Distinct learner ages with rounded gradient bars and smoothed density line."""
    tc = theme or _DEFAULT_TC
    if df.empty or "Age" not in df.columns or df["Learners"].sum() == 0:
        return create_empty_state_figure("No learners match the current filter selection.", theme)

    df_sorted = df.sort_values("Age").copy()
    
    # Generate sequential gradient colors across the age span
    n_bars = len(df_sorted)
    # Indigo to Cyan gradient progression
    bar_colors = [
        f"rgba({int(79 + (6 - 79) * i / max(n_bars - 1, 1))}, "
        f"{int(70 + (182 - 70) * i / max(n_bars - 1, 1))}, "
        f"{int(229 + (212 - 229) * i / max(n_bars - 1, 1))}, 0.85)"
        for i in range(n_bars)
    ]

    fig = go.Figure()

    # Smooth backdrop density area
    fig.add_trace(go.Scatter(
        x=df_sorted["Age"],
        y=df_sorted["Learners"],
        mode="lines",
        line={"shape": "spline", "smoothing": 1.2, "width": 2.5, "color": "#6366F1"},
        fill="tozeroy",
        fillcolor="rgba(99, 102, 241, 0.08)",
        hoverinfo="skip",
        showlegend=False,
    ))

    # Sleek rounded bars
    fig.add_trace(go.Bar(
        x=df_sorted["Age"],
        y=df_sorted["Learners"],
        customdata=df_sorted["Percentage"],
        marker={
            "color": bar_colors,
            "cornerradius": 6,
            "line": {"width": 1, "color": "rgba(255, 255, 255, 0.2)" if tc["background"] == "#080D1A" else "rgba(99, 102, 241, 0.2)"},
        },
        hovertemplate="<b>Age %{x} Years</b><br>Learners: <b>%{y:,}</b><br>Cohort Share: <b>%{customdata:.1f}%</b><extra></extra>",
        showlegend=False,
    ))

    _apply_common_layout(fig, "Learner Age Distribution & Cohort Curve", tc, x_title="Learner Age (Years)", y_title="Distinct Learners")

    # Add subtle weighted mean line
    if len(df_sorted) > 0 and df_sorted["Learners"].sum() > 0:
        mean_age = (df_sorted["Age"] * df_sorted["Learners"]).sum() / df_sorted["Learners"].sum()
        fig.add_vline(
            x=mean_age,
            line_width=2,
            line_dash="dot",
            line_color=tc["amber"],
            annotation_text=f"<b>Avg {mean_age:.1f}y</b>",
            annotation_position="top left",
            annotation_font=dict(size=11, color=tc["amber"], family=FONT_FAMILY),
            annotation_bgcolor=tc["surface"],
            annotation_bordercolor=tc["amber"],
            annotation_borderwidth=1,
            annotation_borderpad=3,
        )

    fig.update_layout(bargap=0.25)
    return fig


# ---------------------------------------------------------
# 2. Gender Representation (Vibrant Donut with Glow & Accents)
# ---------------------------------------------------------
def create_gender_participation_chart(
    df: pd.DataFrame,
    theme: Optional[Dict[str, str]] = None,
) -> go.Figure:
    """Modern donut chart with contrasting gender palette and central metric."""
    tc = theme or _DEFAULT_TC
    if df.empty or df["Learners"].sum() == 0:
        return create_empty_state_figure("No gender data available.", theme)

    colors = [GENDER_PALETTE.get(g, tc["slate"]) for g in df["Gender"]]
    total_learners = int(df["Learners"].sum())

    fig = go.Figure(data=[go.Pie(
        labels=df["Gender"],
        values=df["Learners"],
        hole=0.68,
        marker={
            "colors": colors,
            "line": {"color": tc["surface"], "width": 3},
        },
        textinfo="percent+label",
        textposition="outside",
        textfont={"family": FONT_FAMILY, "size": 11, "weight": 700, "color": tc["text_primary"]},
        hovertemplate="<b>%{label} Learners</b><br>Count: <b>%{value:,}</b><br>Share: <b>%{percent}</b><extra></extra>",
        pull=[0.02, 0.02],
    )])

    # Center hole rich annotation
    fig.add_annotation(
        text=(
            f"<span style='font-size:24px; font-weight:900; letter-spacing:-1px; color:{tc['text_primary']};'>{total_learners:,}</span><br>"
            f"<span style='font-size:10px; font-weight:800; letter-spacing:1px; color:{tc['text_secondary']}; text-transform:uppercase;'>Learners</span>"
        ),
        x=0.5, y=0.5,
        showarrow=False,
        font={"family": FONT_FAMILY},
        align="center",
    )

    _apply_common_layout(fig, "Learner Gender Representation", tc, height=390)
    fig.update_layout(
        showlegend=False,
        margin={"l": 20, "r": 20, "t": 55, "b": 20},
    )
    return fig


# ---------------------------------------------------------
# 3. Age-Wise Enrollment Breakdown (Vibrant Stepped Gradient Bars)
# ---------------------------------------------------------
def create_age_enrollment_chart(
    df: pd.DataFrame,
    theme: Optional[Dict[str, str]] = None,
) -> go.Figure:
    """Enrollment volume by age band with prominent peak cohort badge."""
    tc = theme or _DEFAULT_TC
    if df.empty or df["Enrollments"].sum() == 0:
        return create_empty_state_figure("No enrollment data available by age band.", theme)

    max_idx = df["Enrollments"].idxmax()
    max_val = df["Enrollments"].max()

    # Dynamic palette: Highlight the peak with vivid cyan, others in gradient violet/indigo
    colors = []
    for i, row in df.iterrows():
        if i == max_idx:
            colors.append("#06B6D4")  # Vivid Cyan for peak
        else:
            colors.append("#6366F1")  # Indigo for standard

    fig = go.Figure()

    # Backdrop ghost bar to give pill container depth
    fig.add_trace(go.Bar(
        x=df["AgeGroup"],
        y=[max_val * 1.05] * len(df),
        marker_color="rgba(99, 102, 241, 0.06)",
        marker_cornerradius=10,
        showlegend=False,
        hoverinfo="skip",
        width=0.45,
    ))

    # Main vibrant bar
    fig.add_trace(go.Bar(
        x=df["AgeGroup"],
        y=df["Enrollments"],
        text=df["Percentage"].apply(lambda v: f"<b>{v:.1f}%</b>"),
        textposition="outside",
        textfont={"size": 11, "color": tc["text_primary"], "family": FONT_FAMILY},
        marker_color=colors,
        marker_cornerradius=8,
        marker_line={"width": 0},
        width=0.45,
        customdata=df["Percentage"],
        hovertemplate=(
            "<b>Age Band: %{x}</b><br>"
            "Enrollments: <b>%{y:,}</b><br>"
            "Platform Share: <b>%{customdata:.1f}%</b><extra></extra>"
        ),
        showlegend=False,
    ))

    # Add peak badge
    peak_band = df.loc[max_idx, "AgeGroup"]
    fig.add_annotation(
        x=peak_band, y=max_val,
        text="<b>🏆 Primary Cohort</b>",
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.5,
        arrowcolor="#06B6D4",
        ax=0, ay=-36,
        font={"size": 10, "color": "#06B6D4", "family": FONT_FAMILY, "weight": 700},
        bgcolor=tc["surface"],
        borderpad=4, bordercolor="#06B6D4", borderwidth=1.5,
    )

    _apply_common_layout(
        fig, "Enrollments by Demographic Age Band", tc,
        x_title="Standard Age Band", y_title="Total Enrollments", height=390,
    )
    fig.update_layout(barmode="overlay")
    fig.update_yaxes(range=[0, max_val * 1.25 if max_val > 0 else 100])
    fig.update_xaxes(showgrid=False)
    return fig


# ---------------------------------------------------------
# 4. Course Category Popularity (Ranked with Gradient & Rank Badges)
# ---------------------------------------------------------
def create_category_popularity_chart(
    df: pd.DataFrame,
    top_n: int = 12,
    theme: Optional[Dict[str, str]] = None,
) -> go.Figure:
    """Ranked horizontal bars with sequential spectrum gradient and rank badges."""
    tc = theme or _DEFAULT_TC
    if df.empty or df["Enrollments"].sum() == 0:
        return create_empty_state_figure("No category data available.", theme)

    df_plot = df.head(top_n).sort_values(by="Enrollments", ascending=True).reset_index(drop=True)
    n = len(df_plot)

    # Multi-hue vibrant gradient: Top ranked = vibrant coral/amber, mid = indigo, base = cyan
    spectrum = [
        "#06B6D4", "#0891B2", "#2563EB", "#3B82F6",
        "#4F46E5", "#6366F1", "#7C3AED", "#8B5CF6",
        "#D946EF", "#EC4899", "#F43F5E", "#F59E0B",
    ]
    colors = [spectrum[int(i * (len(spectrum) - 1) / max(n - 1, 1))] for i in range(n)]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_plot["Enrollments"],
        y=df_plot["CourseCategory"],
        orientation="h",
        text=df_plot.apply(lambda r: f"<b>{r['Enrollments']:,}</b> ({r['Percentage']:.1f}%)", axis=1),
        textposition="outside",
        textfont={"size": 10.5, "color": tc["text_secondary"], "family": FONT_FAMILY},
        marker_color=colors,
        marker_cornerradius=6,
        marker_line={"width": 0},
        customdata=list(zip(df_plot["Percentage"], df_plot["ActiveLearners"])),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Total Enrollments: <b>%{x:,}</b><br>"
            "Platform Demand Share: <b>%{customdata[0]:.1f}%</b><br>"
            "Unique Active Learners: <b>%{customdata[1]:,}</b><extra></extra>"
        ),
    ))

    # Add custom rank label indicators
    for i, row in df_plot.iterrows():
        rank = n - i
        badge_symbol = "🥇 " if rank == 1 else ("🥈 " if rank == 2 else ("🥉 " if rank == 3 else f"#{rank} "))
        fig.add_annotation(
            x=0, y=row["CourseCategory"],
            text=f"<b>{badge_symbol}</b>",
            xanchor="right", xshift=-4,
            showarrow=False,
            font={"size": 10, "color": tc["text_secondary"], "family": FONT_FAMILY},
        )

    _apply_common_layout(
        fig, "Course Category Popularity (Ranked Catalog)", tc,
        x_title="Enrollments Volume", y_title="", height=440,
    )
    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=False)
    fig.update_layout(margin={"l": 25, "r": 90, "t": 60, "b": 40})
    return fig


# ---------------------------------------------------------
# 5. Course Level Demand (Difficulty Semantic Trio with Shadow Track)
# ---------------------------------------------------------
def create_level_demand_chart(
    df: pd.DataFrame,
    theme: Optional[Dict[str, str]] = None,
) -> go.Figure:
    """Course-level demand with semantic emerald/indigo/amber tier styling."""
    tc = theme or _DEFAULT_TC
    if df.empty or df["Enrollments"].sum() == 0:
        return create_empty_state_figure("No level data available.", theme)

    level_colors = {
        "Beginner": "#10B981",      # Emerald
        "Intermediate": "#6366F1",  # Electric Indigo
        "Advanced": "#F59E0B",      # Amber
    }
    colors = [level_colors.get(lvl, tc["primary"]) for lvl in df["CourseLevel"]]
    max_enroll = df["Enrollments"].max()

    fig = go.Figure()

    # Backdrop subtle container track
    fig.add_trace(go.Bar(
        x=df["CourseLevel"],
        y=[max_enroll * 1.08] * len(df),
        marker_color="rgba(99, 102, 241, 0.05)",
        marker_cornerradius=10,
        showlegend=False,
        hoverinfo="skip",
        width=0.45,
    ))

    # Main colored bar
    for lvl, enroll, pct, color in zip(df["CourseLevel"], df["Enrollments"], df["Percentage"], colors):
        fig.add_trace(go.Bar(
            x=[lvl],
            y=[enroll],
            marker_color=color,
            marker_cornerradius=8,
            marker_line={"width": 0},
            text=[f"<b>{enroll:,}</b><br><span style='font-size:10px;'>({pct:.1f}%)</span>"],
            textposition="outside",
            textfont={"size": 12, "color": color, "family": FONT_FAMILY},
            width=0.45,
            showlegend=False,
            hovertemplate=f"<b>Difficulty: {lvl}</b><br>Enrollments: <b>{enroll:,}</b><br>Share: <b>{pct:.1f}%</b><extra></extra>",
        ))

    _apply_common_layout(
        fig, "Enrollments by Course Difficulty Level", tc,
        x_title="Course Level", y_title="Total Enrollments", height=390,
    )
    fig.update_layout(barmode="overlay")
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(range=[0, max_enroll * 1.3 if max_enroll > 0 else 100])
    return fig


# ---------------------------------------------------------
# 6. Course Type Distribution (Free vs Paid with Ratio Chip)
# ---------------------------------------------------------
def create_type_distribution_chart(
    df: pd.DataFrame,
    theme: Optional[Dict[str, str]] = None,
) -> go.Figure:
    """Free vs Paid enrollment comparison with dynamic multiplier callout."""
    tc = theme or _DEFAULT_TC
    if df.empty or df["Enrollments"].sum() == 0:
        return create_empty_state_figure("No course type data available.", theme)

    colors = {"Free": "#10B981", "Paid": "#6366F1"}
    bar_colors = [colors.get(t, tc["primary"]) for t in df["CourseType"]]
    max_enroll = df["Enrollments"].max()

    fig = go.Figure()

    # Backdrop track
    fig.add_trace(go.Bar(
        x=df["CourseType"],
        y=[max_enroll * 1.08] * len(df),
        marker_color="rgba(99, 102, 241, 0.05)",
        marker_cornerradius=12,
        showlegend=False,
        hoverinfo="skip",
        width=0.42,
    ))

    # Main bars
    for ctype, enroll, pct, color in zip(df["CourseType"], df["Enrollments"], df["Percentage"], bar_colors):
        fig.add_trace(go.Bar(
            x=[ctype], y=[enroll],
            text=[f"<b>{enroll:,}</b><br><span style='font-size:11px;'>({pct:.1f}%)</span>"],
            textposition="outside",
            textfont={"size": 13, "color": color, "family": FONT_FAMILY},
            marker_color=color,
            marker_cornerradius=8,
            marker_line={"width": 0},
            width=0.42,
            showlegend=False,
            hovertemplate=(
                f"<b>Model: {ctype}</b><br>"
                f"Total Enrollments: <b>{enroll:,}</b><br>"
                f"Enrollment Share: <b>{pct:.1f}%</b><extra></extra>"
            ),
        ))

    # Inset ratio badge chip
    free_row = df[df["CourseType"] == "Free"]
    paid_row = df[df["CourseType"] == "Paid"]
    if not free_row.empty and not paid_row.empty:
        ratio = free_row["Enrollments"].values[0] / max(paid_row["Enrollments"].values[0], 1)
        fig.add_annotation(
            x=0.5, y=max_enroll * 0.55,
            xref="paper",
            text=f"<b style='font-size:14px; color:#10B981;'>{ratio:.1f}×</b><br><span style='font-size:10px; color:{tc['text_secondary']}; font-weight:700;'>Free-to-Paid Ratio</span>",
            showarrow=False,
            font={"family": FONT_FAMILY},
            bgcolor=tc["surface"],
            bordercolor=tc["border"],
            borderwidth=1.5,
            borderpad=8,
            align="center",
        )

    _apply_common_layout(
        fig, "Monetization Model: Free vs Paid Enrollments", tc,
        x_title="Course Access Model", y_title="Total Enrollments", height=390,
    )
    fig.update_layout(barmode="overlay")
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(range=[0, max_enroll * 1.32 if max_enroll > 0 else 100])
    return fig


# ---------------------------------------------------------
# 7. Gender × Category Breakdown (Beautiful Clustered Horizontal Bars)
# ---------------------------------------------------------
def create_gender_category_chart(
    df: pd.DataFrame,
    theme: Optional[Dict[str, str]] = None,
) -> go.Figure:
    """Distinct grouped horizontal bars for female vs male preferences with rounded corners."""
    tc = theme or _DEFAULT_TC
    if df.empty or df["Enrollments"].sum() == 0:
        return create_empty_state_figure("No gender-category preference data available.", theme)

    fig = go.Figure()

    for gender in sorted(df["Gender"].unique()):
        sub_df = df[df["Gender"] == gender].sort_values("CourseCategory")
        color = GENDER_PALETTE.get(gender, tc["primary"])
        
        fig.add_trace(go.Bar(
            y=sub_df["CourseCategory"],
            x=sub_df["Enrollments"],
            name=f"{gender}",
            orientation="h",
            marker={
                "color": color,
                "cornerradius": 4,
                "line": {"width": 0},
            },
            customdata=sub_df["PercentageWithinGender"],
            hovertemplate=(
                f"<b>{gender} • %{{y}}</b><br>"
                f"Enrollments: <b>%{{x:,}}</b><br>"
                f"Share within {gender}: <b>%{{customdata:.1f}}%</b><extra></extra>"
            ),
        ))

    _apply_common_layout(
        fig,
        "Course Category Preferences by Gender",
        tc,
        x_title="Enrollments Volume",
        y_title="",
        height=430,
    )
    fig.update_layout(
        barmode="group",
        bargap=0.22,
        bargroupgap=0.1,
        margin={"l": 25, "r": 25, "t": 60, "b": 40},
    )
    fig.update_yaxes(categoryorder="total ascending")
    return fig


# ---------------------------------------------------------
# 8. Gender × Level Breakdown (Distinct Grouped Vertical Bars)
# ---------------------------------------------------------
def create_gender_level_chart(
    df: pd.DataFrame,
    theme: Optional[Dict[str, str]] = None,
) -> go.Figure:
    """Grouped vertical bars: course level choices by gender with rounded caps."""
    tc = theme or _DEFAULT_TC
    if df.empty or df["Enrollments"].sum() == 0:
        return create_empty_state_figure("No gender-level data available.", theme)

    fig = go.Figure()

    for gender in sorted(df["Gender"].unique()):
        sub_df = df[df["Gender"] == gender]
        color = GENDER_PALETTE.get(gender, tc["primary"])
        
        fig.add_trace(go.Bar(
            x=sub_df["CourseLevel"],
            y=sub_df["Enrollments"],
            name=f"{gender}",
            marker={
                "color": color,
                "cornerradius": 6,
                "line": {"width": 0},
            },
            customdata=sub_df["PercentageWithinGender"],
            text=sub_df["PercentageWithinGender"].apply(lambda v: f"<b>{v:.1f}%</b>"),
            textposition="outside",
            textfont={"size": 11, "color": color, "family": FONT_FAMILY},
            hovertemplate=(
                f"<b>{gender} — %{{x}}</b><br>"
                f"Enrollments: <b>%{{y:,}}</b><br>"
                f"Share within {gender}: <b>%{{customdata:.1f}}%</b><extra></extra>"
            ),
        ))

    _apply_common_layout(
        fig, "Course Difficulty Demand by Gender", tc,
        x_title="Difficulty Level", y_title="Enrollments", height=430,
    )
    fig.update_layout(
        barmode="group",
        bargap=0.28,
        bargroupgap=0.12,
    )
    max_val = df["Enrollments"].max()
    fig.update_yaxes(range=[0, max_val * 1.25 if max_val > 0 else 100])
    return fig


# ---------------------------------------------------------
# 9. Age Group × Category Heatmap (Breathtaking High-Contrast Mosaic)
# ---------------------------------------------------------
def create_age_category_heatmap(
    ct: pd.DataFrame,
    theme: Optional[Dict[str, str]] = None,
) -> go.Figure:
    """Mosaic heatmap of age group × course category enrollments with clear high-contrast palette."""
    tc = theme or _DEFAULT_TC
    if ct.empty or ct.values.sum() == 0:
        return create_empty_state_figure("No cross-tabulation data available.", theme)

    # Gorgeous multi-hue scale: Deep indigo -> Vibrant violet -> Cyan -> Vivid Amber
    is_dark = tc["background"] == "#080D1A"
    
    if is_dark:
        heatmap_scale = [
            [0.0, "#0F172A"],
            [0.25, "#1E3A8A"],
            [0.55, "#4F46E5"],
            [0.8, "#06B6D4"],
            [1.0, "#F59E0B"],
        ]
    else:
        heatmap_scale = [
            [0.0, "#EEF2FF"],
            [0.25, "#C7D2FE"],
            [0.55, "#6366F1"],
            [0.85, "#4338CA"],
            [1.0, "#312E81"],
        ]

    fig = px.imshow(
        ct,
        labels=dict(x="Course Category", y="Age Group", color="Enrollments"),
        x=ct.columns, y=ct.index,
        color_continuous_scale=heatmap_scale,
        aspect="auto",
        text_auto=True,
    )

    fig.update_traces(
        hovertemplate="<b>%{y} Cohort × %{x}</b><br>Total Enrollments: <b>%{z:,}</b><extra></extra>",
        textfont={"family": FONT_FAMILY, "size": 12, "weight": 700},
        xgap=4,
        ygap=4,
    )

    _apply_common_layout(
        fig,
        "Demographic Preference Matrix: Age Band × Course Category Mosaic",
        tc,
        x_title="Course Category",
        y_title="Demographic Age Cohort",
        height=400,
    )
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(tickangle=-25, showgrid=False)
    fig.update_yaxes(showgrid=False)
    return fig


# ---------------------------------------------------------
# 10. Multi-Course Enrollment Concentration
# ---------------------------------------------------------
def create_courses_per_learner_chart(
    df: pd.DataFrame,
    theme: Optional[Dict[str, str]] = None,
) -> go.Figure:
    """Bar chart for learner enrollment concentration buckets with step gradients."""
    tc = theme or _DEFAULT_TC
    if df.empty or df["Learners"].sum() == 0:
        return create_empty_state_figure("No concentration data available.", theme)

    n_bars = len(df)
    # Gradient sequence from Cyan to Indigo to Rose
    palette = ["#06B6D4", "#6366F1", "#8B5CF6", "#EC4899", "#F43F5E"]
    colors = [palette[i % len(palette)] for i in range(n_bars)]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df["CourseCountBucket"],
        y=df["Learners"],
        text=df.apply(lambda r: f"<b>{r['Learners']:,}</b> ({r['Percentage']:.1f}%)", axis=1),
        textposition="outside",
        textfont={"size": 11, "color": tc["text_primary"], "family": FONT_FAMILY},
        marker_color=colors,
        marker_cornerradius=8,
        marker_line={"width": 0},
        width=0.45,
        hovertemplate="<b>%{x} Courses Completed</b><br>Learners: <b>%{y:,}</b><br>Share of Active Base: <b>%{text}</b><extra></extra>",
    ))

    _apply_common_layout(
        fig, "Learner Course Concentration & Repeat Engagement", tc,
        x_title="Courses Completed / Enrolled", y_title="Number of Learners", height=380,
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(range=[0, df["Learners"].max() * 1.22 if not df.empty else 100])
    return fig
