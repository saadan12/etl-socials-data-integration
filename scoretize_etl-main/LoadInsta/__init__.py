import logging
from shared_code.storage_functions import AzureStorage, df_to_sql_social_child
from shared_code.database_helpers import clean_pre_db
from shared_code.db_schemas import Instagram_TblSchema
import pandas as pd
import azure.functions as func
import numpy as np


def main(req: func.HttpRequest) -> func.HttpResponse:
    input_config = req.get_json()
    azs = AzureStorage(input_config["container_name"])
    instagram_table(azs, input_config)

    return func.HttpResponse("Table loaded")


def instagram_table(azs: AzureStorage, data_dict):
    print("downloading instagram file")

    insta_path = "{0}/{1}/{1}_{2}_{0}.csv".format(
        data_dict["timestamp"], "instagram", data_dict["container_name"]
    )
    df = azs.download_blob_df(insta_path)
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
    db_df["posts"] = df["insta_posts"]
    db_df["followers"] = df["insta_followers"]
    db_df["avg_post_likes"] = df["insta_avg_post_likes"]
    db_df["avg_post_comments"] = df["insta_avg_post_comments"]

    # add channel engagement rate
    insta_followers = pd.to_numeric(df["insta_followers"], errors="coerce").fillna(
        0, downcast="int"
    )
    insta_avg_post_likes = pd.to_numeric(
        df["insta_avg_post_likes"], errors="coerce"
    ).fillna(0, downcast="int")
    db_df["insta_engagement_rate"] = (
        insta_avg_post_likes.div(insta_followers).replace([np.nan, np.inf, -np.inf], 0)
        * 100
    )
    logging.info(f"Load insta df :{db_df}")

    score = Instagram_TblSchema()
    db_df = clean_pre_db(db_df, score)
    logging.info(f"Clean df: {db_df.to_string()}")
    df_to_sql_social_child(db_df, "api_instagram", dtype=score)
