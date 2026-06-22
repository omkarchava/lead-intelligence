import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from salesforce.sf_client import sf
import pandas as pd

from salesforce.sf_client import sf
import pandas as pd

# Active Sales Reps

users = sf.query("""
SELECT
    Id,
    Name
FROM User
WHERE IsActive = true
""")["records"]

# Opportunities

opps = sf.query("""
SELECT
    Id,
    OwnerId,
    Amount,
    IsWon,
    IsClosed
FROM Opportunity
""")["records"]

df_users = pd.DataFrame(users)
df_opps = pd.DataFrame(opps)

results = []

for _, user in df_users.iterrows():

    rep_id = user["Id"]

    rep_opps = df_opps[
        df_opps["OwnerId"] == rep_id
    ]

    total_opps = len(rep_opps)

    won_opps = len(
        rep_opps[
            rep_opps["IsWon"] == True
        ]
    )

    total_amount = (
        rep_opps["Amount"]
        .fillna(0)
        .sum()
    )

    if total_opps == 0:
        win_rate = 0
    else:
        win_rate = (
            won_opps / total_opps
        )

    score = (
        (win_rate * 70)
        +
        min(
            total_amount / 100000,
            30
        )
    )

    score = round(
        min(score, 100),
        2
    )

    results.append({
        "rep_id": rep_id,
        "rep_name": user["Name"],
        "total_opps": total_opps,
        "won_opps": won_opps,
        "win_rate": round(win_rate,2),
        "amount": total_amount,
        "score": score
    })

df = pd.DataFrame(results)

df.to_csv(
    "data/rep_scores.csv",
    index=False
)

print(df)