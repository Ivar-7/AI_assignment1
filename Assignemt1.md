Artificial intelligence -Exercise 1
Kaggle Dataset: International Football Results (1872–2024)
 https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017
FOOTBALL ANALYSIS EXERCISE
Step 1: Load the CSV
import pandas as pd

df = pd.read_csv("results.csv")
df.head()

Basic Exploration (You must show code to arrive at your answers. Use markdown to explain logic)
    1. How many matches are in the dataset?
    2. What is the earliest and latest year in the data?
    3. How many unique countries are there?
    4. Which team appears most frequently as home team?
Hints:
df.shape
df["date"].min()
df["home_team"].value_counts().head()

Goals Analysis (You must show code to arrive at your answers. Use markdown to explain logic)
Create total goals:
df["total_goals"] = df["home_score"] + df["away_score"]
Questions:
    5. What is the average number of goals per match?
    6. What is the highest scoring match?
    7. Are more goals scored at home or away?
    8. What is the most common total goals value?
Match Results (You must show code to arrive at your answers. Use markdown to explain logic)
Create match outcome:
def match_result(row):
    if row["home_score"] > row["away_score"]:
        return "Home Win"
    elif row["home_score"] < row["away_score"]:
        return "Away Win"
    else:
        return "Draw"

df["result"] = df.apply(match_result, axis=1)
Questions:
    9. What percentage of matches are home wins?
    10. Does home advantage exist?
    11. Which country has the most wins historically?

Visualization (You must show code to arrive at your answers. Use markdown to explain logic)
produce:
    • Histogram of goals
    • Bar chart of match outcomes
    • Top 10 teams by total wins
Example:
import matplotlib.pyplot as plt

df["total_goals"].hist(bins=15)
plt.title("Distribution of Goals Per Match")
plt.show()
