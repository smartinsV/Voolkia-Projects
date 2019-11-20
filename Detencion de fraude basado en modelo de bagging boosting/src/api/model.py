import os
from pathlib import Path

from helpers import _load_file_from_pickle, expand_datetime
from configs import FILE_MAPPER, MAPPER_FOLDER, MAPPERS, FILE_COLUMNS, FILE_MODEL
from data_preparation import get_full_cols, add_missing_columns

import numpy as np
import pandas as pd

def load_model(model_file):
    """Load the dump model."""
    return _load_file_from_pickle(model_file)


def load_columns(columns_file):
    """Load the array of columns use in the dump model."""
    return _load_file_from_pickle(columns_file)


def load_mapper(mapper_file):
    """Load and return the categorical feature mapper."""
    return _load_file_from_pickle(mapper_file)

def api_feature_transformation(df):
    # transform dtype
    df = transform_dtype(df)
    df = features_formatter(df)
    return df

def transform_dtype(df):
    # convert numeric cols
    df = convert_numeric_cols(df)
    df = str_to_bool(df)
    df = str_to_none(df)
    return df

def convert_numeric_cols(df):
    # getting categorical cols
    mapper_path = Path(MAPPER_FOLDER)
    mapper_file = mapper_path / MAPPERS["categorical"]
    categorical_mapper = _load_file_from_pickle(mapper_file)
    to_float = set(df.columns) - set(categorical_mapper.keys())
    # to_float = set(["CODIGO_VEHICULO", "COD_RIES_sini", "CONDICION_ROBO_EXP50", "CODIGO_REAPERTURA",
    #         "ESTAD_VEH_ASEG", "CODIGO_BAJA", "COD_RAMO_sini"])

    # to_float = to_float.intersection(set(df.columns))
    for col in to_float:
        df.loc[:, col] = pd.to_numeric(df.loc[:, col], errors="coerce")
    
    return df
'''
def feature_transformation(dataset, inplace=False):
    """Map the real value with the transformed value."""
    if inplace:
        df = dataset
    else:
        df = dataset.copy()
    # specific feature format
    df = features_formatter(df)
    df = str_to_bool(df)
    df = str_to_none(df)
    # replace Nulls by np.nan
    # df.fillna(-1, inplace=True)
    # categorical to num transformation
    mapper = load_mapper(FILE_MAPPER)
    cat_cols = list(set(mapper.keys()).intersection(df.columns))
    # df = df.astype(float)
    for col in cat_cols:
        unique_values = df.loc[:, col].unique()
        keys = mapper[col].keys()
        new_vals = list(set(unique_values) - keys)
        if(new_vals):
            # replace new values by np.nan
            df.loc[:,col] = df.loc[:,col].replace(new_vals, "-1")
        df.loc[:,col] = df.loc[:,col].replace(mapper[col])
    df.fillna(-1, inplace=True)
    return df
'''


