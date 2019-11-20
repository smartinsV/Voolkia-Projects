from model import feature_transformation, load_columns, load_model
from configs import TABLES, TMP_TABLES, READ_PATH, TMP_PATH, OUTPUT_PATH, PRED_PATH, FILE_COLUMNS, FILE_MODEL, FILE_MAPPER

import pickle

if __name__ == "__main__":
    # load model
    model = load_model(FILE_MODEL)
    with open("model_bin.pickle", "wb") as file:
        pickle.dump(model, file)