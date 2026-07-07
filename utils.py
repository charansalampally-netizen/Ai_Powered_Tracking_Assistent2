import pandas as pd


def load_assets():

    df = pd.read_csv("assets1.csv")
    return df


def search_assets(df, question):

    question = question.lower()

    matches = df[
        df.astype(str)
        .apply(lambda row: row.str.lower().str.contains(question).any(), axis=1)
    ]

    return matches


def assets_due_for_maintenance(df):

    return df[df["Status"].str.lower() == "maintenance"]


def active_assets(df):

    return df[df["Status"].str.lower() == "active"]