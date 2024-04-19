import logging
from shared_code.storage_functions import AzureStorage, df_to_sql_website
from shared_code.database_helpers import clean_pre_db
from shared_code.db_schemas import Website_TblSchema
import pandas as pd
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    input_config = req.get_json()
    azs = AzureStorage(input_config["container_name"])
    website_table(azs, input_config)

    return func.HttpResponse("Table loaded")


def website_table(azs: AzureStorage, data_dict: dict):
    date_dfs = azs.download_blob_dfs_date(
        data_dict["container_name"], data_dict["timestamp"]
    )
    # print(date_dfs)
    dates = [blob.split("/")[0] for blob in date_dfs]
    for i in dates:
        dfs_path = "{0}/{1}_{2}_{0}.csv".format(
            i, "dataforseo", data_dict["container_name"]
        )
        dfs_df = azs.download_blob_dfs(dfs_path, data_dict["timestamp"])
        dfs_df = dfs_df.drop("Unnamed: 0", axis=1)
        # dfs_path = "{0}/{1}/{1}_{2}_{0}.csv".format(data_dict["timestamp"], "dataforseo", data_dict["container_name"])
        # dfs_df = azs.download_blob_dfs(dfs_path)

        pagespeed_path = "{0}/{1}/{1}_{2}_{0}.csv".format(
            data_dict["timestamp"], "pagespeed", data_dict["container_name"]
        )
        pagespeed_df = azs.download_blob_df(pagespeed_path)
        date = i.replace("-", "")
        dfs_df["website_id"] = dfs_df.apply(
            lambda row: str(data_dict["unique_ids"][row["Site"]]) + date, axis=1
        )
        dfs_df["initial_date"] = dfs_df["date"]

        df_final = pd.merge(dfs_df, pagespeed_df, on="Site")

        # MISSING COMPANY_ID. DIFFERENT COMPANY_ID FOR EACH URL. NEEDS TO COME FROM THE BACKEND.
        db_df = df_final[["website_id", "initial_date"]]
        db_df["Site"] = df_final["Site"]
        db_df["mobile_page_speed"] = df_final["perf_mobile"]
        db_df["desktop_page_speed"] = df_final["perf_desktop"]
        db_df["data_date"] = data_dict["timestamp"]
        db_df["bounce_rate"] = df_final["BounceRate"]
        db_df["monthly_traffic"] = df_final["MonthlyTraffic"]
        db_df["pages_visit"] = df_final["Avg_PageViews"]
        db_df["avg_TimeOnSite"] = df_final["Avg_TimeOnSite"]
        companies_id = [data_dict["unique_ids"][site] for site in db_df["Site"]]

        logging.info(f"Companies proceded: {db_df['Site']}")
        logging.info(f"Company ids: {companies_id}")

        db_df = db_df.drop("Site", axis=1)

        db_df["company_id"] = companies_id
        logging.info(f"Load website df: {db_df}")
        score = Website_TblSchema()
        db_df = clean_pre_db(db_df, score)
        logging.info(f"Clean df: {db_df.to_string()}")
        df_to_sql_website(
            db_df,
            "api_website",
            identity_value=True,
            dtype=score,
        )
