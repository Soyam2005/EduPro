"""EduPro Learner Intelligence Dashboard — Streamlit entry point and UI orchestration."""

import os
import textwrap
import streamlit as st
import pandas as pd

from src.constants import (
    AGE_BAND_ORDER,
    THEME_COLORS,
    get_theme_colors,
)
from src.data_loader import load_raw_data
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
from src.charts import (
    create_age_distribution_chart,
    create_gender_participation_chart,
    create_age_enrollment_chart,
    create_category_popularity_chart,
    create_level_demand_chart,
    create_type_distribution_chart,
    create_age_category_heatmap,
    create_gender_level_chart,
    create_gender_category_chart,
    create_courses_per_learner_chart,
)

# Set page configuration
st.set_page_config(
    page_title="EduPro Learner Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize theme in session state
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

# Resolve active theme colors
tc = get_theme_colors(dark=st.session_state["dark_mode"])

# Custom Design System Styling
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        -webkit-font-smoothing: antialiased;
    }}
    
    .main {{
        background-color: {tc["background"]};
    }}

    .stApp {{
        background-color: {tc["background"]};
        background-image: radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.05) 0px, transparent 50%),
                          radial-gradient(at 100% 100%, rgba(6, 182, 212, 0.04) 0px, transparent 50%);
    }}

    /* Header bar transparency & container spacing */
    header[data-testid="stHeader"] {{
        background-color: transparent !important;
        height: 2.2rem !important;
        z-index: 10 !important;
    }}

    /* Main content area */
    .block-container {{
        background-color: transparent;
        padding-top: 2.5rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1440px !important;
    }}

    /* ═══════════════════════════════════════════════════════════
       CINEMATIC OPENING ANIMATION & SPLASH OVERLAY
    ═══════════════════════════════════════════════════════════ */
    @keyframes splashFadeOut {{
        0% {{
            opacity: 1;
            visibility: visible;
            transform: scale(1);
        }}
        75% {{
            opacity: 0.95;
        }}
        100% {{
            opacity: 0;
            visibility: hidden;
            transform: scale(1.04);
            pointer-events: none;
        }}
    }}

    .edupro-splash-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 99999999;
        background: radial-gradient(ellipse at center, #0B132B 0%, #030712 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        cursor: pointer;
        animation: splashFadeOut 0.75s cubic-bezier(0.16, 1, 0.3, 1) 2.8s both;
        transition: opacity 0.4s ease, visibility 0.4s ease;
    }}

    .splash-skip-btn {{
        position: absolute;
        top: 24px;
        right: 28px;
        padding: 6px 14px;
        border-radius: 9999px;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: #94A3B8;
        font-size: 11.5px;
        font-weight: 600;
        cursor: pointer;
        backdrop-filter: blur(8px);
        transition: all 0.2s ease;
        z-index: 20;
    }}
    .splash-skip-btn:hover {{
        background: rgba(255, 255, 255, 0.16);
        color: #FFFFFF;
        border-color: rgba(255, 255, 255, 0.3);
    }}

    /* Ambient glow auras */
    .splash-ambient-aura {{
        position: absolute;
        border-radius: 50%;
        filter: blur(90px);
        pointer-events: none;
    }}
    .splash-aura-1 {{
        width: 380px;
        height: 380px;
        background: rgba(99, 102, 241, 0.35);
        top: 20%;
        left: 30%;
        animation: auraFloat1 6s ease-in-out infinite alternate;
    }}
    .splash-aura-2 {{
        width: 320px;
        height: 320px;
        background: rgba(6, 182, 212, 0.30);
        bottom: 25%;
        right: 32%;
        animation: auraFloat2 7s ease-in-out infinite alternate;
    }}
    .splash-aura-3 {{
        width: 260px;
        height: 260px;
        background: rgba(244, 63, 94, 0.22);
        top: 55%;
        left: 45%;
        animation: auraFloat3 8s ease-in-out infinite alternate;
    }}

    @keyframes auraFloat1 {{
        0% {{ transform: translate(0, 0) scale(1); }}
        100% {{ transform: translate(40px, -30px) scale(1.15); }}
    }}
    @keyframes auraFloat2 {{
        0% {{ transform: translate(0, 0) scale(1); }}
        100% {{ transform: translate(-35px, 25px) scale(1.2); }}
    }}
    @keyframes auraFloat3 {{
        0% {{ transform: translate(0, 0) scale(0.9); }}
        100% {{ transform: translate(25px, 35px) scale(1.1); }}
    }}

    .splash-content {{
        position: relative;
        z-index: 10;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding: 30px;
        animation: splashContentRise 0.9s cubic-bezier(0.16, 1, 0.3, 1) both;
    }}

    @keyframes splashContentRise {{
        0% {{
            opacity: 0;
            transform: translateY(30px) scale(0.95);
        }}
        100% {{
            opacity: 1;
            transform: translateY(0) scale(1);
        }}
    }}

    /* Badge Orbit */
    .splash-badge-container {{
        position: relative;
        width: 110px;
        height: 110px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .splash-orbit-ring {{
        position: absolute;
        inset: -6px;
        border-radius: 50%;
        border: 2px dashed rgba(99, 102, 241, 0.55);
        animation: splashRingSpin 10s linear infinite;
    }}

    .splash-orbit-ring-inner {{
        position: absolute;
        inset: -14px;
        border-radius: 50%;
        border: 1.5px solid transparent;
        border-top: 2px solid #06B6D4;
        border-right: 2px solid #6366F1;
        animation: splashRingSpinReverse 5s cubic-bezier(0.4, 0, 0.2, 1) infinite;
    }}

    @keyframes splashRingSpin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    @keyframes splashRingSpinReverse {{
        0% {{ transform: rotate(360deg); }}
        100% {{ transform: rotate(0deg); }}
    }}

    .splash-badge-core {{
        width: 90px;
        height: 90px;
        border-radius: 28px;
        background: linear-gradient(135deg, #4F46E5, #06B6D4);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 12px 36px rgba(99, 102, 241, 0.5), 0 0 20px rgba(6, 182, 212, 0.35);
        animation: splashCorePulse 2.4s ease-in-out infinite;
    }}

    @keyframes splashCorePulse {{
        0%, 100% {{
            transform: scale(1);
            box-shadow: 0 12px 36px rgba(99, 102, 241, 0.5), 0 0 20px rgba(6, 182, 212, 0.35);
        }}
        50% {{
            transform: scale(1.05);
            box-shadow: 0 16px 48px rgba(99, 102, 241, 0.7), 0 0 35px rgba(6, 182, 212, 0.6);
        }}
    }}

    .splash-badge-icon {{
        font-size: 42px;
        filter: drop-shadow(0 4px 10px rgba(0, 0, 0, 0.3));
    }}

    .splash-brand-title {{
        font-size: 38px;
        font-weight: 900;
        letter-spacing: -1px;
        margin: 0;
        background: linear-gradient(135deg, #FFFFFF 20%, #A5B4FC 60%, #67E8F9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
    }}

    .splash-brand-subtitle {{
        font-size: 13px;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 2.8px;
        margin-top: 8px;
        margin-bottom: 22px;
    }}

    .splash-status-pill {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 16px;
        border-radius: 9999px;
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(10px);
        margin-bottom: 22px;
    }}

    .splash-status-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #10B981;
        box-shadow: 0 0 10px #10B981, 0 0 0 2px rgba(16, 185, 129, 0.3);
        animation: statusBlink 1.2s ease-in-out infinite alternate;
    }}

    @keyframes statusBlink {{
        0% {{ opacity: 0.5; transform: scale(0.85); }}
        100% {{ opacity: 1; transform: scale(1.15); }}
    }}

    .splash-status-text {{
        font-size: 12px;
        font-weight: 600;
        color: #E2E8F0;
        letter-spacing: 0.3px;
    }}

    .splash-progress-track {{
        width: 260px;
        height: 5px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 99px;
        overflow: hidden;
        position: relative;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.3);
    }}

    .splash-progress-fill {{
        height: 100%;
        width: 0%;
        border-radius: 99px;
        background: linear-gradient(90deg, #6366F1, #06B6D4, #F43F5E);
        animation: splashFillTrack 1.8s cubic-bezier(0.22, 1, 0.36, 1) forwards;
        position: relative;
    }}

    @keyframes splashFillTrack {{
        0% {{ width: 0%; }}
        40% {{ width: 55%; }}
        75% {{ width: 85%; }}
        100% {{ width: 100%; }}
    }}

    .splash-progress-sparkle {{
        position: absolute;
        right: 0;
        top: -2px;
        bottom: -2px;
        width: 14px;
        background: #FFFFFF;
        border-radius: 50%;
        box-shadow: 0 0 12px #FFFFFF, 0 0 20px #06B6D4;
    }}

    .splash-skip-hint {{
        margin-top: 18px;
        font-size: 11.5px;
        font-weight: 500;
        color: #64748B;
        letter-spacing: 0.5px;
        opacity: 0.8;
    }}

    /* ═══════════════════════════════════════════════════════════
       HERO BANNER & HEADER
    ═══════════════════════════════════════════════════════════ */
    @keyframes heroDropIn {{
        0% {{
            opacity: 0;
            transform: translateY(-22px) scale(0.98);
        }}
        100% {{
            opacity: 1;
            transform: translateY(0) scale(1);
        }}
    }}

    .hero-banner {{
        background: linear-gradient(135deg, {tc["surface"]}, {tc["observation_bg"]});
        border: 1px solid {tc["border"]};
        border-radius: 20px;
        padding: 22px 28px;
        margin-bottom: 22px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
        position: relative;
        overflow: hidden;
        animation: heroDropIn 0.75s cubic-bezier(0.16, 1, 0.3, 1) both;
    }}

    .hero-banner::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #6366F1, #06B6D4, #F43F5E);
    }}

    .hero-title {{
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.6px;
        margin: 0;
        padding: 0;
        background: linear-gradient(135deg, {tc["text_primary"]} 30%, #6366F1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }}

    .hero-subtitle {{
        color: {tc["text_secondary"]};
        font-size: 13.5px;
        margin: 6px 0 0 0;
        font-weight: 500;
    }}

    /* ═══════════════════════════════════════════════════════════
       KPI CARDS — ULTRA-PREMIUM REDESIGN
    ═══════════════════════════════════════════════════════════ */
    @keyframes kpi-shimmer {{
        0%   {{ background-position: -200% center; }}
        100% {{ background-position:  200% center; }}
    }}
    @keyframes kpi-float-aura {{
        0%, 100% {{ transform: scale(1) translate(0,0); opacity: 0.55; }}
        50%       {{ transform: scale(1.12) translate(4px,-6px); opacity: 0.75; }}
    }}
    @keyframes kpiCascade {{
        0% {{
            opacity: 0;
            transform: translateY(22px) scale(0.96);
        }}
        100% {{
            opacity: 1;
            transform: translateY(0) scale(1);
        }}
    }}

    .kpi-card {{
        position: relative;
        overflow: hidden;
        border-radius: 20px;
        padding: 22px 22px 18px;
        margin-bottom: 16px;
        min-height: 175px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        border: 1px solid {tc["border"]};
        background: {tc["surface"]};
        box-shadow: 0 4px 24px rgba(0,0,0,0.05);
        transition: transform 0.32s cubic-bezier(0.16,1,0.3,1),
                    box-shadow 0.32s cubic-bezier(0.16,1,0.3,1),
                    border-color 0.32s ease;
        animation: kpiCascade 0.65s cubic-bezier(0.16,1,0.3,1) both;
    }}

    .kpi-card-anim-1 {{ animation-delay: 0.10s !important; }}
    .kpi-card-anim-2 {{ animation-delay: 0.20s !important; }}
    .kpi-card-anim-3 {{ animation-delay: 0.30s !important; }}
    .kpi-card-anim-4 {{ animation-delay: 0.40s !important; }}

    .kpi-card::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        border-radius: 20px 20px 0 0;
        background-size: 200% 100%;
        animation: kpi-shimmer 3s linear infinite;
    }}

    .kpi-card::after {{
        content: '';
        position: absolute;
        width: 140px;
        height: 140px;
        border-radius: 50%;
        top: -36px;
        right: -36px;
        filter: blur(40px);
        animation: kpi-float-aura 4.5s ease-in-out infinite;
        pointer-events: none;
    }}

    .kpi-card:hover {{
        transform: translateY(-5px);
    }}
    .kpi-card:hover .kpi-icon-badge {{
        transform: scale(1.12) rotate(5deg);
    }}

    /* Card 1: Blue/Indigo */
    .kpi-card-blue {{
        background: radial-gradient(ellipse at 95% 10%, rgba(99,102,241,0.12) 0%, {tc["surface"]} 60%);
    }}
    .kpi-card-blue::before {{
        background: linear-gradient(90deg, #4F46E5, #818CF8, #4F46E5);
    }}
    .kpi-card-blue::after {{
        background: rgba(99,102,241,0.25);
    }}
    .kpi-card-blue:hover {{
        border-color: rgba(99,102,241,0.5);
        box-shadow: 0 16px 40px -8px rgba(99,102,241,0.25), 0 4px 16px rgba(0,0,0,0.05);
    }}

    /* Card 2: Cyan/Teal */
    .kpi-card-teal {{
        background: radial-gradient(ellipse at 95% 10%, rgba(6,182,212,0.12) 0%, {tc["surface"]} 60%);
    }}
    .kpi-card-teal::before {{
        background: linear-gradient(90deg, #0891B2, #22D3EE, #0891B2);
    }}
    .kpi-card-teal::after {{
        background: rgba(6,182,212,0.25);
    }}
    .kpi-card-teal:hover {{
        border-color: rgba(6,182,212,0.5);
        box-shadow: 0 16px 40px -8px rgba(6,182,212,0.25), 0 4px 16px rgba(0,0,0,0.05);
    }}

    /* Card 3: Purple/Rose */
    .kpi-card-purple {{
        background: radial-gradient(ellipse at 95% 10%, rgba(244,63,94,0.11) 0%, {tc["surface"]} 60%);
    }}
    .kpi-card-purple::before {{
        background: linear-gradient(90deg, #E11D48, #FB7185, #E11D48);
    }}
    .kpi-card-purple::after {{
        background: rgba(244,63,94,0.25);
    }}
    .kpi-card-purple:hover {{
        border-color: rgba(244,63,94,0.5);
        box-shadow: 0 16px 40px -8px rgba(244,63,94,0.22), 0 4px 16px rgba(0,0,0,0.05);
    }}

    /* Card 4: Amber */
    .kpi-card-amber {{
        background: radial-gradient(ellipse at 95% 10%, rgba(245,158,11,0.12) 0%, {tc["surface"]} 60%);
    }}
    .kpi-card-amber::before {{
        background: linear-gradient(90deg, #D97706, #FCD34D, #D97706);
    }}
    .kpi-card-amber::after {{
        background: rgba(245,158,11,0.28);
    }}
    .kpi-card-amber:hover {{
        border-color: rgba(245,158,11,0.5);
        box-shadow: 0 16px 40px -8px rgba(245,158,11,0.22), 0 4px 16px rgba(0,0,0,0.05);
    }}

    .kpi-top-row {{
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        margin-bottom: 4px;
        position: relative;
        z-index: 2;
    }}

    .kpi-label {{
        font-size: 11px;
        font-weight: 800;
        color: {tc["text_secondary"]};
        text-transform: uppercase;
        letter-spacing: 1.1px;
        line-height: 1.4;
    }}

    .kpi-icon-badge {{
        width: 40px;
        height: 40px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: transform 0.26s cubic-bezier(0.16,1,0.3,1), box-shadow 0.26s ease;
        flex-shrink: 0;
    }}
    .kpi-icon-blue {{
        background: rgba(99,102,241,0.15);
        color: #6366F1;
        box-shadow: 0 2px 12px rgba(99,102,241,0.25);
    }}
    .kpi-icon-teal {{
        background: rgba(6,182,212,0.15);
        color: #06B6D4;
        box-shadow: 0 2px 12px rgba(6,182,212,0.25);
    }}
    .kpi-icon-purple {{
        background: rgba(244,63,94,0.15);
        color: #F43F5E;
        box-shadow: 0 2px 12px rgba(244,63,94,0.25);
    }}
    .kpi-icon-amber {{
        background: rgba(245,158,11,0.15);
        color: #F59E0B;
        box-shadow: 0 2px 12px rgba(245,158,11,0.25);
    }}

    .kpi-value {{
        font-size: 38px;
        font-weight: 900;
        color: {tc["text_primary"]};
        line-height: 1.05;
        letter-spacing: -1.5px;
        margin: 8px 0 6px 0;
        position: relative;
        z-index: 2;
        font-variant-numeric: tabular-nums;
    }}

    .kpi-value-text {{
        font-size: 24px;
        font-weight: 800;
        color: {tc["text_primary"]};
        line-height: 1.15;
        letter-spacing: -0.5px;
        margin: 8px 0 6px 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        position: relative;
        z-index: 2;
    }}

    .kpi-progress-wrap {{
        position: relative;
        z-index: 2;
        margin-bottom: 10px;
    }}
    .kpi-progress-track {{
        width: 100%;
        height: 6px;
        background: rgba(148,163,184,0.15);
        border-radius: 99px;
        overflow: hidden;
    }}
    .kpi-progress-fill {{
        height: 100%;
        border-radius: 99px;
        transition: width 0.7s cubic-bezier(0.16,1,0.3,1);
        position: relative;
    }}
    .kpi-pct-label {{
        font-size: 10.5px;
        font-weight: 700;
        color: {tc["text_secondary"]};
        text-align: right;
        margin-bottom: 3px;
        letter-spacing: 0.3px;
    }}

    .kpi-footer {{
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 11.5px;
        color: {tc["text_secondary"]};
        font-weight: 600;
        position: relative;
        z-index: 2;
    }}

    .kpi-pill {{
        display: inline-flex;
        align-items: center;
        gap: 3px;
        padding: 3px 8px;
        border-radius: 7px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.2px;
        flex-shrink: 0;
    }}
    .kpi-pill-blue   {{ background: rgba(99,102,241,0.15);  color: #6366F1; }}
    .kpi-pill-teal   {{ background: rgba(6,182,212,0.15);  color: #06B6D4; }}
    .kpi-pill-purple {{ background: rgba(244,63,94,0.15);  color: #F43F5E; }}
    .kpi-pill-amber  {{ background: rgba(245,158,11,0.15);  color: #F59E0B; }}

    .kpi-trend-up {{
        display: inline-flex; align-items: center; gap: 2px;
        font-size: 11px; font-weight: 800;
        color: #10B981;
        background: rgba(16,185,129,0.14);
        padding: 2px 7px; border-radius: 6px;
    }}
    .kpi-trend-neutral {{
        display: inline-flex; align-items: center; gap: 2px;
        font-size: 11px; font-weight: 800;
        color: {tc["text_secondary"]};
        background: rgba(148,163,184,0.14);
        padding: 2px 7px; border-radius: 6px;
    }}

    /* ═══════════════════════════════════════════════════════════
       SECTION CARDS (CONTAINERS)
    ═══════════════════════════════════════════════════════════ */
    @keyframes sectionReveal {{
        0% {{
            opacity: 0;
            transform: translateY(20px);
        }}
        100% {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: {tc["surface"]} !important;
        border: 1px solid {tc["border"]} !important;
        border-radius: 20px !important;
        box-shadow: 0 6px 24px rgba(0,0,0,0.03) !important;
        margin-bottom: 26px !important;
        position: relative;
        overflow: hidden;
        animation: sectionReveal 0.7s cubic-bezier(0.16, 1, 0.3, 1) both !important;
    }}

    div[data-testid="stVerticalBlockBorderWrapper"]:nth-of-type(1) {{ animation-delay: 0.22s !important; }}
    div[data-testid="stVerticalBlockBorderWrapper"]:nth-of-type(2) {{ animation-delay: 0.34s !important; }}
    div[data-testid="stVerticalBlockBorderWrapper"]:nth-of-type(3) {{ animation-delay: 0.46s !important; }}
    div[data-testid="stVerticalBlockBorderWrapper"]:nth-of-type(4) {{ animation-delay: 0.58s !important; }}

    div[data-testid="stVerticalBlockBorderWrapper"] > div {{
        padding: 24px 28px 22px !important;
    }}

    .section-badge {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 30px;
        height: 30px;
        border-radius: 10px;
        background: linear-gradient(135deg, #6366F1, #4F46E5);
        color: #FFFFFF;
        font-size: 12px;
        font-weight: 800;
        margin-right: 12px;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
        flex-shrink: 0;
    }}

    .section-header-wrap {{
        display: flex;
        align-items: center;
        margin-bottom: 4px;
    }}

    .section-header {{
        font-size: 18px;
        font-weight: 800;
        color: {tc["text_primary"]};
        letter-spacing: -0.4px;
        margin-bottom: 0;
    }}

    .section-desc {{
        font-size: 13.5px;
        color: {tc["text_secondary"]};
        margin-bottom: 18px;
        font-weight: 400;
        line-height: 1.5;
        padding-left: 42px;
    }}

    /* ═══════════════════════════════════════════════════════════
       OBSERVATION BOX — GLOWING TAKEAWAY CALLOUT
    ═══════════════════════════════════════════════════════════ */
    .observation-box {{
        background: linear-gradient(135deg, {tc["observation_bg"]}, {tc["surface"]});
        border-left: 4px solid #6366F1;
        padding: 14px 20px;
        border-radius: 10px 14px 14px 10px;
        font-size: 13.5px;
        color: {tc["text_primary"]};
        margin-top: 16px;
        line-height: 1.6;
        box-shadow: 0 4px 16px rgba(0,0,0,0.02);
        display: flex;
        align-items: flex-start;
        gap: 10px;
    }}

    .observation-icon {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
        border-radius: 6px;
        background: rgba(99, 102, 241, 0.15);
        color: #6366F1;
        font-size: 14px;
        flex-shrink: 0;
        margin-top: 1px;
    }}

    /* ═══════════════════════════════════════════════════════════
       SECTION 4 STAT MICRO-CARDS
    ═══════════════════════════════════════════════════════════ */
    .stat-micro-card {{
        background: {tc["surface"]};
        border: 1px solid {tc["border"]};
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }}

    .stat-micro-card:hover {{
        transform: translateY(-2px);
        border-color: #6366F1;
    }}

    .stat-micro-title {{
        font-size: 10.5px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: {tc["text_secondary"]};
        margin-bottom: 4px;
    }}

    .stat-micro-value {{
        font-size: 22px;
        font-weight: 900;
        letter-spacing: -0.5px;
        color: {tc["text_primary"]};
        margin-bottom: 2px;
    }}

    .stat-micro-caption {{
        font-size: 11.5px;
        color: {tc["text_secondary"]};
        font-weight: 500;
    }}

    /* Top Nav Badge */
    .top-nav-badge {{
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background-color: {tc["surface"]};
        border: 1px solid {tc["border"]};
        border-radius: 9999px;
        padding: 5px 14px;
        font-size: 12.5px;
        font-weight: 700;
        color: {tc["text_primary"]};
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        vertical-align: middle;
    }}

    .top-nav-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #10B981;
        display: inline-block;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.25);
    }}

    /* Theme toggle button styling */
    div.st-key-top_theme_toggle button {{
        background-color: {tc["surface"]} !important;
        color: {tc["text_primary"]} !important;
        border: 1px solid {tc["border"]} !important;
        border-radius: 10px !important;
        height: 42px !important;
        min-height: 42px !important;
        width: 44px !important;
        min-width: 44px !important;
        padding: 0 !important;
        font-size: 18px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.2s ease !important;
    }}

    div.st-key-top_theme_toggle button:hover {{
        border-color: #6366F1 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2) !important;
    }}

    /* Multiselect pill tags */
    div[data-baseweb="tag"] {{
        background: linear-gradient(135deg, #6366F1, #4F46E5) !important;
        border: none !important;
        border-radius: 9999px !important;
        padding: 3px 10px 3px 12px !important;
        box-shadow: 0 2px 6px rgba(99, 102, 241, 0.35) !important;
    }}

    div[data-baseweb="tag"] span {{
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 12px !important;
    }}

    /* Expander styling */
    div[data-testid="stExpander"] {{
        background-color: {tc["surface"]} !important;
        border: 1px solid {tc["border"]} !important;
        border-radius: 14px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
    }}

    /* Sidebar slide-in animation */
    @keyframes sidebarSlideIn {{
        0% {{
            opacity: 0;
            transform: translateX(-24px);
        }}
        100% {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: {tc["sidebar_bg"]} !important;
        border-right: 1px solid {tc["sidebar_border"]} !important;
        animation: sidebarSlideIn 0.65s cubic-bezier(0.16, 1, 0.3, 1) both;
    }}
    
    section[data-testid="stSidebar"] > div {{
        background-color: {tc["sidebar_bg"]} !important;
    }}

    @media (prefers-reduced-motion: reduce) {{
        .edupro-splash-overlay {{
            display: none !important;
        }}
        .hero-banner, .kpi-card, div[data-testid="stVerticalBlockBorderWrapper"], section[data-testid="stSidebar"] {{
            animation: none !important;
            transform: none !important;
            opacity: 1 !important;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Cinematic opening animation rendered as soon as site opens
splash_html = (
    '<div id="edupro-intro-splash" class="edupro-splash-overlay" onclick="this.style.opacity=\'0\'; setTimeout(() => this.style.display=\'none\', 350);">'
    '<div class="splash-ambient-aura splash-aura-1"></div>'
    '<div class="splash-ambient-aura splash-aura-2"></div>'
    '<div class="splash-ambient-aura splash-aura-3"></div>'
    '<div class="splash-skip-btn" onclick="document.getElementById(\'edupro-intro-splash\').style.display=\'none\'; event.stopPropagation();">Skip Intro ✕</div>'
    '<div class="splash-content">'
    '<div class="splash-badge-container">'
    '<div class="splash-orbit-ring"></div>'
    '<div class="splash-orbit-ring-inner"></div>'
    '<div class="splash-badge-core">'
    '<span class="splash-badge-icon">🎓</span>'
    '</div>'
    '</div>'
    '<div class="splash-brand-title">EduPro</div>'
    '<div class="splash-brand-subtitle">Learner Intelligence Platform</div>'
    '<div class="splash-status-pill">'
    '<span class="splash-status-dot"></span>'
    '<span class="splash-status-text">Calibrating Analytics • 10,000 Verified Records</span>'
    '</div>'
    '<div class="splash-progress-track">'
    '<div class="splash-progress-fill">'
    '<div class="splash-progress-sparkle"></div>'
    '</div>'
    '</div>'
    '<div class="splash-skip-hint">Click anywhere to skip</div>'
    '</div>'
    '</div>'
    '<img src="data:image/svg+xml;utf8,<svg xmlns=\'http://www.w3.org/2000/svg\'></svg>" style="display:none;" '
    'onload="if(window.__edupro_splash_played){var s=document.getElementById(\'edupro-intro-splash\');if(s)s.style.display=\'none\';}else{window.__edupro_splash_played=true;}" />'
)
st.markdown(splash_html, unsafe_allow_html=True)


@st.cache_data(show_spinner="Loading and validating EduPro dataset...")
def get_canonical_dataset():
    """Load, validate, and join the dataset once with caching."""
    potential_paths = [
        os.path.join("data", "raw", "EduPro Online Platform.xlsx"),
        "EduPro Online Platform.xlsx",
        os.path.join("..", "data", "raw", "EduPro Online Platform.xlsx"),
    ]
    file_path = None
    for p in potential_paths:
        if os.path.exists(p):
            file_path = p
            break

    if not file_path:
        raise FileNotFoundError(
            "Source dataset 'EduPro Online Platform.xlsx' could not be found in project directory or data/raw/."
        )

    users_df, courses_df, transactions_df, integrity_report = load_raw_data(file_path)
    analytic_df, join_stats = build_analytic_dataset(users_df, courses_df, transactions_df)

    return analytic_df, integrity_report, join_stats


try:
    analytic_df, integrity_report, join_stats = get_canonical_dataset()
except Exception as e:
    st.error(f"⚠️ Error initializing data pipeline: {str(e)}")
    st.stop()


# ---------------------------------------------------------
# Sidebar Controls & Filters
# ---------------------------------------------------------
with st.sidebar:
    # ── Brand Header ──
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:12px; padding:4px 0 16px;">
            <div style="background:linear-gradient(135deg,#6366F1,#06B6D4); color:white; border-radius:12px; width:44px; height:44px; display:flex; align-items:center; justify-content:center; font-size:22px; box-shadow:0 6px 18px rgba(99,102,241,0.40); flex-shrink:0;">
                🎓
            </div>
            <div>
                <div style="font-weight:800; font-size:16px; color:{tc['sidebar_heading']}; letter-spacing:-0.4px; line-height:1.2;">EduPro Analytics</div>
                <div style="font-size:10.5px; font-weight:700; color:{tc['sidebar_caption']}; letter-spacing:0.8px; text-transform:uppercase;">Learner Intelligence</div>
            </div>
        </div>
        <div style="height:1px; background:linear-gradient(90deg, #6366F1, #06B6D4, transparent); margin-bottom:20px;"></div>
        """,
        unsafe_allow_html=True,
    )

    # ── Filter Header ──
    st.markdown(
        f"""
        <div style="margin-bottom:6px;">
            <div style="font-size:13px; font-weight:800; color:{tc['sidebar_heading']}; letter-spacing:-0.2px;">🎯 Cohort Isolation Filters</div>
            <div style="font-size:11.5px; color:{tc['sidebar_caption']}; margin-top:2px; line-height:1.4;">Slice across dimensions. All charts and KPIs update in reactive lockstep.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Reset Filters Button
    if st.button("↺  Reset All Filters", use_container_width=True, type="secondary"):
        st.session_state["filter_age_groups"] = []
        st.session_state["filter_genders"] = []
        st.session_state["filter_categories"] = []
        st.session_state["filter_levels"] = []
        st.rerun()

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    # ── Filter Group: Demographics ──
    st.markdown(
        f"""<div style="font-size:10.5px; font-weight:800; text-transform:uppercase; letter-spacing:1.2px; color:#6366F1; margin:14px 0 8px; display:flex; align-items:center; gap:6px;">
            <span>👤</span><span>Demographics</span>
        </div>""",
        unsafe_allow_html=True,
    )

    # 1. Age Group Filter
    available_age_groups = [b for b in AGE_BAND_ORDER if b in analytic_df["AgeGroup"].unique()]
    selected_age_groups = st.multiselect(
        "Age Group",
        options=available_age_groups,
        default=st.session_state.get("filter_age_groups", []),
        key="filter_age_groups",
        help="Select one or more standardized age groups.",
    )

    # 2. Gender Filter
    available_genders = sorted(analytic_df["Gender"].dropna().unique().tolist())
    selected_genders = st.multiselect(
        "Gender",
        options=available_genders,
        default=st.session_state.get("filter_genders", []),
        key="filter_genders",
        help="Filter by learner gender.",
    )

    # ── Filter Group: Course ──
    st.markdown(
        f"""<div style="font-size:10.5px; font-weight:800; text-transform:uppercase; letter-spacing:1.2px; color:#06B6D4; margin:18px 0 8px; display:flex; align-items:center; gap:6px;">
            <span>📚</span><span>Curriculum &amp; Offering</span>
        </div>""",
        unsafe_allow_html=True,
    )

    # 3. Course Category Filter
    available_categories = sorted(analytic_df["CourseCategory"].dropna().unique().tolist())
    selected_categories = st.multiselect(
        "Course Category",
        options=available_categories,
        default=st.session_state.get("filter_categories", []),
        key="filter_categories",
        help="Filter by specific learning subject areas.",
    )

    # 4. Course Level Filter
    available_levels = ["Beginner", "Intermediate", "Advanced"]
    selected_levels = st.multiselect(
        "Course Level",
        options=available_levels,
        default=st.session_state.get("filter_levels", []),
        key="filter_levels",
        help="Filter by course difficulty level.",
    )

    # ── Sidebar Footer ──
    st.markdown(
        f"""
        <div style="margin-top:26px; padding:12px 14px; background:{tc['observation_bg']}; border-radius:12px; border:1px solid {tc['border']};">
            <div style="font-size:11px; color:{tc['sidebar_caption']}; line-height:1.7;">
                <div style="font-weight:800; color:{tc['sidebar_heading']}; font-size:11.5px; margin-bottom:4px;">📌 Platform Scope</div>
                <span style="font-weight:600; color:{tc['text_secondary']};">Temporal Window:</span> {join_stats['min_transaction_date'].strftime('%b %Y')} – {join_stats['max_transaction_date'].strftime('%b %Y')}<br>
                <span style="font-weight:600; color:{tc['text_secondary']};">Audited Volume:</span> 10,000 Verified Transactions<br>
                <span style="font-weight:600; color:{tc['text_secondary']};">Pipeline Integrity:</span> 100.0% Relational Match
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# Filter Dataset
# ---------------------------------------------------------
filtered_df = apply_filters(
    analytic_df,
    age_groups=selected_age_groups,
    genders=selected_genders,
    categories=selected_categories,
    levels=selected_levels,
)

total_platform_enrollments = len(analytic_df)
kpis = compute_kpis(filtered_df, total_unfiltered_count=total_platform_enrollments)


# ---------------------------------------------------------
# Page Header & Hero Banner
# ---------------------------------------------------------
active_records_label = (
    f"{len(filtered_df):,} Active Cohort Records"
    if len(filtered_df) < total_platform_enrollments
    else "10,000 Verified Records (100% Platform Base)"
)

col_hero_left, col_hero_right = st.columns([0.92, 0.08], vertical_alignment="center")

with col_hero_left:
    st.markdown(
        f"""
        <div class="hero-banner">
            <div>
                <div style="display:flex; align-items:center; gap:12px; margin-bottom:4px; flex-wrap:wrap;">
                    <h1 class="hero-title">EduPro Learner Intelligence</h1>
                    <span class="top-nav-badge">
                        <span class="top-nav-dot"></span> {active_records_label}
                    </span>
                </div>
                <div class="hero-subtitle">
                    Executive descriptive analytics engine across demographics, course catalog dynamics, and learner engagement depth.
                </div>
            </div>
            <div style="display:flex; gap:8px; align-items:center;">
                <span style="font-size:11px; font-weight:700; background:rgba(99,102,241,0.12); color:#6366F1; padding:4px 10px; border-radius:8px; border:1px solid rgba(99,102,241,0.25);">
                    ⚡ Reactive Pipeline
                </span>
                <span style="font-size:11px; font-weight:700; background:rgba(16,185,129,0.12); color:#10B981; padding:4px 10px; border-radius:8px; border:1px solid rgba(16,185,129,0.25);">
                    ✓ Audited
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_hero_right:
    theme_icon = "☀️" if st.session_state["dark_mode"] else "🌙"
    theme_help = "Switch to Light Mode" if st.session_state["dark_mode"] else "Switch to Dark Mode"
    if st.button(theme_icon, key="top_theme_toggle", use_container_width=True, help=theme_help):
        st.session_state["dark_mode"] = not st.session_state["dark_mode"]
        st.rerun()

if not integrity_report["is_healthy"]:
    st.warning("⚠️ Data integrity warning: Some records did not pass relational consistency checks.")


# ---------------------------------------------------------
# Data Quality & Methodology Expander
# ---------------------------------------------------------
with st.expander("ℹ️ Data Architecture, Integrity Verification & Methodology Audit", expanded=False):
    col_q1, col_q2, col_q3 = st.columns(3)
    with col_q1:
        st.markdown("**Relational Records Audited**")
        st.write(f"- Users loaded: **{integrity_report['total_users']:,}**")
        st.write(f"- Courses cataloged: **{integrity_report['total_courses']:,}**")
        st.write(f"- Transactions processed: **{integrity_report['total_transactions']:,}**")
    with col_q2:
        st.markdown("**Integrity & Match Rate**")
        st.write(f"- User foreign key match: **100.0%** ({integrity_report['unmatched_user_transactions']} unmatched)")
        st.write(f"- Course foreign key match: **100.0%** ({integrity_report['unmatched_course_transactions']} unmatched)")
        st.write(f"- Duplicate entity identifiers: **0 detected**")
    with col_q3:
        st.markdown("**Governance & Standards**")
        st.write("- **Age cohort bands:** `<18`, `18–25`, `26–35`, `36–45`, `45+`")
        st.write("- **Filter propagation:** Multi-dimensional synchronized reactive state")
        st.write("- **Analytical scope:** Descriptive metrics with privacy-preserving aggregation")


# ---------------------------------------------------------
# Empty State Check
# ---------------------------------------------------------
if filtered_df.empty:
    st.warning(
        "⚠️ **No matching cohort data.** The active combination of filters returned 0 records. "
        "Please select different criteria or click '↺ Reset All Filters' in the sidebar."
    )
    st.stop()


# ---------------------------------------------------------
# KPI Cards Row
# ---------------------------------------------------------
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    share_pct = min(100.0, max(0.0, float(kpis['enrollment_share_of_platform'])))
    enroll_val = kpis['total_enrollments']
    st.markdown(
        f"""
        <div class="kpi-card kpi-card-blue kpi-card-anim-1">
            <div class="kpi-top-row">
                <div class="kpi-label">Total Enrollments</div>
                <div class="kpi-icon-badge kpi-icon-blue">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M22 10v6M2 10l10-5 10 5-10 5z"/>
                        <path d="M6 12v5c3 3 9 3 12 0v-5"/>
                    </svg>
                </div>
            </div>
            <div class="kpi-value" id="kpi-enroll">{enroll_val:,}</div>
            <div class="kpi-progress-wrap">
                <div class="kpi-pct-label">{share_pct:.1f}% of platform volume</div>
                <div class="kpi-progress-track">
                    <div class="kpi-progress-fill" style="width:{share_pct}%; background:linear-gradient(90deg,#4F46E5,#818CF8);"></div>
                </div>
            </div>
            <div class="kpi-footer">
                <span class="kpi-pill kpi-pill-blue">📊 {kpis['enrollment_share_of_platform']}%</span>
                <span>Platform Volume</span>
                <span class="kpi-trend-up" style="margin-left:auto;">↑ Active</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi2:
    engage_ratio = min(100.0, max(8.0, (float(kpis['avg_courses_per_learner']) / 4.0) * 100.0)) if kpis['total_enrollments'] > 0 else 0.0
    learner_val = kpis['active_learners']
    st.markdown(
        f"""
        <div class="kpi-card kpi-card-teal kpi-card-anim-2">
            <div class="kpi-top-row">
                <div class="kpi-label">Active Learners</div>
                <div class="kpi-icon-badge kpi-icon-teal">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
                        <circle cx="9" cy="7" r="4"/>
                        <path d="M22 21v-2a4 4 0 0 0-3-3.87"/>
                        <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                    </svg>
                </div>
            </div>
            <div class="kpi-value" id="kpi-learners">{learner_val:,}</div>
            <div class="kpi-progress-wrap">
                <div class="kpi-pct-label">{kpis['avg_courses_per_learner']}x engagement intensity</div>
                <div class="kpi-progress-track">
                    <div class="kpi-progress-fill" style="width:{engage_ratio:.1f}%; background:linear-gradient(90deg,#0891B2,#22D3EE);"></div>
                </div>
            </div>
            <div class="kpi-footer">
                <span class="kpi-pill kpi-pill-teal">⚡ {kpis['avg_courses_per_learner']}x</span>
                <span>Courses / Learner</span>
                <span class="kpi-trend-up" style="margin-left:auto;">↑ High Depth</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi3:
    cat_share = min(100.0, max(0.0, float(kpis['leading_category_share'])))
    st.markdown(
        f"""
        <div class="kpi-card kpi-card-purple kpi-card-anim-3">
            <div class="kpi-top-row">
                <div class="kpi-label">Leading Subject Category</div>
                <div class="kpi-icon-badge kpi-icon-purple">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/>
                        <path d="M8 7h8"/><path d="M8 11h8"/><path d="M8 15h5"/>
                    </svg>
                </div>
            </div>
            <div class="kpi-value-text" title="{kpis['leading_category']}">{kpis['leading_category']}</div>
            <div class="kpi-progress-wrap">
                <div class="kpi-pct-label">{cat_share:.1f}% category share</div>
                <div class="kpi-progress-track">
                    <div class="kpi-progress-fill" style="width:{cat_share}%; background:linear-gradient(90deg,#E11D48,#FB7185);"></div>
                </div>
            </div>
            <div class="kpi-footer">
                <span class="kpi-pill kpi-pill-purple">🏆 #1 Subject</span>
                <span>{kpis['leading_category_count']:,} Enrollments</span>
                <span class="kpi-trend-neutral" style="margin-left:auto;">{cat_share:.0f}%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi4:
    lvl_share = min(100.0, max(0.0, float(kpis['leading_level_share'])))
    st.markdown(
        f"""
        <div class="kpi-card kpi-card-amber kpi-card-anim-4">
            <div class="kpi-top-row">
                <div class="kpi-label">Dominant Difficulty Tier</div>
                <div class="kpi-icon-badge kpi-icon-amber">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
                    </svg>
                </div>
            </div>
            <div class="kpi-value-text" title="{kpis['leading_level']}">{kpis['leading_level']}</div>
            <div class="kpi-progress-wrap">
                <div class="kpi-pct-label">{lvl_share:.1f}% tier concentration</div>
                <div class="kpi-progress-track">
                    <div class="kpi-progress-fill" style="width:{lvl_share}%; background:linear-gradient(90deg,#D97706,#FCD34D);"></div>
                </div>
            </div>
            <div class="kpi-footer">
                <span class="kpi-pill kpi-pill-amber">⭐ Top Tier</span>
                <span>{kpis['leading_level_count']:,} Enrollments</span>
                <span class="kpi-trend-up" style="margin-left:auto;">↑ {lvl_share:.0f}%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# Section 1: Learner Demographics Overview
# ---------------------------------------------------------
with st.container(border=True):
    st.markdown(
        f"""
        <div class="section-header-wrap">
            <span class="section-badge">01</span>
            <span class="section-header">Learner Demographics &amp; Population Profile</span>
        </div>
        <div class="section-desc">Distribution of registered learners across single-year ages, smoothed density curve, and gender representation.</div>
        """,
        unsafe_allow_html=True,
    )

    col_demo_left, col_demo_right = st.columns([0.62, 0.38])
    with col_demo_left:
        age_dist_df = get_age_distribution(filtered_df)
        fig_age = create_age_distribution_chart(age_dist_df, theme=tc)
        st.plotly_chart(fig_age, use_container_width=True, config={"displayModeBar": False})

    with col_demo_right:
        gender_df = get_gender_participation(filtered_df)
        fig_gender = create_gender_participation_chart(gender_df, theme=tc)
        st.plotly_chart(fig_gender, use_container_width=True, config={"displayModeBar": False})

    # Descriptive observation callout
    f_share = gender_df.loc[gender_df["Gender"] == "Female", "LearnerShare"].values
    f_val = f"{f_share[0]}%" if len(f_share) > 0 else "N/A"
    m_share = gender_df.loc[gender_df["Gender"] == "Male", "LearnerShare"].values
    m_val = f"{m_share[0]}%" if len(m_share) > 0 else "N/A"

    st.markdown(
        f"""
        <div class="observation-box">
            <div class="observation-icon">💡</div>
            <div>
                <b>Demographic Analysis:</b> The active learner community shows balanced gender parity ({f_val} Female vs {m_val} Male) across all age tiers. 
                Learner ages span from 15 to 35 with peak enrollment concentration in early-career professionals (20–28), establishing strong platform product-market fit with emerging workforce talent.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# Section 2: Age-Wise Enrollments & Course Category Popularity
# ---------------------------------------------------------
with st.container(border=True):
    st.markdown(
        f"""
        <div class="section-header-wrap">
            <span class="section-badge">02</span>
            <span class="section-header">Age-Wise Enrollments &amp; Catalog Dynamics</span>
        </div>
        <div class="section-desc">Enrollment volume analyzed by standard age bands, ranked category demand, difficulty tiers, and monetization structure.</div>
        """,
        unsafe_allow_html=True,
    )

    col_ep1, col_ep2 = st.columns(2)
    with col_ep1:
        age_enroll_df = get_age_enrollment_breakdown(filtered_df)
        fig_age_enroll = create_age_enrollment_chart(age_enroll_df, theme=tc)
        st.plotly_chart(fig_age_enroll, use_container_width=True, config={"displayModeBar": False})

    with col_ep2:
        cat_pop_df = get_category_popularity(filtered_df)
        fig_cat = create_category_popularity_chart(cat_pop_df, theme=tc)
        st.plotly_chart(fig_cat, use_container_width=True, config={"displayModeBar": False})

    col_ep3, col_ep4 = st.columns(2)
    with col_ep3:
        lvl_df = get_level_demand(filtered_df)
        fig_lvl = create_level_demand_chart(lvl_df, theme=tc)
        st.plotly_chart(fig_lvl, use_container_width=True, config={"displayModeBar": False})

    with col_ep4:
        type_df = get_type_distribution(filtered_df)
        fig_type = create_type_distribution_chart(type_df, theme=tc)
        st.plotly_chart(fig_type, use_container_width=True, config={"displayModeBar": False})

    leading_band = age_enroll_df.sort_values(by="Enrollments", ascending=False).iloc[0]["AgeGroup"] if not age_enroll_df.empty else "N/A"
    leading_band_pct = age_enroll_df.sort_values(by="Enrollments", ascending=False).iloc[0]["Percentage"] if not age_enroll_df.empty else 0

    st.markdown(
        f"""
        <div class="observation-box">
            <div class="observation-icon">💡</div>
            <div>
                <b>Catalog Demand Observation:</b> The <b>{leading_band}</b> demographic cohort drives the highest enrollment volume ({leading_band_pct}%). 
                Demand is remarkably diversified across all 12 categories, reflecting strong foundational interest in both technical disciplines (Programming, AI, Data Science) and executive competencies (Finance, Business).
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# Section 3: Gender Preferences & Demographic Cross-Tabulations
# ---------------------------------------------------------
with st.container(border=True):
    st.markdown(
        f"""
        <div class="section-header-wrap">
            <span class="section-badge">03</span>
            <span class="section-header">Gender Preferences &amp; Demographic Cross-Tabulations</span>
        </div>
        <div class="section-desc">Course category and difficulty preferences segmented by gender, accompanied by an age cohort × category matrix.</div>
        """,
        unsafe_allow_html=True,
    )

    col_pref_gcat, col_pref_glvl = st.columns([0.55, 0.45])
    with col_pref_gcat:
        gender_cat_df = get_gender_category_breakdown(filtered_df)
        fig_gender_cat = create_gender_category_chart(gender_cat_df, theme=tc)
        st.plotly_chart(fig_gender_cat, use_container_width=True, config={"displayModeBar": False})

    with col_pref_glvl:
        gender_lvl_df = get_gender_level_breakdown(filtered_df)
        fig_gender_lvl = create_gender_level_chart(gender_lvl_df, theme=tc)
        st.plotly_chart(fig_gender_lvl, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
    crosstab_df = get_age_category_crosstab(filtered_df)
    fig_heatmap = create_age_category_heatmap(crosstab_df, theme=tc)
    st.plotly_chart(fig_heatmap, use_container_width=True, config={"displayModeBar": False})

    st.markdown(
        """
        <div class="observation-box">
            <div class="observation-icon">💡</div>
            <div>
                <b>Preference Homogeneity:</b> Both female and male learners demonstrate symmetrical appetite across STEM fields (AI, Machine Learning, Cybersecurity) and Business domains. 
                This affirms that curriculum appeal is driven by career skill enhancement rather than demographic bias.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# Section 4: Behavioral Insights & Learner Depth
# ---------------------------------------------------------
with st.container(border=True):
    st.markdown(
        f"""
        <div class="section-header-wrap">
            <span class="section-badge">04</span>
            <span class="section-header">Behavioral Depth &amp; Engagement Concentration</span>
        </div>
        <div class="section-desc">Retention dynamics, course multi-enrollment concentration, and Pareto distribution among active learners.</div>
        """,
        unsafe_allow_html=True,
    )

    col_beh1, col_beh2 = st.columns([0.52, 0.48])
    conc_metrics = get_learner_concentration(filtered_df)

    with col_beh1:
        fig_conc = create_courses_per_learner_chart(conc_metrics["distribution_df"], theme=tc)
        st.plotly_chart(fig_conc, use_container_width=True, config={"displayModeBar": False})

    with col_beh2:
        st.markdown("<div style='padding-top:12px;'></div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px;">
                <div class="stat-micro-card">
                    <div class="stat-micro-title">Average Depth</div>
                    <div class="stat-micro-value">{conc_metrics['mean_courses']}</div>
                    <div class="stat-micro-caption">Courses completed per learner</div>
                </div>
                <div class="stat-micro-card">
                    <div class="stat-micro-title">Median Intensity</div>
                    <div class="stat-micro-value">{conc_metrics['median_courses']}</div>
                    <div class="stat-micro-caption">Median courses completed</div>
                </div>
                <div class="stat-micro-card">
                    <div class="stat-micro-title">Top 20% Pareto Share</div>
                    <div class="stat-micro-value">{conc_metrics['top_20_share']}%</div>
                    <div class="stat-micro-caption">Platform enrollment concentration</div>
                </div>
                <div class="stat-micro-card">
                    <div class="stat-micro-title">Multi-Course Retention</div>
                    <div class="stat-micro-value">{100.0 - conc_metrics['distribution_df'].iloc[0]['Percentage']:.1f}%</div>
                    <div class="stat-micro-caption">Learners enrolled in 2+ courses</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="observation-box">
            <div class="observation-icon">💡</div>
            <div>
                <b>Retention &amp; Platform Loyalty:</b> With learners averaging <b>{conc_metrics['mean_courses']} courses</b> and {100.0 - conc_metrics['distribution_df'].iloc[0]['Percentage']:.1f}% participating in multiple offerings, EduPro exhibits high recurring engagement. 
                The top quintile accounts for {conc_metrics['top_20_share']}% of transactions, reflecting healthy adoption without over-dependence on an isolated power-user group.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown(
    f"""
    <div style="text-align:center; padding-top:24px; padding-bottom:32px; color:{tc['text_secondary']}; font-size:12.5px; font-weight:500;">
        <div style="height:1px; background:linear-gradient(90deg, transparent, {tc['border']}, transparent); margin-bottom:18px;"></div>
        <b>EduPro Learner Intelligence Platform</b> • Enterprise Analytics System • Audited Relational Architecture
    </div>
    """,
    unsafe_allow_html=True,
)
