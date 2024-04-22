import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
import datetime as dt
from os import mkdir
import regex
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MinMaxScaler
import logging


def column_adjuster(df, expected_columns):
    # Loops thorugh the columns needed to calculate score, keeping only those that
    # are actually present in the dataset, and applies that column schema to the dataset

    # Placeholder for scoring features actually present in dataset
    cols = []
    # Looping through expected columns and adding only those who are present in the dataset to cols
    for column in expected_columns:
        if column not in df.columns:
            logging.info(f"Expected column not found in dataset: {column}" )
            logging.info(f"Creating new column: {column}")
            df[column] = 0
        cols.append(column)
    df = df[cols]
    return df


def column_inverter(dataset, invert_cols):
    for column in invert_cols:
        if column in dataset.columns:
            dataset[column] = dataset[column].apply(lambda x: 1 - x)
    return dataset


def clean(data):
    # Removing Whitespace from output Column names
    logging.info(f"Dataframe before cleaning: {data.to_string()}")
    logging.info(f"Dataframe column types: {data.dtypes}")
    data.columns = data.columns.str.replace(" ", "")
    string_cols = data.select_dtypes(exclude=np.number).columns.tolist()
    if "Site" in string_cols:
        string_cols.remove("Site")
    for col in string_cols:
        data[col] = data[col].astype(str)
        if data[col].str.contains("error").any():
            logging.info(f"cols contain error {data[col]}")
            data[col] = data[col].replace(r".*error.*", np.nan, regex=True)
            # data[col] = data[col].apply(lambda x: np.nan if 'error' else x)
            data[col] = pd.to_numeric(data[col], errors="coerce")
            data[col].fillna(0, inplace=True)
            data[col] = data[col].astype(float)
        else:
            data[col] = pd.to_numeric(data[col], errors="coerce")
            data[col].fillna(0, inplace=True)
            data[col] = data[col].astype(float)
    # Replacing nulls with mean for numeric columns
    numeric_cols = data.select_dtypes(include=np.number).columns.tolist()
    for column in data[numeric_cols]:
        data[column].replace(np.nan, 0, inplace=True)
        data[column] = data[column].astype(float)
    data.replace([np.inf, -np.inf], np.nan, inplace=True)
    data.fillna(0, inplace=True)
    logging.info(f"Dataframe after cleaning: {data.to_string()}")
    logging.info(f"Dataframe column types after cleaning: {data.dtypes}")
    logging.info(f"Numeric columns: {numeric_cols}")
    return data, numeric_cols


def scale(data, numeric_cols, scaler):
    # Normalizing Numeric variables, NO Categorical variables included:
    mms = scaler
    for col in numeric_cols:
        data[col] = data[col].replace([np.nan, np.inf], 0)
    dataset = pd.concat(
        [
            data["Site"].reset_index(drop=True),
            pd.DataFrame(
                mms.fit_transform(data[numeric_cols]), columns=numeric_cols
            ).reset_index(drop=True),
        ],
        axis=1,
    )
    return dataset


def redistribute_weights(df, weights):
    # Checking that all columns are present, and redistributing the weights of those that are not evenly amongst the remaining columns
    redistribution = 0
    dropped_cols = []
    for key in weights.keys():
        try:
            df[key]
        except:
            print("Expected column not found in dataset: ", key)
            # storing weight of missing column to be redistributed amongst remaining columns
            redistribution += weights[key]
            dropped_cols.append(key)
    # Dropping columns that are not present in the dataset from weights
    for col in dropped_cols:
        print(col)
        del weights[col]

    # Adding redistributed score back to remaining weights
    for key in weights.keys():
        weights[key] += redistribution / len(weights.keys())

    return weights


def convert(x, a, b, c=0, d=1):
    # Algorithm used by score converter
    if b - a == 0:
        return 0
    else:
        return c + float(x - a) * float(d - c) / (b - a)


def convert_scores(df, score, desired_range_min, desired_range_max):
    # Converting scores into values between range minimum and maximum
    # Actual min score
    min_s = df[score].min()
    # Actual max score
    max_s = df[score].max()
    # Converting score from actual to desired range
    for i in range(len(df)):
        if df[score][i] == 0:
            pass
        else:
            df[score][i] = convert(
                df[score][i], min_s, max_s, desired_range_min, desired_range_max
            )
    return df[score]


def apply_score(df, weights, score_column_name, score_min, score_max):
    # Multiplying each column by weight
    sumWeights = 0
    for key in weights.keys():
        print(key, weights[key])
        sumWeights += weights[key]
        print("Sum of weights: ", sumWeights)
        print("\n")
        df[key] = df[key].apply(lambda x: x * weights[key])
    # Calculating sub-score as weighted average of features
    df[score_column_name] = df.iloc[:, 1:].sum(1)
    # Sorting by subscore
    df.sort_values(by=score_column_name, ascending=False, inplace=True)
    # Converting score to desired range scale
    convert_scores(df, score_column_name, score_min, score_max)
    return df


def create_bestSite(df, cols):
    # Creating BestSite at last row
    df.at[(len(df)), "Site"] = "BestSite"
    # Creating WorstSite at last row
    df.at[(len(df)), "Site"] = "WorstSite"
    invert_cols = [
        "BounceRate",
        "GlobalRank",
        "CountryRank",
        "CategoryRank",
        "youtube_dislike_count",
        "twitter_negative_sentiment",
    ]
    for col in cols:
        if col in invert_cols:
            # For each column, updating the value of BestSite (at index len(df)-2) to be 10 % less than the min column value if it's from invert_cols
            df.at[(len(df) - 2), col] = df[col].min() * 0.9
            # For each column, updating the value of WorstSite (at index len(df)-1) to be 10 % more than the max column value if it's from invert_cols
            df.at[(len(df) - 1), col] = df[col].max() * 1.1
        else:
            # For each column, updating the value of BestSite (at index len(df)-2) to be 10 % more than the max column value
            df.at[(len(df) - 2), col] = df[col].max() * 1.1
            # For each column, updating the value of WorstSite (at index len(df)-1) to be 10% less than the min column value
            df.at[(len(df) - 1), col] = df[col].min() * 0.9
    return df
