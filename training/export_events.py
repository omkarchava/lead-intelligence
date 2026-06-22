import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from salesforce.sf_client import sf
import pandas as pd

query = """
SELECT
    Id,
    OwnerId,
    ActivityDate
FROM Event
"""

result = sf.query(query)

rows = []

if "records" in result:

    for r in result["records"]:

        rows.append({
            "event_id": r.get("Id"),
            "owner_id": r.get("OwnerId"),
            "activity_date": r.get("ActivityDate")
        })

if len(rows) == 0:

    df = pd.DataFrame(
        columns=[
            "event_id",
            "owner_id",
            "activity_date"
        ]
    )

else:

    df = pd.DataFrame(rows)

df.to_csv(
    "data/events.csv",
    index=False
)

print("Events Exported:", len(df))