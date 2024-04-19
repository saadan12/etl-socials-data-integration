# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

from ExtractPagespeed.pagespeed import pagespeed
import logging
import pandas as pd
from shared_code.storage_functions import AzureStorage
import tldextract
from ExtractPagespeed.concatenate import concatenate
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        input_config = req.get_json()

        if not input_config["site_list"]:
            return func.HttpResponse("No new sites to process")

        function_name = "pagespeed"

        logging.info(
            f"{function_name} called with input {input_config} of type {type(input_config)}"
        )

        azs = AzureStorage(input_config["container_name"])

        ext = tldextract.extract(input_config["site_list"][0])
        domain = str(ext.domain) + str(ext.suffix)
        path = "{0}/{1}/{1}_{2}_{0}_{3}.csv".format(
            input_config["timestamp"],
            "pagespeed",
            input_config["container_name"],
            domain,
        )

        # CHECK IF FILE ALREADY EXISTS
        # If so, skip api call
        if azs.blob_exists(path) is True:
            if input_config["last_call"]:
                concatenate(input_config)
            logging.info(
                f'Skip. File already exists: {input_config["container_name"]}/{path}'
            )

            return func.HttpResponse(f"{function_name} csv created: {path}")

        az = AzureStorage("config-files")
        config_dict = az.download_blob_dict("pagespeed.json")
        final_df = pd.DataFrame()
        final_df = pagespeed(input_config, config_dict)

        azs.upload_blob_df(final_df, path)

        if input_config["last_call"]:
            concatenate(input_config)

        return func.HttpResponse(f"{function_name} csv created: {path}")
    except Exception as e:
        logging.error(f"ExtractPageSpeed Init File Error: {e}")
        return func.HttpResponse(f"ExtractPageSpeed Init File Error: {e}")
