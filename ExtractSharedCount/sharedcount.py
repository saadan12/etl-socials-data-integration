import pandas as pd
from sharedcountsdk import SharedCountApi
import logging

# Is function that is only for premium and is for extracted a list of urls
# urls = ["https://www.landsend.com", "https://www.bagborroworsteal.com"]
# bulkPostResponse = sharedCountApiInstance.bulkPost(urls);
# print(bulkPostResponse)


def get_share(url, sharedCountApiInstance):
    try:
        urlGetResponse = sharedCountApiInstance.get(url)
        print(url)
        print(urlGetResponse)
        total_count = urlGetResponse["Facebook"]["total_count"]
        comment_count = urlGetResponse["Facebook"]["comment_count"]
        share_count = urlGetResponse["Facebook"]["share_count"]
        reaction_count = urlGetResponse["Facebook"]["reaction_count"]
        pinterest = urlGetResponse.get("Pinterest", 0)
        return [comment_count, share_count, reaction_count, pinterest]
    except Exception as e:
        logging.warning("Error retrieving metrics from SharedCount",  extra={"url": url})
        return ["error"] * 4


def sharedcount(data_dict, config_dict):

    key = config_dict["key"]
    site_list = data_dict["site_list"]

    sharedCountApiInstance = SharedCountApi(key)
    status = sharedCountApiInstance.status()
    logging.info("SharedCount connection",  extra={"status": status})

    df = pd.DataFrame(site_list, columns=['Site'])

    df[['comment_count', 'share_count', 'reaction_count', 'pinterest']] = df.apply(
        lambda row: get_share(row["Site"], sharedCountApiInstance), axis=1, result_type="expand")

    return df