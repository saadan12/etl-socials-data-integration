from shared_code.storage_functions import AzureStorage, db_to_dfs_social
import pandas as pd
import logging
import pandas as pd
import numpy as np
from shared_code import functions_score_transform as f
from sklearn.preprocessing import MinMaxScaler


def transform(data):
    logging.info("Transforming the data ...")
    Facebookcols = [
        "Site",
        "likes",
        "followers",
        "avg_post_likes",
        "avg_post_shares",
        "avg_post_comments",
    ]
    # Keeping only score columns that are included in dataset
    data = f.column_adjuster(data, Facebookcols)
    # Cleaning errors and NaNs from data
    data, numeric_cols = f.clean(data)
    # data = f.create_bestSite(data, Facebookcols[1:])
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
    logging.info("Creating the model and generating csv file ...")
    # Dropping duplicate rows
    df.drop_duplicates(subset=None, keep="first", inplace=True, ignore_index=False)
    df.drop_duplicates(subset="Site", keep="first", inplace=True, ignore_index=False)
    # Columns to be used in calculating sub-score
    Facebookcols = [
        "Site",
        "likes",
        "followers",
        "avg_post_likes",
        "avg_post_shares",
        "avg_post_comments",
    ]
    # Weights of each column
    weights = {
        "likes": 0.15,
        "followers": 0.10,
        "avg_post_likes": 0.20,
        "avg_post_shares": 0.3,
        "avg_post_comments": 0.25,
    }
    # Adjusting columns for scoring
    df = f.column_adjuster(df, Facebookcols)
    # Redistributing weights if features are missing
    weights = f.redistribute_weights(df, weights)

    # create best/worst sites
    df = f.create_bestSite(df, weights)
    # Applying score
    df = f.apply_score(df, weights, "fb_score", 50, 95)
    df = df[(df["Site"] != "BestSite") & (df["Site"] != "WorstSite")]
    df = df.dropna(axis=1, how="all")
    finalcols = ["Site", "fb_score"]
    df = df[finalcols]
    return df


def facebook_scorer(data_dict):
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
        df = db_to_dfs_social(data_dict, data_date, "api_facebook", "social_media_id")

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
            timestamp, container_name, "facebook_scorer"
        )
        # Uploading subscore to blob
        azs.upload_blob_df(df_final, score_path)

        return "ok"

    except Exception as e:
        logging.error(f"Facebook scorer error: {e}")
        return "Facebook scorer error"
