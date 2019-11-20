import os
import pandas as pd
import pickle
import re
import numpy as np


def args_to_pandas(row_args):
    """Transform the row arguments into a pandas.DataFrame."""
    return pd.DataFrame.from_dict(row_args, orient='index').T

def _load_file_from_pickle(file):
    """Load and return a pickle file."""
    with open(file, "rb") as f:
        o_file = pickle.load(f)
    return o_file

def file_exists(filename, path=""):
    file = os.path.join(path, filename)
    if not(os.path.exists(file) and os.path.isfile(file)):
        raise FileNotFoundError(f"File: {file} doesn't exists.")

def remove_file(file):
    try:
        if os.path.isfile(file):
            os.unlink(file)
    except Exception as e:
        print(e)


def read_csv(file, nrows=None, usecols=None):
    # TODO: SEE UnicodeDecodeError
    try:
       df = pd.read_csv(file, nrows=nrows, usecols=usecols)
    except pd.errors.ParserError:
        raise Exception(f"Format error: File {file} is not ',' separated.")
    except UnicodeDecodeError:
        raise UnicodeDecodeError(f"Format error: File {file} is not utf-8 codec.")
    if df.shape[1] == 1:
            raise Exception(f"Format error: File {file} is not ',' separated.")
    return df


def expand_datetime(data, datefields, drop=True, time=False, inplace=False):
   """Create several features from every datetime column.

   Add new columns to the Dataframe('Year', 'Month', 'Week',
   'Day', 'Dayofweek', 'Dayofyear', 'Is_month_end',
   'Is_month_start', 'Is_quarter_end', 'Is_quarter_start',
   'Is_year_end' and 'Is_year_start') for every feature
   containing the word "Date".

   Parameters
   ----------
   data: pandas.Dataframe
       The entire working dataset.
   
   datefields: list, optional
       List of datefields to expand.

   drop: boolean, optional
       Determines whether to drop the original datetime columns
       or not.

   time: boolean, optional
       If True adds aditional columns (Hour, Min and Sec).
   
   inplace: boolena, optional (default=False)
       If False modify a new object else modify the object pass
       int data.

   Returns
   -------
   new_data: pandas.Dataframe
       The entire dataframe with the new columns.

   """
   if(inplace):
       new_data = data
   else:
       new_data = data.copy(deep=True)
   fields_list = list(new_data)
   for field in fields_list:
       if field in datefields:
           fld = data[field]
           if not np.issubdtype(fld.dtype, np.datetime64):
               fld = pd.to_datetime(fld, infer_datetime_format=True)
               new_data[field] = fld
           targ_pre = re.sub('[Dd]ate$', '', field)
           attr = ['Year', 'Month', 'Week', 'Day', 'Dayofweek',
                   'Dayofyear', 'Is_month_end', 'Is_month_start',
                   'Is_quarter_end', 'Is_quarter_start', 'Is_year_end',
                   'Is_year_start']
           if time:
               attr = attr + ['Hour', 'Minute', 'Second']
           for n in attr:
               new_data[targ_pre + "_" + n] = getattr(fld.dt, n.lower()).astype(float)
           new_data[targ_pre + "_" + 'Elapsed'] = fld.astype(np.int64) // 10 ** 9
           if drop:
               new_data.drop(field, axis=1, inplace=True)
   return new_data