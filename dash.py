import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="LLM Data Analyzer", layout="wide")

# -------------------- LOGO --------------------
st.image("logo.png", width=120)

# -------------------- FINAL UI CSS (BOLD + HIGH VISIBILITY + GAUGE THEME) --------------------
st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background: #111827;
    color: #ffffff;
    font-weight: bold;
}

/* FORCE ALL TEXT VISIBLE */
html, body, [class*="css"] {
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* HEADINGS */
h1, h2, h3 {
    color: #facc15 !important;
    font-weight: 900 !important;
}

/* LABELS */
label {
    color: #ffffff !important;
    font-weight: bold !important;
}

/* METRIC CARDS */
.metric-card {
    background: #1f2937;
    padding: 20px;
    border-radius: 14px;
    text-align: center;
    border: 2px solid #facc15;
    color: #ffffff;
    font-weight: bold;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #020617;
    color: white;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg, #16a34a, #facc15, #ef4444);
    color: black;
    font-weight: 900;
    border-radius: 8px;
}

/* ALERTS */
.stAlert {
    font-weight: bold;
    border-left: 5px solid #facc15;
}

/* FILE UPLOADER */
.stFileUploader {
    color: white !important;
    font-weight: bold !important;
}

/* SLIDER */
.stSlider {
    color: white !important;
    font-weight: bold !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>⚡ Intelligent CSV Analyzer</h1>", unsafe_allow_html=True)

file = st.file_uploader("Upload CSV File", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
    st.success("File Uploaded Successfully")

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if numeric_cols:
        col = st.selectbox("Select Column", numeric_cols)

        # -------------------- FILTER --------------------
        st.subheader("🎛️ Filter Data")

        clean_col = df[col].dropna()
        min_val = float(clean_col.min())
        max_val = float(clean_col.max())

        if min_val == max_val:
            st.warning("Cannot apply filter")
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
            st.success("🟢 Higher values dominate")
        elif skew < 0:
            st.warning("🟡 Lower values dominate")
        else:
            st.info("Balanced data")

        if std > mean:
            st.warning("⚠️ High variance")

        if show_trend:
            if filtered_df["Trend"].iloc[-1] > filtered_df["Trend"].iloc[0]:
                st.success("🟢 Upward trend")
            else:
                st.error("🔴 Downward trend")

        if filtered_df[col].max() > mean * 2:
            st.error("🔴 Outliers detected")

        st.subheader("Suggestions")
        st.write("• Normalize data")
        st.write("• Remove outliers")
        st.write("• Use trend smoothing")
        st.write("• Apply ML models")

    else:
        st.error("No numeric data found")

else:
    st.info("Upload a CSV file")
