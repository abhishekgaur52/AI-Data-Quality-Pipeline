from sklearn.ensemble import RandomForestRegressor
import pandas as pd

def ml_impute(df, target):
    df = df.copy()

    # HARD CHECK
    if target not in df.columns:
        return df

    # ensure numeric
    df[target] = pd.to_numeric(df[target], errors="coerce")

    train = df[df[target].notnull()]
    test = df[df[target].isnull()]

    if len(train) < 3 or len(test) == 0:
        return df  # ❌ prevents fake training

    X_train = train.drop(columns=[target])
    X_test = test.drop(columns=[target])
    y_train = train[target]

    # encode
    X_train = pd.get_dummies(X_train)
    X_test = pd.get_dummies(X_test)
    X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    # inject predictions
    df.loc[df[target].isnull(), target] = preds

    return df