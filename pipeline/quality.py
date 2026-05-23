def calculate_quality_score(
    df,
    anomalies=0,
    drift=0
):

    total = df.size

    missing = (
        df.isnull()
        .sum()
        .sum()
    )

    missing_ratio = (
        missing / total
    )

    anomaly_ratio = (
        anomalies / len(df)
    )

    score = 100

    score -= (
        missing_ratio * 50
    )

    score -= (
        anomaly_ratio * 30
    )

    score -= drift * 5

    return round(
        max(score, 0),
        2
    )