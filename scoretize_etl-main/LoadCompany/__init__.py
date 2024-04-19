import logging
from shared_code.storage_functions import AzureStorage, update_sql
from shared_code.database_helpers import clean_pre_db
from shared_code.db_schemas import Company_TblSchema
import azure.functions as func
import pandas as pd


def main(req: func.HttpRequest) -> func.HttpResponse:
    input_config = req.get_json()
    azs = AzureStorage(input_config["container_name"])
    score_table(azs, input_config)

    return func.HttpResponse("Table loaded")


def score_table(azs: AzureStorage, data_dict: dict):
    final_path = "{0}/social_webscrapper/{1}_{2}_{0}.csv".format(
        data_dict["timestamp"], "social_webscrapper", data_dict["container_name"]
    )
    social_links_df = azs.download_blob_df(final_path)
    logging.info(f"Social media links df: {social_links_df}")

    db_df = pd.DataFrame()
    db_df["url"] = social_links_df[["Site"]]
    db_df["facebook_url"] = social_links_df["facebook"]
    db_df["instagram_url"] = social_links_df["instagram"]
    db_df["twitter_url"] = social_links_df["twitter"]
    db_df["youtube_url"] = social_links_df["youtube"]
    logging.info(f"Load company table:{db_df}")

    company = Company_TblSchema()
    db_df = clean_pre_db(db_df, company)
    logging.info(f"Clean df: {db_df.to_string()}")
    update_sql(db_df, "api_company", "url")
