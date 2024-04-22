import requests
import pandas as pd
import time
from shared_code.storage_functions import AzureStorage
import tldextract
from random import randint
import numpy as np
import logging
import concurrent.futures
import threading
import pandas as pd
import time
import requests

import time


def get_pagespeed(API_Key, page_URL, baseURL, result_dict):
    retry_limit = 3
    retry_count = 0

    while retry_count < retry_limit:
        try:
            t1 = time.time()
            print("Pagespeed request: " + str(page_URL))

            response_url = f'{baseURL}{page_URL}&key={API_Key}&category=performance&category=accessibility&category=seo&category=best_practices&strategy=desktop'
            response_desktop = requests.get(response_url)

            print(response_desktop)

            response_url = f'{baseURL}{page_URL}&key={API_Key}&category=performance&category=accessibility&category=seo&category=best_practices&strategy=mobile'
            response_mobile = requests.get(response_url)

            print(response_mobile)

            # Parsing response:
            json_data_desktop = response_desktop.json()
            categories_desktop = json_data_desktop["lighthouseResult"]["categories"]
            json_data_mobile = response_mobile.json()
            categories_mobile = json_data_mobile["lighthouseResult"]["categories"]

            # Performance Score:
            perf_score_desktop = categories_desktop["performance"]["score"] * 100
            perf_score_mobile = categories_mobile["performance"]["score"] * 100

            # Accessibility Score:
            access_score_desktop = categories_desktop["accessibility"]["score"] * 100
            access_score_mobile = categories_mobile["accessibility"]["score"] * 100

            # SEO Score:
            seo_score_desktop = categories_desktop["seo"]["score"] * 100
            seo_score_mobile = categories_mobile["seo"]["score"] * 100

            # Best Practices Score:
            bestPract_score_desktop = categories_desktop["best-practices"]["score"] * 100
            bestPract_score_mobile = categories_mobile["best-practices"]["score"] * 100

            logging.info(str(page_URL) + " time elapsed: " + str(time.time() - t1))
            result_dict[page_URL] = [perf_score_desktop, access_score_desktop, seo_score_desktop, bestPract_score_desktop, perf_score_mobile,
                    access_score_mobile, seo_score_mobile, bestPract_score_mobile]
            logging.info(f"Result : {result_dict[page_URL]}")
            break  # Exit the loop if the code block executes without an exception
        except Exception as e:
            logging.error(f"ExtractPageSpeed GetPageSpeed func. error: {e}")
            result_dict[page_URL] = ["error"] * 8
            retry_count += 1

def convert_https_to_http(url):
    return url.replace("https://", "http://")
def convert_to_https(url):
        if url.startswith('http://'):
            return 'https://' + url[7:]
        return url

def pagespeed(data_dict, config_dict):
    site_list = data_dict["site_list"]
    key = config_dict["key"]
    host = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url="
    
    result_dict = {}
    threads = []
    
    for site in site_list:
        site = convert_https_to_http(site)
        t = threading.Thread(target=get_pagespeed, args=(key, site, host, result_dict))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    
# Create a new dictionary with updated keys http to https
    updated_data_dict = {convert_to_https(key): value for key, value in result_dict.items()}
    df = pd.DataFrame.from_dict(updated_data_dict, orient='index', columns=['perf_desktop', 'access_desktop', 'seo_desktop', 'best_practice_desktop', 'perf_mobile', 'access_mobile', 'seo_mobile', 'best_practice_mobile'])
   
    df.index.name = 'Site'
  
    
    return df


