import pandas as pd
import os



# --------------------------------------------------
# Load CSV
# --------------------------------------------------

CSV_PATH = os.path.join(os.path.dirname(__file__), "assets1.csv")
print('file path: ' + CSV_PATH)


def load_assets():

    df = pd.read_csv(CSV_PATH)

 #   print (df)

    return df

print (load_assets())
