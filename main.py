import os
from datetime import datetime

from pipeline.ingest import load_data
from pipeline.clean import strict_clean
from pipeline.postprocess import enforce_rules
from pipeline.repair import repair_data
from pipeline.anomaly import detect_anomalies
from pipeline.drift import detect_schema_drift
from pipeline.quality import calculate_quality_score
from pipeline.utils import log


def run_pipeline():

    log("Loading data")
    df = load_data("data/raw/sample.csv")

    log("Cleaning")
    df = strict_clean(df)

    log("Rules")
    df = enforce_rules(df)

    log("Anomalies (before repair)")
    raw_anomalies = detect_anomalies(df)

    log("Repairing")
    df, report = repair_data(df)

    log("Final anomaly check")
    final_anomalies = detect_anomalies(df)

    drift = detect_schema_drift(df)

    score = calculate_quality_score(
        df,
        len(final_anomalies),
        len(drift)
    )

    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("data/version", exist_ok=True)

    df.to_csv("data/processed/cleaned.csv", index=False)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    df.to_csv(f"data/version/cleaned_{ts}.csv", index=False)

    print("\nREPORT:", report)
    print("RAW ANOMALIES:", len(raw_anomalies))
    print("FINAL ANOMALIES:", len(final_anomalies))
    print("DRIFT:", drift)
    print("QUALITY SCORE:", score)

    return {
        "score": score,
        "raw_anomalies": len(raw_anomalies),
        "final_anomalies": len(final_anomalies),
        "drift": len(drift)
    }


if __name__ == "__main__":
    run_pipeline()