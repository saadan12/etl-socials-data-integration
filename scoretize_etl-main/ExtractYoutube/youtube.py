from googleapiclient.discovery import build
import numpy as np
import pandas as pd
from googleapiclient import errors
import glob
import time
import logging
from os import mkdir
from shared_code import storage_functions
import concurrent.futures

class Youtube:
    def __init__(self, key):
        self.youtube = build('youtube', 'v3', developerKey=key)
        self.quota = 0

    def get_video_details(self, channel_id):
        """Returns a dictionary with the statistical information about the videos of a channel.

        Requests the playlist id of a channel,
        then all the video ids of that playlist,
        then the statistics of all the videos.

        Args:
            channel_id (list): List of channel IDs

        Returns:
            video_info (dict): video_info is a dictionary with the sum of comments, likes,
              dislikes and favorites of all the videos in the channel
        """
        playlist = {}  # {"channel id" : "playlist id", ..}
        for i in range(0, len(channel_id), 50):
            response = self.youtube.channels().list(part="contentDetails", id=channel_id, maxResults=50).execute()
            self.quota += 1
            for i in response['items']:
                playlist[i['id']] = i["contentDetails"]["relatedPlaylists"]["uploads"]

        print("Getting video IDs...")
        video_dict = {}  # {"channel id": [list of video ids]}
        for c_id, playlist_id in playlist.items():
            print("Channel ID: " + str(c_id))
            try:
                all_videos = []
                next_page_token = None

                while True:
                    res = self.youtube.playlistItems().list(playlistId=playlist_id, part='snippet', maxResults=50,
                                                            pageToken=next_page_token).execute()
                    all_videos += res['items']
                    next_page_token = res.get('nextPageToken')

                    self.quota += 1

                    if next_page_token is None:
                        break

                video_ids = list(map(lambda x: x['snippet']['resourceId']['videoId'], all_videos))
                video_dict[c_id] = video_ids
            except errors.HttpError as e:
                if e.resp.status == 403:
                    print(e)
                    raise
                else:
                    print(e)
                    pass
            except:
                logging.error(f"Error in get_video_details")

        # Get stats all videos and add them all in one dictionary
        print("Getting video statistics...")
        video_stats = {}  # {"channel id": {dictionary with total video stats}}
        for c_id, list_videos in video_dict.items():
            print("Channel ID: " + str(c_id))
            try:
                all_videos = []
                for i in range(0, len(list_videos), 50):
                    temp_list = list_videos[i:i + 50]

                    res = self.youtube.videos().list(id=temp_list, part='statistics', maxResults=50).execute()
                    for item in res['items']:
                        all_videos.append(item)

                    self.quota += 1

                print("Channel ID: " + str(c_id) + " has " + str(len(all_videos)) + " number of videos.")
                total_stats = {}
                for i in all_videos:
                    stats = i.get('statistics')
                    for k, v in stats.items():
                        total_stats[k] = total_stats.get(k, 0) + int(v)

                final_stats = {"youtube_favorite_count": total_stats.get('favoriteCount', 0),
                               "youtube_comment_count": total_stats.get('commentCount', 0),
                               "youtube_like_count": total_stats.get('likeCount', 0),
                               "youtube_dislike_count": total_stats.get('dislikeCount', 0)
                               }
                video_stats[c_id] = final_stats
            except errors.HttpError as e:
                if e.resp.status == 403:
                    print(e)
                    raise
                else:
                    print(e)
                    pass
            except:
                logging.error(f"Error in get_video_details")

        print("Done. \nQuota use: " + str(self.quota))
        return video_stats

    def get_channel_details(self, channel_id):
        try:
            """Returns a dictionary with all of the statistical information of a channel.

            Requests the statistics of a channel,
            then calls get_video_details() to get the statistics of all the videos of the channel.

            Args:
                channel_id (list): List of channel IDs

            Returns:
                info_dict (dict): info_dict is a dictionary with the sum of videos, views, subscribers, comments, likes,
                dislikes and favorites of the channel
            """
            print("Getting channel statistics...")
            info_dict = {}
            for i in range(0, len(channel_id), 50):
                temp_list = channel_id[i:i + 50]
                response = self.youtube.channels().list(part="snippet,statistics", id=temp_list, maxResults=50).execute()
                self.quota += 1

                for item in response['items']:
                    temp_stats = item['statistics']
                    info_dict[item['id']] = {"youtube_video_count": temp_stats.get('videoCount', 0),
                                            "youtube_view_count": temp_stats.get('viewCount', 0),
                                            "youtube_subscriber_count": temp_stats.get('subscriberCount', 0),
                                            'title': item['snippet']['title']}

            print("Done. \nQuota use: " + str(self.quota))
            video_stats = self.get_video_details(channel_id)

            for k, v in video_stats.items():
                info_dict[k].update(v)

            return info_dict
        except Exception as e:
            logging.error(f"Error in ExtractYoutube get_channel_details func.  {e}")

    def find_channel_id(self, user_id, custom=False):
        try:
            if custom:
                response = self.youtube.search().list(
                    part="snippet",
                    maxResults=1,
                    q=user_id,
                    type="channel",
                ).execute()
                resp = response.get('items')

                self.quota += 100

                if resp:
                    channel_id = resp[0]['snippet']['channelId']
                else:
                    channel_id = np.NaN
                return channel_id
            else:
                resp = self.youtube.channels().list(
                    forUsername=user_id,
                    part='id',
                    fields='items(id)',
                    maxResults=1
                ).execute()
                resp = resp.get('items')

                self.quota += 1

                if resp:
                    channel_id = resp[0]['id']
                else:
                    channel_id = np.NaN
                return channel_id
        except Exception as e:
            logging.error(f"Error in ExtractYoutube find_channelid func. {e}")


