import pandas as pd

def handle_null(value):
    return value if pd.notna(value) else ""