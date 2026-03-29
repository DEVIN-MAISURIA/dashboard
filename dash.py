import streamlit as st
import pandas as pd
import numpy as np
import time

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Advanced Live Dashboard", layout="wide")

# -------------------- TITLE --------------------
st.title("📊 Advanced LIVE Dashboard")

# -------------------- SIDEBAR --------------------
st.sidebar.header("Settings")

num_rows = st.sidebar.slider("Select number of rows", 10, 200, 50)
show_data = st.sidebar.checkbox("Show Raw Data")

# -------------------- AUTO REFRESH --------------------
REFRESH_INTERVAL = 2  # seconds

# -------------------- GENERATE DATA --------------------
@st.cache_data(ttl=2)
def generate_data(n):
    df = pd.DataFrame({
        "Time": pd.date_range(end=pd.Timestamp.now(), periods=n, freq="s"),
        "Sales": np.random.randint(50, 200, n),
        "Profit": np.random.randint(10, 100, n),
        "Users": np.random.randint(100, 1000, n)
    })
    return df

data = generate_data(num_rows)

# -------------------- METRICS --------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", int(data["Sales"].sum()))
col2.metric("Total Profit", int(data["Profit"].sum()))
col3.metric("Active Users", int(data["Users"].mean()))

# -------------------- CHARTS --------------------
st.subheader("📈 Live Trends")

col1, col2 = st.columns(2)

with col1:
    st.line_chart(data.set_index("Time")[["Sales", "Profit"]])

with col2:
    st.bar_chart(data.set_index("Time")[["Users"]])

# -------------------- DATA TABLE --------------------
if show_data:
    st.subheader("📄 Raw Data")
    st.dataframe(data, use_container_width=True)

# -------------------- AUTO REFRESH --------------------
time.sleep(REFRESH_INTERVAL)
st.rerun()
