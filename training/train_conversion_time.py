import pandas as pd
import joblib

from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from xgboost import XGBRegressor


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "training.csv"

MODEL_FILE = BASE_DIR / "models" / "time_model.pkl"


print("BASE_DIR :", BASE_DIR)
print("DATA_FILE:", DATA_FILE)
print("MODEL_FILE:", MODEL_FILE)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv(DATA_FILE)

print(f"Records Loaded: {len(df)}")


# --------------------------------------------------
# ONLY CONVERTED RECORDS
# --------------------------------------------------

df = df[df["days_to_convert"] > 0]

print(f"Converted Records: {len(df)}")

if len(df) == 0:
    raise Exception(
        "No records found where days_to_convert > 0"
    )


# --------------------------------------------------
# FEATURES
# --------------------------------------------------

X = df[
    [
        "industry",
        "source",
        "territory",
        "rep",
        "active_leads",
        "open_opps"
    ]
]

y = df["days_to_convert"]


# --------------------------------------------------
# FEATURE PROCESSING
# --------------------------------------------------

categorical = [
    "industry",
    "source",
    "territory",
    "rep"
]

numeric = [
    "active_leads",
    "open_opps"
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical
        ),
        (
            "num",
            "passthrough",
            numeric
        )
    ]
)


# --------------------------------------------------
# MODEL
# --------------------------------------------------

model = XGBRegressor(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    random_state=42
)


pipeline = Pipeline(
    [
        ("prep", preprocessor),
        ("model", model)
    ]
)


# --------------------------------------------------
# TRAIN
# --------------------------------------------------

print("Training Conversion Time Model...")

pipeline.fit(X, y)

print("Training Complete")


# --------------------------------------------------
# SAVE MODEL
# --------------------------------------------------

MODEL_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

joblib.dump(
    pipeline,
    MODEL_FILE
)

print(f"Model Saved: {MODEL_FILE}")