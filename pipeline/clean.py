import pandas as pd
import numpy as np

def strict_clean(df):

    df = df.copy()

    # lowercase columns
    df.columns = [
        c.lower().strip()
        for c in df.columns
    ]

    # garbage values
    garbage = [
        "not_set",
        "abc",
        "null",
        "",
        " ",
        "NaN",
        "nan",
        "NONE",
        "N/A",
        "missing",
        "error"
    ]

    df = df.replace(garbage, np.nan)

    # -------------------------
    # EXPERIENCE MAP
    # -------------------------
    exp_map = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "thirty": 30
    }

    if "experience" in df.columns:

        df["experience"] = (
            df["experience"]
            .replace(exp_map)
        )

    # -------------------------
    # NUMERIC CONVERSION
    # -------------------------
    numeric_cols = [
        "age",
        "salary",
        "experience",
        "performance_score"
    ]

    for col in numeric_cols:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # -------------------------
    # DATE CLEANING
    # -------------------------
    if "join_date" in df.columns:

        df["join_date"] = (
            df["join_date"]
            .astype(str)
            .str.strip()
            .str.replace("/", "-", regex=False)
        )

        df["join_date"] = pd.to_datetime(
            df["join_date"],
            errors="coerce",
            format="mixed"
        )

    return df