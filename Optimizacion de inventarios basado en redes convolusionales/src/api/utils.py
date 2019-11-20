import os
from urllib.parse import urlencode
from data_preparation import add_missing_columns, get_full_cols
from configs import API_COLUMNS

import pandas as pd

def rows_to_urls(df, n_examples=5):
    # first control required columns
    # add missing columns
    df = add_missing_columns(df, API_COLUMNS)

    url_samples = []
    for i in range(n_examples):
        url = urlencode(df.iloc[i].to_dict())
        html_url = f"<a href='predictions?{url}'>Example {i}</a>"
        url_samples.append(html_url)
    return url_samples


def load_sample_dataset(file_path):
    """Load example dataset."""
    df = pd.read_csv(file_path, index_col=0)
    return df[df["TIPO_EXPED"].notnull()]