def features_formatter(df):
    """Make specific features transformations."""
    
    # Create new variables condicion
    cond_cols = df.filter(regex="^cond_*").columns    
    df["total_condicion"] = df[cond_cols].sum(axis=1)
    df["es_gte_5"] = df["total_condicion"] >= 5
    
    # Create new variables siniestros
    to_date = ['FECHA_SINI', 'FEC_DENU_SINI', 'FECHA_NAC_ASEG', 'FECHA_NAC_TERC', "FECHA_FORMAL"]
    date_format = "%d/%m/%Y"
    for col in to_date:
        df[col] = pd.to_datetime(df[col], format=date_format, errors="coerce")
    # df["TIPO_EXPED"] = df["TIPO_EXPED"].to_string()
    df["TIPO_EXPED"] = df["TIPO_EXPED"].astype(str)
    # making new variables
    if "MCA_COASEG" in df.columns:
        df["MCA_COASEG"] = df["MCA_COASEG"] == "SI"
    df["dist_fformal_fsini"] = (df["FECHA_FORMAL"] - df["FECHA_SINI"]).dt.days
    df["dist_fformal_fdenu"] = (df["FECHA_FORMAL"] - df["FEC_DENU_SINI"]).dt.days
    df["dias_entre_denu_y_sini"] = (df["FEC_DENU_SINI"] - df["FECHA_SINI"]).dt.days
    df["edad_aseg"] = df["FECHA_SINI"].dt.year - df['FECHA_NAC_ASEG'].dt.year
    df["edad_terc"] = df["FECHA_SINI"].dt.year - df['FECHA_NAC_TERC'].dt.year
    df["existe_FECHA_FORMAL"] = df["FECHA_FORMAL"].notna()

    # Create new variables asegurados
    # replace values
    df["TIPO_ACTIVIDAD"].replace("SinDato", np.nan, inplace=True)

    # Create new variables vigabt
    to_date = ['FECHA_VIG_ORIG_POL', 'FECHA_VIG_POL', ]
    date_format = "%d/%m/%Y"
    for col in to_date:
        df[col] = pd.to_datetime(df[col], format=date_format, errors="coerce")    

    df["cambio_cobro"] = (df["COD_COBRO"] != df["COD_COBRO_ANTERIOR"]) & (df["COD_COBRO_ANTERIOR"].notna())
    df["ANTIG_calc"] = (df["FECHA_VIG_POL"] - df["FECHA_VIG_ORIG_POL"]).dt.days
    df["CONV_COMISIONARIO"] = df["CONV_COMISIONARIO"].astype(str)

    # transform
    df["TIPO_EXPED"] = df["TIPO_EXPED"].astype(str).str.zfill(3)
    # creating datetime features
    expand_datetime(df, ["FECHA_SINI"], drop=False, time=True, inplace=True)
    # antiguedad poliza: rename ANTIG_calc as ANTIG_pol
    df.rename(columns={"ANTIG_calc": "ANTIG_pol"}, inplace=True)
    # COD_POST_OCURRENCIA & COD_POST_POLIZA
    post_cols = ["COD_POST_POLIZA", "COD_POST_OCURRENCIA", "COD_POST_TERC"]
    for col in post_cols:
        tmp = df[df[col] >= 1000000]
        # df[col] = df[col].to_string()
        df[col] = df[col].astype(str)
        df[col] = df[col].str.replace(".0","", regex=False)
        # removing last 3 digits
        df.loc[tmp.index, col] = df.loc[tmp.index, col].str[:-3]
        # returning to float for the mapper
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # COD_POSTAL mapper
    maper_path = Path(MAPPER_FOLDER)
    mapper_file = maper_path / MAPPERS["cluster_location"]
    cluster_mapper = _load_file_from_pickle(mapper_file)
    cols_to_map = ["COD_POST_POLIZA", "COD_POST_OCURRENCIA", "COD_POST_TERC"]
    for col in cols_to_map:
        for k, v in cluster_mapper.items():
            new_col = col + "_" + k
            df[new_col] = df[col]
            df[new_col] = df[new_col].map(v)
    
    # create column number of conditions activated
    cond_cols = df.filter(regex="^cond_*").columns    
    df["cant_cond"] = (df[cond_cols] > 0).sum(axis=1)

    # categorical mapper
    full_cols = get_full_cols()
    
    # add missing columns
    df = add_missing_columns(df, full_cols)

    mapper_file = maper_path / MAPPERS["categorical"]
    categorical_mapper = _load_file_from_pickle(mapper_file)
    cat_cols = set(full_cols).intersection(set(categorical_mapper.keys()))
    for col in cat_cols:
        df[col] = df[col].map(categorical_mapper[col])
    
    # reduce number of variables used
    # add tipo_exped always
    full_cols.update(["NUM_SECU_EXPED", "TIPO_EXPED", "total_condicion", "cant_cond"])
    df = df[full_cols].copy()
    # replace nulls by -1
    df.fillna(-1, inplace=True)
    to_float = set(["CODIGO_VEHICULO", "COD_RIES_sini", "CONDICION_ROBO_EXP50", "CODIGO_REAPERTURA",
            "ESTAD_VEH_ASEG", "CODIGO_BAJA", "COD_RAMO_sini"])
    to_float = to_float.intersection(set(df.columns))
    for col in to_float:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

def predict_proba(df):
    """Create prediction dataset."""
    # create prediction column
    df["prediction"] = np.nan
    # 060
    tmp = df[df["TIPO_EXPED"] == 6]
    if tmp.shape[0] > 0:
        model_cols = load_columns(FILE_COLUMNS["060"])
        model = load_model(FILE_MODEL["060"])
        X = tmp[model_cols]
        df.loc[X.index, "prediction"] = model.predict_proba(X)[:, -1]
    else:
        # load model and columns lge4
        tmp = df[(df["total_condicion"] >= 4)]
        if tmp.shape[0] > 0:
            model_cols = load_columns(FILE_COLUMNS["gte4"])
            model = load_model(FILE_MODEL["gte4"])
            X = tmp[model_cols]
            df.loc[X.index, "prediction"] = model.predict_proba(X)[:, -1]
        else:
            # load model and columns  lwe4 g1
            g1 = [6, 5]
            tmp = df[(df["total_condicion"] < 4) & (~df["TIPO_EXPED"].isin(g1))]
            if tmp.shape[0] > 0:
                # load model and columns  lwe4 g2
                model_cols = load_columns(FILE_COLUMNS["lw4_g2"])
                model = load_model(FILE_MODEL["lw4_g2"])
                X = tmp[model_cols]
                df.loc[X.index, "prediction"] = model.predict_proba(X)[:, -1]
            else:
                model_cols = load_columns(FILE_COLUMNS["lw4_g1"])
                model = load_model(FILE_MODEL["lw4_g1"])
                # 'None': 7,  '003': 2,  '060': 6,  '010': 3,  '020': 4,  '002': 1,  '050': 5,  '001': 0
                tmp = df[(df["total_condicion"] < 4) & (df["TIPO_EXPED"].isin(g1))]
                X = tmp[model_cols]
                df.loc[X.index, "prediction"] = model.predict_proba(X)[:, -1]
                df["prediction"] = df["prediction"].astype(float)
    prob = df.loc[0, "prediction"]
    return model, prob, model_cols

def str_to_bool(df):
    """Replace String False and True by 0 and 1."""
    df.replace("True", 1, inplace=True)
    df.replace("False", 0, inplace=True)
    return df


def str_to_none(df):
    """Replace string with Null type string to np.nan."""
    non_types = ["None", "nan", "np.nan", "NaN"]
    df.replace(non_types, np.nan, inplace=True)
    return df


def feature_inverse_mapper():
    """Map the transformed value with the real value."""
    pass
