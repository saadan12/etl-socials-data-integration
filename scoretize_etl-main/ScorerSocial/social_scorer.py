from shared_code.storage_functions import AzureStorage
import pandas as pd
import numpy as np
from shared_code import functions_score_transform as f
import logging


def score_function(df):
    Socialcols = ["Site", "fb_score", "twitter_score", "youtube_score", "insta_score"]
    # Keeping only score columns that are included in dataset
    df = f.column_adjuster(df, Socialcols)
    # Weights of each column
    weights = {
        "fb_score": 0.25,
        "twitter_score": 0.25,
        "youtube_score": 0.25,
        "insta_score": 0.25,
    }
    # Adjusting columns for scoring
    df = f.column_adjuster(df, Socialcols)
    # Redistributing weights if features are missing
    weights = f.redistribute_weights(df, weights)
    # Applying score
    df_final = df.copy()
    df.reset_index(inplace=True)
    df = f.create_bestSite(df, Socialcols[1:])
    df = f.apply_score(df, weights, "score_social", 50, 100)
    df = df[(df["Site"] != "BestSite") & (df["Site"] != "WorstSite")]
    df_final["score_social"] = df["score_social"]
    df_final = df_final.dropna(axis=1, how="all")
    return df_final


def social_scorer(data_dict):
    try:
        container_name = data_dict["container_name"]
        timestamp = data_dict["timestamp"]
        # Establishing connection to Azure Storage
        azs = AzureStorage(container_name)
        scores = ["facebook", "twitter", "youtube", "instagram"]
        df_list = []
        # Downloading sub-scores and combining into one dataframe
        for score in scores:
            path = "{0}/subscores/{2}_{1}_{0}.csv".format(
                timestamp, container_name, score + "_scorer"
            )
            df = azs.download_blob_df(path)
            if score == "facebook":
                score_column_name = "fb_score"
            if score == "twitter":
                score_column_name = "twitter_score"
            if score == "youtube":
                score_column_name = "youtube_score"
            if score == "instagram":
                score_column_name = "insta_score"
            df = df[["Site", score_column_name]]
            df_list.append(df)
        dfs = [df.set_index("Site") for df in df_list]
        df = pd.concat(dfs, axis=1)
        df = df.reset_index()
        df.drop(
            df.columns[df.columns.str.contains("unnamed", case=False)],
            axis=1,
            inplace=True,
            errors="ignore",
        )
        # Transforming and cleaning dataset
        df = score_function(df)
        # Defining social score path
        score_path = "{0}/subscores/social_{1}_{0}.csv".format(
            timestamp, container_name
        )
        # Uploading final score to blob
        azs.upload_blob_df(df, score_path)

        return "ok"

    except Exception as e:
        logging.error(f"Error in Social scorer : {e}")
        return "Social scorer error"
