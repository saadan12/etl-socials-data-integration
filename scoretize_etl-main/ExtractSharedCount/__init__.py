# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

from ExtractSharedCount.sharedcount import sharedcount
import pandas as pd
import azure.functions as func
import logging
from shared_code.storage_functions import AzureStorage


def main(req: func.HttpRequest) -> func.HttpResponse:
    input_config = req.get_json()

    if not input_config["site_list"]:
        return func.HttpResponse("No new sites to process")

    function_name = "sharedcount"

    logging.debug(
        f"{function_name} called with input {input_config} of type {type(input_config)}"
    )
    azs = AzureStorage(input_config["container_name"])
    path = "{0}/{1}/{1}_{2}_{0}.csv".format(
        input_config["timestamp"], function_name, input_config["container_name"]
    )

    if azs.blob_exists(path) is True:
        logging.info(
            f'Skip. File already exists: {input_config["container_name"]}/{path}'
        )

        return f"File already exists: {path}"

    az = AzureStorage("config-files")
    api_config = az.download_blob_dict(f"{function_name}.json")
    final_df = pd.DataFrame()
    final_df = sharedcount(input_config, api_config)

    azs.upload_blob_df(final_df, path)

    return func.HttpResponse(f"{function_name} csv created: {path}")
