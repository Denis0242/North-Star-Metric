from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="North Star Metric & Product Health Dashboard", layout="wide")

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "processed" / "nsm_dataset_clean.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["event_date"] = pd.to_datetime(df["event_date"])
    return df

df = load_data()

st.markdown("""
<style>
.main-title {text-align:center; font-size:34px; font-weight:800; color:#2f5f9f; margin-bottom:0px;}
.sub-title {text-align:center; font-size:15px; color:#666; margin-bottom:20px;}
.kpi-card {background:white; border:1px solid #e7e7e7; border-radius:14px; padding:14px; box-shadow:0 2px 10px rgba(0,0,0,.04);}
.kpi-label {font-size:14px; color:#386cb0; font-weight:700;}
.kpi-value {font-size:30px; color:#555; font-weight:800;}
.insight-card {border-radius:14px; padding:16px; min-height:120px; border:1px solid #ddd;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">North Star Metric & Product Health Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Executive product health readout across activation, conversion, retention, churn, engagement, and revenue</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Dashboard Filters")
    exp = st.multiselect("Experiment Group", sorted(df["experiment_group"].unique()), default=sorted(df["experiment_group"].unique()))
    band = st.multiselect("Engagement Band", sorted(df["engagement_band"].unique()), default=sorted(df["engagement_band"].unique()))
    channel = st.multiselect("Channel", sorted(df["acquisition_channel"].unique()), default=sorted(df["acquisition_channel"].unique()))
    segment = st.multiselect("Segment", sorted(df["segment"].unique()), default=sorted(df["segment"].unique()))
    country = st.multiselect("Country", sorted(df["country"].unique()), default=sorted(df["country"].unique()))
    device = st.multiselect("Device", sorted(df["device"].unique()), default=sorted(df["device"].unique()))
    date_range = st.date_input("Event Date", [df["event_date"].min(), df["event_date"].max()])

filtered = df[
    df["experiment_group"].isin(exp)
    & df["engagement_band"].isin(band)
    & df["acquisition_channel"].isin(channel)
    & df["segment"].isin(segment)
    & df["country"].isin(country)
    & df["device"].isin(device)
]
if len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered = filtered[(filtered["event_date"] >= start) & (filtered["event_date"] <= end)]

if filtered.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

def pct(col):
    return f"{filtered[col].mean()*100:.1f}%"

def num(col):
    return f"{filtered[col].mean():.1f}"

kpis = [
    ("Activation Rate", pct("activation_rate")),
    ("Conversion Rate", pct("conversion_rate")),
    ("D30 Retention", pct("d30_retention")),
    ("Churn Rate", pct("churn_rate")),
    ("Avg Engagement", num("engagement_score")),
    ("Revenue Per User", f"${filtered['revenue_per_user'].mean():.2f}"),
]
cols = st.columns(6)
for col, (label, value) in zip(cols, kpis):
    with col:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div></div>', unsafe_allow_html=True)

st.divider()

monthly = filtered.set_index("event_date").resample("ME").agg({
    "activation_rate":"mean", "conversion_rate":"mean", "d30_retention":"mean", "churn_rate":"mean", "engagement_score":"mean"
}).reset_index()
monthly["month"] = monthly["event_date"].dt.strftime("%Y-%m")

c1, c2, c3 = st.columns([1.3, 1, 1])
with c1:
    fig = px.line(monthly, x="month", y="engagement_score", markers=True, title="Monthly Product Health Trend")
    fig.update_layout(showlegend=False, height=380, margin=dict(l=10,r=10,t=50,b=10))
    st.plotly_chart(fig, use_container_width=True)
with c2:
    seg = filtered.groupby("segment", as_index=False).agg(conversion_rate=("conversion_rate","mean"), engagement_score=("engagement_score","mean"))
    fig = px.bar(seg, x="conversion_rate", y="segment", orientation="h", title="Performance by Segment", text_auto=".1%")
    fig.update_layout(showlegend=False, height=380, margin=dict(l=10,r=10,t=50,b=10), xaxis_tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)
with c3:
    feat = filtered.groupby("primary_feature_used", as_index=False).agg(feature_adoption_rate=("feature_adoption_rate","mean")).sort_values("feature_adoption_rate")
    fig = px.bar(feat, x="feature_adoption_rate", y="primary_feature_used", orientation="h", title="Feature Adoption by Feature", text_auto=".1%")
    fig.update_layout(showlegend=False, height=380, margin=dict(l=10,r=10,t=50,b=10), xaxis_tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

c4, c5, c6 = st.columns([1.2, 1, 1])
with c4:
    fig = px.scatter(filtered, x="d30_retention", y="churn_rate", size="engagement_score", color="experiment_group", hover_data=["segment","country","revenue_per_user"], title="Retention vs Churn Risk")
    fig.update_traces(marker=dict(sizemode="area", sizeref=18, opacity=.65))
    fig.update_layout(height=390, margin=dict(l=10,r=10,t=50,b=10), xaxis_tickformat=".0%", yaxis_tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)
with c5:
    exp_summary = filtered.groupby("experiment_group", as_index=False).agg(conversion_rate=("conversion_rate","mean"), d30_retention=("d30_retention","mean"))
    exp_long = exp_summary.melt(id_vars="experiment_group", value_vars=["conversion_rate","d30_retention"], var_name="Metric", value_name="Rate")
    fig = px.bar(exp_long, x="Rate", y="experiment_group", color="Metric", orientation="h", barmode="group", title="Experiment Readout", text_auto=".1%")
    fig.update_layout(height=390, margin=dict(l=10,r=10,t=50,b=10), xaxis_tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)
with c6:
    ch = filtered.groupby("acquisition_channel", as_index=False).agg(conversion_rate=("conversion_rate","mean"), revenue_per_user=("revenue_per_user","mean")).sort_values("conversion_rate")
    fig = px.bar(ch, x="conversion_rate", y="acquisition_channel", orientation="h", title="Channel Performance", text_auto=".1%")
    fig.update_layout(showlegend=False, height=390, margin=dict(l=10,r=10,t=50,b=10), xaxis_tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("Executive Decision Summary")
insight_cols = st.columns(4)
cards = [
    ("Insight", "Variant B leads conversion but trails D30 retention."),
    ("Action", "Prioritize deeper testing while monitoring retention impact."),
    ("Recommendation", "Scale only if D30 retention does not decline further."),
    ("Decision", "Continue experiment monitoring before full rollout."),
]
for col, (title, text) in zip(insight_cols, cards):
    with col:
        st.markdown(f'<div class="insight-card"><b>{title}</b><br><br>{text}</div>', unsafe_allow_html=True)
