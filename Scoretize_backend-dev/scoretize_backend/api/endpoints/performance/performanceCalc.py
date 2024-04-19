from ...views import viewsets, APIView, IsAuthenticated,\
                    action, Website, end_date_values,\
                    start_date_values,\
                    Project, http_ok, Seo, Q,\
                    Website_traffic, Social_media, Facebook,\
                    PerformanceSerializer, bad_request,\
                    IntegrityError, Instagram, Twitter,\
                    Youtube, Company_wise_scores


class PerformanceCalc(viewsets.ViewSet, APIView):

    @action(methods=["PUT"], detail=False, url_path="calc")
    def store_performance_kpis_general(self, request):
        """
        Endpoint to calculate the Performance KPIs.
        Valid retroactively. Start-date / End-date.
        """

        self.query_params = self.request.query_params
        self.start_date = self.query_params.get("start_date", None)
        self.end_date = self.query_params.get("end_date", None)

        start_full_date = start_date_values(self.start_date, self.end_date)
        end_full_date = end_date_values(self.end_date)

        projects = Project.objects.all().values()

        # Extract the companies id for every project.
        for project in projects:
            if project["is_active"] != 1 and project["is_active"] != 3 or project["id"] > 149:
                pass
            else:
                performance_dict = {}
                project_id = project["id"]
                performance_dict["project"] = project_id
                companies_ids = []
                company_id = project["company_id"]
                companies_ids.append(company_id)

                for key, value in project.items():
                        if 'competitor' in key and value is not None:
                            companies_ids.append(value)

                performance_dict["social_key_first"] = ''
                performance_dict["social_total_followers"] = ''
                performance_dict["social_key_third"] = ''
                performance_dict["facebook_total_followers"] = ''
                performance_dict["facebook_total_page_likes"] = ''

                project_first_date_temp = Company_wise_scores.objects.filter(
                    project=project_id).order_by('initial_date').values(
                    'initial_date').first()

                if project_first_date_temp is None:
                    start_full_date = start_date_values(self.start_date, self.end_date)
                    end_full_date = end_date_values(self.end_date)
                else:
                    start_full_date = project_first_date_temp["initial_date"]

                # Calculate Seo Performance KPIs
                seo_companies_data = []
                for company in companies_ids:
                    seo_data = Seo.objects.filter(
                                                    Q(company_id=company) &
                                                    Q(initial_date__range=(
                                                        start_full_date,
                                                        end_full_date
                                                    ))
                                                ).values().last()
                    seo_companies_data.append(seo_data)
                if None in seo_companies_data or len(seo_companies_data) == 1:
                    pass
                else:

                    seo_organic_traffic = []
                    seo_total_keywords = []
                    seo_w_authority = []
                    seo_avg_organic_rank = []
                    seo_referring_domains = []
                    seo_backlinks = []

                    paid_paid_traffic = []
                    paid_est_cpc_links = []
                    paid_paid_keywords = []
                    paid_est_ppc_budget = []

                    for seo_data in seo_companies_data:
                        if len(seo_companies_data) == len(companies_ids):

                            seo_organic_traffic.append(seo_data["organic_traffic"])
                            seo_total_keywords.append(seo_data["total_keywords"])
                            seo_w_authority.append(seo_data["web_authority"])
                            seo_avg_organic_rank.append(seo_data["avg_organic_rank"])
                            seo_referring_domains.append(seo_data["referring_domains"])
                            seo_backlinks.append(seo_data["backlinks"])

                            paid_paid_traffic.append(seo_data["paid_traffic"])
                            paid_est_cpc_links.append(seo_data["estimatedCPC"])
                            paid_paid_keywords.append(seo_data["paid_keywords"])
                            paid_est_ppc_budget.append(seo_data["estm_ppc_budget"])

                    seo_organic_traffic = \
                        [0.0 if v is None else v for v in seo_organic_traffic]
                    seo_total_keywords = \
                        [0.0 if v is None else v for v in seo_total_keywords]
                    seo_w_authority = \
                        [0.0 if v is None else v for v in seo_w_authority]
                    seo_avg_organic_rank = \
                        [0.0 if v is None else v for v in seo_w_authority]
                    seo_referring_domains = \
                        [0.0 if v is None else v for v in seo_w_authority]
                    seo_backlinks = \
                        [0.0 if v is None else v for v in seo_w_authority]

                    paid_paid_traffic = \
                        [0.0 if v is None else v for v in paid_paid_traffic]
                    paid_est_cpc_links = \
                        [0.0 if v is None else v for v in paid_est_cpc_links]
                    paid_paid_keywords = \
                        [0.0 if v is None else v for v in paid_paid_keywords]
                    paid_est_ppc_budget = \
                        [0.0 if v is None else v for v in paid_paid_keywords]

                    seo_organic_traffic_value = get_performance_index(seo_organic_traffic)
                    seo_total_keywords_value = get_performance_index(seo_total_keywords)
                    seo_w_authority_value = get_performance_index(seo_w_authority)
                    seo_avg_organic_rank_value = get_performance_index(seo_organic_traffic)
                    seo_referring_domains_value = get_performance_index(seo_referring_domains)
                    seo_backlinks_value = get_performance_index(seo_backlinks)

                    performance_dict["seo_organic_traffic"] = seo_organic_traffic_value
                    performance_dict["seo_total_keywords"] = seo_total_keywords_value
                    performance_dict["seo_w_authority"] = seo_w_authority_value
                    performance_dict["seo_avg_organic_rank"] = seo_avg_organic_rank_value
                    performance_dict["seo_referring_domains"] = seo_referring_domains_value
                    performance_dict["seo_backlinks"] = seo_backlinks_value

                    # Calculate Paid Performance KPIs
                    paid_paid_traffic_value = get_performance_index(paid_paid_traffic)
                    paid_est_cpc_links_value = get_performance_index(paid_est_cpc_links)
                    paid_paid_keywords_value = get_performance_index(paid_paid_keywords)
                    paid_paid_estm_ppc_budget_value = get_performance_index(paid_est_ppc_budget)

                    performance_dict["paid_paid_traffic"] = paid_paid_traffic_value
                    performance_dict["paid_est_cpc_links"] = paid_est_cpc_links_value
                    performance_dict["paid_paid_keywords"] = paid_paid_keywords_value
                    performance_dict["paid_est_ppc_budget"] = paid_paid_estm_ppc_budget_value

                # Calculate Website Performance KPIs
                website_companies_data = []
                for company in companies_ids:
                    website_data = Website.objects.filter(
                                                    Q(company_id=company) &
                                                    Q(initial_date__range=(
                                                        start_full_date,
                                                        end_full_date
                                                    ))
                                                ).values().last()
                    website_companies_data.append(website_data)

                if None in website_companies_data or \
                        len(website_companies_data) == 1:
                    pass
                else:
                    website_mobile_page_speed = []
                    website_desktop_page_speed = []
                    website_bounce_rate = []
                    website_monthly_traffic = []
                    website_pages_visit = []
                    website_avg_time = []

                    website_mail_traffic = []
                    website_referred_traffic = []
                    website_social_traffic = []
                    website_organic_traffic = []
                    website_paid_traffic = []
                    website_direct_traffic = []

                    for website_data in website_companies_data:
                        if len(website_companies_data) == len(companies_ids):
                            
                            website_mobile_page_speed.append(
                                website_data["mobile_page_speed"]
                            )
                            website_desktop_page_speed.append(
                                website_data["desktop_page_speed"]
                            )
                            website_bounce_rate.append(
                                website_data["bounce_rate"]
                            )
                            website_monthly_traffic.append(
                                website_data["monthly_traffic"]
                            )
                            website_pages_visit.append(
                                website_data["pages_visit"]
                            )
                            website_avg_time.append(
                                website_data["avg_TimeOnSite"]
                            )

                            website_mobile_page_speed = \
                                [0.0 if v is None else v
                                    for v in website_mobile_page_speed]
                            website_desktop_page_speed = \
                                [0.0 if v is None else v
                                    for v in website_desktop_page_speed]
                            website_bounce_rate = \
                                [0.0 if v is None else v
                                    for v in website_bounce_rate]
                            website_monthly_traffic = \
                                [0.0 if v is None else v
                                    for v in website_monthly_traffic]
                            website_pages_visit = \
                                [0.0 if v is None else v
                                    for v in website_pages_visit]
                            website_avg_time = \
                                [0.0 if v is None else v
                                    for v in website_avg_time]

                            # Website Traffic Performance
                            website_traffic_id = website_data["website_id"]
                            website_secondary_data = \
                                Website_traffic\
                                .objects.filter(
                                            website_id=website_traffic_id
                                        ).values().last()

                            if not website_secondary_data:
                                performance_dict["web_mail_traffic"] = ''
                                performance_dict["web_referred_traffic"] = ''
                                performance_dict["web_social_traffic"] = ''
                                performance_dict["web_organic_traffic"] = ''
                                performance_dict["web_paid_traffic"] = ''
                                performance_dict["web_direct_traffic"] = ''

                            else:
                                website_mail_traffic.append(
                                    website_secondary_data["organic_traffic"]
                                )
                                website_referred_traffic.append(
                                    website_secondary_data["paid_traffic"]
                                )
                                website_social_traffic.append(
                                    website_secondary_data["social_traffic"]
                                )
                                website_organic_traffic.append(
                                    website_secondary_data["organic_traffic"]
                                )
                                website_paid_traffic.append(
                                    website_secondary_data["paid_traffic"]
                                )
                                website_direct_traffic.append(
                                    website_secondary_data["paid_traffic"]
                                )
                                
                                
                                website_mail_traffic = \
                                    [0.0 if v is None else v
                                        for v in website_mail_traffic]
                                website_referred_traffic = \
                                    [0.0 if v is None else v
                                        for v in website_referred_traffic]
                                website_social_traffic = \
                                    [0.0 if v is None else v
                                        for v in website_social_traffic]
                                website_organic_traffic = \
                                    [0.0 if v is None else v
                                        for v in website_organic_traffic]
                                website_paid_traffic = \
                                    [0.0 if v is None else v
                                        for v in website_paid_traffic]
                                website_direct_traffic = \
                                    [0.0 if v is None else v
                                        for v in website_direct_traffic]

                                website_traffic_mail_value = get_performance_index(website_mail_traffic)
                                website_traffic_referred_traffic_value = get_performance_index(website_referred_traffic)
                                website_traffic_social_traffic_value = get_performance_index(website_social_traffic)
                                website_traffic_organic_traffic_value = get_performance_index(website_organic_traffic)
                                website_traffic_paid_traffic_value = get_performance_index(website_paid_traffic)
                                website_traffic_direct_traffic_value = get_performance_index(website_direct_traffic)

                                performance_dict["web_mail_traffic"] = \
                                    website_traffic_mail_value
                                performance_dict["web_referred_traffic"] = \
                                    website_traffic_referred_traffic_value
                                performance_dict["web_social_traffic"] = \
                                    website_traffic_social_traffic_value
                                performance_dict["web_organic_traffic"] = \
                                    website_traffic_organic_traffic_value
                                performance_dict["web_paid_traffic"] = \
                                    website_traffic_paid_traffic_value
                                performance_dict["web_direct_traffic"] = \
                                    website_traffic_direct_traffic_value 

                    website_mobile_page_speed_value = get_performance_index(website_mobile_page_speed)
                    website_desktop_page_speed_value = get_performance_index(website_desktop_page_speed)
                    website_bounce_rate_value = (1 - get_performance_index(website_bounce_rate))
                    website_monthly_traffic_value = get_performance_index(website_monthly_traffic)
                    website_pages_visit_value = get_performance_index(website_pages_visit)
                    website_avg_time = str_to_int(website_avg_time)
                    website_avg_time_value = get_performance_index(website_avg_time)

                    performance_dict["performance_date"] = \
                        website_data["initial_date"]
                    
                    if website_mobile_page_speed_value:
                        performance_dict["web_mobile_page_speed"] = website_mobile_page_speed_value
                    else:
                        performance_dict["web_mobile_page_speed"] = 0
                    performance_dict["web_desktop_page_speed"] = \
                        website_desktop_page_speed_value
                    performance_dict["web_bounce_rate"] = website_bounce_rate_value
                    performance_dict["web_monthly_traffic"] = \
                        website_monthly_traffic_value
                    performance_dict["web_pages_visit"] = \
                        website_pages_visit_value
                    performance_dict["web_avg_time"] = \
                        website_avg_time_value

                # Calculate Social Media Performance KPIs
                social_companies_data = []
                for company in companies_ids:
                    social_data = Social_media.objects.filter(
                                                    Q(company_id=company) &
                                                    Q(initial_date__range=(
                                                        start_full_date,
                                                        end_full_date
                                                    ))
                                                ).values().last()

                    social_companies_data.append(social_data)
                if None in social_companies_data or \
                        len(social_companies_data) == 1:
                    pass
                else:
                    social_engagement_rate = []
                    social_total_followers = []
                    social_total_interactions = []
                    social_total_clicks = []

                    facebook_total_followers = []
                    facebook_total_page_likes = []
                    facebook_avg_post_likes = []
                    facebook_avg_post_shares = []
                    facebook_avg_post_comments = []
                    
                    instagram_total_followers = []
                    instagram_total_posts = []
                    instagram_avg_likes = []
                    instagram_avg_comments = []

                    twitter_total_followers = []
                    twitter_total_following = []
                    twitter_avg_retweets = []
                    twitter_avg_replies = []
                    twitter_avg_likes = []
                    twitter_tweet_count = []
                    
                    youtube_total_videos = []
                    youtube_total_views = []
                    youtube_total_likes = []
                    youtube_subscriber_count = []

                    for social_data in social_companies_data:
                        if len(social_companies_data) == len(companies_ids):

                            social_engagement_rate.append(
                                social_data["global_engagement_rate"]
                            )
                            social_total_followers.append(
                                social_data["total_followers"]
                            )
                            social_total_interactions.append(
                                social_data["total_average_interactions"]
                            )
                            social_total_clicks.append(
                                social_data["total_clicks"]
                            )

                            social_engagement_rate = \
                                [0.0 if v is None else v for v in social_engagement_rate]
                            social_total_followers = \
                                [0.0 if v is None else v
                                    for v in social_total_followers]
                            social_total_interactions = \
                                [0.0 if v is None else v for v in social_total_interactions]
                            social_total_clicks = \
                                [0.0 if v is None else v for v in social_total_clicks]

                            # Facebook Traffic Performance
                            social_id = social_data["social_id"]
                            facebook_secondary_data = \
                                Facebook.objects.filter(
                                                    social_media_id=social_id
                                                ).values().last()

                            if not facebook_secondary_data:
                                performance_dict["facebook_total_followers"] = ''
                                performance_dict["facebook_total_page_likes"] = ''
                                performance_dict["facebook_avg_post_likes"] = ''
                                performance_dict["facebook_avg_post_shares"] = ''
                                performance_dict["facebook_avg_post_comments"] = ''
                            else:
                                facebook_total_followers.append(
                                    facebook_secondary_data["followers"]
                                )
                                facebook_total_page_likes.append(
                                    facebook_secondary_data["likes"]
                                )
                                facebook_avg_post_likes.append(
                                    facebook_secondary_data["avg_post_likes"]
                                )
                                facebook_avg_post_shares.append(
                                    facebook_secondary_data["avg_post_shares"]
                                )
                                facebook_avg_post_comments.append(
                                    facebook_secondary_data["avg_post_comments"]
                                )

                                facebook_total_followers = \
                                    [0.0 if v is None else v
                                        for v in facebook_total_followers]
                                facebook_total_page_likes = \
                                    [0.0 if v is None else v
                                        for v in facebook_total_page_likes]
                                facebook_avg_post_likes = \
                                    [0.0 if v is None else v
                                        for v in facebook_avg_post_likes]
                                facebook_avg_post_shares = \
                                    [0.0 if v is None else v
                                        for v in facebook_avg_post_shares]
                                facebook_avg_post_comments = \
                                    [0.0 if v is None else v
                                        for v in facebook_avg_post_comments]
                                
                                facebook_total_followers_value = get_performance_index(facebook_total_followers)
                                facebook_total_page_likes_value = get_performance_index(facebook_total_page_likes)
                                facebook_avg_post_likes_value = get_performance_index(facebook_avg_post_likes)
                                facebook_avg_post_shares_value = get_performance_index(facebook_avg_post_shares)
                                facebook_avg_post_comments_value = get_performance_index(facebook_avg_post_comments)

                                performance_dict["facebook_total_followers"] = \
                                    facebook_total_followers_value
                                performance_dict["facebook_total_page_likes"] = \
                                    facebook_total_page_likes_value
                                performance_dict["facebook_avg_post_likes"] = \
                                    facebook_avg_post_likes_value
                                performance_dict["facebook_avg_post_shares"] = \
                                    facebook_avg_post_shares_value
                                performance_dict["facebook_avg_post_comments"] = \
                                    facebook_avg_post_comments_value
                                    
                            # Instagram Traffic Performance
                            instagram_secondary_data = \
                                Instagram.objects.filter(
                                                    social_media_id=social_id
                                                ).values().last()

                            if not instagram_secondary_data:
                                performance_dict["instagram_total_followers"] = ''
                                performance_dict["instagram_total_posts"] = ''
                                performance_dict["instagram_avg_likes"] = ''
                                performance_dict["instagram_avg_comments"] = ''
                            else:
                                instagram_total_followers.append(
                                    instagram_secondary_data["followers"]
                                )
                                instagram_total_posts.append(
                                    instagram_secondary_data["posts"]
                                )
                                instagram_avg_likes.append(
                                    instagram_secondary_data["avg_post_likes"]
                                )
                                instagram_avg_comments.append(
                                    instagram_secondary_data["avg_post_comments"]
                                )

                                instagram_total_followers = \
                                    [0.0 if v is None else v
                                        for v in instagram_total_followers]
                                instagram_total_posts = \
                                    [0.0 if v is None else v
                                        for v in instagram_total_posts]
                                instagram_avg_likes = \
                                    [0.0 if v is None else v
                                        for v in instagram_avg_likes]
                                instagram_avg_comments = \
                                    [0.0 if v is None else v
                                        for v in instagram_avg_comments]
                                
                                instagram_total_followers_value = get_performance_index(instagram_total_followers)
                                instagram_total_posts_value = get_performance_index(instagram_total_posts)
                                instagram_avg_likes_value = get_performance_index(instagram_avg_likes)
                                instagram_avg_comments_value = get_performance_index(instagram_avg_comments)

                                performance_dict["instagram_total_followers"] = \
                                    instagram_total_followers_value
                                performance_dict["instagram_total_posts"] = \
                                    instagram_total_posts_value
                                performance_dict["instagram_avg_likes"] = \
                                    instagram_avg_likes_value
                                performance_dict["instagram_avg_comments"] = \
                                    instagram_avg_comments_value

                            # Twitter Traffic Performance
                            twitter_secondary_data = \
                                Twitter.objects.filter(
                                                    social_media_id=social_id
                                                ).values().last()

                            if not twitter_secondary_data:
                                performance_dict["twitter_total_followers"] = ''
                                performance_dict["twitter_total_following"] = ''
                                performance_dict["twitter_avg_retweets"] = ''
                                performance_dict["twitter_avg_replies"] = ''
                                performance_dict["twitter_avg_likes"] = ''
                                performance_dict["twitter_tweet_count"] = ''
                            else:
                                twitter_total_followers.append(
                                    twitter_secondary_data["followers_count"]
                                )
                                twitter_total_following.append(
                                    twitter_secondary_data["following_count"]
                                )
                                twitter_avg_retweets.append(
                                    twitter_secondary_data["avg_retweet_count"]
                                )
                                twitter_avg_replies.append(
                                    twitter_secondary_data["avg_reply_count"]
                                )
                                twitter_avg_likes.append(
                                    twitter_secondary_data["avg_likes_count"]
                                )
                                twitter_tweet_count.append(
                                    twitter_secondary_data["tweet_count"]
                                )

                                twitter_total_followers = \
                                    [0.0 if v is None else v
                                        for v in twitter_total_followers]
                                twitter_total_following = \
                                    [0.0 if v is None else v
                                        for v in twitter_total_following]
                                twitter_avg_retweets = \
                                    [0.0 if v is None else v
                                        for v in twitter_avg_retweets]
                                twitter_avg_replies = \
                                    [0.0 if v is None else v
                                        for v in twitter_avg_replies]
                                twitter_avg_likes = \
                                    [0.0 if v is None else v
                                        for v in twitter_avg_likes]
                                twitter_tweet_count = \
                                    [0.0 if v is None else v
                                        for v in twitter_avg_likes]
                                
                                twitter_total_followers_value = get_performance_index(twitter_total_followers)
                                twitter_total_following_value = get_performance_index(twitter_total_following)
                                twitter_avg_retweets_value = get_performance_index(twitter_avg_retweets)
                                twitter_avg_replies_value = get_performance_index(twitter_avg_replies)
                                twitter_avg_likes_value = get_performance_index(twitter_avg_likes)
                                twitter_tweet_count_value = get_performance_index(twitter_tweet_count)

                                performance_dict["twitter_total_followers"] = \
                                    twitter_total_followers_value
                                performance_dict["twitter_total_following"] = \
                                    twitter_total_following_value
                                performance_dict["twitter_avg_retweets"] = \
                                    twitter_avg_retweets_value
                                performance_dict["twitter_avg_replies"] = \
                                    twitter_avg_replies_value
                                performance_dict["twitter_avg_likes"] = \
                                    twitter_avg_likes_value
                                performance_dict["twitter_tweet_count"] = \
                                    twitter_tweet_count_value
                                    
                            # Youtube Traffic Performance
                            youtube_secondary_data = \
                                Youtube.objects.filter(
                                                    social_media_id=social_id
                                                ).values().last()

                            if not youtube_secondary_data:
                                performance_dict["youtube_total_videos"] = ''
                                performance_dict["youtube_total_views"] = ''
                                performance_dict["youtube_total_likes"] = ''
                                performance_dict["youtube_subscriber_count"] = ''


                            else:
                                youtube_total_videos.append(
                                    youtube_secondary_data["video_count"]
                                )
                                youtube_total_views.append(
                                    youtube_secondary_data["view_count"]
                                )
                                youtube_total_likes.append(
                                    youtube_secondary_data["subscriber_count"]
                                )
                                youtube_subscriber_count.append(
                                    youtube_secondary_data["subscriber_count"]
                                )

                                youtube_total_videos = \
                                    [0.0 if v is None else v
                                        for v in youtube_total_videos]
                                youtube_total_views = \
                                    [0.0 if v is None else v
                                        for v in youtube_total_views]
                                youtube_total_likes = \
                                    [0.0 if v is None else v
                                        for v in youtube_total_likes]
                                youtube_subscriber_count = \
                                    [0.0 if v is None else v
                                        for v in youtube_subscriber_count]
                                
                                youtube_total_videos_value = get_performance_index(youtube_total_videos)
                                youtube_total_views_value = get_performance_index(youtube_total_views)
                                youtube_total_likes_value = get_performance_index(youtube_total_likes)
                                youtube_subscriber_count_value = get_performance_index(youtube_subscriber_count)

                                performance_dict["youtube_total_videos"] = \
                                    youtube_total_videos_value
                                performance_dict["youtube_total_views"] = \
                                    youtube_total_views_value
                                performance_dict["youtube_total_likes"] = \
                                    youtube_total_likes_value
                                performance_dict["youtube_subscriber_count"] = \
                                    youtube_subscriber_count_value

                    social_engagement_rate_value = get_performance_index(social_engagement_rate)
                    social_total_followers_value = get_performance_index(social_total_followers)
                    social_total_interactions_value = get_performance_index(social_total_interactions)
                    social_total_clicks_value = get_performance_index(social_total_clicks)

                    performance_dict["performance_date"] = \
                        social_data["initial_date"]
                    performance_dict["social_engagement_rate"] = \
                        social_engagement_rate_value
                    performance_dict["social_total_followers"] = \
                        social_total_followers_value
                    performance_dict["social_total_interactions"] = \
                        social_total_interactions_value
                    performance_dict["social_total_clicks"] = \
                        social_total_clicks_value

                    performanceSerializer = PerformanceSerializer(
                        data=performance_dict
                    )

                    if not performanceSerializer.is_valid(raise_exception=True):
                        return bad_request(
                            'There has been an error',
                            'There has been an error',
                            ''
                        )
                    try:
                        performanceSerializer.save()

                    except IntegrityError as e:
                        return bad_request(
                            e,
                            'There has been an error',
                            ''
                        )
        return http_ok('Successful')

    @action(methods=["PUT"], detail=False, url_path="calc-project/(?P<pk>\\d+)")
    def store_performance_kpis(self, request, pk):
        """
        Endpoint to calculate the Performance KPIs.
        Valid retroactively. Start-date / End-date.
        """

        self.query_params = self.request.query_params
        self.start_date = self.query_params.get("start_date", None)
        self.end_date = self.query_params.get("end_date", None)

        start_full_date = start_date_values(self.start_date, self.end_date)
        end_full_date = end_date_values(self.end_date)

        projects = Project.objects.filter(id=pk).values()

        # Extract the companies id for every project.
        for project in projects:
            if project["is_active"] != 1:
                pass
            else:
                performance_dict = {}
                project_id = project["id"]
                performance_dict["project"] = project_id
                companies_ids = []
                company_id = project["company_id"]
                companies_ids.append(company_id)

                for key, value in project.items():
                        if 'competitor' in key and value is not None:
                            companies_ids.append(value)

                performance_dict["social_key_first"] = ''
                performance_dict["social_total_followers"] = ''
                performance_dict["social_key_third"] = ''
                performance_dict["facebook_total_followers"] = ''
                performance_dict["facebook_total_page_likes"] = ''

                # Calculate Seo Performance KPIs
                seo_companies_data = []

                project_first_date_temp = Company_wise_scores.objects.filter(
                    project=project_id).order_by('initial_date').values(
                    'initial_date').last()

                if project_first_date_temp is None:
                    start_full_date = start_date_values(self.start_date, self.end_date)
                    end_full_date = end_date_values(self.end_date)
                else:
                    start_full_date = project_first_date_temp["initial_date"]

                for company in companies_ids:
                    seo_data = Seo.objects.filter(
                                                    Q(company_id=company) &
                                                    Q(initial_date__range=(
                                                        start_full_date,
                                                        end_full_date
                                                    ))
                                                ).values().last()
                    seo_companies_data.append(seo_data)

                if None in seo_companies_data or len(seo_companies_data) == 1:
                    pass
                else:

                    seo_organic_traffic = []
                    seo_total_keywords = []
                    seo_w_authority = []
                    seo_avg_organic_rank = []
                    seo_referring_domains = []
                    seo_backlinks = []

                    paid_paid_traffic = []
                    paid_est_cpc_links = []
                    paid_paid_keywords = []
                    paid_est_ppc_budget = []

                    for seo_data in seo_companies_data:
                        if len(seo_companies_data) == len(companies_ids):

                            seo_organic_traffic.append(seo_data["organic_traffic"])
                            seo_total_keywords.append(seo_data["total_keywords"])
                            seo_w_authority.append(seo_data["web_authority"])
                            seo_avg_organic_rank.append(seo_data["avg_organic_rank"])
                            seo_referring_domains.append(seo_data["referring_domains"])
                            seo_backlinks.append(seo_data["backlinks"])

                            paid_paid_traffic.append(seo_data["paid_traffic"])
                            paid_est_cpc_links.append(seo_data["estimatedCPC"])
                            paid_paid_keywords.append(seo_data["paid_keywords"])
                            paid_est_ppc_budget.append(seo_data["estm_ppc_budget"])

                    seo_organic_traffic = \
                        [0.0 if v is None else v for v in seo_organic_traffic]
                    seo_total_keywords = \
                        [0.0 if v is None else v for v in seo_total_keywords]
                    seo_w_authority = \
                        [0.0 if v is None else v for v in seo_w_authority]
                    seo_avg_organic_rank = \
                        [0.0 if v is None else v for v in seo_w_authority]
                    seo_referring_domains = \
                        [0.0 if v is None else v for v in seo_w_authority]
                    seo_backlinks = \
                        [0.0 if v is None else v for v in seo_w_authority]

                    paid_paid_traffic = \
                        [0.0 if v is None else v for v in paid_paid_traffic]
                    paid_est_cpc_links = \
                        [0.0 if v is None else v for v in paid_est_cpc_links]
                    paid_paid_keywords = \
                        [0.0 if v is None else v for v in paid_paid_keywords]
                    paid_est_ppc_budget = \
                        [0.0 if v is None else v for v in paid_paid_keywords]

                    seo_organic_traffic_value = get_performance_index(seo_organic_traffic)
                    seo_total_keywords_value = get_performance_index(seo_total_keywords)
                    seo_w_authority_value = get_performance_index(seo_w_authority)
                    seo_avg_organic_rank_value = get_performance_index(seo_organic_traffic)
                    seo_referring_domains_value = get_performance_index(seo_referring_domains)
                    seo_backlinks_value = get_performance_index(seo_backlinks)

                    performance_dict["seo_organic_traffic"] = seo_organic_traffic_value
                    performance_dict["seo_total_keywords"] = seo_total_keywords_value
                    performance_dict["seo_w_authority"] = seo_w_authority_value
                    performance_dict["seo_avg_organic_rank"] = seo_avg_organic_rank_value
                    performance_dict["seo_referring_domains"] = seo_referring_domains_value
                    performance_dict["seo_backlinks"] = seo_backlinks_value

                    # Calculate Paid Performance KPIs
                    paid_paid_traffic_value = get_performance_index(paid_paid_traffic)
                    paid_est_cpc_links_value = get_performance_index(paid_est_cpc_links)
                    paid_paid_keywords_value = get_performance_index(paid_paid_keywords)
                    paid_paid_estm_ppc_budget_value = get_performance_index(paid_est_ppc_budget)

                    performance_dict["paid_paid_traffic"] = paid_paid_traffic_value
                    performance_dict["paid_est_cpc_links"] = paid_est_cpc_links_value
                    performance_dict["paid_paid_keywords"] = paid_paid_keywords_value
                    performance_dict["paid_est_ppc_budget"] = paid_paid_estm_ppc_budget_value

                # Calculate Website Performance KPIs
                website_companies_data = []
                for company in companies_ids:
                    website_data = Website.objects.filter(
                                                    Q(company_id=company) &
                                                    Q(initial_date__range=(
                                                        start_full_date,
                                                        end_full_date
                                                    ))
                                                ).values().last()
                    website_companies_data.append(website_data)

                if None in website_companies_data or \
                        len(website_companies_data) == 1:
                    pass
                else:
                    website_mobile_page_speed = []
                    website_desktop_page_speed = []
                    website_bounce_rate = []
                    website_monthly_traffic = []
                    website_pages_visit = []
                    website_avg_time = []

                    website_mail_traffic = []
                    website_referred_traffic = []
                    website_social_traffic = []
                    website_organic_traffic = []
                    website_paid_traffic = []
                    website_direct_traffic = []

                    for website_data in website_companies_data:
                        if len(website_companies_data) == len(companies_ids):
                            
                            website_mobile_page_speed.append(
                                website_data["mobile_page_speed"]
                            )
                            website_desktop_page_speed.append(
                                website_data["desktop_page_speed"]
                            )
                            website_bounce_rate.append(
                                website_data["bounce_rate"]
                            )
                            website_monthly_traffic.append(
                                website_data["monthly_traffic"]
                            )
                            website_pages_visit.append(
                                website_data["pages_visit"]
                            )
                            website_avg_time.append(
                                website_data["avg_TimeOnSite"]
                            )

                            website_mobile_page_speed = \
                                [0.0 if v is None else v
                                    for v in website_mobile_page_speed]
                            website_desktop_page_speed = \
                                [0.0 if v is None else v
                                    for v in website_desktop_page_speed]
                            website_bounce_rate = \
                                [0.0 if v is None else v
                                    for v in website_bounce_rate]
                            website_monthly_traffic = \
                                [0.0 if v is None else v
                                    for v in website_monthly_traffic]
                            website_pages_visit = \
                                [0.0 if v is None else v
                                    for v in website_pages_visit]
                            website_avg_time = \
                                [0.0 if v is None else v
                                    for v in website_avg_time]

                            # Website Traffic Performance
                            website_traffic_id = website_data["website_id"]
                            website_secondary_data = \
                                Website_traffic\
                                .objects.filter(
                                            website_id=website_traffic_id
                                        ).values().last()

                            if not website_secondary_data:
                                performance_dict["web_mail_traffic"] = ''
                                performance_dict["web_referred_traffic"] = ''
                                performance_dict["web_social_traffic"] = ''
                                performance_dict["web_organic_traffic"] = ''
                                performance_dict["web_paid_traffic"] = ''
                                performance_dict["web_direct_traffic"] = ''

                            else:
                                website_mail_traffic.append(
                                    website_secondary_data["organic_traffic"]
                                )
                                website_referred_traffic.append(
                                    website_secondary_data["paid_traffic"]
                                )
                                website_social_traffic.append(
                                    website_secondary_data["social_traffic"]
                                )
                                website_organic_traffic.append(
                                    website_secondary_data["organic_traffic"]
                                )
                                website_paid_traffic.append(
                                    website_secondary_data["paid_traffic"]
                                )
                                website_direct_traffic.append(
                                    website_secondary_data["paid_traffic"]
                                )
                                
                                
                                website_mail_traffic = \
                                    [0.0 if v is None else v
                                        for v in website_mail_traffic]
                                website_referred_traffic = \
                                    [0.0 if v is None else v
                                        for v in website_referred_traffic]
                                website_social_traffic = \
                                    [0.0 if v is None else v
                                        for v in website_social_traffic]
                                website_organic_traffic = \
                                    [0.0 if v is None else v
                                        for v in website_organic_traffic]
                                website_paid_traffic = \
                                    [0.0 if v is None else v
                                        for v in website_paid_traffic]
                                website_direct_traffic = \
                                    [0.0 if v is None else v
                                        for v in website_direct_traffic]

                                website_traffic_mail_value = get_performance_index(website_mail_traffic)
                                website_traffic_referred_traffic_value = get_performance_index(website_referred_traffic)
                                website_traffic_social_traffic_value = get_performance_index(website_social_traffic)
                                website_traffic_organic_traffic_value = get_performance_index(website_organic_traffic)
                                website_traffic_paid_traffic_value = get_performance_index(website_paid_traffic)
                                website_traffic_direct_traffic_value = get_performance_index(website_direct_traffic)

                                performance_dict["web_mail_traffic"] = \
                                    website_traffic_mail_value
                                performance_dict["web_referred_traffic"] = \
                                    website_traffic_referred_traffic_value
                                performance_dict["web_social_traffic"] = \
                                    website_traffic_social_traffic_value
                                performance_dict["web_organic_traffic"] = \
                                    website_traffic_organic_traffic_value
                                performance_dict["web_paid_traffic"] = \
                                    website_traffic_paid_traffic_value
                                performance_dict["web_direct_traffic"] = \
                                    website_traffic_direct_traffic_value 

                    website_mobile_page_speed_value = get_performance_index(website_mobile_page_speed)
                    website_desktop_page_speed_value = get_performance_index(website_desktop_page_speed)
                    website_bounce_rate_value = (1 - get_performance_index(website_bounce_rate))
                    website_monthly_traffic_value = get_performance_index(website_monthly_traffic)
                    website_pages_visit_value = get_performance_index(website_pages_visit)
                    website_avg_time = str_to_int(website_avg_time)
                    website_avg_time_value = get_performance_index(website_avg_time)

                    performance_dict["performance_date"] = \
                        website_data["initial_date"]
                    
                    if website_mobile_page_speed_value:
                        performance_dict["web_mobile_page_speed"] = website_mobile_page_speed_value
                    else:
                        performance_dict["web_mobile_page_speed"] = 0
                    performance_dict["web_desktop_page_speed"] = \
                        website_desktop_page_speed_value
                    performance_dict["web_bounce_rate"] = website_bounce_rate_value
                    performance_dict["web_monthly_traffic"] = \
                        website_monthly_traffic_value
                    performance_dict["web_pages_visit"] = \
                        website_pages_visit_value
                    performance_dict["web_avg_time"] = \
                        website_avg_time_value

                # Calculate Social Media Performance KPIs
                social_companies_data = []
                for company in companies_ids:
                    social_data = Social_media.objects.filter(
                                                    Q(company_id=company) &
                                                    Q(initial_date__range=(
                                                        start_full_date,
                                                        end_full_date
                                                    ))
                                                ).values().last()

                    social_companies_data.append(social_data)
                if None in social_companies_data or \
                        len(social_companies_data) == 1:
                    pass
                else:
                    social_engagement_rate = []
                    social_total_followers = []
                    social_total_interactions = []
                    social_total_clicks = []

                    facebook_total_followers = []
                    facebook_total_page_likes = []
                    facebook_avg_post_likes = []
                    facebook_avg_post_shares = []
                    facebook_avg_post_comments = []
                    
                    instagram_total_followers = []
                    instagram_total_posts = []
                    instagram_avg_likes = []
                    instagram_avg_comments = []

                    """
                    twitter_total_followers = []
                    twitter_total_following = []
                    twitter_avg_retweets = []
                    twitter_avg_replies = []
                    twitter_avg_likes = []
                    twitter_tweet_count = []
                    """
                    
                    youtube_total_videos = []
                    youtube_total_views = []
                    youtube_total_likes = []
                    youtube_subscriber_count = []

                    for social_data in social_companies_data:
                        if len(social_companies_data) == len(companies_ids):

                            social_engagement_rate.append(
                                social_data["global_engagement_rate"]
                            )
                            social_total_followers.append(
                                social_data["total_followers"]
                            )
                            social_total_interactions.append(
                                social_data["total_average_interactions"]
                            )
                            social_total_clicks.append(
                                social_data["total_clicks"]
                            )

                            social_engagement_rate = \
                                [0.0 if v is None else v for v in social_engagement_rate]
                            social_total_followers = \
                                [0.0 if v is None else v
                                    for v in social_total_followers]
                            social_total_interactions = \
                                [0.0 if v is None else v for v in social_total_interactions]
                            social_total_clicks = \
                                [0.0 if v is None else v for v in social_total_clicks]

                            # Facebook Traffic Performance
                            social_id = social_data["social_id"]
                            facebook_secondary_data = \
                                Facebook.objects.filter(
                                                    social_media_id=social_id
                                                ).values().last()

                            if not facebook_secondary_data:
                                performance_dict["facebook_total_followers"] = ''
                                performance_dict["facebook_total_page_likes"] = ''
                                performance_dict["facebook_avg_post_likes"] = ''
                                performance_dict["facebook_avg_post_shares"] = ''
                                performance_dict["facebook_avg_post_comments"] = ''
                            else:
                                facebook_total_followers.append(
                                    facebook_secondary_data["followers"]
                                )
                                facebook_total_page_likes.append(
                                    facebook_secondary_data["likes"]
                                )
                                facebook_avg_post_likes.append(
                                    facebook_secondary_data["avg_post_likes"]
                                )
                                facebook_avg_post_shares.append(
                                    facebook_secondary_data["avg_post_shares"]
                                )
                                facebook_avg_post_comments.append(
                                    facebook_secondary_data["avg_post_comments"]
                                )

                                facebook_total_followers = \
                                    [0.0 if v is None else v
                                        for v in facebook_total_followers]
                                facebook_total_page_likes = \
                                    [0.0 if v is None else v
                                        for v in facebook_total_page_likes]
                                facebook_avg_post_likes = \
                                    [0.0 if v is None else v
                                        for v in facebook_avg_post_likes]
                                facebook_avg_post_shares = \
                                    [0.0 if v is None else v
                                        for v in facebook_avg_post_shares]
                                facebook_avg_post_comments = \
                                    [0.0 if v is None else v
                                        for v in facebook_avg_post_comments]
                                
                                facebook_total_followers_value = get_performance_index(facebook_total_followers)
                                facebook_total_page_likes_value = get_performance_index(facebook_total_page_likes)
                                facebook_avg_post_likes_value = get_performance_index(facebook_avg_post_likes)
                                facebook_avg_post_shares_value = get_performance_index(facebook_avg_post_shares)
                                facebook_avg_post_comments_value = get_performance_index(facebook_avg_post_comments)

                                performance_dict["facebook_total_followers"] = \
                                    facebook_total_followers_value
                                performance_dict["facebook_total_page_likes"] = \
                                    facebook_total_page_likes_value
                                performance_dict["facebook_avg_post_likes"] = \
                                    facebook_avg_post_likes_value
                                performance_dict["facebook_avg_post_shares"] = \
                                    facebook_avg_post_shares_value
                                performance_dict["facebook_avg_post_comments"] = \
                                    facebook_avg_post_comments_value
                                    
                            # Instagram Traffic Performance
                            instagram_secondary_data = \
                                Instagram.objects.filter(
                                                    social_media_id=social_id
                                                ).values().last()

                            if not instagram_secondary_data:
                                performance_dict["instagram_total_followers"] = ''
                                performance_dict["instagram_total_posts"] = ''
                                performance_dict["instagram_avg_likes"] = ''
                                performance_dict["instagram_avg_comments"] = ''
                            else:
                                instagram_total_followers.append(
                                    instagram_secondary_data["followers"]
                                )
                                instagram_total_posts.append(
                                    instagram_secondary_data["posts"]
                                )
                                instagram_avg_likes.append(
                                    instagram_secondary_data["avg_post_likes"]
                                )
                                instagram_avg_comments.append(
                                    instagram_secondary_data["avg_post_comments"]
                                )

                                instagram_total_followers = \
                                    [0.0 if v is None else v
                                        for v in instagram_total_followers]
                                instagram_total_posts = \
                                    [0.0 if v is None else v
                                        for v in instagram_total_posts]
                                instagram_avg_likes = \
                                    [0.0 if v is None else v
                                        for v in instagram_avg_likes]
                                instagram_avg_comments = \
                                    [0.0 if v is None else v
                                        for v in instagram_avg_comments]
                                
                                instagram_total_followers_value = get_performance_index(instagram_total_followers)
                                instagram_total_posts_value = get_performance_index(instagram_total_posts)
                                instagram_avg_likes_value = get_performance_index(instagram_avg_likes)
                                instagram_avg_comments_value = get_performance_index(instagram_avg_comments)

                                performance_dict["instagram_total_followers"] = \
                                    instagram_total_followers_value
                                performance_dict["instagram_total_posts"] = \
                                    instagram_total_posts_value
                                performance_dict["instagram_avg_likes"] = \
                                    instagram_avg_likes_value
                                performance_dict["instagram_avg_comments"] = \
                                    instagram_avg_comments_value

                            """
                            # Twitter Traffic Performance
                            twitter_secondary_data = \
                                Twitter.objects.filter(
                                                    social_media_id=social_id
                                                ).values().last()

                            if not twitter_secondary_data:
                                performance_dict["twitter_total_followers"] = ''
                                performance_dict["twitter_total_following"] = ''
                                performance_dict["twitter_avg_retweets"] = ''
                                performance_dict["twitter_avg_replies"] = ''
                                performance_dict["twitter_avg_likes"] = ''
                                performance_dict["twitter_tweet_count"] = ''
                            else:
                                twitter_total_followers.append(
                                    twitter_secondary_data["followers_count"]
                                )
                                twitter_total_following.append(
                                    twitter_secondary_data["following_count"]
                                )
                                twitter_avg_retweets.append(
                                    twitter_secondary_data["avg_retweet_count"]
                                )
                                twitter_avg_replies.append(
                                    twitter_secondary_data["avg_reply_count"]
                                )
                                twitter_avg_likes.append(
                                    twitter_secondary_data["avg_likes_count"]
                                )
                                twitter_tweet_count.append(
                                    twitter_secondary_data["tweet_count"]
                                )

                                twitter_total_followers = \
                                    [0.0 if v is None else v
                                        for v in twitter_total_followers]
                                twitter_total_following = \
                                    [0.0 if v is None else v
                                        for v in twitter_total_following]
                                twitter_avg_retweets = \
                                    [0.0 if v is None else v
                                        for v in twitter_avg_retweets]
                                twitter_avg_replies = \
                                    [0.0 if v is None else v
                                        for v in twitter_avg_replies]
                                twitter_avg_likes = \
                                    [0.0 if v is None else v
                                        for v in twitter_avg_likes]
                                twitter_tweet_count = \
                                    [0.0 if v is None else v
                                        for v in twitter_avg_likes]
                                
                                twitter_total_followers_value = get_performance_index(twitter_total_followers)
                                twitter_total_following_value = get_performance_index(twitter_total_following)
                                twitter_avg_retweets_value = get_performance_index(twitter_avg_retweets)
                                twitter_avg_replies_value = get_performance_index(twitter_avg_replies)
                                twitter_avg_likes_value = get_performance_index(twitter_avg_likes)
                                twitter_tweet_count_value = get_performance_index(twitter_tweet_count)

                                performance_dict["twitter_total_followers"] = \
                                    twitter_total_followers_value
                                performance_dict["twitter_total_following"] = \
                                    twitter_total_following_value
                                performance_dict["twitter_avg_retweets"] = \
                                    twitter_avg_retweets_value
                                performance_dict["twitter_avg_replies"] = \
                                    twitter_avg_replies_value
                                performance_dict["twitter_avg_likes"] = \
                                    twitter_avg_likes_value
                                performance_dict["twitter_tweet_count"] = \
                                    twitter_tweet_count_value
                            """
                                    
                            # Youtube Traffic Performance
                            youtube_secondary_data = \
                                Youtube.objects.filter(
                                                    social_media_id=social_id
                                                ).values().last()

                            if not youtube_secondary_data:
                                performance_dict["youtube_total_videos"] = ''
                                performance_dict["youtube_total_views"] = ''
                                performance_dict["youtube_total_likes"] = ''
                                performance_dict["youtube_subscriber_count"] = ''


                            else:
                                youtube_total_videos.append(
                                    youtube_secondary_data["video_count"]
                                )
                                youtube_total_views.append(
                                    youtube_secondary_data["view_count"]
                                )
                                youtube_total_likes.append(
                                    youtube_secondary_data["subscriber_count"]
                                )
                                youtube_subscriber_count.append(
                                    youtube_secondary_data["subscriber_count"]
                                )

                                youtube_total_videos = \
                                    [0.0 if v is None else v
                                        for v in youtube_total_videos]
                                youtube_total_views = \
                                    [0.0 if v is None else v
                                        for v in youtube_total_views]
                                youtube_total_likes = \
                                    [0.0 if v is None else v
                                        for v in youtube_total_likes]
                                youtube_subscriber_count = \
                                    [0.0 if v is None else v
                                        for v in youtube_subscriber_count]
                                
                                youtube_total_videos_value = get_performance_index(youtube_total_videos)
                                youtube_total_views_value = get_performance_index(youtube_total_views)
                                youtube_total_likes_value = get_performance_index(youtube_total_likes)
                                youtube_subscriber_count_value = get_performance_index(youtube_subscriber_count)

                                performance_dict["youtube_total_videos"] = \
                                    youtube_total_videos_value
                                performance_dict["youtube_total_views"] = \
                                    youtube_total_views_value
                                performance_dict["youtube_total_likes"] = \
                                    youtube_total_likes_value
                                performance_dict["youtube_subscriber_count"] = \
                                    youtube_subscriber_count_value

                    social_engagement_rate_value = get_performance_index(social_engagement_rate)
                    social_total_followers_value = get_performance_index(social_total_followers)
                    social_total_interactions_value = get_performance_index(social_total_interactions)
                    social_total_clicks_value = get_performance_index(social_total_clicks)

                    performance_dict["performance_date"] = \
                        social_data["initial_date"]
                    performance_dict["social_engagement_rate"] = \
                        social_engagement_rate_value
                    performance_dict["social_total_followers"] = \
                        social_total_followers_value
                    performance_dict["social_total_interactions"] = \
                        social_total_interactions_value
                    performance_dict["social_total_clicks"] = \
                        social_total_clicks_value

                    performanceSerializer = PerformanceSerializer(
                        data=performance_dict
                    )

                    if not performanceSerializer.is_valid(raise_exception=True):
                        return bad_request(
                            'There has been an error',
                            'There has been an error',
                            ''
                        )
                    try:
                        performanceSerializer.save()
                        return http_ok('Successful')

                    except IntegrityError as e:
                        return bad_request(
                            e,
                            'There has been an error',
                            ''
                        )
                return http_ok('Successful')



def get_performance_index(data):
    minus = min(data)
    maxim = max(data)
    if minus == maxim:
        index = 1
    else:
        index = ((data[0] - minus)/(maxim - minus))
    return index

def str_to_int(str_list):
    int_list = []
    for s in str_list:
        # Remove any thousands separators (commas or periods)
        s = s.replace(',', '').replace('.', '')
        # Convert the string to an integer and append it to the list
        int_list.append(int(s))
    return int_list


def calculate_avg_time(website_avg_times):
    avg_times_in_seconds = []
    for website_avg_time in website_avg_times:
        hours, minutes, seconds = map(int, website_avg_time.split(":"))
        total_seconds = hours * 3600 + minutes * 60 + seconds
        avg_times_in_seconds.append(total_seconds)
    return avg_times_in_seconds


