import pandas as pd
import numpy as np

def enforce_rules(df):

    df = df.copy()

    # -------------------------
    # AGE
    # -------------------------
    if "age" in df.columns:

        df.loc[
            (df["age"] < 18) |
            (df["age"] > 65),
            "age"
        ] = np.nan

        df["age"] = (
            df["age"]
            .fillna(df["age"].median())
            .round(0)
        )

    # -------------------------
    # SALARY
    # -------------------------
    if "salary" in df.columns:

        df.loc[
            df["salary"] <= 0,
            "salary"
        ] = np.nan

        q1 = df["salary"].quantile(0.25)
        q3 = df["salary"].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        df["salary"] = (
            df["salary"]
            .clip(lower, upper)
        )

        df["salary"] = (
            df["salary"]
            .fillna(df["salary"].median())
            .round(0)
        )

    # -------------------------
    # EXPERIENCE
    # -------------------------
    if "experience" in df.columns:

        df.loc[
            df["experience"] < 0,
            "experience"
        ] = np.nan

        if "age" in df.columns:

            df.loc[
                df["experience"] >
                (df["age"] - 18),
                "experience"
            ] = np.nan

        df["experience"] = (
            df["experience"]
            .fillna(df["experience"].median())
            .round(0)
        )

    # -------------------------
    # PERFORMANCE SCORE
    # -------------------------
    if "performance_score" in df.columns:

        mapping = {
            "poor": 0.3,
            "average": 0.5,
            "good": 0.7,
            "excellent": 0.9
        }

        df["performance_score"] = (
            df["performance_score"]
            .replace(mapping)
        )

        df["performance_score"] = pd.to_numeric(
            df["performance_score"],
            errors="coerce"
        )

        df["performance_score"] = (
            df["performance_score"]
            .clip(0, 1)
        )

        df["performance_score"] = (
            df["performance_score"]
            .fillna(
                df["performance_score"].median()
            )
            .round(2)
        )

    # -------------------------
    # DEPARTMENT
    # -------------------------
    if "department" in df.columns:

        valid = [
            "HR",
            "Engineering",
            "Sales",
            "Finance",
            "Management",
            "Intern"
        ]

        df.loc[
            ~df["department"].isin(valid),
            "department"
        ] = np.nan

        df["department"] = (
            df["department"]
            .fillna(
                df["department"].mode()[0]
            )
        )

    # -------------------------
    # LOCATION
    # -------------------------
    if "location" in df.columns:

        df["location"] = (
            df["location"]
            .fillna(
                df["location"].mode()[0]
            )
        )

    # -------------------------
    # DATE IMPUTATION
    # -------------------------
    if "join_date" in df.columns:

        df["join_date"] = (
            df.groupby("department")[
                "join_date"
            ].transform(
                lambda x:
                x.fillna(
                    x.mode()[0]
                    if not x.mode().empty
                    else pd.NaT
                )
            )
        )

    # -------------------------
    # REMOVE DUPLICATES
    # -------------------------
    df = df.drop_duplicates()

    return df