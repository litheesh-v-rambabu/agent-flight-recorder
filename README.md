---
title: Agent Flight Recorder
emoji: "🛩️"
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: "1.37.1"
app_file: app.py
pinned: false
license: mit
---

# Agent Flight Recorder — Failure Analysis & Regression Testing for LLM Agents

> **Demo / sample data notice:** This is a scaled-down public reproduction. All traces in
> `data/` and in the live app are **synthetic demo data** generated deterministically
> (`scripts/generate_data.py`, seed 42). No production traces are included.

## Why
LLM agents fail silently: a run returns a plausible answer while a tool call, retrieval
step, or intermediate LLM call quietly broke. Without a trace you cannot tell *which*
step failed, whether a new model/prompt version regressed, or reproduce the failure.

## How (architecture from the original project)
- **Recorder:** every LLM and tool call is recorded as a structured span in SQLite
  (`src/recorder.py`) — run id, task id, step type, latency, status, error text.
- **Service + dashboard:** FastAPI-style service layer + Streamlit dashboard (`app.py`).
- **Failure detection (`src/scoring.py`):** rule-based checks (timeouts, empty tool
  results, schema errors) + an LLM-as-judge-*style* scorer. In this public demo the
  judge is a **local heuristic scoring function — no paid API key is used** — and is
  labelled as such in code and UI.
- **Clustering (`src/clustering.py`):** failures are grouped so recurring failure modes
  surface. The original used sentence-transformers embeddings + HDBSCAN/UMAP; this
  light HF-Spaces reproduction uses TF-IDF vectors + k-means (numpy) as a fallback
  with the same interface, so it installs on free CPU.
- **Regression testing (`src/regression.py`):** failed traces become test cases;
  agent versions are compared with Wilson score intervals and McNemar's test, with a
  **CI gate blocking pass-rate drops beyond 7 points**.

## Reported results (original project, from resume)
- Traced **~700 runs across 120 tasks**
- Failure detection: **0.76 precision / 0.56 recall** against 100 hand-labelled failures
  on a frozen held-out test split
- CI gate: blocks pass-rate drops **> 7 points**

These are the original project's reported results. Demo-data metrics shown in the app
are computed on synthetic data and are labelled separately.

## Run locally
```bash
pip install -r requirements.txt
python scripts/generate_data.py   # creates data/demo_traces.csv (700 runs, 120 tasks)
streamlit run app.py
pytest -q
```

## Layout
`app.py` Streamlit entry · `src/` recorder/scoring/clustering/regression ·
`scripts/generate_data.py` · `tests/` pytest (stats + recorder)
