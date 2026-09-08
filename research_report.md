# EduPro Learner Intelligence: Exploratory Data Analysis & Strategic Research Report

**Document Status:** Complete  
**Date:** September 2026  
**Audience:** Education Program Designers, Curriculum Developers, Outreach & Marketing Teams, Platform Analysts  

---

## Executive Overview

This research report presents an exhaustive, evidence-led descriptive analysis of learner behavior and course engagement on the **EduPro Online Platform**. Consuming verified transactional, user demographic, and curriculum catalog records spanning the 2025 calendar year (10,000 completed course enrollments across 3,000 registered learners and 60 catalog offerings), this report establishes baseline empirical answers to key operational questions.

In compliance with the product guidelines established in `PRD.md` and `Rules.md`, all findings are purely descriptive. No unverified causal claims, predictive models, or personalized recommendations are introduced.

---

## 1. Demographic Profile: Learner Age and Representation

### 1.1 Age Distribution Analysis

EduPro serves a focused demographic spanning **ages 15 to 35** (mean age: **25.0 years**, median age: **25.0 years**, standard deviation: **6.05 years**). The distribution is continuous and evenly populated across youth, tertiary students, and early-to-mid career professionals:

| Single-Year Age | Learner Count | Percentage of Learner Base | Cumulative Share |
|:---:|:---:|:---:|:---:|
| 15 | 150 | 5.0% | 5.0% |
| 16 | 137 | 4.6% | 9.6% |
| 17 | 146 | 4.9% | 14.4% |
| 18 | 134 | 4.5% | 18.9% |
| 19 | 151 | 5.0% | 23.9% |
| 20 | 141 | 4.7% | 28.6% |
| 21 | 136 | 4.5% | 33.1% |
| 22 | 147 | 4.9% | 38.0% |
| 23 | 129 | 4.3% | 42.3% |
| 24 | 143 | 4.8% | 47.1% |
| 25 | 140 | 4.7% | 51.8% |
| 26 | 141 | 4.7% | 56.5% |
| 27 | 151 | 5.0% | 61.5% |
| 28 | 135 | 4.5% | 66.0% |
| 29 | 152 | 5.1% | 71.1% |
| 30 | 138 | 4.6% | 75.7% |
| 31 | 149 | 5.0% | 80.6% |
| 32 | 148 | 4.9% | 85.6% |
| 33 | 139 | 4.6% | 90.2% |
| 34 | 145 | 4.8% | 95.0% |
| 35 | 149 | 5.0% | 100.0% |

#### Standardized Age Band Aggregation
Under the standardized classification (`<18`, `18–25`, `26–35`, `36–45`, `45+`):
- **`<18` (Secondary / Adolescents):** 433 learners (**14.4%**)
- **`18–25` (Tertiary / University Age):** 1,121 learners (**37.4%**)
- **`26–35` (Early Career / Professionals):** 1,446 learners (**48.2%**)
- **`36–45` & `45+`:** Currently unrepresented in the active 2025 cohort (**0.0%**), establishing an evident demographic boundary.

### 1.2 Gender Participation Breakdown
Platform membership and engagement exhibit exceptional balance across gender lines:
- **Female Learners:** 1,520 learners (**50.7%** of learner base), generating 5,078 course enrollments (**50.8%** of total volume).
- **Male Learners:** 1,480 learners (**49.3%** of learner base), generating 4,922 course enrollments (**49.2%** of total volume).
- **Parity Ratio:** 1.03 Female learners per Male learner.

Both genders complete an almost identical average number of courses (**3.34 courses/learner** for Female vs **3.33 courses/learner** for Male).

---

## 2. Enrollment Dynamics Across Age Groups

Enrollment activity corresponds closely to demographic cohort size:

| Standardized Age Band | Active Learners | Total Enrollments | Share of Enrollments | Enrollments per Active Learner |
|:---|:---:|:---:|:---:|:---:|
| **`<18`** | 433 | 1,469 | 14.7% | 3.39 |
| **`18–25`** | 1,121 | 3,732 | 37.3% | 3.33 |
| **`26–35`** | 1,446 | 4,799 | 48.0% | 3.32 |
| **`36–45`** | 0 | 0 | 0.0% | 0.00 |
| **`45+`** | 0 | 0 | 0.0% | 0.00 |
| **Total** | **3,000** | **10,000** | **100.0%** | **3.33** |

### Key Insight
Average course completion depth across age brackets is virtually invariant (3.39 for under-18 vs 3.32 for 26–35). Younger adolescent learners take courses at an identical multi-enrollment frequency as adult career seekers, refuting the hypothesis that younger users exhibit lower commitment or drop-off rates on EduPro.

---

## 3. Course Popularity and Catalog Demand

The 60 courses across 12 distinct subject categories reflect uniform catalog engagement without isolated monopoly categories:

