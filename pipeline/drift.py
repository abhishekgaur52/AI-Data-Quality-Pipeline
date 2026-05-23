import json
import os

SCHEMA_FILE = "config/schema.json"

def detect_schema_drift(df):

    schema = {
    c.lower(): str(t)
    for c, t in df.dtypes.items()
}
    os.makedirs(
        "config",
        exist_ok=True
    )

    if not os.path.exists(
        SCHEMA_FILE
    ):

        with open(
            SCHEMA_FILE,
            "w"
        ) as f:

            json.dump(
                schema,
                f,
                indent=4
            )

        return []

    with open(
        SCHEMA_FILE
    ) as f:

        old = json.load(f)

    drift = []

    # new columns
    for col in schema:

        if col not in old:

            drift.append(
                f"New column: {col}"
            )

    # removed columns
    for col in old:

        if col not in schema:

            drift.append(
                f"Removed column: {col}"
            )

    # datatype changes
    for col in schema:

        if col in old:

            if schema[col] != old[col]:

                drift.append(
                    f"Type changed: {col}"
                )

    return drift