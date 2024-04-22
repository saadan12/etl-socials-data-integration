import sqlalchemy


class Facebook_TblSchema:
    def __init__(self):
        schema_dict = {
            "id": {"sqlalchemy": sqlalchemy.types.BigInteger(), "pandas": "int64"},
            "social_media_id": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "int64",
            },
            "likes": {"sqlalchemy": sqlalchemy.types.BigInteger(), "pandas": "float"},
            "followers": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "avg_post_likes": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=False),
                "pandas": "float",
            },
            "avg_post_comments": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "avg_post_shares": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "fb_engagement_rate": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
        }
        self.pandas_dtypes = {k: schema_dict[k]["pandas"] for k in schema_dict.keys()}
        self.sqlalchemy_dtypes = {k: schema_dict[k]["sqlalchemy"] for k in schema_dict.keys()}


class Youtube_TblSchema:
    def __init__(self):
        schema_dict = {
            "id": {"sqlalchemy": sqlalchemy.types.BigInteger(), "pandas": "float"},
            "social_media_id": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "int64",
            },
            "video_count": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "view_count": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "subscriber_count": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "like_count": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "comment_count": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "youtube_engagement_rate": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },   
        }

        self.pandas_dtypes = {k: schema_dict[k]["pandas"] for k in schema_dict.keys()}
        self.sqlalchemy_dtypes = {k: schema_dict[k]["sqlalchemy"] for k in schema_dict.keys()}


class Instagram_TblSchema:
    def __init__(self):
        schema_dict = {
            "id": {"sqlalchemy": sqlalchemy.types.BigInteger(), "pandas": "int64"},
            "social_media_id": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "int64",
            },
            "posts": {"sqlalchemy": sqlalchemy.types.BigInteger(), "pandas": "float"},
            "followers": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "avg_post_likes": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "avg_post_comments": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "insta_engagement_rate": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },   
        }
        self.pandas_dtypes = {k: schema_dict[k]["pandas"] for k in schema_dict.keys()}
        self.sqlalchemy_dtypes = {k: schema_dict[k]["sqlalchemy"] for k in schema_dict.keys()}


class Twitter_TblSchema:
    def __init__(self):
        schema_dict = {
            "id": {"sqlalchemy": sqlalchemy.types.BigInteger(), "pandas": "int64"},
            "social_media_id": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "int64",
            },
            "followers_count": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "following_count": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "avg_retweet_count": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "avg_reply_count": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "avg_likes_count": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "listed_count": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "tweet_count": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "twitter_engagement_rate": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
        }

        self.pandas_dtypes = {k: schema_dict[k]["pandas"] for k in schema_dict.keys()}
        self.sqlalchemy_dtypes = {k: schema_dict[k]["sqlalchemy"] for k in schema_dict.keys()}


class SocialMedia_TblSchema:
    def __init__(self):
        schema_dict = {
            "social_id": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "int64",
            },
            "project_id": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "int64",
            },
            "company_id": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "int64",
            },
            "initial_date": {
                "sqlalchemy": sqlalchemy.types.DateTime(),
                "pandas": "datetime64[ns]",
            },
            "global_engagement_rate": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "total_followers": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "total_average_interactions": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "total_clicks": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
        }

        self.pandas_dtypes = {k: schema_dict[k]["pandas"] for k in schema_dict.keys()}
        self.sqlalchemy_dtypes = {k: schema_dict[k]["sqlalchemy"] for k in schema_dict.keys()}


class Seo_TblSchema:
    def __init__(self):
        schema_dict = {
            "seo_id": {"sqlalchemy": sqlalchemy.types.BigInteger(), "pandas": "int64"},
            "company_id": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "int64",
            },
            "initial_date": {
                "sqlalchemy": sqlalchemy.types.DateTime(),
                "pandas": "datetime64[ns]",
            },
            "organic_traffic": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "web_authority": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "total_keywords": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "avg_keywords_search": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "traffic_value": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "paid_traffic": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "estimatedCPC": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "paid_keywords": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "estm_ppc_budget": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "backlinks": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "referring_domains": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "avg_organic_rank": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
        }
        self.pandas_dtypes = {k: schema_dict[k]["pandas"] for k in schema_dict.keys()}
        self.sqlalchemy_dtypes = {k: schema_dict[k]["sqlalchemy"] for k in schema_dict.keys()}


class Website_TblSchema:
    def __init__(self):
        schema_dict = {
            "website_id": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "company_id": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "initial_date": {
                "sqlalchemy": sqlalchemy.types.DateTime(),
                "pandas": "datetime64[ns]",
            },
            "mobile_page_speed": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "desktop_page_speed": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "bounce_rate": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "monthly_traffic": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "pages_visit": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "avg_TimeOnSite": {
                "sqlalchemy": sqlalchemy.types.NVARCHAR(length=255),
                "pandas": "object",
            },
        }

        self.pandas_dtypes = {k: schema_dict[k]["pandas"] for k in schema_dict.keys()}
        self.sqlalchemy_dtypes = {k: schema_dict[k]["sqlalchemy"] for k in schema_dict.keys()}


