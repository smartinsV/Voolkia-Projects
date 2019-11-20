from config import PATH_DATASET, PATH_MODELO, PATH_PREDICCIONES
import pickle
import pandas as pd
from pyarrow.lib import ArrowIOError

if __name__ == "__main__":
    # LOADING DATASET
    try:
        print(f"Leyendo dataset en {PATH_DATASET} ...")
        dataset = pd.read_feather(PATH_DATASET)
        dataset = dataset.fillna(-999)

        # LODAING MODEL
        print(f"Cargando modelo {PATH_MODELO} ...")
        with open(PATH_MODELO, 'rb') as file:
            model = pickle.load(file)

        print(f"Armando archivo de predicciones en {PATH_PREDICCIONES} ...")
        results = pd.DataFrame(dataset["CIF_ID"])
        dataset = dataset.drop(["CIF_ID"], axis=1)
        predictions = model.predict(dataset)
        predictions_proba = model.predict_proba(dataset)

        results['BAJA'] = predictions
        results[['PROB_NO_BAJA',
                'PROB_BAJA_1M',
                'PROB_BAJA_2M',
                'PROB_BAJA_3M']] = pd.DataFrame(predictions_proba)

        # SAVING RESULTS
        results.to_csv(PATH_PREDICCIONES, index=False)
        print("Listo.")
    except FileNotFoundError:
        print("ARCHIVO NO ENCONTRADO")
    except ArrowIOError:
        print("ARCHIVO NO ENCONTRADO")
