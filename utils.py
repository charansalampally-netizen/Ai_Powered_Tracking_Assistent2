import pandas as pd


# --------------------------------------------------
# Load CSV
# --------------------------------------------------

def load_assets():

    df = pd.read_csv("assets1.csv")

    df["Last Seen"] = pd.to_datetime(df["Last Seen"])

    df["Next Maintenance"] = pd.to_datetime(df["Next Maintenance"])

    return df


# --------------------------------------------------
# Asset Lookup
# --------------------------------------------------

def get_asset_by_id(df, asset_id):

    return df[
        df["ID"].str.upper() == asset_id.upper()
    ]


def get_asset_by_name(df, asset_name):

    return df[
        df["Asset Name"]
        .str.lower()
        .str.contains(asset_name.lower(), na=False)
    ]


# --------------------------------------------------
# Status Functions
# --------------------------------------------------

def active_assets(df):

    return df[
        df["Status"].str.lower() == "active"
    ]


def inactive_assets(df):

    return df[
        df["Status"].str.lower() == "inactive"
    ]


# --------------------------------------------------
# Maintenance
# --------------------------------------------------

def assets_due_for_maintenance(df):

    today = pd.Timestamp.today()

    return df[
        df["Next Maintenance"] <= today
    ]


# --------------------------------------------------
# Department
# --------------------------------------------------

def assets_in_department(df, department):

    return df[
        df["Department"]
        .str.lower()
        == department.lower()
    ]


# --------------------------------------------------
# Location
# --------------------------------------------------

def assets_in_location(df, location):

    return df[
        df["Location"]
        .str.lower()
        .str.contains(location.lower(), na=False)
    ]


# --------------------------------------------------
# Last Seen
# --------------------------------------------------

def assets_not_seen_recently(df):

    cutoff = pd.Timestamp.today() - pd.Timedelta(days=30)

    return df[
        df["Last Seen"] < cutoff
    ]


# --------------------------------------------------
# Main Question Handler
# --------------------------------------------------

def process_question(df, question):

    question = question.lower().strip()

    # ---------------------------------------------
    # Where is asset A001?
    # ---------------------------------------------

    if "where is asset" in question:

        words = question.upper().split()

        asset_id = None

        for word in words:

            if word.startswith("A"):

                asset_id = word.replace("?", "")

                break

        if asset_id:

            asset = get_asset_by_id(df, asset_id)

            if asset.empty:

                return "I couldn't find that asset."

            row = asset.iloc[0]

            return (
                f"{row['Asset Name']} ({row['ID']}) "
                f"is located in {row['Location']}."
            )

    # ---------------------------------------------
    # Where is the Dell Laptop?
    # ---------------------------------------------

    if "where is the" in question:

        asset_name = (
            question
            .replace("where is the", "")
            .replace("?", "")
            .strip()
        )

        asset = get_asset_by_name(df, asset_name)

        if asset.empty:

            return "I couldn't find that asset."

        row = asset.iloc[0]

        return (
            f"{row['Asset Name']} ({row['ID']}) "
            f"is located in {row['Location']}."
        )

    # ---------------------------------------------
    # Maintenance
    # ---------------------------------------------

    if "maintenance" in question:

        results = assets_due_for_maintenance(df)

        if results.empty:

            return "No assets currently have overdue maintenance."

        return results

    # ---------------------------------------------
    # Active
    # ---------------------------------------------

    if "active" in question:

        return active_assets(df)

    # ---------------------------------------------
    # Inactive
    # ---------------------------------------------

    if "inactive" in question:

        return inactive_assets(df)

    # ---------------------------------------------
    # Not Seen Recently
    # ---------------------------------------------

    if (
        "not been seen" in question
        or "recently" in question
        or "last seen" in question
    ):

        return assets_not_seen_recently(df)

    # ---------------------------------------------
    # Department Search
    # ---------------------------------------------

    departments = df["Department"].dropna().unique()

    for department in departments:

        if department.lower() in question:

            return assets_in_department(df, department)

    # ---------------------------------------------
    # Location Search
    # ---------------------------------------------

    locations = df["Location"].dropna().unique()

    for location in locations:

        if location.lower() in question:

            return assets_in_location(df, location)

    # ---------------------------------------------
    # Asset Name Search
    # ---------------------------------------------

    asset = get_asset_by_name(df, question)

    if not asset.empty:

        return asset

    # ---------------------------------------------
    # Unknown Question
    # ---------------------------------------------

    return (
        "Sorry, I couldn't understand your question.\n\n"
        "Try asking:\n"
        "• Where is asset A001?\n"
        "• Where is the Dell Laptop?\n"
        "• Show maintenance due assets\n"
        "• Show all active assets\n"
        "• Show assets in Finance\n"
        "• Which assets have not been seen recently?"
    )

