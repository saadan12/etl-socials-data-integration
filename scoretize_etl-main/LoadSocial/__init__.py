import logging
from shared_code.storage_functions import AzureStorage, df_to_sql_social
from shared_code.database_helpers import clean_pre_db
from shared_code.db_schemas import SocialMedia_TblSchema
from functools import reduce
import pandas as pd
import numpy as np
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    input_config = req.get_json()

    azs = AzureStorage(input_config["container_name"])
    social_table(azs, input_config)

    return func.HttpResponse("Table loaded")


def social_table(azs: AzureStorage, data_dict: dict):
    # Downloading fb insta ytb twitter dfs and putting all together
    fb_path = "{0}/{1}/{1}_{2}_{0}.csv".format(
        data_dict["timestamp"], "facebook", data_dict["container_name"]
    )

    fb_df = azs.download_blob_df(fb_path)

    insta_path = "{0}/{1}/{1}_{2}_{0}.csv".format(
        data_dict["timestamp"], "instagram", data_dict["container_name"]
    )
    insta_df = azs.download_blob_df(insta_path)

    youtube_path = "{0}/{1}/{1}_{2}_{0}.csv".format(
        data_dict["timestamp"], "youtube", data_dict["container_name"]
    )
    youtube_df = azs.download_blob_df(youtube_path)

    twitter_path = "{0}/{1}/{1}_{2}_{0}.csv".format(
        data_dict["timestamp"], "twitter", data_dict["container_name"]
    )
    twitter_df = azs.download_blob_df(twitter_path)
    date_dfs = azs.download_blob_dfs_date(
        data_dict["container_name"], data_dict["timestamp"]
    )
    date_list = [blob.split("/")[0] for blob in date_dfs]
    # Get the latest date
    latest_date = max(date_list)
    dfs_path = "{0}/{1}_{2}_{0}.csv".format(
        latest_date, "dataforseo", data_dict["container_name"]
    )
    dfs_df = azs.download_blob_dfs(dfs_path, data_dict["timestamp"])
    # dfs_path = "{0}/{1}/{1}_{2}_{0}.csv".format(data_dict["timestamp"], "dataforseo", data_dict["container_name"])
    # dfs_df = azs.download_blob_df(dfs_path)
    dfs_df = dfs_df.drop("Unnamed: 0", axis=1)
    date = latest_date.replace("-", "")
    fb_df["social_id"] = fb_df.apply(
        lambda row: str(data_dict["unique_ids"][row["Site"]]) + date + str(data_dict["project_id"]), axis=1
    )

    dfs = [fb_df, insta_df, youtube_df, twitter_df, dfs_df]

    df_final = reduce(lambda left, right: pd.merge(left, right, on="Site"), dfs)

    df_final = df_final.loc[:, ~df_final.columns.duplicated()]

    # Cleaning the dataframe and creating extra columns

    df_final["total_followers"] = (
        pd.to_numeric(df_final["fb_followers"], errors="coerce").fillna(
            0, downcast="int"
        )
        + pd.to_numeric(df_final["insta_followers"], errors="coerce").fillna(
            0, downcast="int"
        )
        + pd.to_numeric(df_final["youtube_subscriber_count"], errors="coerce").fillna(
            0, downcast="int"
        )
        + pd.to_numeric(df_final["twitter_followers_count"], errors="coerce").fillna(
            0, downcast="int"
        )
    )
    df_final["total_followers"] = df_final["total_followers"].astype(
        int, errors="ignore"
    )

    # if youtube_video_count = 0, set youtube_avg_interactions = 0
    youtube_avg_interations = (
        pd.to_numeric(df_final["youtube_like_count"], errors="coerce")
        .fillna(0, downcast="int")
        .div(
            pd.to_numeric(df_final["youtube_video_count"], errors="coerce").fillna(
                0, downcast="int"
            )
        )
        .replace(np.nan, 0)
    )
    df_final["total_average_interactions"] = (
        pd.to_numeric(df_final["fb_avg_post_likes"], errors="coerce").fillna(
            0, downcast="int"
        )
        + youtube_avg_interations.astype(float)
        + pd.to_numeric(df_final["twitter_avg_like_count"], errors="coerce").fillna(
            0, downcast="int"
        )
        + pd.to_numeric(df_final["insta_avg_post_likes"], errors="coerce").fillna(
            0, downcast="int"
        )
    )

    global_engagement = (
        df_final["total_average_interactions"]
        .div(df_final["total_followers"])
        .replace([np.nan, np.inf, -np.inf], 0)
    )

    df_final["global_engagement_rate"] = global_engagement * 100
    df_final["data_date"] = data_dict["timestamp"]
    df_final["total_clicks"] = df_final["SocialTraffic"]
    df_final["initial_date"] = df_final["date"]

    db_df = df_final[
        [
            "Site",
            "social_id",
            "initial_date",
            "global_engagement_rate",
            "total_followers",
            "total_average_interactions",
            "total_clicks",
            "data_date",
        ]
    ]

    companies_id = [data_dict["unique_ids"][site] for site in db_df["Site"]]

    db_df = db_df.drop("Site", axis=1)

    db_df["company_id"] = companies_id
    db_df["project_id"] = data_dict["project_id"]
    logging.info(f"Load social df: {db_df}")

    score = SocialMedia_TblSchema()
    db_df = clean_pre_db(db_df, score)
    logging.info(f"Clean df: {db_df.to_string()}")

    df_to_sql_social(
        db_df,
        "api_social_media",
        identity_value=True,
        dtype=score,
    )
