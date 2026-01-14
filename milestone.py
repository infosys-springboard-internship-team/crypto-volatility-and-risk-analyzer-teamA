import streamlit as st
import pandas as pd
import plotly.express as px

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="Crypto Risk Analytics Dashboard",
    layout="wide"
)

st.title("📊 Crypto Risk Analytics Dashboard")
st.markdown("*Milestone 3 – Visualization Dashboard*")

# ================== LOAD DATA ==================
DATA_PATH = "data/"

# ---- Load processed time-series data (Milestone 2 output) ----
df = pd.read_csv(
    DATA_PATH + "processed_crypto_data.csv",
    parse_dates=["Date"]
)

# ---- Load risk metrics summary (Milestone 2 output) ----
metrics_df = pd.read_csv(DATA_PATH + "crypto_metrics.csv")

# ================== DATA TRANSFORMATION ==================
# Convert wide format to long format (IMPORTANT)
price_cols = ["bitcoin", "ethereum", "solana", "cardano", "dogecoin"]

df_long = df.melt(
    id_vars=["Date"],
    value_vars=price_cols,
    var_name="Crypto",
    value_name="Close"
)

# ================== SIDEBAR FILTERS ==================
st.sidebar.header("🔍 Filters")

crypto_list = df_long["Crypto"].unique()

selected_crypto = st.sidebar.multiselect(
    "Select Cryptocurrencies",
    crypto_list,
    default=crypto_list[:2]
)

start_date = st.sidebar.date_input(
    "Start Date", df_long["Date"].min()
)

end_date = st.sidebar.date_input(
    "End Date", df_long["Date"].max()
)

filtered_df = df_long[
    (df_long["Crypto"].isin(selected_crypto)) &
    (df_long["Date"] >= pd.to_datetime(start_date)) &
    (df_long["Date"] <= pd.to_datetime(end_date))
]

# ================== DASHBOARD LAYOUT ==================
left, right = st.columns(2)

# ================== PRICE TREND ==================
with left:
    st.subheader("📈 Price Trend")
    price_fig = px.line(
        filtered_df,
        x="Date",
        y="Close",
        color="Crypto",
        title="Crypto Price Over Time",
        template="plotly_dark"
    )
    st.plotly_chart(price_fig, use_container_width=True)

# ================== VOLATILITY COMPARISON ==================
with left:
    st.subheader("📉 Volatility Comparison")

    vol_fig = px.bar(
        metrics_df,
        x="Asset",
        y="Annual Volatility",
        color="Asset",
        title="Annual Volatility by Cryptocurrency",
        template="plotly_dark"
    )
    st.plotly_chart(vol_fig, use_container_width=True)

# ================== RISK–RETURN ANALYSIS ==================
with right:
    st.subheader("⚖ Risk–Return Analysis")

    risk_return = metrics_df.rename(columns={
        "Asset": "Crypto",
        "Annual Volatility": "Volatility",
        "Sharpe Ratio": "Sharpe"
    })

    scatter_fig = px.scatter(
        risk_return,
        x="Volatility",
        y="Sharpe",
        color="Crypto",
        size="Sharpe",
        title="Risk vs Return (Sharpe Ratio)",
        template="plotly_dark"
    )
    st.plotly_chart(scatter_fig, use_container_width=True)

# ================== KPI METRICS ==================
st.subheader("📌 Key Metrics")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Assets Selected",
    len(selected_crypto)
)

c2.metric(
    "Avg Volatility",
    round(risk_return["Volatility"].mean(), 3)
)

c3.metric(
    "Avg Sharpe Ratio",
    round(risk_return["Sharpe"].mean(), 2)
)

c4.metric(
    "Market Benchmark",
    "BTC"
)

# ================== FOOTER ==================
st.markdown("---")
st.markdown("✅ **Milestone 3 Completed – Interactive Visualization Dashboard**")