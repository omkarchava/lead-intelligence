import pandas as pd
import joblib

assignment_model = joblib.load(
    "models/assignment_model.pkl"
)

time_model = joblib.load(
    "models/time_model.pkl"
)

lead = {
    "industry":"Manufacturing",
    "source":"Website",
    "territory":"Pune"
}

reps = [
    {
        "rep":"John",
        "active_leads":12,
        "open_opps":4
    },
    {
        "rep":"Sarah",
        "active_leads":6,
        "open_opps":2
    }
]

results = []

for rep in reps:

    row = pd.DataFrame(
        [
            {
                **lead,
                **rep
            }
        ]
    )

    probability = assignment_model.predict_proba(
        row
    )[0][1]

    days = time_model.predict(
        row
    )[0]

    capacity = (
        100
        - rep["active_leads"] * 2
        - rep["open_opps"] * 3
    )

    score = (
        probability * 70
        + capacity * 0.3
    )

    results.append(
        {
            "rep": rep["rep"],
            "score": round(score,2),
            "conversion_probability":
                round(probability*100,2),
            "predicted_days":
                round(days)
        }
    )

results = sorted(
    results,
    key=lambda x: x["score"],
    reverse=True
)

print(results)