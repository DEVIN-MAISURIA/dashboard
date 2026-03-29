import streamlit as st
import pandas as pd
import numpy as np

# -------------------- CONFIG --------------------
st.set_page_config(page_title="LLM Data Analyzer", layout="wide")

# -------------------- PROFESSIONAL CSS --------------------
st.markdown("""
<style>
/* Main background */
.stApp {
    background-color: #0f172a;
    color: #e2e8f0;
}

/* Titles */
h1, h2, h3 {
    color: #f8fafc;
}

/* Card style */
.block-container {
    padding-top: 2rem;
}

/* Metric cards */
.metric-card {
    background: #1e293b;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #334155;
}

/* Buttons */
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #020617;
}

/* Success / Info colors */
.stAlert {
    border-radius: 10px;
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

    # -------------------- INPUT TYPE --------------------
    st.subheader("📥 Input Type")
    st.write("Structured CSV Data")

    # -------------------- PROCESSING --------------------
    st.subheader("⚙️ Data Processing")
    st.write("• Handling numeric columns")
    st.write("• Statistical computation")
    st.write("• Pattern detection")

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if numeric_cols:

        # -------------------- OUTPUT TYPE --------------------
        st.subheader("📤 Output Type")
        st.write("Interactive Dashboard + AI Insights")

        # -------------------- GRAPH SELECTION --------------------
        st.subheader("📊 Graph Selection Logic")

        col = st.selectbox("Select column for analysis", numeric_cols)

        unique_vals = df[col].nunique()

        if unique_vals < 10:
            graph_type = "Bar Chart"
            st.bar_chart(df[col])
        else:
            graph_type = "Line Chart"
            st.line_chart(df[col])

        st.info(f"Selected Graph: {graph_type}")

        # -------------------- STATISTICS --------------------
        st.subheader("📈 Statistical Analysis")

        mean = df[col].mean()
        median = df[col].median()
        std = df[col].std()

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f"<div class='metric-card'><h3>Mean</h3><h2>{round(mean,2)}</h2></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='metric-card'><h3>Median</h3><h2>{round(median,2)}</h2></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='metric-card'><h3>Std Dev</h3><h2>{round(std,2)}</h2></div>", unsafe_allow_html=True)

        # -------------------- GRAPH EXPLANATION --------------------
        st.subheader("🧾 Graph Explanation")

        if graph_type == "Line Chart":
            st.write("This graph shows trends over continuous data.")
        else:
            st.write("This graph compares discrete values.")

        # -------------------- INSIGHTS --------------------
        st.subheader("🧠 Insights")

        if mean > median:
            st.info("Data is right-skewed (higher values dominate)")
        else:
            st.info("Data is left-skewed (lower values dominate)")

        # -------------------- PROBLEM PREDICTION --------------------
        st.subheader("⚠️ Problem Prediction")

        if df[col].max() > mean * 2:
            st.error("Possible outliers detected → may affect analysis")

        if std > mean:
            st.warning("High variance → unstable data")

        # -------------------- SUGGESTIONS --------------------
        st.subheader("💡 Suggestions")

        st.write("• Consider removing outliers")
        st.write("• Normalize data for better comparison")
        st.write("• Use smoothing techniques for trends")

        # -------------------- ALTERNATIVE APPROACH --------------------
        st.subheader("🔄 Alternative Approach")

        st.write("• Try using moving average for better trend analysis")
        st.write("• Use histogram for distribution understanding")
        st.write("• Apply ML models for prediction")

        # -------------------- GRAPHICAL vs STATISTICAL --------------------
        st.subheader("📊 Graphical vs Statistical")

        st.write("Graphical: Visual trends using charts")
        st.write("Statistical: Mean, median, variance analysis")

        # -------------------- AUTOMATION --------------------
        st.subheader("⚡ Automation")

        st.success("Pipeline fully automated: input → analysis → insights → recommendations")

    else:
        st.error("❌ No numeric data found")

else:
    st.info("Upload a CSV file to begin")
