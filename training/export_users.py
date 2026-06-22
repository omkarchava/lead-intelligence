import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from salesforce.sf_client import sf
import pandas as pd

query = """
SELECT
    Id,
    Name,
    Title,
    Department
FROM User
WHERE IsActive = true
"""

result = sf.query(query)

rows = []

for r in result["records"]:

    rows.append({
        "user_id": r["Id"],
        "name": r["Name"],
        "title": r.get("Title"),
        "department": r.get("Department")
    })

df = pd.DataFrame(rows)

df.to_csv(
    "data/users.csv",
    index=False
)

print(df)