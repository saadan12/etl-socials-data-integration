from shared_code.storage_functions import AzureStorage, db_to_dfs
import time
import pandas as pd
from shared_code import functions_score_transform as f
import logging
from sklearn.preprocessing import MinMaxScaler
import numpy as np


def transform(data):
    print("Transforming the data ...")
    SearchAdscols = [
        "Site",
        "paid_traffic",
        "paid_keywords",
        "estm_ppc_budget",
        "estimatedCPC",
    ]
    # Keeping only score columns that are included in dataset
    data = f.column_adjuster(data, SearchAdscols)
    # In case paid traffic is 0, replace inf with NaN
    data = data.replace([np.inf, -np.inf], np.nan)
    # Cleaning errors and NaNs from data
    data, numeric_cols = f.clean(data)
    # Should clean the data then do the math, spyfu or dsf could have 'error'
    data["EstimatedCPC"] = (data["estm_ppc_budget"] / data["paid_traffic"]).replace([np.inf, -np.inf], 0)
    data = f.create_bestSite(data, SearchAdscols[1:])

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
    SearchAdscols = [
        "Site",
        "paid_traffic",
        "paid_keywords",
        "estm_ppc_budget",
        "estimatedCPC",
    ]
    # Weights of each column
    weights = {
        "paid_traffic": 0.2,
        "paid_keywords": 0.10,
        "estm_ppc_budget": 0.25,
        "estimatedCPC": 0.45,
    }
    # Adjusting columns for scoring
    df = f.column_adjuster(df, SearchAdscols)
    # Redistributing weights if features are missing
    weights = f.redistribute_weights(df, weights)
    # Applying score
    df = f.apply_score(df, weights, "score_searchads", 50, 100)
    df = df[(df["Site"] != "BestSite") & (df["Site"] != "WorstSite")]
    df = df.dropna(axis=1, how="all")
    finalcols = ["Site", "score_searchads"]
    df = df[finalcols]
    return df


def paid_scorer(data_dict):
    try:
        container_name = data_dict["container_name"]
        timestamp = data_dict["timestamp"]
        # Establishing connection to Azure Storage
        azs = AzureStorage(container_name)
        # Downloading datasets used to generate subscore

        if "old_unique_ids" in data_dict.keys():
            if data_dict["old_unique_ids"]:
                data_dict["unique_ids"] = data_dict["old_unique_ids"]
        date_dfs = azs.download_blob_dfs_date(data_dict["container_name"],data_dict["timestamp"])
        date_list = [blob.split("/")[0] for blob in date_dfs]
        # Get the latest date
        data_date = max(date_list)
        data_date = data_date.replace("-","")
        df = db_to_dfs(data_dict, data_date,"api_seo", "seo_id")

        # Joining input datasets into one
        df = df.reset_index()
        df.drop(
            df.columns[df.columns.str.contains("unnamed", case=False)],
            axis=1,
            inplace=True,
            errors="ignore",
        )

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

        # Defining subscore path
        score_path = "{}/subscores/searchads_{}_{}.csv".format(
            timestamp, container_name, timestamp
        )
        # Uploading subscore to blob
        azs.upload_blob_df(df_final, score_path)
        return "ok"

    except Exception as e:
        logging.exception(e)
        return "ok"
