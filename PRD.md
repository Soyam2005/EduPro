# EduPro Learner Intelligence Dashboard — Product Requirements Document

## 1. Product summary

EduPro needs a Streamlit analytics dashboard that converts its user, course, and transaction data into clear **descriptive learner intelligence**. The product will help stakeholders understand who learns on the platform and how learners choose courses. It is not a prediction, recommendation, monetization, or automated decision-making system.

## 2. Background and context

The platform serves learners with different ages, genders, learning goals, and subject interests. Understanding these dimensions supports relevant course design, stronger learner engagement, targeted outreach, and inclusive, accessible learning offerings.

## 3. Problem statement

Although EduPro holds user and enrollment data, stakeholders cannot readily answer:

- Which age groups are most active?
- How do enrollment patterns differ by gender?
- Which course categories do learner segments prefer?
- Are beginner, intermediate, or advanced courses more popular for particular age groups?

Without this evidence, decisions about courses, marketing, and platform growth rely too heavily on intuition.

## 4. Target users

- **Education and program teams:** plan course catalogues and levels.
- **Marketing and outreach teams:** identify audiences and engagement opportunities.
- **Platform leadership / government stakeholders:** review inclusive reach, demand, and learner behavior.
- **Analysts:** explore and communicate validated descriptive findings.

## 5. Data inputs

The app consumes three related sheets/tables:

| Source | Required fields |
| --- | --- |
| Users | `UserID`, `UserName`, `Age`, `Gender` |
| Courses | `CourseID`, `CourseName`, `CourseCategory`, `CourseType`, `CourseLevel` |
| Transactions | `TransactionID`, `UserID`, `CourseID`, `TransactionDate` |

Records are linked as `Users.UserID → Transactions.UserID` and `Courses.CourseID → Transactions.CourseID`.

## 6. Core analytical questions

1. What is the age distribution of learners on EduPro?
2. How does enrollment vary across age groups?
3. Are there gender-based differences in course selection?
4. Which course categories receive the highest enrollments?
5. Do beginners prefer particular course types or course levels?

## 7. Functional requirements

### Dashboard modules

1. **Learner demographic overview** — learner count, age distribution, gender distribution, and participation overview.
2. **Age-wise enrollment analysis** — enrollment counts and shares by defined age band.
3. **Gender-based course preference analysis** — comparisons of category, type, and level across gender.
4. **Course popularity analysis** — category, course type, and course level demand.
5. **Demographic × preference analysis** — age-group/category heatmap and gender/level comparison.
6. **Behavioral insights** — average courses per learner, enrollment concentration among active learners, and beginner-versus-advanced behavior.

### Filters and controls

Users must be able to filter the analysis by:

- Age group
- Gender
- Course category
- Course level

Filters apply consistently to KPI cards, charts, tables, and written observations. The dashboard must communicate when a filter produces no matching data.

## 8. KPI definitions

| KPI | Definition | Decision use |
| --- | --- | --- |
| Total Enrollments | Count of valid transaction records after filters | Platform engagement |
| Enrollments by Age Group | Enrollment count/share for each age band | Demographic reach |
| Gender Participation Ratio | Share/count of active learners or enrollments by gender | Inclusivity |
| Category Popularity Index | Enrollment count/share by course category | Course demand |
| Level Preference Distribution | Enrollment count/share by course level | Skill maturity |

## 9. Deliverables

- Streamlit dashboard with live analysis of loaded data.
- Research paper/report containing EDA, insights, and actionable recommendations.
- Executive summary for government stakeholders.

## 10. Success criteria

- A stakeholder can answer each core analytical question without manually joining data.
- Every displayed metric is traceable to the source fields and active filters.
- Invalid or unmatched data is surfaced clearly rather than silently distorting findings.
- The dashboard supports evidence-based course planning and outreach decisions.

## 11. Out of scope

- Predicting future enrollments or learner outcomes.
- Personalized course recommendations.
- Revenue optimization or monetization analysis.
- Causal claims about why a demographic chooses a course.
