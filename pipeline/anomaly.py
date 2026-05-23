def detect_anomalies(df):

    anomalies = []

    # age
    if "age" in df.columns:

        bad = df[
            (df["age"] < 18) |
            (df["age"] > 65)
        ]

        anomalies.extend(
            bad.index.tolist()
        )

    # salary
    if "salary" in df.columns:

        bad = df[
            df["salary"] < 0
        ]

        anomalies.extend(
            bad.index.tolist()
        )

    # experience logic
    if (
        "experience" in df.columns and
        "age" in df.columns
    ):

        bad = df[
            df["experience"] >
            (df["age"] - 18)
        ]

        anomalies.extend(
            bad.index.tolist()
        )

    return list(set(anomalies))