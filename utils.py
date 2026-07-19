from pathlib import Path

import pandas as pd


def load_assets() -> pd.DataFrame:
    base_dir = Path(__file__).resolve().parent
    csv_path = base_dir / "assets.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"Asset file not found: {csv_path}")

    df = pd.read_csv(csv_path, parse_dates=["Last Maintenance", "Next Maintenance"])
    df["Status"] = df["Status"].fillna("Unknown")
    return df


def active_assets(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["Status"].str.lower() == "active"]


def inactive_assets(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["Status"].str.lower() == "inactive"]


def assets_due_for_maintenance(df: pd.DataFrame) -> pd.DataFrame:
    today = pd.Timestamp.today().normalize()
    return df[df["Next Maintenance"] <= today]


def assets_not_seen_recently(df: pd.DataFrame, days: int = 30) -> pd.DataFrame:
    cutoff = pd.Timestamp.today().normalize() - pd.Timedelta(days=days)
    return df[df["Last Maintenance"] < cutoff]


def find_asset_by_id(df: pd.DataFrame, asset_id: str) -> pd.DataFrame:
    return df[df["ID"].str.upper() == asset_id.upper()]


def find_assets_by_name(df: pd.DataFrame, asset_name: str) -> pd.DataFrame:
    return df[df["Asset Name"].str.contains(asset_name, case=False, na=False)]


def find_assets_by_department(df: pd.DataFrame, department: str) -> pd.DataFrame:
    return df[df["Department"].str.lower() == department.lower()]


def find_assets_by_location(df: pd.DataFrame, location: str) -> pd.DataFrame:
    return df[df["Location"].str.contains(location, case=False, na=False)]


def query_assets(df: pd.DataFrame, question: str):
    question_text = question.strip().lower()

    if not question_text:
        return "Please ask a question about the assets."

    if "where is asset" in question_text:
        asset_id = question_text.replace("where is asset", "").replace("?", "").strip().upper()
        if asset_id:
            result = find_asset_by_id(df, asset_id)
            if result.empty:
                return f"I could not find asset {asset_id}."
            row = result.iloc[0]
            return f"{row['Asset Name']} ({row['ID']}) is located in {row['Location']}."

    if question_text.startswith("where is") or question_text.startswith("find"):
        candidate = question_text.replace("where is", "").replace("find", "").replace("?", "").strip()
        if candidate:
            result = find_assets_by_name(df, candidate)
            if not result.empty:
                row = result.iloc[0]
                return f"{row['Asset Name']} ({row['ID']}) is located in {row['Location']}."

    if "maintenance" in question_text:
        result = assets_due_for_maintenance(df)
        if result.empty:
            return "No assets are currently due for maintenance."
        return result

    if "inactive" in question_text:
        result = inactive_assets(df)
        if result.empty:
            return "No inactive assets were found."
        return result

    if "active" in question_text:
        result = active_assets(df)
        if result.empty:
            return "No active assets were found."
        return result

    if "not been seen" in question_text or "not seen" in question_text or "last seen" in question_text or "seen in" in question_text:
        result = assets_not_seen_recently(df)
        if result.empty:
            return "All assets have been seen in the last 30 days."
        return result

    departments = df["Department"].dropna().unique()
    for department in departments:
        if department.lower() in question_text:
            result = find_assets_by_department(df, department)
            if not result.empty:
                return result

    locations = df["Location"].dropna().unique()
    for location in locations:
        if location.lower() in question_text:
            result = find_assets_by_location(df, location)
            if not result.empty:
                return result

    result = find_assets_by_name(df, question_text)
    if not result.empty:
        return result

    return (
        "I couldn't understand that request. Try questions like:\n"
        "- Where is asset A001?\n"
        "- Show maintenance due assets.\n"
        "- List inactive assets.\n"
        "- Show assets in Finance.\n"
        "- Which assets have not been seen in 30 days?"
    )
