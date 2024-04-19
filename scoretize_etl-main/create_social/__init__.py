import logging
import azure.functions as func
from shared_code import storage_functions
from shared_code.storage_functions import AzureStorage
import pandas as pd


def main(req: func.HttpRequest) -> func.HttpResponse:
    input_config = req.get_json()
    print(input_config)
    azs = storage_functions.AzureStorage(input_config["container_name"])
    path = "{0}/{1}/{1}_{2}_{0}.csv".format(
        input_config["timestamp"], "social_webscrapper", input_config["container_name"]
    )

    social_dct = input_config["social_ids"]

    df = pd.DataFrame.from_dict(
        social_dct,
        orient="index",
        columns=["facebook", "twitter", "instagram", "youtube", "linkedin"],
    )
    df.reset_index(inplace=True)
    df = df.rename(columns={"index": "Site"})

    azs = AzureStorage(input_config["container_name"])
    azs.upload_blob_df(df, path)

    logging.info(df)

    return func.HttpResponse("ok")
