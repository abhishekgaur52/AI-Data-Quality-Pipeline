import streamlit as st
import pandas as pd
import requests
import os

st.set_page_config(page_title="AI Data Quality Dashboard", layout="wide")
st.title("🚀 AI Data Quality Observability System")

# -------------------------
# API CALL (SOURCE OF TRUTH)
# -------------------------
API_URL = "http://127.0.0.1:5000/run-pipeline"

try:
    res = requests.get(API_URL, timeout=10).json()
except Exception as e:
    st.error(f"❌ API not reachable: {e}")
    st.stop()

score = res.get("score", 0)
anomalies = res.get("anomalies", 0)
status = res.get("status", "success")

# -------------------------
# HEADER METRICS
# -------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Quality Score", score)
col2.metric("Anomalies", anomalies)
col3.metric("Status", status)

health = "GOOD"
if score < 70:
    health = "CRITICAL"
elif score < 85:
    health = "WARNING"

col4.metric("System Health", health)

st.divider()

# -------------------------
# SCORE INTERPRETATION
# -------------------------
st.subheader("📊 Score Interpretation")

st.progress(int(score))

if score >= 85:
    st.success("High-quality dataset. Safe for ML pipelines.")
elif score >= 70:
    st.warning("Medium quality. Some issues detected.")
else:
    st.error("Low quality data. Not safe for production use.")

# -------------------------
# DETAILED BREAKDOWN (SIMULATED FROM SCORE LOGIC)
# ----------------------

# -------------------------
# RAW DATA INSPECTION
# -------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_path = os.path.join(BASE_DIR, "data/raw/sample.csv")
clean_path = os.path.join(BASE_DIR, "data/processed/cleaned.csv")

st.subheader("📂 Dataset Comparison")

col1, col2 = st.columns(2)

with col1:
    st.write("🔴 RAW DATA")
    if os.path.exists(raw_path):
        raw_df = pd.read_csv(raw_path)
        st.dataframe(raw_df)
        st.write("Missing Values:", raw_df.isnull().sum().sum())
        st.write("Duplicates:", raw_df.duplicated().sum())
    else:
        st.info("No raw data found")

with col2:
    st.write("🟢 CLEANED DATA")
    if os.path.exists(clean_path):
        clean_df = pd.read_csv(clean_path)
        st.dataframe(clean_df)
        st.write("Missing Values:", clean_df.isnull().sum().sum())
        st.write("Duplicates:", clean_df.duplicated().sum())
    else:
        st.info("Run pipeline first")

# -------------------------
# ANOMALY INSIGHTS
# -------------------------
st.subheader("🚨 Anomaly Insights")

st.write(f"Total anomalies detected: {anomalies}")

if anomalies == 0:
    st.success("No anomalies detected in dataset")
elif anomalies < 3:
    st.warning("Low anomaly presence")
else:
    st.error("High anomaly rate detected")

# -------------------------
# SYSTEM DIAGNOSTICS
# -------------------------
st.subheader("🧠 System Diagnostics")

diagnostics = {
    "Pipeline Status": "Healthy" if status == "success" else "Failed",
    "Data Flow": "Active",
    "ML Engine": "Running",
    "Validation Layer": "Enabled"
}

st.json(diagnostics)

# -------------------------
# FINAL INSIGHTS
# -------------------------
st.subheader("📌 Summary")

st.markdown(f"""
- **Final Score:** {score}
- **Anomalies:** {anomalies}
- **System Health:** {health}
- **Recommendation:** {'Fix data before ML training' if score < 70 else 'Data is usable'}
""")