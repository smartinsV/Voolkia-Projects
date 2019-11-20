import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path

from model import feature_transformation, load_columns, load_model
from control import control_init
from data_preparation import create_datasets, merge_datasets, transform_data
from configs import OUTPUT_FOLDER, FILE_COLUMNS, FILE_MODEL, PRED_FOLDER

# Making predictions

def predict(df=None):
    """Create prediction dataset."""
    print("Making predictions ", end="")
    # load from file if not dataframe passed
    if df is None:
        file = Path(OUTPUT_FOLDER) / "merged_transformed.feather"
        df = pd.read_feather(file)
    # create prediction column
    df["prediction"] = np.nan

    # load model and columns lge4
    model_cols = load_columns(FILE_COLUMNS["gte4"])
    model = load_model(FILE_MODEL["gte4"])
    X = df[(df["total_condicion"] >= 4)][model_cols]
    df.loc[X.index, "prediction"] = model.predict_proba(X)[:, -1]

    # load model and columns  lwe4 g1
    model_cols = load_columns(FILE_COLUMNS["lw4_g1"])
    model = load_model(FILE_MODEL["lw4_g1"])
    # 'None': 7,  '003': 2,  '060': 6,  '010': 3,  '020': 4,  '002': 1,  '050': 5,  '001': 0
    g1 = [6, 5]

    X = df[(df["total_condicion"] < 4) & (df["TIPO_EXPED"].isin(g1))][model_cols]
    df.loc[X.index, "prediction"] = model.predict_proba(X)[:, -1]
    # load model and columns  lwe4 g2
    model_cols = load_columns(FILE_COLUMNS["lw4_g2"])
    model = load_model(FILE_MODEL["lw4_g2"])
    X = df[(df["total_condicion"] < 4) & (~df["TIPO_EXPED"].isin(g1))][model_cols]
    df.loc[X.index, "prediction"] = model.predict_proba(X)[:, -1]

    # 060
    model_cols = load_columns(FILE_COLUMNS["060"])
    model = load_model(FILE_MODEL["060"])
    X = df[df["TIPO_EXPED"] == 6][model_cols]
    df.loc[X.index, "prediction"] = model.predict_proba(X)[:, -1]
    print("... OK")
    
    print("Saving predictions ", end="")
    # loading not transformed dataset
    file = Path(OUTPUT_FOLDER) / "merged.feather"
    df_pred = pd.read_feather(file)
    df_pred["prediction"] = df["prediction"]
    save_file = Path(PRED_FOLDER) /  "pred_set.csv"
    df_pred.reset_index(drop=True).to_csv(save_file)
    print("... OK")


def main():
    # avoid traceback
    # sys.tracebacklimit = 0
    print("Controlling initial configuration")
    print("---------------------------------")
    control_init()
    print()
    print("Preparing datasets")
    print("------------------")
    create_datasets()
    print()
    # forcing exit to evaluate controls only
    # sys.exit()
    print("Merging datasets")
    print("----------------")
    merge_datasets()
    print()
    print("Transforming Data")
    print("--------------")
    transform_data()
    print()
    print("Making Predictions")
    print("------------------")
    predict()
    print("------------------")
    print()
    print("PROCESS ENDED SUCCESSFULLY")
    save_file = Path(PRED_FOLDER) / "pred_set.csv"
    print(f"RESULT FILE: {save_file}")


if __name__ == "__main__":
    main()