from salesforce.sf_client import sf
import pandas as pd

leads = sf.query("""
SELECT
    Id,
    OwnerId
FROM Lead
WHERE IsConverted = false
""")["records"]

df = pd.DataFrame(leads)

capacity = (
    df.groupby("OwnerId")
      .size()
      .reset_index(name="active_leads")
)

capacity.to_csv(
    "data/rep_capacity.csv",
    index=False
)

print(capacity)