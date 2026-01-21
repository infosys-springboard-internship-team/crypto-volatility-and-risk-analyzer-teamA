import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Milestone 4 – Risk Classification & Reporting",
    layout="wide"
)
# ================= CUSTOM CSS =================
st.markdown("""
<style>
.stApp {
    background-color: #0B1220;
    color: #E5E7EB;
}

h1, h2, h3 {
    color: #38BDF8;
    font-weight: 700;
}

/* === RISK CARDS === */
.risk-card {
    width: 100%;
    min-height: 260px;
    height:auto;
    padding: 22px;
    border-radius: 18px;
    box-sizing: border-box;
    overflow:visible;
}

.risk-high {
    background: rgba(239, 68, 68, 0.22);
    border: 1px solid rgba(239, 68, 68, 0.5);
}

.risk-medium {
    background: rgba(250, 204, 21, 0.22);
    border: 1px solid rgba(250, 204, 21, 0.5);
}

.risk-low {
    background: rgba(34, 197, 94, 0.22);
    border: 1px solid rgba(34, 197, 94, 0.5);
}

/* === ASSET ROW === */
.asset-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 10px 0;
    font-size: 15px;
}

.asset-name {
    color: #F8FAFC;
    font-weight: 500;
}

.asset-badge {
    background: rgba(255, 255, 255, 0.25);
    padding: 4px 10px;
    border-radius: 12px;
    font-weight: 600;
    color: #FFFFFF;
}

/* DOWNLOAD BUTTON */
.stDownloadButton button {
    background-color: white !important;
    color: black !important;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ================= LOAD DATA =================
metrics_df = pd.read_csv("data/crypto_metrics.csv")

# ================= RISK CLASSIFICATION =================
def classify_risk(vol):
    if vol > 0.7:
        return "High Risk"
    elif vol > 0.4:
        return "Medium Risk"
    else:
        return "Low Risk"

metrics_df["Risk Level"] = metrics_df["Annual Volatility"].apply(classify_risk)

# ================= CARD RENDER FUNCTION =================
def render_card(title, df, color_class):
    html = f"<div class='risk-card {color_class}'>"
    html += f"<h3>{title}</h3>"

    for _, r in df.iterrows():
        html += (
        "<div class='asset-row'>"
        f"<div class='asset-name'>{r['Asset']}</div>"
        f"<div class='asset-badge'>{r['Annual Volatility']*100:.1f}%</div>"
        "</div>"
        )
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# ================= HEADER =================
st.title("🚨 Milestone 4: Risk Classification & Reporting")

# ================= REQUIREMENTS & OUTPUTS =================
c1, c2 = st.columns(2)

with c1:
    st.subheader("📋 Requirements")
    st.markdown("""
    - Risk thresholds for classification  
    - Visual highlighting of high-risk assets  
    - Summary reports (CSV, PDF)  
    - System validation & documentation  
    """)

with c2:
    st.subheader("📦 Outputs")
    st.markdown("""
    - Risk classification dashboard  
    - Categorized risk report  
    - Risk distribution visualization  
    - Exportable reports  
    """)

st.markdown("---")

# ================= PROJECT COMPLETION =================
st.subheader("📈 Project Completion Status")

status_df = pd.DataFrame({
    "Milestone": ["Milestone 1", "Milestone 2", "Milestone 3", "Milestone 4"],
    "Completion": [100, 100, 100, 100]
})

fig = px.bar(
    status_df,
    x="Milestone",
    y="Completion",
    text="Completion",
    color_discrete_sequence=["#22C55E"],
    template="plotly_dark"
)

fig.update_layout(yaxis_range=[0, 100],plot_bgcolor="#0B1220")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ================= RISK DASHBOARD =================
st.subheader("📌 Risk Classification Dashboard")

high = metrics_df[metrics_df["Risk Level"] == "High Risk"]
medium = metrics_df[metrics_df["Risk Level"] == "Medium Risk"]
low = metrics_df[metrics_df["Risk Level"] == "Low Risk"]

c1, c2, c3 = st.columns(3)

with c1:
    render_card("🔴 High Risk", high, "risk-high")

with c2:
    render_card("🟡 Medium Risk", medium, "risk-medium")

with c3:
    render_card("🟢 Low Risk", low, "risk-low")

# ================= SUMMARY =================
st.markdown("---")
st.subheader("📊 Risk Summary Report")

st.markdown(f"""
<b>Total Assets:</b> {len(metrics_df)}  
<br><b>Average Volatility:</b> {metrics_df['Annual Volatility'].mean():.2f}  
<br><b>Risk Distribution:</b> {len(high)} High / {len(medium)} Medium / {len(low)} Low  
""", unsafe_allow_html=True)

# ================= DONUT =================
counts = metrics_df["Risk Level"].value_counts().reset_index()
counts.columns = ["Risk Level", "Count"]

donut = px.pie(
    counts,
    values="Count",
    names="Risk Level",
    hole=0.55,
    color="Risk Level",
    color_discrete_map={
        "High Risk": "#EF4444",
        "Medium Risk": "#FACC15",
        "Low Risk": "#22C55E"
    },
    template="plotly_dark"
)
 
donut.update_layout(
    title_text="Risk Distribution",
    title_x=0.45,
    plot_bgcolor="#0B1220"
)
st.plotly_chart(donut, use_container_width=True)

# ================= EXPORT =================
st.markdown("---")
st.subheader("⬇ Report Export")

st.download_button(
    "📥 Download CSV",
    metrics_df.to_csv(index=False).encode("utf-8"),
    "risk_report.csv",
    "text/csv"
)

# ================= PDF =================
def create_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "Risk Classification Report", ln=True)
    pdf.ln(5)

    for _, r in df.iterrows():
        pdf.cell(
            0, 8,
            f"{r['Asset']} - {r['Risk Level']} ({r['Annual Volatility']*100:.1f}%)",
            ln=True
        )

    return pdf.output(dest="S").encode("latin-1")

st.download_button(
    "📄 Download PDF",
    create_pdf(metrics_df),
    "risk_report.pdf",
    "application/pdf"
)

st.success("✅ Milestone 4 Completed – Risk Classification & Reporting")