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
    Status,
    ActivityDate
FROM Task
"""

result = sf.query(query)

rows = []

if "records" in result:

    for r in result["records"]:

        rows.append({
            "task_id": r.get("Id"),
            "owner_id": r.get("OwnerId"),
            "status": r.get("Status"),
            "activity_date": r.get("ActivityDate")
        })

if len(rows) == 0:

    df = pd.DataFrame(
        columns=[
            "task_id",
            "owner_id",
            "status",
            "activity_date"
        ]
    )

else:

    df = pd.DataFrame(rows)

df.to_csv(
    "data/tasks.csv",
    index=False
)

print("Tasks Exported:", len(df))