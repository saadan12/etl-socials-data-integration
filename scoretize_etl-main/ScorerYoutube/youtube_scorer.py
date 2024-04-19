from shared_code.storage_functions import AzureStorage, db_to_dfs_social
import pandas as pd
import logging
import pandas as pd
import numpy as np
from shared_code import functions_score_transform as f
from sklearn.preprocessing import MinMaxScaler


def transform(data):
    print("Transforming the data ...")
    YouTubecols = [
        "Site",
        "video_count",
        "subscriber_count",
        "view_count",
        "like_count",
    ]
    # Keeping only score columns that are included in dataset
    data = f.column_adjuster(data, YouTubecols)
    # Cleaning errors and NaNs from data
    data, numeric_cols = f.clean(data)
    data = f.create_bestSite(data, YouTubecols[1:])
    logging.info(f"data: {data.to_string()}")
    logging.info(f"numeric cols: {numeric_cols}")
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
    YouTubecols = [
        "Site",
        "video_count",
        "subscriber_count",
        "view_count",
        "like_count",
    ]
    # Weights of each column
    weights = {
        "video_count": 0.2,
        "subscriber_count": 0.3,
        "view_count": 0.3,
        "like_count": 0.2,
    }
    # Adjusting columns for scoring
    df = f.column_adjuster(df, YouTubecols)
    # Redistributing weights if features are missing
    weights = f.redistribute_weights(df, weights)
    # Applying score
    df = f.apply_score(df, weights, "youtube_score", 50, 100)
    df = df[(df["Site"] != "BestSite") & (df["Site"] != "WorstSite")]
    df = df.dropna(axis=1, how="all")
    finalcols = ["Site", "youtube_score"]
    df = df[finalcols]
    return df


def youtube_scorer(data_dict):
    try:
        container_name = data_dict["container_name"]
        timestamp = data_dict["timestamp"]
        # Establishing connection to Azure Storage
        azs = AzureStorage(container_name)

        if "old_unique_ids" in data_dict.keys():
            if data_dict["old_unique_ids"]:
                for k, v in data_dict["old_unique_ids"].items():
                    if k in data_dict["new_unique_ids"].keys():
                        pass
                    else:
                        data_dict["unique_ids"][k] = v
        date_dfs = azs.download_blob_dfs_date(
            data_dict["container_name"], data_dict["timestamp"]
        )
        date_list = [blob.split("/")[0] for blob in date_dfs]
        # Get the latest date
        data_date = max(date_list)
        data_date = data_date.replace("-", "")
        df = db_to_dfs_social(data_dict, data_date, "api_youtube", "social_media_id")

        logging.info(f"df: {df.to_string()}")
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
        score_path = "{0}/subscores/{2}_{1}_{0}.csv".format(
            timestamp, container_name, "youtube_scorer"
        )
        # Uploading subscore to blob
        azs.upload_blob_df(df_final, score_path)

        return "ok"

    except Exception as e:
        logging.error(f"Error in Youtube scorer: {e}, \n Input config: {data_dict}")
        return "Error in Youtube scorer"
