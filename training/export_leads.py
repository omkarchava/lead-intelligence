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
    LeadSource,
    Industry,
    IsConverted
FROM Lead
"""

result = sf.query(query)

rows = []

for r in result["records"]:

    rows.append({
        "owner_id": r.get("OwnerId"),
        "lead_source": r.get("LeadSource"),
        "industry": r.get("Industry"),
        "converted": r.get("IsConverted")
    })

df = pd.DataFrame(rows)

df.to_csv(
    "data/leads.csv",
    index=False
)

print("Leads Exported:", len(df))
print(df.head())