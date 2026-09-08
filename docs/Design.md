# EduPro Learner Intelligence Dashboard — Design Specification

## 1. Design intent

Create a calm, credible educational analytics experience: light, spacious, and easy to scan. The visual language should help policy and education stakeholders understand patterns quickly while remaining approachable for non-technical users.

## 2. Theme and color system

| Role | Color | Use |
| --- | --- | --- |
| Page background | `#F8FAFC` | Main canvas |
| Surface | `#FFFFFF` | Cards, tables, filter areas |
| Primary text | `#0F172A` | Headings and key figures |
| Secondary text | `#475569` | Explanatory text and labels |
| Border | `#E2E8F0` | Card/table separation |
| Primary blue | `#2563EB` | Actions, selected states, primary series |
| Teal | `#0F766E` | Secondary positive comparison series |
| Amber | `#D97706` | Attention / secondary highlight |
| Red | `#B91C1C` | Errors only |

Use sequential color scales for intensity-based charts and color-blind-considerate categorical palettes. Never encode an important distinction with red versus green alone.

## 3. Typography

- Font family: `Inter`, with `system-ui, sans-serif` fallback.
- Page title: 28–32 px, 700 weight.
- Section title: 20–24 px, 700 weight.
- Card KPI: 28–36 px, 700 weight.
- Body and chart labels: 14–16 px, 400–500 weight.
- Use sentence case for headings and labels; avoid all-caps body text.

## 4. Layout

- Wide desktop-first dashboard with a collapsible sidebar for filters.
- Keep primary content within a generous maximum width and use 24–32 px page padding.
- Use a 12-column responsive grid: four KPI cards in one row on wide screens, two on medium screens, one on narrow screens.
- Group related charts in cards with 16–24 px inner padding and 12–16 px corner radius.
- Maintain consistent vertical rhythm: 24 px between major sections, 16 px within a section.

## 5. Component guidance

### Header

Show “EduPro Learner Intelligence” as the title, a one-sentence descriptive scope statement, and a subtle data-load/status indicator.

### Filters

Place filters in the sidebar in this order: age group, gender, course category, course level. Use multi-select controls with clear defaults and a visible reset action.

### KPI cards

Each card includes a concise label, prominent number, and a short denominator/context note. Avoid decorative gauges.

### Charts

- Prefer horizontal bars for longer category names.
- Use a heatmap for age group × category because it supports cross-segment comparison.
- Place labels/totals where they improve scanning; retain hover details for exact values.
- Start bar-chart axes at zero.
- Display a friendly empty state in place of a chart with no data.

### Data-quality callout

Use an unobtrusive expandable panel. Normal status is blue/neutral; warnings use amber; blocking data errors use red with a clear corrective action.

## 6. Accessibility requirements

- Maintain WCAG AA contrast for text and interactive controls.
- Provide text titles and descriptions for every chart.
- Ensure keyboard operation for filters and reset controls.
- Do not rely on hover alone: show key values in labels, tables, or supporting text.
- Use plain-language status and error messages.

## 7. Content tone

Use precise, neutral, evidence-led language. Example: “Learners aged 18–25 account for 42% of filtered enrollments.” Avoid value judgments or unsupported explanations such as “this group prefers learning more.”
