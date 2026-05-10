from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / 'data' / 'nsm_product_health_data.csv'


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, parse_dates=['event_date'])
    return df


def kpi_summary(df: pd.DataFrame) -> dict:
    return {
        'Activation Rate': df['activation_rate'].mean(),
        'Conversion Rate': df['conversion_rate'].mean(),
        'D30 Retention': df['d30_retention'].mean(),
        'Churn Rate': df['churn_rate'].mean(),
        'Avg Engagement Score': df['engagement_score'].mean(),
        'Revenue Per User': df['revenue_per_user'].mean(),
    }
