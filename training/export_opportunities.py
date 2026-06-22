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
    Amount,
    IsWon,
    IsClosed,
    StageName,
    CreatedDate,
    CloseDate
FROM Opportunity
"""

result = sf.query(query)

records = []

for r in result["records"]:

    records.append({
        "owner_id": r.get("OwnerId"),
        "amount": r.get("Amount"),
        "won": r.get("IsWon"),
        "closed": r.get("IsClosed"),
        "stage": r.get("StageName")
    })

df = pd.DataFrame(records)

df.to_csv(
    "data/opportunities.csv",
    index=False
)

print(df.head())
print("Total:", len(df))