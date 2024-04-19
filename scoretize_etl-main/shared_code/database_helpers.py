import pandas as pd
import numpy as np
import logging


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def clean_pre_db(data: pd.DataFrame, schema, impute=False):
    logging.info(f"pre clean df: {data.to_string()}")
    schema_dictionary = schema.pandas_dtypes
    # Removing Whitespace from output Column names
    data.columns = data.columns.str.replace(" ", "")
    if "initial_date" in data.columns:
        data["initial_date"] = pd.to_datetime(data["initial_date"], format="%Y-%m-%d")
    if "modified_date" in data.columns:
        data["modified_date"] = pd.to_datetime(data["modified_date"], format="%Y-%m-%d")
    schema_dictionary = {
        k: v for k, v in schema_dictionary.items() if k in data.columns
    }
    logging.info(f"schema_dictionary: {schema_dictionary}")
    schema_dictionary.pop("initial_date", None)
    for k, v in schema_dictionary.items():
        if data[k].dtypes != v:
            logging.info(f"modifying data column: {data[k]}")
            data[k] = data[k].astype(str)
            for value in data[k]:
                if isfloat(value):
                    pass
                else:
                    data[k] = data[k].replace(value, np.nan)
            data[k] = pd.to_numeric(data[k], errors="coerce")
    data.replace([np.inf, -np.inf], np.nan, inplace=True)
    if impute:
        data.fillna(0, axis=1, inplace=True)

    logging.info(f"post clean df: {data.to_string()}")
    return data
