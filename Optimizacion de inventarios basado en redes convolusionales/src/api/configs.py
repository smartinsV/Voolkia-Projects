from pathlib import Path


### API  ###

# TARGET = "EXISTE_FRAUDE"
API_COLUMNS = ['cond_04', 'cond_05', 'cond_06', 'cond_09', 'cond_11', 'cond_12', 'cond_32', 'cond_37', 'cond_C1', 'cond_C10', 'cond_C11', 'cond_C12', 'cond_C13', 'cond_C14', 'cond_C15', 'cond_C16', 'cond_C17', 'cond_C18', 'cond_C19', 'cond_C2', 'cond_C20', 'cond_C21', 'cond_C3', 'cond_C4', 'cond_C5', 'cond_C6', 'cond_C7', 'cond_C8', 'cond_C9', 'preg_12', 'preg_15', 'preg_22', 'preg_27', 'preg_28', 'preg_31', 'preg_32', 'preg_33', 'preg_34', 'preg_37', 'CODIGO_BAJA', 'CODIGO_CARATULA', 'CODIGO_REAPERTURA', 'CODIGO_VEHICULO', 'COD_CAUSA_SINI', 'COD_POST_OCURRENCIA', 'COD_POST_POLIZA', 'COD_POST_TERC', 'CONDICION_ROBO_EXP50', 'DESCRIPCION_TIPO', 'DESCRIPCION_VEHICULO', 'ESTADO_CIVIL', 'ESTADO_CIVIL_TERC', 'ESTAD_VEH_ASEG', 'FALTANTE', 'FECHA_FORMAL', 'FECHA_NAC_ASEG', 'FECHA_NAC_TERC', 'FECHA_SINI', 'FEC_DENU_SINI', 'MCA_JUICIO', 'MCA_VIP', 'METRO', 'NUM_SECU_EXPED', 'NUM_SECU_POL', 'OCUPACION_ASEG', 'SEXO', 'SEXO_TERC', 'TELEFONO_TERC', 'TIPO', 'TIPO_EXPED', 'TIPO_LESION', 'TIPO_SINIESTRO', 'SEXO_ASEG', 'TIPO_ACTIVIDAD', 'CANT_RENOVACION', 'CAPITAL_ACCESORIOS', 'CAPITAL_ASEGURADO_COTIZACION', 'CAPITAL_VEHICULO', 'COD_COBRO', 'COD_COBRO_ANTERIOR', 'COD_PROD', 'COD_RAMO', 'COD_RIES', 'COD_ZONA_CASCO', 'COD_ZONA_RC', 'COD_ZONA_ROBO', 'CONV_COMISIONARIO', 'FECHA_PROCESO', 'FECHA_VENC_POL', 'FECHA_VIG_ORIG_POL', 'FECHA_VIG_POL', 'MCA_AGRAVANTE', 'MCA_EMPLEADO', 'MCA_MOVIMIENTO', 'MCA_POLIZA_VIP', 'NEGOCIO', 'PRENDARIO', 'SEGMENTO']

# binary files
FILE_MODEL = "../models/1.1 - df_train 01-18to12-18/1.1.b.2.f(Model) - Model Optimization recall - class_weight (1, 18) - time sorted - valid score (0.403, 0.972).pickle"
FILE_MAPPER = "../features/1.1 - df_train 01-18to12-18/1.1 - dict categorical mappers.pickle"

# Example file
# ONLY FOR DEBUG PURPOSE
DEBUG = False
FILE_EXAMPLE_DS = "test_input_dataset/test results_2019.csv"

### BATCH PROCESS  ###

# configs
TABLES = {
    "condiciones": "CONDICIONES",
    "preguntas": "PREGUNTAS",
    "siniestros": "DSS_SINI_AUTOS_ID",
    "asegurados": "BTT_ASEGURADOS",
    "cif": "tb_cif",
    "vigabt": "VIGABT_POLIZAS",
    #     "investigacion": "INVESTIGACION",  # only to check the results
}

