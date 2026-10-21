"""
Student Performance Factors Analysis
====================================
This script generates a synthetic student performance dataset, performs
exploratory data analysis, and produces publication-quality visualizations.

Research Question:
    To what extent do study habits, attendance, and sleep patterns influence
    student exam performance, and which factors are most predictive?
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------
np.random.seed(42)

# Paths
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
VIZ_DIR = ROOT / "visualizations"
DATA_DIR.mkdir(exist_ok=True)
VIZ_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Generate synthetic dataset (n = 1000 students)
# ---------------------------------------------------------------------------
N = 1000

hours_studied = np.clip(np.random.normal(5, 2.5, N), 0, 12)
attendance = np.clip(np.random.normal(80, 12, N), 40, 100)
sleep_hours = np.clip(np.random.normal(7, 1.2, N), 4, 10)
previous_scores = np.clip(np.random.normal(65, 12, N), 30, 100)
extracurricular = np.random.choice([0, 1], size=N, p=[0.45, 0.55])
parental_education = np.random.choice(
    ["High School", "Bachelor's", "Master's", "Doctorate"],
    size=N, p=[0.4, 0.35, 0.2, 0.05]
)

# True generating model for exam_score (with noise)
#   hours_studied  -> strong positive
#   attendance     -> moderate positive
#   sleep_hours    -> small inverted-U effect
#   prev_scores    -> strong positive
#   parental_edu   -> small bonus for higher education
parental_bonus = pd.Categorical(
    parental_education,
    categories=["High School", "Bachelor's", "Master's", "Doctorate"]
).codes * 1.2

sleep_effect = 2.0 * sleep_hours - 0.25 * (sleep_hours - 7) ** 2

exam_score = (
    0.4 * previous_scores
    + 1.8 * hours_studied
    + 0.15 * attendance
    + 0.8 * sleep_effect
    + parental_bonus
    + np.random.normal(0, 4, N)
)
exam_score = np.clip(exam_score, 20, 100).round(1)

df = pd.DataFrame({
    "student_id": [f"S{str(i+1).zfill(4)}" for i in range(N)],
    "hours_studied": hours_studied.round(1),
    "attendance_pct": attendance.round(1),
    "sleep_hours": sleep_hours.round(1),
    "previous_scores": previous_scores.round(1),
    "extracurricular": extracurricular,
    "parental_education": parental_education,
    "exam_score": exam_score,
})

csv_path = DATA_DIR / "student_performance.csv"
df.to_csv(csv_path, index=False)
print(f"Dataset saved to {csv_path}  ({len(df)} rows, {df.shape[1]} columns)")
print(df.head())
print("\nSummary statistics:")
print(df.describe())

# ---------------------------------------------------------------------------
# 2. Visualisation 1: Correlation heatmap of numeric factors
# ---------------------------------------------------------------------------
sns.set_theme(style="whitegrid", context="talk")
fig, ax = plt.subplots(figsize=(9, 7))
numeric_cols = ["hours_studied", "attendance_pct", "sleep_hours",
                "previous_scores", "exam_score"]
corr = df[numeric_cols].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r",
            center=0, square=True, linewidths=0.5, ax=ax,
            cbar_kws={"shrink": 0.8})
ax.set_title("Correlation Heatmap — Student Performance Factors",
             fontweight="bold", pad=15)
plt.tight_layout()
viz1_path = VIZ_DIR / "correlation_heatmap.png"
plt.savefig(viz1_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"\nVisualisation 1 saved: {viz1_path}")

# ---------------------------------------------------------------------------
# 3. Visualisation 2: Exam score vs hours studied (coloured by attendance)
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6.5))
sc = ax.scatter(df["hours_studied"], df["exam_score"],
                c=df["attendance_pct"], cmap="viridis",
                alpha=0.6, edgecolors="none", s=30)
cbar = plt.colorbar(sc, ax=ax)
cbar.set_label("Attendance (%)", rotation=270, labelpad=20)

# Trend line
z = np.polyfit(df["hours_studied"], df["exam_score"], 2)
p = np.poly1d(z)
x_line = np.linspace(0, 12, 200)
ax.plot(x_line, p(x_line), color="crimson", linewidth=2.5,
        linestyle="--", label="Quadratic trend")

ax.set_xlabel("Hours Studied per Week")
ax.set_ylabel("Exam Score (0–100)")
ax.set_title("Exam Score vs. Weekly Study Hours\n"
             "(colour = attendance rate)",
             fontweight="bold")
ax.legend()
plt.tight_layout()
viz2_path = VIZ_DIR / "score_vs_hours_studied.png"
plt.savefig(viz2_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"Visualisation 2 saved: {viz2_path}")

# ---------------------------------------------------------------------------
# 4. Key findings
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("KEY FINDINGS")
print("=" * 60)
print(f"Correlation of hours_studied  with exam_score: "
      f"{corr.loc['hours_studied','exam_score']:.3f}")
print(f"Correlation of previous_scores with exam_score: "
      f"{corr.loc['previous_scores','exam_score']:.3f}")
print(f"Correlation of attendance_pct  with exam_score: "
      f"{corr.loc['attendance_pct','exam_score']:.3f}")
print(f"Correlation of sleep_hours     with exam_score: "
      f"{corr.loc['sleep_hours','exam_score']:.3f}")

mean_by_parent = df.groupby("parental_education")["exam_score"].mean()
print("\nMean exam score by parental education level:")
print(mean_by_parent.round(2))
