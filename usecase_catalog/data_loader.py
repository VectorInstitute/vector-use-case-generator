import pandas as pd

def load_use_cases(file_path):
    return pd.read_excel(file_path)

def filter_use_cases(use_cases_df, search_query, show_all):
    if show_all:
        return use_cases_df
    elif search_query:
        return use_cases_df[
            use_cases_df.apply(lambda row: search_query.lower() in row.astype(str).str.lower().str.cat(sep=' '), axis=1)
        ]
    else:
        return pd.DataFrame()  # Empty DataFrame if no search is made