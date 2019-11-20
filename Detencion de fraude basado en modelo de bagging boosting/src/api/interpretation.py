import numpy as np
import eli5


def row_explainer(model, row):
    try:
        pred = (eli5.formatters.as_dataframe.explain_prediction_df(
                            model.get_booster(), row, feature_names=list(row.columns)))
    except Exception:
        pred = (eli5.formatters.as_dataframe.explain_prediction_df(
                            model, row, feature_names=list(row.columns)))
    # removing bias term
    # pred = pred[pred["feature"].str.contains("BIAS") == False]
    return pred[["feature", "weight"]]

def get_feature_contributions(model, row):
    """Return a dictionary of the contribution by feature."""
    # prediction, bias, contributions = ti.predict(model, row)
    cont = row_explainer(model, row)
    # cont["weight"] = np.around(calc_prop_impact(cont["weight"]),5)
    return contributions_to_json(cont["feature"], np.around(cont["weight"], 4) )

def calc_prop_impact(contributions):
    sum_abs = np.abs(contributions).sum()
    prop_imp = (contributions / sum_abs)
    return prop_imp

def contributions_to_json(columns, contributions):
    """Generate the contributions json.
    
    Parameters
    ----------
    columns: pandas.core.indexes.base.Index
    
    contributions: numpy.ndarray
    
    TODO:
        - finish docstring
    """
    json = {}
    idxs = np.argsort(contributions)
    for i in idxs:
        json[columns[i]] = contributions[i]
    return json
