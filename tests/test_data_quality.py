from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "processed" / "nsm_dataset_clean.csv"

def test_dataset_exists():
    assert DATA_PATH.exists()

def test_required_columns_present():
    df = pd.read_csv(DATA_PATH)
    required = {"user_id", "event_date", "conversion_rate", "d30_retention", "churn_rate", "revenue_per_user", "engagement_score"}
    assert required.issubset(set(df.columns))

def test_no_duplicate_user_ids():
    df = pd.read_csv(DATA_PATH)
    assert df["user_id"].duplicated().sum() == 0
