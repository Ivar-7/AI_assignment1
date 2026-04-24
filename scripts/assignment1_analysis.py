from __future__ import annotations

import json
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlretrieve

import matplotlib.pyplot as plt
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
OUTPUT_DIR = ROOT_DIR / "outputs"
DATA_FILE = DATA_DIR / "results.csv"

DATASET_URLS = [
    "https://raw.githubusercontent.com/martj42/international_results/master/results.csv",
]


def ensure_dataset() -> Path:
    local_candidates = [
        DATA_FILE,
        ROOT_DIR / "results.csv",
    ]

    for candidate in local_candidates:
        if candidate.exists():
            return candidate

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for url in DATASET_URLS:
        try:
            print(f"Trying to download dataset from: {url}")
            urlretrieve(url, DATA_FILE)
            print(f"Dataset downloaded to: {DATA_FILE}")
            return DATA_FILE
        except (URLError, OSError) as exc:
            print(f"Download failed from {url}: {exc}")

    raise RuntimeError(
        "Could not locate results.csv locally and download failed. "
        "Place the file at data/results.csv or repository root as results.csv."
    )


def match_result(row: pd.Series) -> str:
    if row["home_score"] > row["away_score"]:
        return "Home Win"
    if row["home_score"] < row["away_score"]:
        return "Away Win"
    return "Draw"


def build_markdown_report(answers: dict[str, object]) -> str:
    lines = [
        "# Assignment 1 Analysis Report",
        "",
        "This report contains the answers for all required questions with code-driven results.",
        "",
        "## Basic Exploration",
        f"1. Matches in dataset: **{answers['q1_matches_count']}**",
        (
            "2. Earliest and latest year: "
            f"**{answers['q2_earliest_year']}** to **{answers['q2_latest_year']}**"
        ),
        f"3. Unique countries/teams (home + away union): **{answers['q3_unique_countries']}**",
        (
            "4. Most frequent home team: "
            f"**{answers['q4_most_common_home_team']}** "
            f"({answers['q4_most_common_home_team_count']} matches as home)"
        ),
        "",
        "## Goals Analysis",
        f"5. Average goals per match: **{answers['q5_avg_goals_per_match']:.3f}**",
        (
            "6. Highest scoring match: "
            f"**{answers['q6_highest_scoring_match']}** "
            f"with **{answers['q6_highest_scoring_total_goals']} goals**"
        ),
        (
            "7. More goals scored at: "
            f"**{answers['q7_more_goals_scored_where']}** "
            f"(home={answers['q7_total_home_goals']}, away={answers['q7_total_away_goals']})"
        ),
        f"8. Most common total goals value: **{answers['q8_most_common_total_goals']}**",
        "",
        "## Match Results",
        (
            "9. Percentage of home wins: "
            f"**{answers['q9_home_win_percentage']:.2f}%**"
        ),
        f"10. Home advantage exists: **{answers['q10_home_advantage_exists']}**",
        (
            "11. Country with most historical wins: "
            f"**{answers['q11_country_most_wins']}** "
            f"({answers['q11_country_most_wins_count']} wins)"
        ),
        "",
        "## Visualizations Generated",
        "- hist_total_goals.png",
        "- bar_match_outcomes.png",
        "- bar_top10_wins.png",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    dataset_path = ensure_dataset()
    df = pd.read_csv(dataset_path)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["total_goals"] = df["home_score"] + df["away_score"]
    df["result"] = df.apply(match_result, axis=1)

    home_wins = df.loc[df["result"] == "Home Win", "home_team"].value_counts()
    away_wins = df.loc[df["result"] == "Away Win", "away_team"].value_counts()
    total_wins = home_wins.add(away_wins, fill_value=0).sort_values(ascending=False)

    highest_scoring_row = df.loc[df["total_goals"].idxmax()]
    result_counts = df["result"].value_counts()

    answers: dict[str, object] = {
        "q1_matches_count": int(df.shape[0]),
        "q2_earliest_year": int(df["date"].dt.year.min()),
        "q2_latest_year": int(df["date"].dt.year.max()),
        "q3_unique_countries": int(pd.unique(pd.concat([df["home_team"], df["away_team"]])).size),
        "q4_most_common_home_team": str(df["home_team"].value_counts().index[0]),
        "q4_most_common_home_team_count": int(df["home_team"].value_counts().iloc[0]),
        "q5_avg_goals_per_match": float(df["total_goals"].mean()),
        "q6_highest_scoring_match": (
            f"{highest_scoring_row['home_team']} {highest_scoring_row['home_score']}-"
            f"{highest_scoring_row['away_score']} {highest_scoring_row['away_team']} "
            f"on {highest_scoring_row['date'].date()}"
        ),
        "q6_highest_scoring_total_goals": int(highest_scoring_row["total_goals"]),
        "q7_total_home_goals": int(df["home_score"].sum()),
        "q7_total_away_goals": int(df["away_score"].sum()),
        "q7_more_goals_scored_where": (
            "Home"
            if int(df["home_score"].sum()) > int(df["away_score"].sum())
            else "Away"
        ),
        "q8_most_common_total_goals": int(df["total_goals"].mode().iloc[0]),
        "q9_home_win_percentage": float((result_counts.get("Home Win", 0) / len(df)) * 100),
        "q10_home_advantage_exists": bool(
            result_counts.get("Home Win", 0) > result_counts.get("Away Win", 0)
        ),
        "q11_country_most_wins": str(total_wins.index[0]),
        "q11_country_most_wins_count": int(total_wins.iloc[0]),
    }

    (OUTPUT_DIR / "answers.json").write_text(json.dumps(answers, indent=2), encoding="utf-8")
    (OUTPUT_DIR / "analysis_report.md").write_text(
        build_markdown_report(answers),
        encoding="utf-8",
    )

    plt.figure(figsize=(8, 5))
    df["total_goals"].hist(bins=15)
    plt.title("Distribution of Goals Per Match")
    plt.xlabel("Total Goals")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "hist_total_goals.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    result_counts.reindex(["Home Win", "Draw", "Away Win"]).plot(kind="bar")
    plt.title("Match Outcomes")
    plt.xlabel("Outcome")
    plt.ylabel("Matches")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "bar_match_outcomes.png", dpi=150)
    plt.close()

    plt.figure(figsize=(10, 6))
    total_wins.head(10).plot(kind="bar")
    plt.title("Top 10 Teams by Total Wins")
    plt.xlabel("Team")
    plt.ylabel("Wins")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "bar_top10_wins.png", dpi=150)
    plt.close()

    print("Assignment 1 analysis completed successfully.")
    print(f"Dataset used: {dataset_path}")
    print(f"Outputs written to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
