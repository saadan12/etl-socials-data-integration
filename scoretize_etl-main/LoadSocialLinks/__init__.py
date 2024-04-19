import logging
from shared_code.storage_functions import AzureStorage, df_to_sql
from shared_code.database_helpers import clean_pre_db
from shared_code.db_schemas import SL_TblSchema
import azure.functions as func
import pandas as pd


def main(req: func.HttpRequest) -> func.HttpResponse:
    input_config = req.get_json()
    azs = AzureStorage(input_config["container_name"])
    score_table(azs, input_config)

    return func.HttpResponse("Table loaded")


def score_table(azs: AzureStorage, data_dict: dict):
    final_path = "{0}/{1}/{1}_{2}_{0}.csv".format(
        data_dict["timestamp"], "social_webscrapper", data_dict["container_name"]
    )

    social_links_df = azs.download_blob_df(final_path)
    logging.info(f"Final score: {social_links_df}")

    db_df = pd.DataFrame()
    db_df["Site"] = social_links_df["Site"]
    db_df["facebook_url"] = social_links_df["facebook"]
    db_df["instagram_url"] = social_links_df["instagram"]
    db_df["twitter_url"] = social_links_df["twitter"]
    db_df["youtube_url"] = social_links_df["youtube"]

    db_df["modified_date"] = data_dict["timestamp"]
    db_df["project_id"] = data_dict["project_id"]
    companies_id = [data_dict["unique_ids"][site] for site in db_df["Site"]]

    logging.info(f"Companies proceded: {db_df['Site']}")
    logging.info(f"Company ids: {companies_id}")

    db_df = db_df.drop("Site", axis=1)

    db_df["company_id"] = companies_id

    logging.info(f"load social links df: {db_df}")
    sl = SL_TblSchema()
    db_df = clean_pre_db(db_df, sl)
    logging.info(f"Clean df: {db_df.to_string()}")
    df_to_sql(db_df, "api_social_links", dtype=sl)