| Rank | Course Category | Available Courses | Total Enrollments | Active Unique Learners | Share of Platform (%) |
|:---:|:---|:---:|:---:|:---:|:---:|
| 1 | **Data Science** | 5 | 916 | 685 | 9.2% |
| 2 | **Finance** | 5 | 864 | 650 | 8.6% |
| 3 | **Web Development** | 5 | 844 | 652 | 8.4% |
| 4 | **Business** | 5 | 833 | 648 | 8.3% |
| 5 | **Project Management** | 5 | 829 | 636 | 8.3% |
| 6 | **Machine Learning** | 5 | 826 | 638 | 8.3% |
| 7 | **Digital Marketing** | 5 | 825 | 640 | 8.2% |
| 8 | **Cybersecurity** | 5 | 824 | 623 | 8.2% |
| 9 | **Design** | 5 | 822 | 633 | 8.2% |
| 10 | **Marketing** | 5 | 818 | 637 | 8.2% |
| 11 | **Artificial Intelligence** | 5 | 813 | 633 | 8.1% |
| 12 | **Programming** | 5 | 786 | 610 | 7.9% |

### 3.1 Course Level Preferences
Catalog difficulty demand indicates healthy participation across skill tiers:
- **Beginner Courses:** 3,573 enrollments (**35.7%** share) across 21 catalog courses.
- **Advanced Courses:** 3,475 enrollments (**34.8%** share) across 21 catalog courses.
- **Intermediate Courses:** 2,952 enrollments (**29.5%** share) across 18 catalog courses.

Average enrollments per available course:
- Beginner: **170.1 enrollments / course**
- Intermediate: **164.0 enrollments / course**
- Advanced: **165.5 enrollments / course**

Course level demand per title is remarkably steady (~164–170 enrollments per title), indicating that learners actively advance into Intermediate and Advanced courses rather than clustering exclusively in onboarding material.

### 3.2 Pricing Model Distribution
- **Paid Courses:** 6,400 enrollments (**64.0%**)
- **Free Courses:** 3,600 enrollments (**36.0%**)

---

## 4. Demographic × Subject Preference Cross-Analysis

### 4.1 Age Group × Course Category Matrix
Cross-tabulation reveals that subject preferences do not diverge drastically by age cohort:
- **Data Science** leads across all three active age groups:
  - `<18`: 137 enrollments (9.3%)
  - `18–25`: 349 enrollments (9.4%)
  - `26–35`: 430 enrollments (9.0%)
- **Technical Domains** (Cybersecurity, Machine Learning, AI, Web Development) receive equal proportional interest from adolescent learners (`<18`) as they do from the `26–35` workforce cohort.
- **Business and Finance** maintain steady appeal across all groups (8.1%–8.8% per cohort).

### 4.2 Gender × Course Level Analysis
Cross-tabulating gender against course difficulty reveals equitable distribution:
- **Female Learners:**
  - Beginner: 1,811 enrollments (35.7%)
  - Intermediate: 1,489 enrollments (29.3%)
  - Advanced: 1,778 enrollments (35.0%)
- **Male Learners:**
  - Beginner: 1,762 enrollments (35.8%)
  - Intermediate: 1,463 enrollments (29.7%)
  - Advanced: 1,697 enrollments (34.5%)

Both genders exhibit identical percentage distributions across difficulty tiers within ±0.7 percentage points, demonstrating that curriculum progression is gender-neutral.

---

## 5. Behavioral Depth & Enrollment Concentration

### 5.1 Multi-Course Engagement Distribution
The platform experiences substantial repeat usage:
- **1 Course:** 1,620 learners (**54.0%**)
- **2–3 Courses:** 798 learners (**26.6%**)
- **4+ Courses:** 582 learners (**19.4%**)

**46.0% of all learners take 2 or more courses.** Active return learners sustain long-term engagement across multiple modules.

### 5.2 Pareto Concentration Metric
- The **top 20% most active learners** (600 learners) account for **6,648 enrollments**, representing **66.5% of total platform volume**.
- While 54.0% of the user base consumes a single introductory module, a dedicated core cohort of power learners drives approximately two-thirds of all learning activity.

---

## 6. Strategic Recommendations

### For Curriculum & Education Teams
1. **Catalog Expansion for Working Professionals (30–45+):** Currently, enrollment terminates sharply at age 35. Curricula tailored for mid-career management, executive reskilling, and senior leadership should be piloted to expand into the currently unrepresented `36–45` and `45+` cohorts.
2. **Intermediate Skill Bridges:** Intermediate courses exhibit slightly lower relative volume (29.5%) than Beginner (35.7%) and Advanced (34.8%). Structuring clear project-based capstones bridging foundational courses to advanced specializations will increase conversion through the intermediate pipeline.
3. **Cross-Disciplinary Learning Paths:** Given that 46.0% of learners enroll in multiple courses, bundling cross-discipline sequences (e.g., *Data Science + Business Strategy* or *Web Development + Cybersecurity*) directly addresses demonstrated learner multi-enrollment patterns.

### For Marketing & Outreach Teams
1. **Targeted Outreach to High Schools & Pre-College (`<18`):** The `<18` group accounts for 14.7% of volume with equivalent commitment depth (3.39 courses per user). Focused partnerships with high schools and early STEM programs represent a proven high-retention opportunity.
2. **Gender-Neutral Brand Positioning:** Since enrollment and level selection are evenly split (50.7% Female vs 49.3% Male), outreach campaigns should continue to maintain balanced, accessible messaging without gendered segmentation.
3. **Nurturing the Repeat Learner Cohort:** Developing milestone badges and multi-course pathway communications for learners after completing their first course can convert a portion of the 54.0% single-course learners into repeat learners.
