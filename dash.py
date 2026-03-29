import streamlit as st
import pandas as pd
import numpy as np

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="AI CSV Dashboard", layout="wide")

st.title("🤖 AI-Powered CSV Dashboard")

# -------------------- MODE SELECTION --------------------
mode = st.sidebar.radio("Select Mode", ["📊 Dashboard", "🧠 AI Insights"])

# -------------------- FILE UPLOAD --------------------
file = st.file_uploader("Upload your CSV file", type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    st.success("File uploaded successfully!")

    # -------------------- DASHBOARD MODE --------------------
    if mode == "📊 Dashboard":

        st.subheader("📄 Data Preview")
        st.dataframe(df, use_container_width=True)

        st.subheader("📊 Summary Statistics")
        st.write(df.describe())

        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

        if numeric_cols:
            col = st.selectbox("Select column", numeric_cols)

            col1, col2, col3 = st.columns(3)
            col1.metric("Mean", round(df[col].mean(), 2))
            col2.metric("Max", df[col].max())
            col3.metric("Min", df[col].min())

            st.subheader("📈 Chart")
            st.line_chart(df[col])

        else:
            st.error("No numeric columns found")

    # -------------------- AI INSIGHTS MODE --------------------
    elif mode == "🧠 AI Insights":

        st.subheader("🤖 Smart Insights")

        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

        if numeric_cols:
            insights = []

            for col in numeric_cols:
                mean = df[col].mean()
                median = df[col].median()
                max_val = df[col].max()
                min_val = df[col].min()

                # Insight 1: skewness
                if mean > median:
                    insights.append(f"📌 '{col}' is right-skewed (higher values dominate)")
                else:
                    insights.append(f"📌 '{col}' is left-skewed (lower values dominate)")

                # Insight 2: outlier detection
                if max_val > mean * 2:
                    insights.append(f"⚠️ '{col}' may contain outliers")

                # Insight 3: range analysis
                if max_val - min_val > mean:
                    insights.append(f"📊 '{col}' has high variation")

            # Display insights
            for i in insights:
                st.write(i)

            # -------------------- SUGGESTIONS --------------------
            st.subheader("💡 AI Suggestions")

            st.write("• Consider removing outliers for better accuracy")
            st.write("• Normalize data if variation is high")
            st.write("• Use visualization to detect trends")
            st.write("• Focus on columns with high impact")

        else:
            st.error("No numeric data available for AI analysis")

else:
    st.info("Please upload a CSV file to begin")
