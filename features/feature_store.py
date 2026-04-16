import pandas as pd
from features.build_features import build_features

def load_and_process(data_input):
    """
    Loads data from a CSV path or processes a provided DataFrame.
    """
    if isinstance(data_input, str):
        df = pd.read_csv(data_input)
    elif isinstance(data_input, pd.DataFrame):
        df = data_input.copy()
    else:
        raise ValueError("Input must be a file path (str) or a pandas DataFrame.")
        
    df = build_features(df)
    return df
