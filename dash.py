import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="LLM Data Analyzer", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f0c29, #1a1a40);
    color: #f8fafc;
}
h1, h2, h3 {
    color: #facc15;
}
.metric-card {
    background: linear-gradient(145deg, #1a1a40, #2a2a72);
    padding: 20px;
    border-radius: 14px;
    text-align: center;
    border: 1px solid rgba(250, 204, 21, 0.3);
    box-shadow: 0 0 15px rgba(250, 204, 21, 0.2);
    transition: 0.3s;
}
.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 0 25px rgba(250, 204, 21, 0.4);
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #1a1a40);
}
.stButton>button {
    background: linear-gradient(90deg, #facc15, #9333ea);
    color: black;
    border-radius: 8px;
    border: none;
    font-weight: 600;
}
.stAlert {
    border-left: 4px solid #facc15;
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

        # -------------------- FIXED FILTER (NO ERROR) --------------------
        st.subheader("🎛️ Filter Data")

        clean_col = df[col].dropna()

        min_val = float(clean_col.min())
        max_val = float(clean_col.max())

        if min_val == max_val:
            st.warning("⚠️ Cannot apply filter (all values are same)")
            filtered_df = df.copy()
        else:
            selected_range = st.slider(
                f"Select range for {col}",
                min_value=min_val,
                max_value=max_val,
                value=(min_val, max_val)
            )

            filtered_df = df[(df[col] >= selected_range[0]) & (df[col] <= selected_range[1])]

        st.write(f"Filtered Data Count: {len(filtered_df)}")

        # -------------------- GRAPH RECOMMENDATION --------------------
        recommended_graph = "Line Chart"

        if filtered_df[col].nunique() < 10:
            recommended_graph = "Bar Chart"
        elif "year" in col.lower() or "date" in col.lower() or "time" in col.lower():
            recommended_graph = "Line Chart"
        elif any(k in col.lower() for k in ["mrp", "price", "cost", "category"]):
            recommended_graph = "Bar Chart"
        else:
            recommended_graph = "Line Chart"

        st.info(f"Recommended Graph for '{col}' is: {recommended_graph}")

        graph_type = st.selectbox(
            "Graph Type",
            ["Line Chart", "Bar Chart", "Area Chart"],
            index=["Line Chart", "Bar Chart", "Area Chart"].index(recommended_graph)
        )

        show_trend = st.checkbox("Show Trend Line")

        filtered_df["Trend"] = filtered_df[col].rolling(5).mean()

        chart_data = filtered_df[[col]].copy()
        if show_trend:
            chart_data["Trend"] = filtered_df["Trend"]

        if graph_type == "Line Chart":
            st.line_chart(chart_data)
        elif graph_type == "Bar Chart":
            st.bar_chart(chart_data)
        else:
            st.area_chart(chart_data)

        mean = filtered_df[col].mean()
        median = filtered_df[col].median()
        std = filtered_df[col].std()
        skew = filtered_df[col].skew()

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
            if filtered_df["Trend"].iloc[-1] > filtered_df["Trend"].iloc[0]:
                st.success("Upward trend detected")
            else:
                st.error("Downward trend detected")

        if filtered_df[col].max() > mean * 2:
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
