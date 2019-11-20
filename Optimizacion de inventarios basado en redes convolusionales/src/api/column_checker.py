from configs import FILE_COLUMNS
from helpers import _load_file_from_pickle
from data_preparation import get_full_cols


if __name__ == "__main__":
    print("all columns")
    # print(get_full_cols())
    for k, path in FILE_COLUMNS.items():
        # cant_cond
        cols = _load_file_from_pickle(path)
        val = "MCA_POLIZA_VIP"
        if val in cols:
            print(f"{k} -> {val}")