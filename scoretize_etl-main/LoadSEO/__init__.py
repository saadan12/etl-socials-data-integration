import datetime
import logging
from shared_code.storage_functions import AzureStorage, df_to_sql_seo
from shared_code.database_helpers import clean_pre_db
from shared_code.db_schemas import Seo_TblSchema
import pandas as pd
import azure.functions as func
import numpy as np


def main(req: func.HttpRequest) -> func.HttpResponse:
    input_config = req.get_json()

    azs = AzureStorage(input_config["container_name"])
    seo_table(azs, input_config)

    return func.HttpResponse("Table loaded")


def seo_table(azs: AzureStorage, data_dict: dict):
    logging.info(f"data_dict: {data_dict}")

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
    dfs_df = dfs_df.drop("Unnamed: 0", axis=1)
    # dfs_path = "{0}/{1}/{1}_{2}_{0}.csv".format(
    #     data_dict["timestamp"], "dataforseo", data_dict["container_name"]
    # )
    # dfs_df = azs.download_blob_df(dfs_path)

    spyfu_path = "{0}/{1}/{1}_{2}_{0}.csv".format(
        data_dict["timestamp"], "spyfu", data_dict["container_name"]
    )
    spyfu_df = azs.download_blob_df(spyfu_path)
    date = latest_date.replace("-", "")
    dfs_df["seo_id"] = dfs_df.apply(
        lambda row: str(data_dict["unique_ids"][row["Site"]]) + date, axis=1
    )
    logging.info(dfs_df["seo_id"])
    dfs_df["initial_date"] = dfs_df["date"]

    df_final = pd.merge(dfs_df, spyfu_df, on="Site")

    db_df = df_final[["seo_id", "initial_date"]]
    db_df["Site"] = df_final["Site"]
    db_df["data_date"] = data_dict["timestamp"]
    db_df["organic_traffic"] = df_final["OrganicTraffic"]
    db_df["web_authority"] = df_final["WebAuthority"]
    db_df["total_keywords"] = df_final["spyfu_last_month_total_organic_results"]
    db_df["traffic_value"] = df_final["spyfu_last_month_organic_value"]
    db_df["avg_keywords_search"] = df_final["spyfu_avg_kw_search_volume"]
    db_df["avg_organic_rank"] = df_final["spyfu_last_month_avg_organic_rank"]
    db_df["paid_traffic"] = df_final["PaidTraffic"]
    db_df["paid_keywords"] = df_final["spyfu_num_paid_keywords"]
    db_df["estm_ppc_budget"] = df_final["spyfu_last_month_budget"]
    db_df["estimatedCPC"] = (
        pd.to_numeric(df_final["spyfu_last_month_budget"], errors="coerce")
        .fillna(0)
        .div(pd.to_numeric(df_final["PaidTraffic"], errors="coerce").fillna(0))
        .replace([np.nan, np.inf, -np.inf], 0)
    )
    db_df["backlinks"] = df_final["Totalbacklinks"]
    db_df["referring_domains"] = df_final["Referringdomains"]

    companies_id = [data_dict["unique_ids"][site] for site in db_df["Site"]]

    db_df = db_df.drop("Site", axis=1)

    db_df["company_id"] = companies_id

    logging.info(f"Load SEO df: {db_df}")

    score = Seo_TblSchema()
    db_df = clean_pre_db(db_df, score)
    print(db_df.to_string())
    logging.info(f"Clean df: {db_df.to_string()}")
    df_to_sql_seo(
        db_df,
        "api_seo",
        identity_value=True,
        dtype=score,
    )
