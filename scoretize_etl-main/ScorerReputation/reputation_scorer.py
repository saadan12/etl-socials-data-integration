import pandas as pd
import numpy as np
from shared_code import functions_score_transform as f
from sklearn.preprocessing import MinMaxScaler
import logging
from shared_code.storage_functions import AzureStorage


def transform(data):
    print("Transforming the data ...")
    Reputationcols = [
        "Site",
        "twitter_positive_sentiment",
        "twitter_negative_sentiment",
        "total_Mentions",
    ]
    # Keeping only score columns that are included in dataset
    data = f.column_adjuster(data, Reputationcols)
    # Cleaning errors and NaNs from data
    data, numeric_cols = f.clean(data)
    data = f.create_bestSite(data, Reputationcols[1:])
    # Scaling the dataset for scoring
    dataset = f.scale(data, numeric_cols, MinMaxScaler())
    # Inverting scores of columns where lower = better
    invert_cols = [
        "BounceRate",
        "GlobalRank",
        "CountryRank",
        "CategoryRank",
        "youtube_dislike_count",
        "twitter_negative_sentiment",
    ]
    dataset = f.column_inverter(dataset, invert_cols)
    return dataset


def score(df):
    print("Creating the model and generating csv file ...")
    # Dropping duplicate rows
    df.drop_duplicates(subset=None, keep="first", inplace=True, ignore_index=False)
    df.drop_duplicates(subset="Site", keep="first", inplace=True, ignore_index=False)
    # Columns to be used in calculating sub-score
    Reputationcols = [
        "Site",
        "twitter_positive_sentiment",
        "twitter_negative_sentiment",
        "total_Mentions",
    ]
    # Weights of each column
    weights = {
        "twitter_positive_sentiment": 60,
        "twitter_negative_sentiment": 10,
        "total_Mentions": 30,
    }
    # Adjusting columns for scoring
    df = f.column_adjuster(df, Reputationcols)
    # Redistributing weights if features are missing
    weights = f.redistribute_weights(df, weights)
    # Applying score
    df = f.apply_score(df, weights, "score_reputation", 50, 100)
    df = df[(df["Site"] != "BestSite") & (df["Site"] != "WorstSite")]
    df = df.dropna(axis=1, how="all")
    finalcols = ["Site", "score_reputation"]
    df = df[finalcols]
    return df


def reputation_scorer(data_dict):
    try:
        container_name = data_dict["container_name"]
        timestamp = data_dict["timestamp"]
        # Establishing connection to Azure Storage
        azs = AzureStorage(container_name)
        path = "{0}/{1}/{1}_{2}_{0}.csv".format(
            data_dict["timestamp"], "twitter", data_dict["container_name"]
        )
        df = azs.download_blob_df(path)
        # Transforming and cleaning dataset
        df_metrics = df.copy()
        # Transforming and cleaning dataset
        df = transform(df)
        # Applying subscore to dataset
        df = score(df)
        df_list = [df_metrics, df]
        dfs = [df.set_index("Site") for df in df_list]
        df_final = pd.concat(dfs, axis=1)
        df_final = df_final.reset_index()
        df_final.drop(
            df_final.columns[df_final.columns.str.contains("unnamed", case=False)],
            axis=1,
            inplace=True,
            errors="ignore",
        )

        # Defining social score path
        score_path = "{0}/subscores/reputation_{1}_{0}.csv".format(
            timestamp, container_name
        )
        # Uploading final score to blob
        azs.upload_blob_df(df_final, score_path)

        return "ok"

    except Exception as e:
        logging.error(f"Error in reputation score: {e}, Input config: {data_dict}")
        return "Error in reputation score"
