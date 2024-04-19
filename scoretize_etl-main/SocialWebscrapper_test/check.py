import pandas as pd
from shared_code.storage_functions import AzureStorage
import logging
from SocialWebscrapper.social_webscrapper import social_webscrapper

def check(azs: AzureStorage, path: str, datajson: dict):
    if azs.blob_exists(path) == True:
        logging.info(f'File already exists: {datajson["container_name"]}/{path}')
        return True
    else:
        return False


def retry(azs: AzureStorage, path: str, datajson: dict):
    logging.info(f'Retrying for: {datajson["container_name"]}/{path}')
    saved_df = azs.download_blob_df(path)
    nf_df = saved_df[saved_df.duplicated(subset=["facebook", "twitter", "instagram", "youtube", "linkedin"], keep=False)]
    f_df = saved_df.drop_duplicates(subset=["facebook", "twitter", "instagram", "youtube", "linkedin"], keep=False)

    if not nf_df.empty:
        site_list = nf_df["Site"].unique()
        logging.info(f'Retrying for: {site_list}')
        datajson["new_site_list"] = site_list
        retry_df = social_webscrapper(datajson)
        final_df = f_df.append(retry_df, ignore_index=True)
        azs.delete_blob(path)
        azs.upload_blob_df(final_df, path)
    else:
        logging.info('No rows to retry')
