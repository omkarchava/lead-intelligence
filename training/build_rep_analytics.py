import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

import pandas as pd

users = pd.read_csv("data/users.csv")
opps = pd.read_csv("data/opportunities.csv")
leads = pd.read_csv("data/leads.csv")

try:
    tasks = pd.read_csv("data/tasks.csv")
except:
    tasks = pd.DataFrame(
        columns=[
            "task_id",
            "owner_id",
            "status",
            "activity_date"
        ]
    )

try:
    events = pd.read_csv("data/events.csv")
except:
    events = pd.DataFrame(
        columns=[
            "event_id",
            "owner_id",
            "activity_date"
        ]
    )

results = []

for _, user in users.iterrows():

    rep_id = user["user_id"]

    rep_opps = opps[
        opps["owner_id"] == rep_id
    ]

    rep_leads = leads[
        leads["owner_id"] == rep_id
    ]

    rep_tasks = tasks[
        tasks["owner_id"] == rep_id
    ]

    rep_events = events[
        events["owner_id"] == rep_id
    ]

    total_opps = len(rep_opps)

    won_opps = len(
        rep_opps[
            rep_opps["won"] == True
        ]
    )

    open_opps = len(
        rep_opps[
            rep_opps["closed"] == False
        ]
    )

    active_leads = len(
        rep_leads[
            rep_leads["converted"] == False
        ]
    )

    open_tasks = len(
        rep_tasks[
            rep_tasks["status"] != "Completed"
        ]
    )

    upcoming_events = len(
        rep_events
    )

    revenue = (
        rep_opps["amount"]
        .fillna(0)
        .sum()
    )

    avg_deal_size = 0

    if total_opps > 0:
        avg_deal_size = (
            revenue / total_opps
        )

    win_rate = 0

    if total_opps > 0:
        win_rate = (
            won_opps / total_opps
        )

    results.append({

        "rep_id": rep_id,
        "rep_name": user["name"],

        "total_opps": total_opps,
        "won_opps": won_opps,

        "open_opps": open_opps,
        "active_leads": active_leads,

        "open_tasks": open_tasks,
        "upcoming_events": upcoming_events,

        "revenue": revenue,
        "avg_deal_size": avg_deal_size,

        "win_rate": round(
            win_rate * 100,
            2
        )
    })

df = pd.DataFrame(results)

if len(df) > 0:

    df["revenue_score"] = (
        df["revenue"]
        /
        max(
            df["revenue"].max(),
            1
        )
    ) * 100

    df["deal_score"] = (
        df["avg_deal_size"]
        /
        max(
            df["avg_deal_size"].max(),
            1
        )
    ) * 100

    df["capacity_score"] = (
        100
        -
        (
            df["active_leads"] * 2
            +
            df["open_opps"] * 5
            +
            df["open_tasks"] * 1
            +
            df["upcoming_events"] * 2
        )
    )

    df["capacity_score"] = (
        df["capacity_score"]
        .clip(lower=0)
    )

    df["estimated_days"] = (
        2
        +
        (df["active_leads"] * 0.5)
        +
        (df["open_opps"] * 1.5)
        +
        (df["open_tasks"] * 0.2)
        +
        (df["upcoming_events"] * 0.3)
    )

    df["estimated_days"] = (
        df["estimated_days"]
        .round(1)
    )

    df["rep_score"] = (

        df["win_rate"] * 0.40

        +

        df["revenue_score"] * 0.20

        +

        df["capacity_score"] * 0.30

        +

        df["deal_score"] * 0.10

    )

    df["rep_score"] = (
        df["rep_score"]
        .round(2)
    )
    
    df["assignment_score"] = (
    (
        df["rep_score"]
        *
        df["capacity_score"]
    ) / 100).round(2)

    # FINAL ASSIGNMENT SCORE

    df["assignment_score"] = (
        (
            df["rep_score"]
            *
            df["capacity_score"]
        )
        / 100
    ).round(2)

df.to_csv(
    "data/rep_analytics.csv",
    index=False
)

print(
    df[
        [
            "rep_name",
            "assignment_score",
            "rep_score",
            "estimated_days",
            "active_leads",
            "open_opps",
            "open_tasks",
            "upcoming_events"
        ]
    ].sort_values(
        "assignment_score",
        ascending=False
    )
)

print("\nRep Analytics Generated")