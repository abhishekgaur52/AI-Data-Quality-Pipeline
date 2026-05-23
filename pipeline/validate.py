def validate_data(df):
    return {
        "missing": df.isnull().sum().to_dict(),
        "duplicates": int(df.duplicated().sum())
    }