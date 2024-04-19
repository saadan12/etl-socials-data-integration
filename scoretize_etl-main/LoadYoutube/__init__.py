import logging
from shared_code.storage_functions import AzureStorage, df_to_sql_social_child
from shared_code.database_helpers import clean_pre_db
from shared_code.db_schemas import Youtube_TblSchema
import pandas as pd
import azure.functions as func
import numpy as np


def main(req: func.HttpRequest) -> func.HttpResponse:
    input_config = req.get_json()
    azs = AzureStorage(input_config["container_name"])
    youtube_table(azs, input_config)

    return func.HttpResponse("Table loaded")


def youtube_table(azs: AzureStorage, data_dict):
    print("downloading youtube file")

    youtube_path = "{0}/{1}/{1}_{2}_{0}.csv".format(
        data_dict["timestamp"], "youtube", data_dict["container_name"]
    )
    df = azs.download_blob_df(youtube_path)
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
    logging.info("social_media_id: {0}".format(df["social_media_id"]))
    db_df = pd.DataFrame()
    db_df["social_media_id"] = df["social_media_id"]
    db_df["video_count"] = df["youtube_video_count"]
    db_df["subscriber_count"] = df["youtube_subscriber_count"]
    db_df["view_count"] = df["youtube_view_count"]
    db_df["like_count"] = df["youtube_like_count"]
    db_df["comment_count"] = df["youtube_comment_count"]
    youtube_avg_interations = (
        pd.to_numeric(df["youtube_like_count"], errors="coerce")
        .fillna(0, downcast="int")
        .div(
            pd.to_numeric(df["youtube_video_count"], errors="coerce").fillna(
                0, downcast="int"
            )
        )
        .replace(np.nan, 0)
    )
    db_df["youtube_engagement_rate"] = (
        youtube_avg_interations.div(
            pd.to_numeric(df["youtube_subscriber_count"], errors="coerce").fillna(
                0, downcast="int"
            )
        ).replace([np.nan, np.inf, -np.inf], 0)
        * 100
    )
    logging.info(f"Load youtube df:{db_df}")
    score = Youtube_TblSchema()
    db_df = clean_pre_db(db_df, score)
    logging.info(f"Clean df: {db_df.to_string()}")
    df_to_sql_social_child(db_df, "api_youtube", dtype=score)
