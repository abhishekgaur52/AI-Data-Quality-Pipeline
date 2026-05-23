import pandas as pd

from sklearn.ensemble import (
    RandomForestRegressor
)

def repair_data(df):

    df = df.copy()

    report = {}

    num_cols = df.select_dtypes(
        include=["float64", "int64"]
    ).columns

    for col in num_cols:

        if df[col].isnull().sum() == 0:
            continue

        train = df[df[col].notnull()]
        test = df[df[col].isnull()]

        if len(train) < 5:

            df[col] = df[col].fillna(
                df[col].median()
            )

            report[col] = (
                "median fallback"
            )

            continue

        features = [
            c for c in df.columns
            if c != col
        ]

        X_train = train[features]
        X_test = test[features]

        # datetime split
        for dfx in [X_train, X_test]:

            date_cols = dfx.select_dtypes(
                include=["datetime64[ns]"]
            ).columns

            for c in date_cols:

                dfx[c+"_year"] = (
                    dfx[c].dt.year
                )

                dfx[c+"_month"] = (
                    dfx[c].dt.month
                )

                dfx[c+"_day"] = (
                    dfx[c].dt.day
                )

                dfx.drop(
                    columns=[c],
                    inplace=True
                )

        X_train = pd.get_dummies(
            X_train
        )

        X_test = pd.get_dummies(
            X_test
        )

        X_test = X_test.reindex(
            columns=X_train.columns,
            fill_value=0
        )

        X_train = (
            X_train
            .astype(float)
            .fillna(0)
        )

        X_test = (
            X_test
            .astype(float)
            .fillna(0)
        )

        model = RandomForestRegressor(
            n_estimators=50,
            random_state=42
        )

        model.fit(
            X_train,
            train[col]
        )

        preds = model.predict(X_test)

        df.loc[
            df[col].isnull(),
            col
        ] = preds

        report[col] = "ML imputed"

    return df, report