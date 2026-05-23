#  AI Data Quality Pipeline

End-to-end data quality pipeline using Flask + ML + Streamlit with optional n8n automation.

---

#  Overview

This project processes raw messy datasets and converts them into clean, validated, ML-ready data while providing:

- Data cleaning pipeline
- ML-based missing value repair
- Anomaly detection
- Schema drift detection
- Data quality scoring system
- Streamlit dashboard for visualization
- Flask API backend
- n8n automation support (optional email alerts)

---

#  Architecture

Raw Data → Flask API → Cleaning → Rules → ML Repair → Analysis → Quality Score → Streamlit Dashboard

---

#  Features

## Data Pipeline
- Strict data cleaning
- Type normalization
- Garbage value handling
- Missing value handling

## ML Repair
- RandomForest-based imputation
- Median fallback safety

## Anomaly Detection
- Age validation (18–65)
- Salary validation (no negatives)
- Experience logic check

## Schema Drift Detection
- New columns detection
- Removed columns tracking
- Type change detection

## Quality Score
- Missing value penalty
- Anomaly penalty
- Drift penalty

Score Range:
- 85–100 → Good
- 70–85 → Medium
- <70 → Bad


#  Project Structure
AI_Data_Quality_Pipeline/
│
├── app.py                          # Flask API entrypoint (runs pipeline)
├── streamlit_app.py               # Streamlit dashboard UI
├── requirements.txt               # Dependencies
│
├── pipeline/                      # Core data pipeline logic
│   ├── __init__.py
│   ├── ingest.py                  # Load data
│   ├── clean.py                   # Strict cleaning (type fixing, garbage removal)
│   ├── rules.py                   # Business rules enforcement
│   ├── repair.py                  # ML-based imputation (RandomForest)
│   ├── anomaly.py                # Anomaly detection (Isolation Forest / rules)
│   ├── drift.py                  # Schema drift detection
│   ├── quality.py                # Quality score calculation
│   └── logger.py                 # Logging utility
│
├── config/
│   └── schema.json               # Stored schema baseline for drift detection
│
├── data/
│   ├── raw/
│   │   ├── sample.csv            # Input datasets
│   │
│   ├── processed/
│   │   └── cleaned.csv           # Final cleaned output
│   │
│   └── version/                  # Historical versions (optional)
│
├── logs/
│   └── pipeline.log              # System logs
│
└── README.md                     # Project documentation

---

## API Response

{
  "status": "success",
  "quality_score": 92,
  "raw_anomalies": 2,
  "final_anomalies": 1,
  "drift": [],
  "report": {}
}
