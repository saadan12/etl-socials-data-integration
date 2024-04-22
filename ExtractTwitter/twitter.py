import numpy as np
import tweepy
import pandas as pd
import re
import logging
from os import mkdir
import logging
# from obsei.analyzer import ZeroShotClassificationAnalyzer, ClassificationAnalyzerConfig
# from obsei.source import TwitterSourceConfig, TwitterSource, TwitterCredentials
from shared_code import storage_functions


class Twitter:
    def __init__(self, BEARER_TOKEN):
        self.api = tweepy.Client(bearer_token=BEARER_TOKEN)
        self.requests = 0

    # def get_sentiment(self, user_names, user_ids, twitter_cred_info):
    #     print("Analysing sentiment ...")
    #     print(user_ids)
    #     user_sentiment = {}
    #     neg_mention_num = 0
    #     pos_mention_num = 0
        
    #     # get past 7 days mentioned tweets, max_length = 100
    #     for user_id, user_name in zip(user_ids, user_names):
    #         try:
    #             print("Sentiment for " + str(user_id))
    #             source_config = TwitterSourceConfig(
    #                 # query="cocacola",
    #                 usernames=[f'@{user_name}'],
    #                 lookup_period="7d",
    #                 tweet_fields=[
    #                     "author_id",
    #                     "conversation_id",
    #                     "created_at",
    #                     "id",
    #                     "public_metrics",
    #                     "text",
    #                 ],
    #                 user_fields=["id", "name", "public_metrics", "username", "verified"],
    #                 expansions=["author_id"],
    #                 place_fields=None,
    #                 max_tweets=100,
    #                 cred_info=twitter_cred_info or None
    #             )

    #             source = TwitterSource()

    #             text_analyzer = ZeroShotClassificationAnalyzer(
    #                 model_name_or_path="typeform/mobilebert-uncased-mnli", device="auto"
    #             )

    #             analyzer_config = ClassificationAnalyzerConfig(
    #                 labels=["positive", "negative"],
    #                 add_positive_negative_labels=True,
    #             )

    #             source_response_list = source.lookup(source_config)
    #             # for idx, source_response in enumerate(source_response_list):
    #             #     logger.info(f"source_response#'{idx}'='{source_response.__dict__}'")

    #             analyzer_response_list = text_analyzer.analyze_input(
    #                 source_response_list=source_response_list,
    #                 analyzer_config=analyzer_config,
    #             )
    #             sentiment_dict = {}

    #             pos_tweets, neg_tweets = [], []
    #             for idx, an_response in enumerate(analyzer_response_list):
    #                 sentiment_dict['Positive'] = sentiment_dict.get('Positive', 0) + \
    #                                              an_response.segmented_data['classifier_data']['positive']
    #                 sentiment_dict['Negative'] = sentiment_dict.get('Negative', 0) + \
    #                                              an_response.segmented_data['classifier_data']['negative']
    #                 if an_response.segmented_data['classifier_data']['positive'] > \
    #                         an_response.segmented_data['classifier_data']['negative']:
    #                     pos_mention_num += 1
    #                     pos_tweets.append(an_response.meta['text'])
    #                 if an_response.segmented_data['classifier_data']['negative'] > \
    #                         an_response.segmented_data['classifier_data']['positive']:
    #                     neg_mention_num += 1
    #                     neg_tweets.append(an_response.meta['text'])

    #             for k, v in sentiment_dict.items():
    #                 sentiment_dict[k] = v / len(analyzer_response_list) if v else 0
    #             print(sentiment_dict)


    #             user_sentiment[user_id] = {"twitter_positive_sentiment": sentiment_dict.get('Positive', 0),
    #                                        "twitter_positive_mentions": pos_mention_num,
    #                                        "twitter_negative_sentiment": sentiment_dict.get('Negative', 0),
    #                                        "twitter_negative_mentions": neg_mention_num
    #                                        }
    #             neg_mention_num = 0
    #             pos_mention_num = 0
    #         except Exception as e:

    #             user_sentiment[user_id] = {"twitter_positive_sentiment": "error",
    #                                        "twitter_positive_mentions": "error",
    #                                        "twitter_negative_sentiment": "error",
    #                                        "twitter_negative_mentions": "error"
    #                                        }
    #             logging.exception("user id: " + str(user_id))
    #             print(e)
    #             pass
    #     print(user_sentiment)
    #     return user_sentiment

    def get_tweets(self, user_ids):
        print("GETTING TWEETS...")
        print(user_ids)
        user_dict = {}  # {"user id" : {public metrics}, ..}
        for user_id in user_ids:
            try:
                print("Getting tweet for " + str(user_id))
                response = self.api.get_users_tweets(id=user_id, exclude="retweets", max_results=100,
                                                     tweet_fields=['public_metrics'])
                self.requests += 1

                tweets_dict = {}
                for tweet in response.data:
                    for k, v in tweet.public_metrics.items():
                        tweets_dict[k] = tweets_dict.get(k, 0) + int(v)

                tweets = len(response.data)

                for k, v in tweets_dict.items():
                    tweets_dict[k] = v / tweets if v else 0

                user_dict[user_id] = {"twitter_avg_retweet_count": tweets_dict.get('retweet_count', 0),
                                      "twitter_avg_reply_count": tweets_dict.get('reply_count', 0),
                                      "twitter_avg_like_count": tweets_dict.get('like_count', 0),
                                      "twitter_avg_quote_count": tweets_dict.get('quote_count', 0)
                                      }
            except Exception as e:
                logging.warning(e)
                user_dict[user_id] = {"twitter_avg_retweet_count": "error",
                                      "twitter_avg_reply_count": "error",
                                      "twitter_avg_like_count": "error",
                                      "twitter_avg_quote_count": "error"
                                      }
                logging.exception("user id: " + str(user_id))
                pass
        print(user_dict)
        return user_dict

    def get_user_stats(self, usernames, twitter_cred_info):

        user_stats = {}
        for i in range(0, len(usernames), 100):
            temp_list = usernames[i:i + 100]
            response = self.api.get_users(usernames=temp_list, user_fields=['id', 'public_metrics'])
            self.requests += 1
            print(response)
            for user in response.data:
                temp_dict = user.data
                print(temp_dict)
                username = temp_dict.get("username", 0)
                username = username.lower()
                metrics_dict = temp_dict.get("public_metrics", 0)
                id = temp_dict.get("id")
                if metrics_dict:
                    user_stats[username] = {"twitter_id": id,
                                            "twitter_followers_count": metrics_dict.get("followers_count", 0),
                                            "twitter_following_count": metrics_dict.get("following_count", 0),
                                            "twitter_tweet_count": metrics_dict.get("tweet_count", 0),
                                            "twitter_listed_count": metrics_dict.get("listed_count", 0)
                                            }

        user_ids = []
        for k, v in user_stats.items():
            user_ids.append(v.get('twitter_id'))

        tweets_stat = self.get_tweets(user_ids)

        for k, v in user_stats.items():
            v.update(tweets_stat.get(v['twitter_id']))

        print(user_ids)
        # tweets_sentiment = self.get_sentiment(user_ids, twitter_cred_info)

        #tweets_sentiment = self.get_sentiment(usernames, user_ids, twitter_cred_info)

        #for k, v in user_stats.items():
        #    try:
        #        v.update(tweets_sentiment.get(v['twitter_id']))
        #        print("Sucesfull")
        #    except:
        #        pass

        print(user_stats)
        return user_stats


