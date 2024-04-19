from shared_code.storage_functions import AzureStorage, db_to_dfs
import time
import pandas as pd
from azure.storage.blob import ContainerClient
import logging
import pandas as pd
import numpy as np
from shared_code import functions_score_transform as f
from sklearn.preprocessing import MinMaxScaler


def transform(data):
    print("Transforming the data ...")
    # rename the columns
    data.rename(
        columns={
            "MonthlyTraffic": "monthly_traffic",
            "Avg_TimeOnSite": "avg_TimeOnSite",
            "BounceRate": "bounce_rate",
            "Avg_PageViews": "pages_visit",
            "OrganicTraffic": "organic_traffic",
            "DirectTraffic": "direct_traffic",
            "PaidTraffic": "paid_traffic",
            "ReferredTraffic": "reffered_traffic",
            "MailTraffic": "mail_traffic",
            "SocialTraffic": "social_traffic",
            "perf_desktop": "desktop_page_speed",
            "perf_mobile": "mobile_page_speed",
        },
        inplace=True,
    )
    Websitecols = [
        "Site",
        "monthly_traffic",
        "avg_TimeOnSite",
        "bounce_rate",
        "pages_visit",
        "organic_traffic",
        "direct_traffic",
        "paid_traffic",
        "reffered_traffic",
        "mail_traffic",
        "social_traffic",
        "desktop_page_speed",
        "mobile_page_speed",
    ]
    # Keeping only score columns that are included in dataset
    data = f.column_adjuster(data, Websitecols)

    # Formatting Avg_TimeOnSite to appear in Seconds:
    data["avg_TimeOnSite"] = pd.to_datetime(
        data["avg_TimeOnSite"], errors="coerce", format="%H:%M:%S"
    )
    data["avg_TimeOnSite"] = (
        data["avg_TimeOnSite"].dt.hour * 3600
        + data["avg_TimeOnSite"].dt.minute * 60
        + data["avg_TimeOnSite"].dt.second
    )
    # Cleaning errors and NaNs from data
    data, numeric_cols = f.clean(data)
    data = f.create_bestSite(data, Websitecols[1:])
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
    Websitecols = [
        "Site",
        "monthly_traffic",
        "avg_TimeOnSite",
        "bounce_rate",
        "pages_visit",
        "organic_traffic",
        "direct_traffic",
        "paid_traffic",
        "reffered_traffic",
        "mail_traffic",
        "social_traffic",
        "desktop_page_speed",
        "mobile_page_speed",
    ]
    # Weights of each column
    weights = {
        "monthly_traffic": 0.1,
        "avg_TimeOnSite": 0.15,
        "bounce_rate": 0.10,
        "pages_visit": 0.15,
        "organic_traffic": 0,
        "direct_traffic": 0,
        "paid_traffic": 0,
        "reffered_traffic": 0.1,
        "mail_traffic": 0,
        "social_traffic": 0,
        "desktop_page_speed": 0.2,
        "mobile_page_speed": 0.2,
    }
    # Adjusting columns for scoring
    df = f.column_adjuster(df, Websitecols)
    # Redistributing weights if features are missing
    weights = f.redistribute_weights(df, weights)
    # Applying score
    df = f.apply_score(df, weights, "score_website", 50, 100)
    df = df[(df["Site"] != "BestSite") & (df["Site"] != "WorstSite")]
    df = df.dropna(axis=1, how="all")
    finalcols = ["Site", "score_website"]
    df = df[finalcols]
    return df


def website_scorer(data_dict):
    try:
        container_name = data_dict["container_name"]
        timestamp = data_dict["timestamp"]
        # Establishing connection to Azure Storage
        azs = AzureStorage(container_name)
        CONNECT_STR = azs.connect_str
        container_client = ContainerClient.from_connection_string(
            conn_str=CONNECT_STR, container_name=container_name
        )

        date_dfs = azs.download_blob_dfs_date(
            data_dict["container_name"], data_dict["timestamp"]
        )
        # print(date_dfs)
        dates = [blob.split("/")[0] for blob in date_dfs]
        print(dates)
        if "old_unique_ids" in data_dict.keys():
            if data_dict["old_unique_ids"]:
                data_dict["unique_ids"] = data_dict["old_unique_ids"]
        for date in dates:
            df_list = []
            data_date = date.replace("-", "")
            df = db_to_dfs(data_dict, data_date, "api_website", "website_id")
            df_list.append(df)

            df = db_to_dfs(data_dict, data_date, "api_website_traffic", "website_id")
            df_list.append(df)

            # Joining input datasets into one
            dfs = [df.set_index("Site") for df in df_list]
            df = pd.concat(dfs, axis=1)
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
            score_path = "{}/subscores/website/website_{}_{}.csv".format(
                timestamp, container_name, date
            )
            # Uploading subscore to blob
            azs.upload_blob_df(df_final, score_path)

        return "ok"

    except Exception as e:
        logging.error(f"Error in Website scorer: {e}, Input config: {data_dict}")
        return "Error in Website scorer"
