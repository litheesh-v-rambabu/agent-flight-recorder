"""Agent Flight Recorder — Streamlit dashboard (HF Spaces entry point).
Demo/sample data only: traces are synthetic (seed 42). Reported project results
(0.76 precision / 0.56 recall) are from the original project — see README."""
import pathlib, subprocess, sys
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Agent Flight Recorder", layout="wide")
st.title("🛩️ Agent Flight Recorder")
st.caption("DEMO — synthetic sample traces only. Failure analysis & regression testing for LLM agents that fail silently.")

data_path = pathlib.Path(__file__).parent/"data"/"demo_traces.csv"
if not data_path.exists():
    subprocess.run([sys.executable, str(pathlib.Path(__file__).parent/"scripts"/"generate_data.py")], check=False)
df = pd.read_csv(data_path) if data_path.exists() else pd.DataFrame()

c1,c2,c3,c4 = st.columns(4)
c1.metric("Demo runs (synthetic)", len(df))
c2.metric("Demo tasks", df["task_id"].nunique() if len(df) else 0)
c3.metric("Demo failed runs", int((df["status"]!="ok").sum()) if len(df) else 0)
c4.metric("Reported detection (original)", "0.76 P / 0.56 R")
st.subheader("Why this exists")
st.write("LLM agents fail silently — a tool call breaks but the final answer still looks plausible. "
         "This recorder captures every LLM/tool call as a structured span, groups failures, and turns "
         "failed traces into regression tests with a CI gate (Wilson intervals + McNemar, >7pt drop blocked).")
if len(df):
    st.subheader("Failure modes in demo data")
    st.bar_chart(df[df["error"].fillna("")!="" ]["error"].value_counts())
    st.subheader("Sample traces (demo)")
    st.dataframe(df.head(50), use_container_width=True)
