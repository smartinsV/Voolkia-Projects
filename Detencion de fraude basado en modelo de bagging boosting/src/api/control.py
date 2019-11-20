"""control functions"""
from configs import TABLES, READ_FOLDER, FILE_MODEL, FILE_COLUMNS, MAPPER_FILE, TMP_FOLDER, \
                    OUTPUT_FOLDER, PRED_FOLDER, READ_FILES_FORMAT
from helpers import file_exists, remove_file, read_csv

import os
from pathlib import Path

import pandas as pd


# CONFIG PARAMS
SAMPLE_SIZE = 200
ID_FIELD = "NUM_SECU_EXPED"

def control_init():
    """Check if files and folders are ready."""
    control_folder()
    control_files()
    control_file_structure()
    clean_files()

def control_folder():
    print("Controlling folders ", end="")
    for folder in [READ_FOLDER, TMP_FOLDER, OUTPUT_FOLDER, PRED_FOLDER]:
        Path(folder).mkdir(exist_ok=True)
        print(".", end="")
    print(" OK")

def control_files():
    """Control datasets and model files"""
    print("Controlling dataset files ", end="")
    for k, v in TABLES.items():
        file_exists(v+READ_FILES_FORMAT, READ_FOLDER)
        print(".", end="")
    print(" OK")
    print("Controlling model files ", end="")
    for file in [*FILE_MODEL.values(), *FILE_COLUMNS.values(), *MAPPER_FILE.values()]:
        file_exists(file)
        print(".", end="")
    print(" OK")

def control_file_structure():
    """Check if all files have the ID column and all other required columns."""
    print("Controlling files structure ", end="")
    # loading files
    dfs = {}
    for k, v in TABLES.items():
        file = Path(READ_FOLDER) / (v+READ_FILES_FORMAT)
        dfs[k] = read_csv(file, nrows=SAMPLE_SIZE)
    # controlling files
    control_id_column(dfs)
    print(".", end="")
    # control_merging_compatibility(dfs)
    print(".", end="")
    print(" OK")

def control_id_column(dfs):
    """Check if all files have the ID column."""
    TABLES_IDS = {
        "condiciones": ["NUM_SECU_EXPED"],
        "preguntas": ["NUM_SECU_EXPED"],
        "siniestros": ["NUM_SECU_EXPED", "NUM_SECU_POL"],
        "asegurados": ["CIF_ID"],
        "cif": ["ID"],
        "vigabt": ["ID", "NUM_SECU_POL"],
    }

    for k, v in dfs.items():
        for col in TABLES_IDS[k]:
            if col not in v.columns:
                raise Exception(f"Missing KEY column '{col}'' in file {k}.")

def control_merging_compatibility(dfs):
    """Check if the files are mergeables and return a merged sample."""
    # TODO: check how to implement this functionality.
    # merge condiciones y preguntas
    df_merged = safe_merge(dfs["condiciones"], dfs["preguntas"], ["condiciones", "preguntas"], "", "_preg")
    # merge with siniestros
    df_merged = safe_merge(df_merged, dfs["siniestros"], ["condiciones", "siniestros"], "_cond_side", "_sini_side")
    return df_merged


def safe_merge(df_l, df_r, tables_names, suffix_l="", suffix_r=""):
    try:
        df_merge = pd.merge(df_l, df_r, on=ID_FIELD, how="left", suffixes=(suffix_l, suffix_r))
    except ValueError:
        Exception(f"Tables {' and '.join(tables_names)} are not compatible to merge. Please check if the structure it's correct.")
    return df_merge

def clean_files():
    print("Cleaning old tmp files ", end="")
    for folder in [TMP_FOLDER, OUTPUT_FOLDER]:
        files = list(Path(folder).glob("*.feather"))
        for file in files:
            remove_file(file)
            print(".", end="")
    print(" OK")
