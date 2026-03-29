import streamlit as st
import pandas as pd
import numpy as np

# -------------------- CONFIG --------------------
st.set_page_config(page_title="LLM Data Analyzer", layout="wide")

# -------------------- PROFESSIONAL CSS --------------------
st.markdown("""
<style>
.stApp { background-color: #0f172a; color: #e2e8f0; }
h1, h2, h3 { color: #f8fafc; }
.metric-card {
    background: #1e293b;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #334155;
}
section[data-testid="stSidebar"] {
    background-color: #020617;
}
</style>
""", unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.markdown("<h1 style='text-align:center;'>🤖 Intelligent CSV Analyzer</h1>", unsafe_allow_html=True)

# -------------------- INPUT --------------------
file = st.file_uploader("Upload CSV File", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
    st.success("✅ File Uploaded Successfully")

    # -------------------- BASIC PROCESSING --------------------
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if numeric_cols:

        st.subheader("📊 Graph Control Panel")

        col = st.selectbox("Select Column", numeric_cols)

        graph_type = st.selectbox(
            "Select Graph Type",
            ["Line Chart", "Bar Chart", "Area Chart"]
        )

        show_trend = st.checkbox("Show Trend Line (Moving Average)")

        # -------------------- TREND LINE --------------------
        df["Trend"] = df[col].rolling(window=5).mean()

        # -------------------- GRAPH --------------------
        st.subheader("📈 Visualization")

        chart_data = df[[col]].copy()

        if show_trend:
            chart_data["Trend"] = df["Trend"]

        if graph_type == "Line Chart":
            st.line_chart(chart_data)

        elif graph_type == "Bar Chart":
            st.bar_chart(chart_data)

        elif graph_type == "Area Chart":
            st.area_chart(chart_data)

        # -------------------- STATISTICS --------------------
        st.subheader("📈 Statistical Analysis")

        mean = df[col].mean()
        median = df[col].median()
        std = df[col].std()
        skew = df[col].skew()

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(f"<div class='metric-card'><h3>Mean</h3><h2>{round(mean,2)}</h2></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='metric-card'><h3>Median</h3><h2>{round(median,2)}</h2></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='metric-card'><h3>Std Dev</h3><h2>{round(std,2)}</h2></div>", unsafe_allow_html=True)
        with c4:
            st.markdown(f"<div class='metric-card'><h3>Skewness</h3><h2>{round(skew,2)}</h2></div>", unsafe_allow_html=True)

        # -------------------- TECHNICAL INSIGHTS --------------------
        st.subheader("🧠 Technical Insights")

        # Skewness insight
        if skew > 0:
            st.info("Positive skew detected → higher value concentration on right tail")
        elif skew < 0:
            st.info("Negative skew detected → lower value concentration on left tail")
        else:
            st.info("Data is approximately symmetric")

        # Variance insight
        if std > mean:
            st.warning("High variance → data is highly dispersed and unstable")

        # Trend insight
        if show_trend:
            if df["Trend"].iloc[-1] > df["Trend"].iloc[0]:
                st.success("Upward trend detected over time")
            else:
                st.error("Downward trend detected")

        # Outlier detection
        if df[col].max() > mean * 2:
            st.error("Outliers detected → may distort analysis")

        # -------------------- LOGICAL INSIGHTS --------------------
        st.subheader("🔍 Logical Insights")

        st.write("• Compare mean and median to understand distribution")
        st.write("• Use trend line to smooth fluctuations")
        st.write("• High std deviation indicates inconsistent behavior")

        # -------------------- SUGGESTIONS --------------------
        st.subheader("💡 Recommendations")

        st.write("• Apply normalization if variance is high")
        st.write("• Remove outliers for better model accuracy")
        st.write("• Use moving average for better trend clarity")
        st.write("• Consider ML models for predictive analysis")

        # -------------------- AUTOMATION --------------------
        st.subheader("⚡ Automation")

        st.success("Fully automated pipeline: Input → Analysis → Visualization → Insights → Recommendations")

    else:
        st.error("❌ No numeric data found")

else:
    st.info("Upload a CSV file to begin")
