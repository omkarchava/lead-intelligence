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

records = result["records"]

clean = []

for r in records:

    clean.append({
        "lead_source": r.get("LeadSource"),
        "industry": r.get("Industry"),
        "converted": 1 if r.get("IsConverted") else 0
    })

df = pd.DataFrame(clean)

df.to_csv(
    "data/lead_conversion_training.csv",
    index=False
)

print(df.head())
print("Total Records:", len(df))