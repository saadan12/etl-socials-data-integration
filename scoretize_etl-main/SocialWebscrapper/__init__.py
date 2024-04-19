# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

from SocialWebscrapper.social_webscrapper import social_webscrapper
import logging
import pandas as pd
import tldextract
from SocialWebscrapper.concatenate import concatenate
from shared_code.storage_functions import AzureStorage
from SocialWebscrapper.check import check
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        input_config = req.get_json()

        if not input_config["site_list"]:
            return func.HttpResponse("No new sites to process")

        function_name = "social_webscrapper"

        logging.debug(
            f"{function_name} called with input {input_config} of type {type(input_config)}"
        )

        azs = AzureStorage(input_config["container_name"])
        ext = tldextract.extract(input_config["site_list"][0])
        domain = str(ext.domain) + str(ext.suffix)
        path = "{0}/{1}/{1}_{2}_{0}_{3}.csv".format(
            input_config["timestamp"],
            "social_webscrapper",
            input_config["container_name"],
            domain,
        )

        if azs.blob_exists(path) is True:
            if input_config["last_call"]:
                concatenate(input_config)
            logging.info(
                f'Skip. File already exists: {input_config["container_name"]}/{path}'
            )
            return func.HttpResponse("Social media links scrapped")

        final_df = pd.DataFrame()
        final_df = social_webscrapper(input_config, use_multithreading=False)
        logging.info(
            f"SocialWebScraper final dataset {final_df} for this input: {input_config}"
        )

        azs.upload_blob_df(final_df, path)
        if input_config["last_call"]:
            concatenate(input_config)

        return func.HttpResponse("Social media links scrapped")
    except Exception as e:
        logging.error(
            f"SocialWebScraper func Error: {e} for this input: {input_config}"
        )
        return func.HttpResponse(
            f"Social Web Scrapper Error: {e}for this input: {input_config}",
            status_code=500,
        )