class TwitterDF:
    def __init__(self, df, key, twitter_cred_info, start=0, size=100):
        self.df = df[start:start + size]
        self.df[['twitter_id', 'twitter_followers_count', 'twitter_following_count', 'twitter_tweet_count',
                 'twitter_listed_count', 'twitter_avg_retweet_count', 'twitter_avg_reply_count',
                 'twitter_avg_like_count', 'twitter_avg_quote_count', 'twitter_positive_sentiment', 'twitter_positive_mentions',
                 'twitter_negative_sentiment', 'twitter_negative_mentions']] = np.nan
        self.key = key
        self.twitter_cred_info = twitter_cred_info
        self.start = start
        self.range = size

    def execute(self):
        try:
            print("API KEY: " + str(self.key))
            print("ROW NUMBER: " + str(self.start))
            tw = Twitter(self.key)

            df = self.df
            tw_df = df

            tw_df = tw_df.join(tw_df['twitter'].str.rpartition('twitter.com/'))
            print(tw_df)

            tw_df.rename(columns={2: 'twitter_username'}, inplace=True)

            tw_df['twitter_username'] = tw_df['twitter_username'].str.lower()
            if 0 in tw_df.columns:
                tw_df.drop(axis=1, columns=[0, 1], inplace=True)
            tw_df['twitter_username'] = tw_df['twitter_username'].str.replace('#!', '', regex=False)
            tw_df['twitter_username'] = tw_df['twitter_username'].str.replace('/', '', regex=False)
            tw_df['twitter_username'] = tw_df['twitter_username'].str.replace(r'[/?].*', '', regex=True)

            username_list = tw_df.twitter_username.tolist()
            regex = re.compile(r'^[A-Za-z0-9_]{1,15}$')
            filtered = [i for i in username_list if regex.search(i)]
            print(filtered)
            try:
                user_stats = tw.get_user_stats(filtered, self.twitter_cred_info)
            except Exception as e:
                logging.warning(e)
                pass

            stats_df = pd.DataFrame.from_dict(user_stats, orient='index')
            stats_df.reset_index(inplace=True)
            stats_df = stats_df.rename(columns={'index': 'twitter_username'})

            tw_df.set_index('twitter_username', inplace=True)
            tw_df.update(stats_df.set_index('twitter_username'))
            tw_df.reset_index(inplace=True)

            df.set_index('Site', inplace=True)
            df.update(tw_df.set_index('Site'))
            df.reset_index(inplace=True)
            df.drop(['twitter_id'], axis=1, inplace=True)

            return df
        except Exception as e:
            logging.warning(e)
            return self.df

def twitter(data_dict, config_dict):

    # Input
    az = storage_functions.AzureStorage(data_dict["container_name"])
    path = "{0}/{1}/{1}_{2}_{0}.csv".format(data_dict["timestamp"], "social_webscrapper", data_dict["container_name"])
    df = az.download_blob_df(path)
    try:
        twitter_key = config_dict["key"]

        # twitter_cred_info = TwitterCredentials(
        #     bearer_token=config_dict["key"],
        #     consumer_key=config_dict["api_key"],
        #     consumer_secret=config_dict["api_key_secret"]
        # )
        twitter_cred_info = "placeholder"

        tw = TwitterDF(df, twitter_key, twitter_cred_info)
        df = tw.execute()
    except Exception as e:
        logging.warning('General error on the twitter script: ', e)
        df[['twitter_id', 'twitter_followers_count', 'twitter_following_count', 'twitter_tweet_count',
                 'twitter_listed_count', 'twitter_avg_retweet_count', 'twitter_avg_reply_count',
                 'twitter_avg_like_count', 'twitter_avg_quote_count', 'twitter_positive_sentiment', 'twitter_positive_mentions',
                 'twitter_negative_sentiment', 'twitter_negative_mentions']] = 0

    df.fillna(0, inplace=True)

    # Output
    return df