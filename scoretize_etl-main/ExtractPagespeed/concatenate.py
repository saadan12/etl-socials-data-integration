import pandas as pd
from shared_code.storage_functions import AzureStorage
import time
import logging


def concatenate(datajson):
    try:
        pagespeed_path = "{0}/{1}/{1}_{2}_{0}.csv".format(datajson["timestamp"], "pagespeed",
                                                        datajson["container_name"])
        azs = AzureStorage(datajson["container_name"])
        folder_path = "{0}/{1}/".format(datajson["timestamp"], "pagespeed")

        attempt = 0
        while True:
            files_path = azs.download_blob_folder(folder_path)
            if pagespeed_path in files_path:
                files_path.remove(pagespeed_path)
                for path in files_path:
                    azs.delete_blob(blob_path=path)
                break
            n_files_path = len(files_path)
            n_links = datajson['n_sites']
            logging.debug(f"n files path: {n_files_path} n links: {n_links}")
            if n_files_path == n_links:
                df = pd.DataFrame()
                for path in files_path:
                    current_df = azs.download_blob_df(path)
                    df = pd.concat([df, current_df], ignore_index=True)

                    # Delete the csv file after concat it with final df
                    azs.delete_blob(blob_path=path)
                # upload the final pagespeed result to container
                path = "{0}/{1}/{1}_{2}_{0}.csv".format(datajson["timestamp"], "pagespeed",
                                                        datajson["container_name"])
                                                    
                azs.upload_blob_df(df, path)
                break

            elif attempt == 20:
                break
            else:
                time.sleep(20)
                attempt += 1
    except Exception as e:
        logging.error(f"ExtractPageSpeed Concatenate func. error: {e}")