class WebsiteTraffic_TblSchema:
    def __init__(self):
        schema_dict = {
            "id": {"sqlalchemy": sqlalchemy.types.BigInteger(), "pandas": "float"},
            "website_id": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "int64",
            },
            "direct_traffic": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "paid_traffic": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "organic_traffic": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "social_traffic": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "reffered_traffic": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "mail_traffic": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "country_first": {
                "sqlalchemy": sqlalchemy.types.VARCHAR(length=255),
                "pandas": "object",
            },
            "country_second": {
                "sqlalchemy": sqlalchemy.types.VARCHAR(length=255),
                "pandas": "object",
            },
            "country_third": {
                "sqlalchemy": sqlalchemy.types.VARCHAR(length=255),
                "pandas": "object",
            },
            "country_forth": {
                "sqlalchemy": sqlalchemy.VARCHAR(length=255),
                "pandas": "object",
            },
            "country_fifth": {
                "sqlalchemy": sqlalchemy.VARCHAR(length=255),
                "pandas": "object",
            },
            "country_value_first": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "country_value_second": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "country_value_third": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "country_value_forth": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "country_value_fifth": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "social_first": {
                "sqlalchemy": sqlalchemy.types.VARCHAR(length=255),
                "pandas": "object",
            },
            "social_second": {
                "sqlalchemy": sqlalchemy.types.VARCHAR(length=255),
                "pandas": "object",
            },
            "social_third": {
                "sqlalchemy": sqlalchemy.types.VARCHAR(length=255),
                "pandas": "object",
            },
            "social_value_first": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "social_value_second": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
            "social_value_third": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            },
        }

        self.pandas_dtypes = {k: schema_dict[k]["pandas"] for k in schema_dict.keys()}
        self.sqlalchemy_dtypes = {k: schema_dict[k]["sqlalchemy"] for k in schema_dict.keys()}


class CompanyWiseScores_TblSchema:
    def __init__(self):
        schema_dict = {
            "id": {"sqlalchemy": sqlalchemy.types.BigInteger(), "pandas": "int64"},
            "company_id": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "int64",
            },
            "project_id": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "int64",
            },
            "initial_date": {
                "sqlalchemy": sqlalchemy.types.DateTime(),
                "pandas": "datetime64[ns]",
            },
            "global_score": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "website_score": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "sm_score": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "sm_facebook_score": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "sm_instagram_score": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "sm_youtube_score": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "sm_twitter_score": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "seo_score": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
            "searchAds_score": {
                "sqlalchemy": sqlalchemy.types.Float(precision=2, asdecimal=True),
                "pandas": "float",
            },
        }
        self.pandas_dtypes = {k: schema_dict[k]["pandas"] for k in schema_dict.keys()}
        self.sqlalchemy_dtypes = {k: schema_dict[k]["sqlalchemy"] for k in schema_dict.keys()}


class Company_TblSchema:
    def __init__(self):
        schema_dict = {
            "url": {"sqlalchemy": sqlalchemy.types.VARCHAR(length=255),
                    "pandas": "object"},
            "facebook_url": {
                "sqlalchemy": sqlalchemy.types.VARCHAR(length=255),
                "pandas": "object",
            },
            "instagram_url": {
                "sqlalchemy": sqlalchemy.types.VARCHAR(length=255),
                "pandas": "object",
            },
            "twitter_url": {
                "sqlalchemy": sqlalchemy.types.VARCHAR(length=255),
                "pandas": "object",
            },
            "youtube_url": {
                "sqlalchemy": sqlalchemy.types.VARCHAR(length=255),
                "pandas": "object",
            }
        }
        self.pandas_dtypes = {k: schema_dict[k]["pandas"] for k in schema_dict.keys()}
        self.sqlalchemy_dtypes = {k: schema_dict[k]["sqlalchemy"] for k in schema_dict.keys()}


class SL_TblSchema:
    def __init__(self):
        schema_dict = {
            "project_id": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "int64",
            },
            "modified_date": {
                "sqlalchemy": sqlalchemy.types.DateTime(),
                "pandas": "datetime64[ns]",
            },
            "facebook_url": {
                "sqlalchemy": sqlalchemy.types.VARCHAR(length=255),
                "pandas": "object",
            },
            "instagram_url": {
                "sqlalchemy": sqlalchemy.types.VARCHAR(length=255),
                "pandas": "object",
            },
            "twitter_url": {
                "sqlalchemy": sqlalchemy.types.VARCHAR(length=255),
                "pandas": "object",
            },
            "youtube_url": {
                "sqlalchemy": sqlalchemy.types.VARCHAR(length=255),
                "pandas": "object",
            },
            "company_id": {
                "sqlalchemy": sqlalchemy.types.BigInteger(),
                "pandas": "float",
            }
        }
        self.pandas_dtypes = {k: schema_dict[k]["pandas"] for k in schema_dict.keys()}
        self.sqlalchemy_dtypes = {k: schema_dict[k]["sqlalchemy"] for k in schema_dict.keys()}
