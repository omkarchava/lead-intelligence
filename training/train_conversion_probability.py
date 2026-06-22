import pandas as pd
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv(
    "data/lead_conversion_training.csv"
)

X = df[
    [
        "lead_source",
        "industry"
    ]
]

y = df["converted"]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            [
                "lead_source",
                "industry"
            ]
        )
    ]
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

pipeline = Pipeline(
    [
        ("prep", preprocessor),
        ("model", model)
    ]
)

pipeline.fit(X, y)

joblib.dump(
    pipeline,
    "models/conversion_probability.pkl"
)

print("Model Trained")