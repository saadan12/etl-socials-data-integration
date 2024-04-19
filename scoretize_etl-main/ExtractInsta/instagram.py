import pandas as pd
from instascrape import *
import numpy as np
import time
from random import randint
from shared_code import storage_functions
import logging
import requests
import random
# https://github.com/chris-greening/instascrape


def scaper(page, headers, attempt):
    try:

        url = "https://instagram-data1.p.rapidapi.com/user/info"

        querystring = {"username":page}

        response = requests.request("GET", url, headers=headers, params=querystring)
        res = response.json()
        like_count, comment_count = 0 ,0
        for media in res['edge_owner_to_timeline_media']['edges'][:12]:
            like_count += media['node']['edge_liked_by']['count']
            comment_count += media['node']['edge_media_to_comment']['count']

        avg_like_count = like_count/12
        avg_comment_count = comment_count/12

        return [res['edge_followed_by']['count'], res['edge_owner_to_timeline_media']['count'], avg_like_count, avg_comment_count]

    except Exception as e:
        # if api has error, rerun the function, max retry: 2 times
        if attempt < 2:
            attempt += 1
            logging.warning(f'ig scaper rapid api error:+ {str(e)}, retry {attempt} time(s)')
            return scaper(page, headers, attempt)
        else:
            logging.warning('ig scaper rapid api error:' + str(e))
            return ['error'] * 4
        
def instagram(data_dict, config_dict):

    # Input
    az = storage_functions.AzureStorage(data_dict["container_name"])
    path = "{0}/{1}/{1}_{2}_{0}.csv".format(data_dict["timestamp"], "social_webscrapper", data_dict["container_name"])
    df = az.download_blob_df(path)
    headers = config_dict
    instagram_df = df[~df['instagram'].str.contains('Not Found')]
    attempt = 0
    if len(instagram_df) == 0:
        df[["insta_followers", "insta_posts", "insta_avg_post_likes", "insta_avg_post_comments"]] = 0
    else:
        # instagram_df = df

        # Get the profile name from the facebook link
        instagram_df["instagram"].str.rpartition("instagram.com/")
        instagram_df = instagram_df.join(df['instagram'].str.rpartition('instagram.com/'))

        # Rename the profile column, delete unnecessary columns
        instagram_df.rename(columns={2: 'instagram_profile'}, inplace=True)
        if 0 in instagram_df.columns:
            instagram_df.drop(axis=1, columns=[0, 1], inplace=True)

        # Clean profile name
        instagram_df['instagram_profile'] = instagram_df['instagram_profile'].str.replace(r'[/?].*', '', regex=True)

        # Apply the insta_scraper() function to the dataframe, row by row
        instagram_df[["insta_followers", "insta_posts", "insta_avg_post_likes", "insta_avg_post_comments"]] \
            = instagram_df.apply(lambda row: scaper(row["instagram_profile"], headers, attempt), axis=1, result_type="expand")

        # Create empty columns in the dataframe to update it
        df[["insta_followers", "insta_posts", "insta_avg_post_likes", "insta_avg_post_comments"]] = np.nan

        # Update final dataframe with the resulting dataframe from the apply function
        logging.info("Instagram df columns: " + str(instagram_df.columns), extra={"df_info": instagram_df.info()})
        df.set_index("Site", inplace=True)
        df.update(instagram_df.set_index('Site'))
        df.reset_index(inplace=True)

    df.fillna(0, inplace=True)

    return df