import logging
from shared_code.storage_functions import AzureStorage, df_to_sql_website_traffic
from shared_code.database_helpers import clean_pre_db
from shared_code.db_schemas import WebsiteTraffic_TblSchema
import pandas as pd
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    input_config = req.get_json()
    azs = AzureStorage(input_config["container_name"])
    traffic_table(azs, input_config)

    return func.HttpResponse("Table loaded")


def traffic_table(azs: AzureStorage, data_dict: dict):
    # dfs_path = "{0}/{1}/{1}_{2}_{0}.csv".format(data_dict["timestamp"], "dataforseo", data_dict["container_name"])
    # dfs_df = azs.download_blob_df(dfs_path)

    date_dfs = azs.download_blob_dfs_date(
        data_dict["container_name"], data_dict["timestamp"]
    )
    # print(date_dfs)
    dates = [blob.split("/")[0] for blob in date_dfs]
    # print(dates)
    # Print the folder dates
    for date in dates:
        # print(date)
        dfs_path = "{0}/{1}_{2}_{0}.csv".format(
            date, "dataforseo", data_dict["container_name"]
        )
        dfs_df = azs.download_blob_dfs(dfs_path, data_dict["timestamp"])
        dfs_df = dfs_df.drop("Unnamed: 0", axis=1)
        date = date.replace("-", "")
        print(date)
        dfs_df["website_id"] = dfs_df.apply(
            lambda row: str(data_dict["unique_ids"][row["Site"]]) + date, axis=1
        )

        # MISSING COMPANY_ID. DIFFERENT COMPANY_ID FOR EACH URL. NEEDS TO COME FROM THE BACKEND.

        db_df = pd.DataFrame()
        db_df["direct_traffic"] = dfs_df["DirectTraffic"]
        db_df["paid_traffic"] = dfs_df["PaidTraffic"]
        db_df["organic_traffic"] = dfs_df["OrganicTraffic"]
        db_df["social_traffic"] = dfs_df["SocialTraffic"]
        db_df["reffered_traffic"] = dfs_df["ReferredTraffic"]
        db_df["mail_traffic"] = dfs_df["MailTraffic"]
        db_df["website_id"] = dfs_df["website_id"]

        # Countries

        db_df["country_fifth"] = dfs_df["TopCountry_5"]
        db_df["country_first"] = dfs_df["TopCountry_1"]
        db_df["country_forth"] = dfs_df["TopCountry_4"]
        db_df["country_second"] = dfs_df["TopCountry_2"]
        db_df["country_third"] = dfs_df["TopCountry_3"]
        db_df["country_value_fifth"] = dfs_df["TopCountryTraffic_5"]
        db_df["country_value_first"] = dfs_df["TopCountryTraffic_1"]
        db_df["country_value_forth"] = dfs_df["TopCountryTraffic_4"]
        db_df["country_value_second"] = dfs_df["TopCountryTraffic_2"]
        db_df["country_value_third"] = dfs_df["TopCountryTraffic_3"]
        db_df["social_first"] = "No data"
        db_df["social_second"] = "No data"
        db_df["social_third"] = "No data"
        db_df["social_value_first"] = 0
        db_df["social_value_second"] = 0
        db_df["social_value_third"] = 0

        logging.info(f"Load website df: {db_df}")

        score = WebsiteTraffic_TblSchema()
        db_df = clean_pre_db(db_df, score)
        logging.info(f"Clean df: {db_df.to_string()}")
        df_to_sql_website_traffic(db_df, "api_website_traffic", dtype=score)
