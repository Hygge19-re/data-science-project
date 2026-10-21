# Student Performance Factors Analysis

## Problem / Research Question

**To what extent do study habits, attendance, and sleep patterns influence student exam performance, and which factors are most predictive of final exam scores?**

Understanding the drivers of academic performance can help students, educators, and policymakers design more effective learning interventions. This project quantifies the relative importance of several commonly cited factors and identifies which have the strongest association with exam outcomes.

## Dataset Source and Usage Permissions

The dataset (`data/student_performance.csv`) is a **synthetic dataset of 1,000 students** generated for educational purposes using a pre-specified data-generating process. It contains no real personal information.

| Column | Type | Description |
|---|---|---|
| `student_id` | string | Anonymous student identifier (S0001–S1000) |
| `hours_studied` | float | Self-reported weekly study hours (0–12) |
| `attendance_pct` | float | Attendance rate (40–100 %) |
| `sleep_hours` | float | Average nightly sleep (4–10 hours) |
| `previous_scores` | float | Average score in prior assessments (30–100) |
| `extracurricular` | binary | Participation in extracurricular activities (0 = No, 1 = Yes) |
| `parental_education` | categorical | Highest parental education level |
| `exam_score` | float | Final exam score (20–100) |

**Usage rights:** The synthetic dataset is free to use, modify, and distribute for educational and non-commercial purposes. No personal data was collected from real individuals.

## Methods and Tools Used

- **Language:** Python 3.12
- **Libraries:**
  - `pandas` – data loading, cleaning, and summary statistics
  - `numpy` – synthetic data generation and numerical computations
  - `matplotlib` and `seaborn` – data visualisation
- **Analytical methods:**
  - Descriptive statistics and exploratory data analysis (EDA)
  - Pearson correlation analysis (heatmap)
  - Bivariate scatter plots with a quadratic trend line
  - Group-wise means (ANOVA-style comparison across parental education levels)

## Key Findings

1. **Prior academic performance is the strongest predictor** of exam score (Pearson *r* = 0.60), suggesting that consistent performance over time is highly stable.
2. **Weekly study hours have a moderate-to-strong positive relationship** with exam performance (*r* = 0.53). The scatter plot shows a roughly linear upward trend — students who study more tend to score higher, with diminishing returns beyond ~10 hours/week.
3. **Sleep hours show a weak positive correlation** (*r* = 0.27), consistent with the expected small inverted-U shape (too little or too much sleep is suboptimal).
4. **Attendance rate has only a weak linear association** with exam score in this synthetic dataset (*r* = 0.14), indicating that attendance alone may not be sufficient to predict outcomes.
5. **Parental education level shows a small gradient**: students whose parents hold a doctorate average ~5 points higher than those whose parents' highest level is high school.

### Visualisations

| Figure | File |
|---|---|
| Correlation heatmap of numeric factors | `visualizations/correlation_heatmap.png` |
| Exam score vs. weekly study hours (coloured by attendance) | `visualizations/score_vs_hours_studied.png` |

## One Limitation

Because the dataset is **synthetic and generated from a known linear-plus-noise model**, the observed correlations reflect the true underlying parameters rather than real-world complexity. In a real student population, confounders such as socioeconomic status, mental health, and teaching quality would likely modify these relationships. The results should therefore be interpreted as illustrative rather than causal or generalisable.

## Instructions for Running the Analysis

### Prerequisites

- Python 3.9 or higher
- `pip` package manager

### Setup

```bash
# 1. Clone or download this repository
cd data-science-project

# 2. (Recommended) Create a virtual environment
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Run

```bash
# Run the full analysis (regenerates the dataset and all figures)
python notebooks/analysis.py
```

### Expected output

- `data/student_performance.csv` — the dataset (1,000 rows)
- `visualizations/correlation_heatmap.png`
- `visualizations/score_vs_hours_studied.png`
- Printed summary statistics and key findings in the terminal

---

*Course: CISC7204 — Data Science Portfolio (Practice 09)*
*Author: HUANG LINJIE (mc64240)*
