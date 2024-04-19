from django.db import models


class Performance(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        'Project', on_delete=models.CASCADE, null=False)
    initial_date = models.DateTimeField(auto_now=True)
    performance_date = models.DateTimeField(auto_now=False)
    web_mobile_page_speed = models.FloatField(max_length=255, blank=True)
    web_desktop_page_speed = models.FloatField(max_length=255, blank=True)
    web_bounce_rate = models.FloatField(max_length=255, blank=True)
    web_monthly_traffic = models.FloatField(max_length=255, blank=True)
    web_pages_visit = models.FloatField(max_length=255, blank=True)
    web_avg_time = models.FloatField(max_length=255, blank=True)
    web_mail_traffic = models.FloatField(max_length=255, blank=True)
    web_referred_traffic = models.FloatField(max_length=255, blank=True)
    web_social_traffic = models.FloatField(max_length=255, blank=True)
    web_organic_traffic = models.FloatField(max_length=255, blank=True)
    web_paid_traffic = models.FloatField(max_length=255, blank=True)
    web_direct_traffic = models.FloatField(max_length=255, blank=True)
    seo_organic_traffic = models.FloatField(max_length=255, blank=True)
    seo_w_authority = models.FloatField(max_length=255, blank=True)
    seo_total_keywords = models.FloatField(max_length=255, blank=True)
    seo_avg_organic_rank = models.FloatField(max_length=255, blank=True)
    seo_referring_domains = models.FloatField(max_length=255, blank=True)
    seo_backlinks = models.FloatField(max_length=255, blank=True)
    paid_paid_traffic = models.FloatField(max_length=255, blank=True)
    paid_est_cpc_links = models.FloatField(max_length=255, blank=True)
    paid_paid_keywords = models.FloatField(max_length=255, blank=True)
    paid_est_ppc_budget = models.FloatField(max_length=255, blank=True)
    social_engagement_rate = models.FloatField(max_length=255, blank=True)
    social_total_followers = models.FloatField(max_length=255, blank=True)
    social_total_interactions = models.FloatField(max_length=255, blank=True)
    social_total_clicks = models.FloatField(max_length=255, blank=True)
    facebook_total_followers = models.FloatField(max_length=255, blank=True)
    facebook_total_page_likes = models.FloatField(max_length=255, blank=True)
    facebook_avg_post_likes = models.FloatField(max_length=255, blank=True)
    facebook_avg_post_shares = models.FloatField(max_length=255, blank=True)
    facebook_avg_post_comments = models.FloatField(max_length=255, blank=True)
    instagram_total_followers = models.FloatField(
        max_length=255,
        blank=True,
        null=True
    )
    instagram_total_posts = models.FloatField(
        max_length=255,
        blank=True,
        null=True
    )
    instagram_avg_likes = models.FloatField(
        max_length=255,
        blank=True,
        null=True
    )
    instagram_avg_comments = models.FloatField(
        max_length=255,
        blank=True,
        null=True
    )
    twitter_total_followers = models.FloatField(
        max_length=255,
        blank=True,
        null=True
    )
    twitter_total_following = models.FloatField(
        max_length=255,
        blank=True,
        null=True
    )
    twitter_avg_retweets = models.FloatField(
        max_length=255,
        blank=True,
        null=True
    )
    twitter_avg_replies = models.FloatField(
        max_length=255,
        blank=True,
        null=True
    )
    twitter_avg_likes = models.FloatField(
        max_length=255,
        blank=True,
        null=True
    )
    twitter_tweet_count = models.FloatField(
        max_length=255,
        blank=True,
        null=True
    )
    youtube_total_videos = models.FloatField(
        max_length=255,
        blank=True,
        null=True
    )
    youtube_total_views = models.FloatField(
        max_length=255,
        blank=True,
        null=True
    )
    youtube_total_likes = models.FloatField(
        max_length=255,
        blank=True,
        null=True
    )
    youtube_subscriber_count = models.FloatField(
        max_length=255,
        blank=True,
        null=True
    )
