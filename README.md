# AI Assignment 1 - International Football Results Analysis

This project completes Assignment 1 using the International Football Results dataset.

## What this includes
- Data loading (local file or automatic download fallback)
- Basic exploration questions (Q1-Q4)
- Goals analysis questions (Q5-Q8)
- Match result analysis questions (Q9-Q11)
- Required visualizations:
  - Histogram of goals
  - Bar chart of match outcomes
  - Top 10 teams by total wins

## Project structure
- `scripts/assignment1_analysis.py`: End-to-end analysis pipeline
- `data/results.csv`: Dataset location (auto-fetched if missing)
- `outputs/`: Generated plots and summary files

## Setup
```bash
pip install -r requirements.txt
```

## Run
```bash
python scripts/assignment1_analysis.py
```

## Output files
After running, these files are generated in `outputs/`:
- `answers.json`
- `analysis_report.md`
- `hist_total_goals.png`
- `bar_match_outcomes.png`
- `bar_top10_wins.png`
