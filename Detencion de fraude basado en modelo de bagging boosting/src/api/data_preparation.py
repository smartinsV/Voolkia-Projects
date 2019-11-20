""" preparing datasets functions"""
from configs import READ_FOLDER, READ_FILES_FORMAT, TABLES, TABLE_COLS, TMP_FOLDER, OUTPUT_FOLDER, \
                    MAPPERS, MAPPER_FOLDER, FILE_COLUMNS
from helpers import read_csv, expand_datetime, _load_file_from_pickle

from pathlib import Path
import numpy as np
import pandas as pd

read_path = Path(READ_FOLDER)


### transform data ###

def transform_data():
    print("Formatting data: ", end="")
    output_path = Path(OUTPUT_FOLDER)
    file = output_path / "merged.feather"
    df = pd.read_feather(file)

    # transform data
    # df["TIPO_EXPED"] = df["TIPO_EXPED"].to_string().zfill(3)
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

    # save file
    save_file = Path(OUTPUT_FOLDER) / "merged_transformed.feather"
    df.to_feather(save_file)

    print("... OK")
    return df

def get_full_cols():
    """Return all the columns use by all the models."""
    # make list of all useful columns
    full_cols = []
    for k, v in FILE_COLUMNS.items():
        full_cols.extend(_load_file_from_pickle(v))
    return(set(full_cols))

def add_missing_columns(df, model_cols):
    """Add missing columns with np.nan."""
    missing_cols = control_required_columns(df, model_cols)
    cols = dict.fromkeys(missing_cols, np.nan)
    df = df.assign(**cols)
    return df


def control_required_columns(df, model_cols):
    """Check if all the required columns are after merging the files."""
    # loading model columns
    missing_cols = set(model_cols) - set(df.columns)
    if missing_cols:
        print()
        print(f"** Alert: the following columns are missing: {', '.join(missing_cols)}. **")
    return missing_cols

### merging datasets ###

def merge_datasets():
    tmp_path = Path (TMP_FOLDER)
    print("Merging condiciones and preguntas ", end="")
    # Merge condiciones y preguntas sector
    # loading condiciones
    file = tmp_path / (TABLES["condiciones"]+".feather")
    df_cond = pd.read_feather(file)
    # loading preguntas
    file = tmp_path / (TABLES["preguntas"]+".feather")
    df_preg = pd.read_feather(file)
    # Merging cond + preg
    df_int = pd.merge(df_cond, df_preg, on="NUM_SECU_EXPED", how="left", suffixes=("", "_preg"))
    print("... OK")
    
    print("Merging btt_asegurados, vigabt_polizas y tb_cif ", end="")
    # Merge vigabt, btt y tb_cif sector
    file = tmp_path / (TABLES["vigabt"]+".feather")
    df_vigabt = pd.read_feather(file)
    # merging btt asegurados y tbcif
    file = tmp_path / (TABLES["asegurados"]+".feather")
    df_aseg = pd.read_feather(file)
    df_vigabt_aseg = pd.merge(df_vigabt, df_aseg, on="CIF_ID", how="left", suffixes=("_vigabt", "_aseg"))
    file = tmp_path / (TABLES["cif"]+".feather")
    df_cif = pd.read_feather(file)
    df_vigabt_aseg_cif = pd.merge(df_vigabt_aseg, df_cif, on="CIF_ID", how="left", suffixes=("", "_tbcif"))
    print("... OK")

    print("Merging siniestros ", end="")
    # loading siniestros
    file = tmp_path / (TABLES["siniestros"]+".feather")
    df_sini = pd.read_feather(file)
    # df_sini.drop_duplicates(subset=["NUM_SECU_EXPED"], keep="last", inplace=True)
    df_sini["NUM_SECU_POL"] = pd.to_numeric(df_sini["NUM_SECU_POL"], errors="coerce")
    # merge sini with aseg & cif
    df_tmp = pd.merge(df_sini, df_vigabt_aseg_cif, on="NUM_SECU_POL", how="left", suffixes=("_sini", "_vigabt_aseg_cif"))

    # Merging Merge sini side with cond+preg
    df_tmp["NUM_SECU_EXPED"] = pd.to_numeric(df_tmp["NUM_SECU_EXPED"], errors="coerce")
    df_merged = pd.merge(df_int, df_tmp, on="NUM_SECU_EXPED", how="left", suffixes=("_cond_side", "_sini_side"))
    # save file
    save_file = Path(OUTPUT_FOLDER) / "merged.feather"
    df_merged.reset_index(drop=True).to_feather(save_file)
    print("... OK")


