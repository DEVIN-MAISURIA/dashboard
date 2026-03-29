import streamlit as st
import pandas as pd
import numpy as np

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="CSV Live Dashboard", layout="wide")

st.title("📊 CSV Live Dashboard with Insights")

# -------------------- FILE UPLOAD --------------------
file = st.file_uploader("Upload your CSV file", type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    st.success("File uploaded successfully!")

    # -------------------- SHOW DATA --------------------
    st.subheader("📄 Data Preview")
    st.dataframe(df, use_container_width=True)

    # -------------------- BASIC INFO --------------------
    st.subheader("📊 Summary Statistics")
    st.write(df.describe())

    # -------------------- COLUMN SELECTION --------------------
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if numeric_cols:
        col = st.selectbox("Select column for analysis", numeric_cols)

        # -------------------- METRICS --------------------
        col1, col2, col3 = st.columns(3)

        col1.metric("Mean", round(df[col].mean(), 2))
        col2.metric("Max", df[col].max())
        col3.metric("Min", df[col].min())

        # -------------------- CHART --------------------
        st.subheader("📈 Visualization")
        st.line_chart(df[col])

        # -------------------- SIMPLE INSIGHTS --------------------
        st.subheader("🧠 Insights")

        if df[col].mean() > df[col].median():
            st.info("Data is slightly right-skewed (higher values dominate)")
        else:
            st.info("Data is slightly left-skewed (lower values dominate)")

        if df[col].max() > df[col].mean() * 2:
            st.warning("Possible outliers detected")

    else:
        st.error("No numeric columns found in the dataset")

else:
    st.info("Please upload a CSV file to start")
