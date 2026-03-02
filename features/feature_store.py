import pandas as pd
from features.build_features import build_features

def load_and_process(path: str):
    df = pd.read_csv(path)
    df = build_features(df)
    return df