### pre processing tables ###

def create_datasets():
    print("Processing: condiciones ", end="")
    create_condiciones()
    print("... OK")
    print("Processing: preguntas ", end="")
    create_preguntas()
    print("... OK")
    print("Processing: siniestros ", end="")
    create_siniestros()
    print("... OK")
    print("Processing: btt_asegurados ", end="")
    create_asegurados()
    print("... OK")
    print("Processing: tb_cif ", end="")
    create_tb_cif()
    print("... OK")
    print("Processing: vigabt_polizas ", end="")
    create_vigabt_polizas()
    print("... OK")


def create_condiciones():
    # path to raw file
    table_name = "condiciones"
    file = read_path / (TABLES[table_name]+READ_FILES_FORMAT)
    df = read_csv(file, usecols=TABLE_COLS[table_name])
    # creating pivot
    id_col = "NUM_SECU_EXPED"
    condition = "CONDICION"
    value_col = "VALOR_CONDICION"
    # test if all values are numbers, if not change by null
    # df[value_col] = pd.to_numeric(df[value_col], errors="coerce")
    # getting last repeated record
    pv_df = df.pivot_table(index=id_col, columns=condition, values=value_col, aggfunc="last")
    # renaming columns
    pv_df = pv_df.add_prefix("cond_")
    # Create new variables
    pv_df["total_condicion"] = pv_df.sum(axis=1)
    pv_df["es_gte_5"] = pv_df["total_condicion"] >= 5
    # save file
    tmp_file = Path(TMP_FOLDER)
    pv_df.reset_index().to_feather(tmp_file / (TABLES[table_name]+".feather"))

def create_preguntas():
    # path to raw file
    table_name = "preguntas"
    file = read_path / (TABLES[table_name]+READ_FILES_FORMAT)
    df = read_csv(file, usecols=TABLE_COLS[table_name])

    # creating pivot
    id_col = "NUM_SECU_EXPED"
    condition = "COD_PREGUNTA"
    value_col = "VALOR_PREGUNTA"
    # test if all values are numbers, if not change by null
    # df[value_col] = pd.to_numeric(df[value_col], errors="coerce")    
    # getting oldest repeated record
    pv_df = df.pivot_table(index=id_col, columns=condition, values=value_col, aggfunc="last")
    #renaming columns
    pv_df = pv_df.add_prefix("preg_")
    # tmp save file
    tmp_file = Path(TMP_FOLDER)
    pv_df.reset_index().to_feather(tmp_file / (TABLES[table_name]+".feather"))

