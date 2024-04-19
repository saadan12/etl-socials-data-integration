from shared_code.storage_functions import AzureStorage, db_to_dfs, df_to_sql
import time
import pandas as pd
import logging
import numpy as np
from shared_code import functions_score_transform as f
from sklearn.preprocessing import MinMaxScaler
from shared_code.db_schemas import Seo_TblSchema


def transform(data):
    print("Transforming the data ...")
    SEOcols = [
        "Site",
        "organic_traffic",
        "web_authority",
        "paid_keywords",
        "total_keywords",
        "avg_organic_rank",
        "backlinks",
        "referring_domains",
    ]
    # Keeping only score columns that are included in dataset
    data = f.column_adjuster(data, SEOcols)
    # Cleaning errors and NaNs from data
    data, numeric_cols = f.clean(data)
    data = f.create_bestSite(data, SEOcols[1:])
    # data.rename(columns={'perf_desktop': 'DesktopPagespeed', 'perf_mobile': 'MobilePagespeed'}, inplace=True)
    # Scaling the dataset for scoring
    dataset = f.scale(data, numeric_cols, MinMaxScaler())
    # Inverting scores of columns where lower = better
    invert_cols = [
        "bounce_rate",
        "GlobalRank",
        "CountryRank",
        "CategoryRank",
        "youtube_dislike_count",
        "twitter_negative_sentiment",
    ]
    dataset = f.column_inverter(dataset, invert_cols)
    return dataset


def score(df):
    print("Creating the model and generating csv file ...")
    # Dropping duplicate rows
    df.drop_duplicates(subset=None, keep="first", inplace=True, ignore_index=False)
    df.drop_duplicates(subset="Site", keep="first", inplace=True, ignore_index=False)
    # Columns to be used in calculating sub-score
    SEOcols = [
        "Site",
        "organic_traffic",
        "web_authority",
        "total_keywords",
        "avg_organic_rank",
        "backlinks",
        "referring_domains",
    ]
    # Weights of each column
    weights = {
        "organic_traffic": 20,
        "web_authority": 25,
        "total_keywords": 15,
        "avg_organic_rank": 10,
        "backlinks": 20,
        "referring_domains": 10,
    }
    # Adjusting columns for scoring
    df = f.column_adjuster(df, SEOcols)
    # Redistributing weights if features are missing
    weights = f.redistribute_weights(df, weights)
    # Applying score
    df = f.apply_score(df, weights, "score_seo", 50, 100)
    df = df[(df["Site"] != "BestSite") & (df["Site"] != "WorstSite")]
    df = df.dropna(axis=1, how="all")
    finalcols = ["Site", "score_seo"]
    df = df[finalcols]
    return df


def seo_scorer(data_dict):
    try:
        container_name = data_dict["container_name"]
        timestamp = data_dict["timestamp"]
        # Establishing connection to Azure Storage
        azs = AzureStorage(container_name)

        if "old_unique_ids" in data_dict.keys():
            if data_dict["old_unique_ids"]:
                data_dict["unique_ids"] = data_dict["old_unique_ids"]
        date_dfs = azs.download_blob_dfs_date(
            data_dict["container_name"], data_dict["timestamp"]
        )
        date_list = [blob.split("/")[0] for blob in date_dfs]
        # Get the latest date
        data_date = max(date_list)
        data_date = data_date.replace("-", "")
        df = db_to_dfs(data_dict, data_date, "api_seo", "seo_id")

        # if "old_unique_ids" in data_dict.keys():
        #     if data_dict["old_unique_ids"]:
        #         new_df = df.loc[df['Site'] == data_dict["new_site_list"][[0]]]
        #         new_df["seo_id"] = data_dict["new_unique_ids"].values()[0]
        #         score = Seo_TblSchema()
        #         df_to_sql(
        #                     new_df,
        #                     "api_seo",
        #                     identity_value=True,
        #                     dtype=score,
        #                 )

        df = df.reset_index()
        df.drop(
            df.columns[df.columns.str.contains("unnamed", case=False)],
            axis=1,
            inplace=True,
            errors="ignore",
        )

        df_metrics = df.copy()
        # Transforming and cleaning dataset
        df = transform(df)
        # Applying subscore to dataset
        df = score(df)
        print(df)
        print(df_metrics)
        print(df.dtypes)
        print(df_metrics.dtypes)
        df_list = [df_metrics, df]
        dfs = [df.set_index("Site") for df in df_list]
        df_final = pd.concat(dfs, axis=1)
        df_final = df_final.reset_index()
        df_final.drop(
            df_final.columns[df_final.columns.str.contains("unnamed", case=False)],
            axis=1,
            inplace=True,
            errors="ignore",
        )

        # Defining subscore path
        score_path = "{}/subscores/seo_{}_{}.csv".format(
            timestamp, container_name, timestamp
        )
        # Uploading subscore to blob
        azs.upload_blob_df(df_final, score_path)

        return "ok"

    except Exception as e:
        logging.error(f"Error in seo score: {e}, \n Input config: {data_dict}")
        return "Error in seo score"
