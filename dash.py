import streamlit as st
import pandas as pd
import numpy as np

# -------------------- CONFIG --------------------
st.set_page_config(page_title="LLM Data Analyzer", layout="wide")

st.title("🤖 Intelligent CSV Analyzer (LLM Style)")

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

        st.write(f"✅ Selected Graph: **{graph_type}** (based on data distribution)")

        # -------------------- STATISTICS --------------------
        st.subheader("📈 Statistical Analysis")

        mean = df[col].mean()
        median = df[col].median()
        std = df[col].std()

        col1, col2, col3 = st.columns(3)
        col1.metric("Mean", round(mean, 2))
        col2.metric("Median", round(median, 2))
        col3.metric("Std Dev", round(std, 2))

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

        st.success("All steps are automated: input → processing → analysis → insights → suggestions")

    else:
        st.error("❌ No numeric data found")

else:
    st.info("Upload a CSV file to begin")