def create_siniestros():
    # path to raw file
    table_name = "siniestros"
    file = read_path / (TABLES[table_name]+READ_FILES_FORMAT)
    usecols = set(TABLE_COLS[table_name])
    extra_cols = ['FECHA_SINI', 'FEC_DENU_SINI', 'FECHA_NAC_ASEG', 'FECHA_NAC_TERC', "FECHA_FORMAL",
                  "NUM_SECU_EXPED", "NUM_SECU_POL", "TIPO_EXPED"]
    usecols.update(extra_cols)
    df = read_csv(file, usecols=usecols)
    df.drop_duplicates(subset=["NUM_SECU_EXPED"], keep="last", inplace=True)
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
    # adding list to vars to drop after finishing the transformation
    to_drop = ['FEC_DENU_SINI', 'FECHA_NAC_ASEG', 'FECHA_NAC_TERC', "FECHA_FORMAL"]
    df.drop(columns=to_drop, inplace=True)
    # fixing export error
    to_drop = []
    for v in df["NUM_SECU_POL"].unique():
        try:
            int(v)
        except Exception as e:
            print(f"{e}: {v}")
            to_drop.append(v)
    to_drop
    df = df[~df["NUM_SECU_POL"].isin(to_drop)]
    # df["NUM_SECU_POL"] = df["NUM_SECU_POL"].to_string()
    # df["NUM_SECU_EXPED"] = df["NUM_SECU_EXPED"].to_string()
    # this explote
    # obj_cols = df.select_dtypes("object").columns
    # df[obj_cols] = df[obj_cols].to_string()
    # for col in df.select_dtypes("object").columns:
        # df[col] = df[col].to_string()
    # tmp save file
    tmp_file = Path(TMP_FOLDER)
    df.reset_index(drop=True).to_feather(tmp_file / (TABLES[table_name]+".feather"))

def create_asegurados():
    # path to raw file
    table_name = "asegurados"
    file = read_path / (TABLES[table_name]+READ_FILES_FORMAT)
    df = read_csv(file, usecols=TABLE_COLS[table_name])
    # transform dataset
    df.drop_duplicates(subset=["CIF_ID"], keep="last", inplace=True)
    to_date = ["FECHA_DESDE", "FECHA_NACIMIENTO"]
    date_format = "%d/%m/%Y"
    for col in to_date:
        df[col] = pd.to_datetime(df[col], format=date_format, errors="coerce")
    # replace values
    df["TIPO_ACTIVIDAD"].replace("SinDato", np.nan, inplace=True)
    # tmp save file
    tmp_file = Path(TMP_FOLDER)
    df.reset_index(drop=True).to_feather(tmp_file / (TABLES[table_name]+".feather"))

def create_tb_cif():
    # path to raw file
    table_name = "cif"
    file = read_path / (TABLES[table_name]+READ_FILES_FORMAT)
    df = read_csv(file, usecols=TABLE_COLS[table_name])
    # transform dataset
    df.rename(columns={"ID": "CIF_ID"}, inplace=True)

    # tmp save file
    tmp_file = Path(TMP_FOLDER)
    df.reset_index(drop=True).to_feather(tmp_file / (TABLES[table_name]+".feather"))

def create_vigabt_polizas():
    # path to raw file
    table_name = "vigabt"
    file = read_path / (TABLES[table_name]+READ_FILES_FORMAT)
    df = read_csv(file, usecols=TABLE_COLS[table_name])
    # transform dataset
    df.rename(columns={"ID": "CIF_ID"}, inplace=True)
    df.drop_duplicates(subset=["NUM_SECU_POL"], keep="last", inplace=True)

    to_date = ['FECHA_PROCESO', 'FECHA_VENC_POL', 'FECHA_VIG_ORIG_POL', 'FECHA_VIG_POL', ]
    date_format = "%d/%m/%Y"
    for col in to_date:
        df[col] = pd.to_datetime(df[col], format=date_format, errors="coerce")    

    df["cambio_cobro"] = (df["COD_COBRO"] != df["COD_COBRO_ANTERIOR"]) & (df["COD_COBRO_ANTERIOR"].notna())
    df["ANTIG_calc"] = (df["FECHA_VIG_POL"] - df["FECHA_VIG_ORIG_POL"]).dt.days

    # df["CONV_COMISIONARIO"] = df["CONV_COMISIONARIO"].to_string()
    df["CONV_COMISIONARIO"] = df["CONV_COMISIONARIO"].astype(str)
    # tmp save file
    tmp_file = Path(TMP_FOLDER)
    df.reset_index(drop=True).to_feather(tmp_file / (TABLES[table_name]+".feather"))


