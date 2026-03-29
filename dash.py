import streamlit as st
import pandas as pd
import numpy as np
import time   # ✅ used instead of streamlit_autorefresh

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Advanced Live Dashboard", layout="wide")

# -------------------- AUTO REFRESH (NO ERROR VERSION) --------------------
time.sleep(1)
st.rerun()

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.metric-card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 0px 15px rgba(0,255,204,0.2);
    transition: 0.3s;
}
.metric-card:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 25px rgba(0,255,204,0.6);
}
.metric-title {
    font-size: 18px;
    color: #aaa;
}
.metric-value {
    font-size: 35px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.markdown(
    "<h1 style='text-align:center; color:#00ffcc;'>⚡ Live System Dashboard</h1>",
    unsafe_allow_html=True
)

# -------------------- SESSION STATE --------------------
if "data" not in st.session_state or not isinstance(st.session_state.data, list):
    st.session_state.data = np.random.randint(50, 100, 20).tolist()

# -------------------- GENERATE NEW VALUE --------------------
new_value = np.random.randint(50, 100)

# SAFE UPDATE (NO CRASH)
if len(st.session_state.data) >= 20:
    st.session_state.data.pop(0)

st.session_state.data.append(new_value)

# -------------------- METRICS (RIBBON STYLE) --------------------
col1, col2, col3 = st.columns(3)

def metric_card(title, value, color):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value" style="color:{color}">{value}</div>
    </div>
    """, unsafe_allow_html=True)

with col1:
    metric_card("Load", new_value, "#00ffcc")

with col2:
    metric_card("Temperature (°C)", np.random.randint(20, 40), "#ffcc00")

with col3:
    metric_card("Pressure", np.random.randint(70, 120), "#ff4d4d")

st.markdown("---")

# -------------------- GRAPH (FIXED WINDOW, NO SCROLL) --------------------
chart_placeholder = st.empty()

df = pd.DataFrame({
    "Time": list(range(len(st.session_state.data))),
    "Load": st.session_state.data
})

with chart_placeholder:
    st.line_chart(df.set_index("Time"))

# -------------------- STATUS --------------------
if new_value > 90:
    st.error("🔴 Critical Condition")
elif new_value > 75:
    st.warning("🟡 High Load")
else:
    st.success("🟢 System Stable")