TABLE_COLS = {
    "condiciones": ['CONDICION', 'FEC_ACT', 'NUM_SECU_EXPED', 'USR_ACT', 'VALOR_CONDICION', ],
    "preguntas": ['COD_PREGUNTA', 'FEC_ACT', 'NUM_SECU_EXPED', 'TIPO_EXPED', 'VALOR_PREGUNTA', ],
    "siniestros": ['CATASTROFICO', 'CERRADURA_BAUL', 'CERRADURA_DERECHA', 'CERRADURA_IZQUIERDA', 'CODIGO_BAJA', 'CODIGO_CARATULA', 'CODIGO_REAPERTURA', 'CODIGO_VEHICULO', 'COD_ACT_BENEF', 'COD_CAUSA_SINI', 'COD_POST_OCURRENCIA', 'COD_POST_POLIZA', 'COD_POST_TERC', 'COD_RAMO', 'COD_RIES', 'CONDICION_ROBO_EXP50', 'DANOS_MATERIALES', 'DESCRIPCION_TIPO', 'DESCRIPCION_VEHICULO', 'ESTADO_CIVIL', 'ESTADO_CIVIL_TERC', 'ESTAD_VEH_ASEG', 'FALTANTE', 'FECHA_FORMAL', 'FECHA_NAC_ASEG', 'FECHA_NAC_TERC', 'FECHA_SINI', 'FEC_DENU_SINI', 'FIN_INVESTIGACION', 'MCA_COASEG', 'MCA_JUICIO', 'MCA_VIP', 'METRO', 'NUM_SECU_EXPED', 'NUM_SECU_POL', 'OCUPACION_ASEG', 'SEXO', 'SEXO_TERC', 'TELEFONO_TERC', 'TIPO', 'TIPO_EXPED', 'TIPO_LESION', 'TIPO_LESION_MAXIMA', 'TIPO_SINIESTRO', 'USO', ],
    "asegurados": ['CIF_ID', 'COD_EST_CIVIL', 'FECHA_DESDE', 'FECHA_NACIMIENTO', 'SEXO_ASEG', 'TIPO_ACTIVIDAD', ],
    "cif": ['CLIENTE', 'CODIGO_NACION', 'DATECO_TIPO_ACTIVIDAD', 'DOMICILIO_CODIGO_POSTAL', 'HABILITADO', 'ID', ],
    "vigabt": ['CANT_RENOVACION', 'CAPITAL_ACCESORIOS', 'CAPITAL_ASEGURADO_COTIZACION', 'CAPITAL_VEHICULO', 'COD_COBRO', 'COD_COBRO_ANTERIOR', 'COD_POSTAL', 'COD_PROD', 'COD_RAMO', 'COD_RIES', 'COD_ZONA_CASCO', 'COD_ZONA_RC', 'COD_ZONA_ROBO', 'CONV_COMISIONARIO', 'FECHA_PROCESO', 'FECHA_VENC_POL', 'FECHA_VIG_ORIG_POL', 'FECHA_VIG_POL', 'ID', 'MCA_AGRAVANTE', 'MCA_EMPLEADO', 'MCA_MOVIMIENTO', 'MCA_POLIZA_VIP', 'NEGOCIO', 'NUM_SECU_POL', 'PRENDARIO', 'SEGMENTO', ],
}
# file folders
READ_FOLDER = "input_dataset"
if DEBUG:
    READ_FOLDER = "test_input_dataset"
READ_FILES_FORMAT = ".csv"
TMP_FOLDER = "tmp"
OUTPUT_FOLDER = "output_dataset"
PRED_FOLDER = "pred_output"

# mapper files
MAPPER_FOLDER = "models/mapper"
MAPPERS = {
    "categorical": "1.2 - dict categorical mappers.pickle",
    "cluster_location": "cod_postal_to_cluster_mapper.pickle",
}
MAPPER_FILE = {}
for k, v in MAPPERS.items():
    MAPPER_FILE[k] = Path(MAPPER_FOLDER) / v

# model files
MODEL_FOLDER = "models"

# 3 columns and models
FILE_COLUMNS = {}
FILE_MODEL = {}

model_path = Path(MODEL_FOLDER)
MODEL = {
    "gte4": '3.2.0.b - 6m total_condiciones_split_gte_4 with ZONE GROUPS without comp_cond and time_cond',    
    "lw4_g1": '3.2.0.lw4.g1 - total_condiciones_split lw4 - recall with zone groups',
    "lw4_g2": '3.2.0.lw4.g2 - 18-5 total_condiciones_split lw4 - recall with zone groups',
    # 1.1.b.2.f.6m
    "060": "1.1.b.2.f.6m - model",
}

for k, v in MODEL.items():
    FILE_MODEL[k] = model_path / MODEL[k] / 'model.pickle'
    FILE_COLUMNS[k] = model_path / MODEL[k] / 'columns.pickle'