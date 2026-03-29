import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="LLM Data Analyzer", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0a0f1c, #111827);
    color: #e5e7eb;
}
h1, h2, h3 {
    color: #22d3ee;
}
.metric-card {
    background: linear-gradient(145deg, #111827, #1f2937);
    padding: 20px;
    border-radius: 14px;
    text-align: center;
    border: 1px solid rgba(34, 211, 238, 0.3);
    box-shadow: 0 0 15px rgba(34, 211, 238, 0.15);
}
.metric-card:hover {
    transform: translateY(-5px);
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #0f172a);
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🤖 Intelligent CSV Analyzer</h1>", unsafe_allow_html=True)

file = st.file_uploader("Upload CSV File", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
    st.success("File Uploaded Successfully")

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if numeric_cols:
        col = st.selectbox("Select Column", numeric_cols)
        graph_type = st.selectbox("Graph Type", ["Line Chart", "Bar Chart", "Area Chart"])
        show_trend = st.checkbox("Show Trend Line")

        df["Trend"] = df[col].rolling(5).mean()

        chart_data = df[[col]].copy()
        if show_trend:
            chart_data["Trend"] = df["Trend"]

        if graph_type == "Line Chart":
            st.line_chart(chart_data)
        elif graph_type == "Bar Chart":
            st.bar_chart(chart_data)
        else:
            st.area_chart(chart_data)

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

        st.subheader("Insights")

        if skew > 0:
            st.info("Positive skew → higher values dominate")
        elif skew < 0:
            st.info("Negative skew → lower values dominate")
        else:
            st.info("Balanced distribution")

        if std > mean:
            st.warning("High variance → unstable data")

        if show_trend:
            if df["Trend"].iloc[-1] > df["Trend"].iloc[0]:
                st.success("Upward trend detected")
            else:
                st.error("Downward trend detected")

        if df[col].max() > mean * 2:
            st.error("Outliers detected")

        st.subheader("Suggestions")
        st.write("• Normalize data if variance is high")
        st.write("• Remove outliers")
        st.write("• Use moving average for trends")
        st.write("• Apply ML models for prediction")

    else:
        st.error("No numeric data found")

else:
    st.info("Upload a CSV file")
