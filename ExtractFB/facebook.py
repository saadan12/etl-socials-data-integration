import pandas as pd
from facebook_scraper import get_page_info, get_posts, set_proxy
import numpy as np
from shared_code import storage_functions, get_proxy
import logging
from random import randint
import requests
from urllib3 import exceptions


def get_likes_followers(urls):
    try:
        url = "https://facebook-company-data.p.rapidapi.com/fbAboutData"

        payload = {"FBUrls": urls}
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Host": "facebook-company-data.p.rapidapi.com",
            "X-RapidAPI-Key": "9c33b473demsh0fd262e6ed2a3f0p1ab63cjsn8e3f12e367ad",
        }
        response = requests.request("POST", url, json=payload, headers=headers)
        print(response)
        res = response.json()["results"]
        print(res)
        return res
    except Exception as e:
        logging.warning("fb rapid api error:" + str(e))
        return ["error"] * 2


# https://github.com/tnychn/instascrape


def fb_scraper(page, fb_url, proxy, n_posts, attempt):
    try:
        print("Scrapping " + str(page) + " ...")
        set_proxy(proxy)
        # Get page information
        # page_info = get_page_info(page)
        # time.sleep(randint(4, 10))
        # Create post generator. Must iterate over generator to get post information
        posts_gen = get_posts(page, options={"posts_per_page": n_posts})
        # Iterate through post generator until start hits n_posts. Information stored in posts_dict
        posts_dict = {}  # {"avg_post_likes": likes(int), ...}
        start = 0
        for i in posts_gen:
            if start == n_posts:
                break
            # print(i)
            likes = i.get("likes", 0)
            if likes is None:
                likes = 0
            comments = i.get("comments", 0)
            if comments is None:
                comments = 0
            shares = i.get("shares", 0)
            if shares is None:
                shares = 0
            posts_dict["post_likes"] = posts_dict.get("post_likes", 0) + likes
            posts_dict["comments"] = posts_dict.get("comments", 0) + comments
            posts_dict["shares"] = posts_dict.get("shares", 0) + shares
            posts_dict[start] = i
            start += 1
        # Fix dictionary and create average
        # posts_dict["followers"], posts_dict["likes"] = get_followers(fb_url)
        # posts_dict["likes"] = page_info.get("likes", "error")
        posts_dict["avg_post_likes"] = posts_dict.get("post_likes", 0) / n_posts
        posts_dict["avg_comments"] = posts_dict.get("comments", 0) / n_posts
        posts_dict["avg_shares"] = posts_dict.get("shares", 0) / n_posts
        # print(posts_dict)

        return [
            posts_dict["avg_post_likes"],
            posts_dict["avg_comments"],
            posts_dict["avg_shares"],
        ]

    except Exception as e:
        # if there is proxy error, we rotate the proxy. max retry times: 2
        if (
            e == requests.exceptions.ConnectionError
            or requests.exceptions.ProxyError
            or requests.exceptions.ConnectTimeout
            or exceptions.MaxRetryError
            or exceptions.ConnectTimeoutError
            or exceptions.ProxyError
            or exceptions.ReadTimeoutError
        ):
            if attempt < 1:
                attempt += 1
                proxy = get_proxy.get_proxy()
                return fb_scraper(page, fb_url, proxy, n_posts, attempt)
            else:
                logging.warning("fb proxy error:" + str(e))
                return ["error"] * 3
        else:
            logging.warning("fb proxy error:" + str(e))
            return ["error"] * 3


def prepare_df(df):
     # Create a df without missing facebook links
    facebook_df = df

    # Get the profile name from the facebook link
    facebook_df = facebook_df.join(df["facebook"].str.rpartition("facebook.com/"))

    # Rename the profile column, delete unnecessary columns
    facebook_df.rename(columns={2: "facebook_profile"}, inplace=True)
    if 0 in facebook_df.columns:
        facebook_df.drop(axis=1, columns=[0, 1], inplace=True)

    # Clean profile name
    facebook_df["facebook_profile"] = facebook_df["facebook_profile"].str.replace(
        r"[/?].*", "", regex=True
    )

    # only scaper non-empty fb profile
    mask = facebook_df["facebook_profile"] != "Not Found"
    facebook_df = facebook_df.loc[mask]

    return facebook_df


def response_to_df(res):
    df_list = []

    for item in res:
        for k, v in item.items():
            try:
                temp = {"facebook": k, "fb_likes": v["follower_count"], "fb_followers": v["page_likers"]["global_likers_count"]}
                df_list.append(temp)
            except:
                temp = {"facebook": k, "fb_likes": v.get('Likes'), "fb_followers": v.get('Followers')}
                df_list.append(temp)

    df = pd.DataFrame(df_list)

    return df



def facebook(data_dict, config_dict, n_posts=5):

    # Input
    az = storage_functions.AzureStorage(data_dict["container_name"])
    path = "{0}/{1}/{1}_{2}_{0}.csv".format(
        data_dict["timestamp"], "social_webscrapper", data_dict["container_name"]
    )
    df = az.download_blob_df(path)
    cookies = config_dict

    try:
        proxy = get_proxy.get_proxy()
        attempt = 0

        # Create a df without missing facebook links
        facebook_df = prepare_df(df)

        res = get_likes_followers(facebook_df["facebook"].to_list())

        res_df = response_to_df(res)

        facebook_df = facebook_df.join(res_df.set_index('facebook'), on="facebook")

        facebook_df[
            ["fb_avg_post_likes", "fb_avg_post_comments", "fb_avg_post_shares"]
        ] = facebook_df.apply(
            lambda row: fb_scraper(
                row["facebook_profile"], row["facebook"], proxy, n_posts, attempt
            ),
            axis=1,
            result_type="expand",
        )

        # Create empty columns in the dataframe to update it
        df[
            [
                "fb_likes",
                "fb_followers",
                "fb_avg_post_likes",
                "fb_avg_post_comments",
                "fb_avg_post_shares",
            ]
        ] = np.nan

        logging.info(
            "Facebook df columns: " + str(facebook_df.columns),
            extra={"df_info": facebook_df.info()},
        )

        # Update final dataframe with the resulting dataframe from the apply function
        df.set_index("Site", inplace=True)
        # df.update(facebook_df)
        df.update(facebook_df.set_index("Site"))
        df.reset_index(inplace=True)

    except Exception as e:
        logging.warning("General error on fb script: " + str(e))
        df[
            [
                "fb_likes",
                "fb_followers",
                "fb_avg_post_likes",
                "fb_avg_post_comments",
                "fb_avg_post_shares",
            ]
        ] = 0

    df.fillna(0, inplace=True)

    # Output
    return df