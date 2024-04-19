import logging
from shared_code.storage_functions import AzureStorage, df_to_sql_social_child
from shared_code.database_helpers import clean_pre_db
from shared_code.db_schemas import Twitter_TblSchema
import pandas as pd
import azure.functions as func
import numpy as np


def main(req: func.HttpRequest) -> func.HttpResponse:
    input_config = req.get_json()
    azs = AzureStorage(input_config["container_name"])
    twitter_table(azs, input_config)

    return func.HttpResponse("Table loaded")


def twitter_table(azs: AzureStorage, data_dict):
    print("downloading twitter file")

    twitter_path = "{0}/{1}/{1}_{2}_{0}.csv".format(
        data_dict["timestamp"], "twitter", data_dict["container_name"]
    )
    df = azs.download_blob_df(twitter_path)
    date_dfs = azs.download_blob_dfs_date(
        data_dict["container_name"], data_dict["timestamp"]
    )
    date_list = [blob.split("/")[0] for blob in date_dfs]
    # Get the latest date
    latest_date = max(date_list)
    date = latest_date.replace("-", "")
    df["social_media_id"] = df.apply(
        lambda row: str(data_dict["unique_ids"][row["Site"]])
        + date
        + str(data_dict["project_id"]),
        axis=1,
    )

    db_df = pd.DataFrame()
    db_df["social_media_id"] = df["social_media_id"]
    db_df["followers_count"] = df["twitter_followers_count"]
    db_df["following_count"] = df["twitter_following_count"]
    db_df["avg_retweet_count"] = df["twitter_avg_retweet_count"]
    db_df["avg_reply_count"] = df["twitter_avg_reply_count"]
    db_df["avg_likes_count"] = df["twitter_avg_like_count"]
    db_df["tweet_count"] = df["twitter_tweet_count"]
    db_df["listed_count"] = df["twitter_listed_count"]

    # add channel engagement rate
    twitter_followers_count = pd.to_numeric(
        df["twitter_followers_count"], errors="coerce"
    ).fillna(0, downcast="int")
    twitter_avg_like_count = pd.to_numeric(
        df["twitter_avg_like_count"], errors="coerce"
    ).fillna(0, downcast="int")
    db_df["twitter_engagement_rate"] = (
        twitter_avg_like_count.div(twitter_followers_count).replace(
            [np.nan, np.inf, -np.inf], 0
        )
        * 100
    )
    logging.info(f"Load twitter df: {db_df}")
    score = Twitter_TblSchema()
    db_df = clean_pre_db(db_df, score)
    logging.info(f"Clean df: {db_df.to_string()}")
    df_to_sql_social_child(db_df, "api_twitter", dtype=score)
