"""
CONFIGURACIÓN PARA LA ETAPA DE CARGA DE DATOS

En este script se guardan las variables correspondientes a los nombres
de los archivos así como también las columnas que se usan en cada uno.

NOTE: Se deben modificar solamente aquellas variables que comiencen con el
      prefijo ARCHIVO_ o SEP_
"""

# MODIFICAR ESTA PARTE
FOLDER = "../feb19/"
ARCHIVO_POLIZAS = FOLDER + "TB_POLIZAS.tsv"
ARCHIVO_PAGOS = FOLDER + "TB_PAGOS.tsv"
ARCHIVO_CLIENTES = FOLDER + "TB_CIF.tsv"
ARCHIVO_SINIESTROS = FOLDER + "DSS_SINIESTROS_AUTOS.tsv"
ARCHIVO_INTERACCIONES = FOLDER + "TB_INTERACCIONES.tsv"

SEP_POLIZAS = "\t"
SEP_PAGOS = "\t"
SEP_CLIENTES = "\t"
SEP_SINIESTROS = "\t"
SEP_INTERACCIONES = "\t"

PATH_DATASET = FOLDER + "test_dataset_final.feather"
PATH_MODELO = "model.md"
PATH_PREDICCIONES = FOLDER + "test_predicciones.csv"

"""
Modificar estos valores de acuerdo al período analizado.
NOTE: Formato: aaaa-mm-dd
      PERIODO_FIN debe ser el último día del mes a analizar.
      EJ: PERIODO_INI = '2018-06-01'
          PERIODO_FIN = '2018-11-30'
"""
PERIODO_INI = '2018-09-01'
PERIODO_FIN = '2019-02-28'

# NO MODIFICAR ESTO
COLS_POLIZA = [
    'CIF_ID',
    'MCA_VIGENCIA',
    'NUM_SECU_POL',
    'COD_INICIADOR',
    'FECHA_VIG_POL',
]
COLS_PAGOS = [
    'COD_COBRO',
    'COD_SITUACION',
    'FECHA_VTO',
    'FEC_PAGO',
    'MONTO_PAGO',
    'NUM_SECU_POL'
]
COLS_CLIENTES = [
    'ANO_DE_NACIMIENTO',
    'ID',
    'POSICION_IVA'
]
COLS_SINIESTROS = [
    "NUM_SECU_POL",
    "MODELO_VEHICULO",
    "FEC_DENU_SINI",
    "FECHA_LIQUIDACION",
    "FECHA_RECHAZO"
]
COLS_INTERACCIONES = [
    'ID',
    'CIF_ID',
    'FECHA',
    'IN_OUT'
]