class YoutubeDF:
    def __init__(self, df, key, start=0, size=100):
        self.df = df[start:start + size]
        self.df[['youtube_video_count', 'youtube_view_count', 'youtube_subscriber_count', 'title',
                 'youtube_favorite_count', 'youtube_comment_count', 'youtube_like_count',
                 'youtube_dislike_count']] = np.nan
        self.key = key
        self.start = start
        self.range = size

        self.channel_df = None
        self.user_df = None
        self.custom_df = None

    def partition(self):
        try:
            self.channel_df = self.df[self.df['youtube'].str.contains("/channel/")]
            self.channel_df = self.channel_df.join(self.channel_df['youtube'].str.rpartition('/channel/'))
            self.channel_df.rename(columns={2: 'channel_id'}, inplace=True)
            if 0 in self.channel_df.columns:
                self.channel_df.drop(axis=1, columns=[0, 1], inplace=True)
            self.channel_df['channel_id'] = self.channel_df['channel_id'].str.replace(r'[/?].*', '', regex=True)
        except KeyError:
            pass

        try:
            self.user_df = self.df[self.df['youtube'].str.contains("/user/")]
            self.user_df = self.user_df.join(self.user_df['youtube'].str.rpartition('/user/'))
            self.user_df.rename(columns={2: 'user_id'}, inplace=True)
            if 0 in self.user_df.columns:
                self.user_df.drop(axis=1, columns=[0, 1], inplace=True)
            self.user_df['user_id'] = self.user_df['user_id'].str.replace(r'[/?].*', '', regex=True)
        except KeyError:
            pass

        try:
            self.custom_df = self.df[~self.df['youtube'].str.contains("Not Found")]
            self.custom_df = self.custom_df[~self.custom_df['youtube'].str.contains("/user/")]
            self.custom_df = self.custom_df[~self.custom_df['youtube'].str.contains("/channel/")]
            self.custom_df = self.custom_df.join(self.custom_df['youtube'].str.rpartition('youtube.com/'))
            self.custom_df.rename(columns={2: 'custom_id'}, inplace=True)
            if 0 in self.custom_df.columns:
                self.custom_df.drop(axis=1, columns=[0, 1], inplace=True)
            self.custom_df['custom_id'] = self.custom_df['custom_id'].str.replace(r'c/', '', regex=True)
            self.custom_df['custom_id'] = self.custom_df['custom_id'].str.replace(r'[/?].*', '', regex=True)
            self.custom_df['custom_id'] = self.custom_df['custom_id'].replace(r'^(watch|playlist|results)$', np.nan,
                                                                            regex=True)
            self.custom_df = self.custom_df[self.custom_df['custom_id'].notna()]
        except KeyError:
            pass
    
    

    def execute(self):
        import concurrent.futures
        """Returns a dataframe with the statistical information of each youtube url.

        Partitions the dataframe between channel, users and custom links.
        Then requests the channel id of all users and custom links iterating on all the rows (no batch available)
        Then requests the channel information of all channel ids in batch

        Returns:
            df (pd.DataFrame): df is the dataframe loaded on the object with the statistical information of each url
        """

        print("API KEY: " + str(self.key))
        print("ROW NUMBER: " + str(self.start))
        yt = Youtube(self.key)
        self.partition()
        print("Searching channel ids from user ids...")
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = executor.map(lambda row: yt.find_channel_id(row['user_id']), self.user_df.to_dict('records'))
            self.user_df['channel_id'] = list(results)
            print(f"Threading result: {self.user_df}")
            print("Done. \nQuota use: " + str(yt.quota))
        except Exception as e:
            logging.error(f"ExtractYoutube Multithreading process error: {e}")
            pass
        
        print("Searching channel ids from custom ids...")
        try:
            self.custom_df['channel_id'] = self.custom_df.apply(
                lambda row: yt.find_channel_id(row['custom_id'], custom=True),
                axis=1)
            print("Done. \nQuota use: " + str(yt.quota))
        except Exception as e:
            logging.error(f"ExtractYoutube Execute func. error: {e}")

    
        concat_df = pd.concat([self.channel_df, self.user_df, self.custom_df])
        channel_ids = concat_df['channel_id'].dropna().tolist()

        temp_dict = yt.get_channel_details(channel_ids)
        stats_df = pd.DataFrame.from_dict(temp_dict, orient='index')
        stats_df.reset_index(inplace=True)
        stats_df = stats_df.rename(columns={'index': 'channel_id'})

        concat_df.set_index('channel_id', inplace=True)
        concat_df.update(stats_df.set_index('channel_id'))
        concat_df.reset_index(inplace=True)
        df = self.df
        df[['channel_id', 'user_id', 'custom_id']] = np.nan

        df.set_index('Site', inplace=True)
        df.update(concat_df.set_index('Site'))
        df.reset_index(inplace=True)
        df.drop(['channel_id', 'user_id', 'custom_id', 'title'], axis=1, inplace=True)

        print("QUOTA USE: " + str(yt.quota))
        return df




def youtube(data_dict, config_dict, start=0, size=100):

    # Input
    az = storage_functions.AzureStorage(data_dict["container_name"])
    path = "{0}/{1}/{1}_{2}_{0}.csv".format(data_dict["timestamp"], "social_webscrapper", data_dict["container_name"])
    df = az.download_blob_df(path)

    # Read youtube api keys
    key = config_dict["key"]

    try:
        ydf = YoutubeDF(df, key, start, size)
        final_df = ydf.execute()
    except Exception as e:
        print("YOUTUBE ERROR: " + str(e))
        logging.error(f"Error in ExtractYoutube youtube func. {e}")
        final_df = df
        final_df[['youtube_video_count', 'youtube_view_count', 'youtube_subscriber_count', 'title',
                 'youtube_favorite_count', 'youtube_comment_count', 'youtube_like_count',
                 'youtube_dislike_count']] = 0



    final_df.fillna(0, inplace=True)

    return final_df