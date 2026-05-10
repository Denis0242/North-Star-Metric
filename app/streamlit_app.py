import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
sys.path.append(str(APP_DIR))
from utils import load_data, kpi_summary
from components import metric_card, decision_panel

st.set_page_config(page_title='North Star Metric & Product Health', layout='wide')
st.title('North Star Metric & Product Health Dashboard')
st.caption('Portfolio companion app for product analytics, KPI monitoring, retention risk, and experiment decisions.')

df = load_data()

with st.sidebar:
    st.header('Filters')
    segment = st.multiselect('Segment', sorted(df['segment'].unique()), default=sorted(df['segment'].unique()))
    channel = st.multiselect('Channel', sorted(df['acquisition_channel'].unique()), default=sorted(df['acquisition_channel'].unique()))
    experiment = st.multiselect('Experiment Group', sorted(df['experiment_group'].unique()), default=sorted(df['experiment_group'].unique()))
    date_range = st.date_input('Event Date Range', [df['event_date'].min().date(), df['event_date'].max().date()])

filtered = df[df['segment'].isin(segment) & df['acquisition_channel'].isin(channel) & df['experiment_group'].isin(experiment)]
if len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered = filtered[(filtered['event_date'] >= start) & (filtered['event_date'] <= end)]

summary = kpi_summary(filtered)
cols = st.columns(6)
with cols[0]: metric_card('Activation Rate', summary['Activation Rate'], is_percent=True)
with cols[1]: metric_card('Conversion Rate', summary['Conversion Rate'], is_percent=True)
with cols[2]: metric_card('D30 Retention', summary['D30 Retention'], is_percent=True)
with cols[3]: metric_card('Churn Rate', summary['Churn Rate'], is_percent=True)
with cols[4]: metric_card('Avg Engagement', summary['Avg Engagement Score'])
with cols[5]: metric_card('Revenue/User', summary['Revenue Per User'], is_currency=True)

monthly = filtered.assign(month=filtered['event_date'].dt.to_period('M').astype(str)).groupby('month', as_index=False).agg(
    avg_engagement_score=('engagement_score', 'mean'),
    conversion_rate=('conversion_rate', 'mean'),
    d30_retention=('d30_retention', 'mean'),
    churn_rate=('churn_rate', 'mean')
)
st.plotly_chart(px.line(monthly, x='month', y='avg_engagement_score', markers=True, title='Monthly Product Health Trend'), use_container_width=True)

c1, c2 = st.columns(2)
with c1:
    seg = filtered.groupby('segment', as_index=False).agg(conversion_rate=('conversion_rate','mean'), d30_retention=('d30_retention','mean'))
    st.plotly_chart(px.bar(seg, x='conversion_rate', y='segment', orientation='h', title='Performance by Segment'), use_container_width=True)
with c2:
    feat = filtered.groupby('primary_feature_used', as_index=False).agg(feature_adoption_rate=('feature_adoption_rate','mean'))
    st.plotly_chart(px.bar(feat.sort_values('feature_adoption_rate'), x='feature_adoption_rate', y='primary_feature_used', orientation='h', title='Feature Adoption by Feature'), use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    exp = filtered.groupby('experiment_group', as_index=False).agg(conversion_rate=('conversion_rate','mean'), d30_retention=('d30_retention','mean'), churn_rate=('churn_rate','mean'))
    st.dataframe(exp, use_container_width=True)
with c4:
    ch = filtered.groupby('acquisition_channel', as_index=False).agg(conversion_rate=('conversion_rate','mean'), d30_retention=('d30_retention','mean'), revenue_per_user=('revenue_per_user','mean'))
    st.plotly_chart(px.bar(ch.sort_values('conversion_rate'), x='conversion_rate', y='acquisition_channel', orientation='h', title='Channel Performance'), use_container_width=True)

decision_panel()

st.subheader('Raw Data Preview')
st.dataframe(filtered.head(100), use_container_width=True)
