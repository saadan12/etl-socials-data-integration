from ..views import viewsets, APIView, IsAuthenticated, \
    action, is_user_project, \
    start_date_values, end_date_values, \
    get_company_id, \
    Website, Website_traffic, Social_media, \
    not_found, http_ok, \
    isCompanyProjectID, get_company_url_by_id, \
    Youtube, check_competitors, \
    get_secondaries_sm_by_primaryid, Twitter, \
    Instagram, Facebook, \
    get_secondary_sm_by_primaryid, \
    get_secondary_by_primaryid, \
    get_data_group_by_range, \
    get_primary_by_companyid_date, \
    get_primary_table_by_companyid, \
    get_data_by_range, \
    br_project_not_user, \
    get_data_last_by_company_id_table, \
    get_socialUrl_by_company_id, \
    get_unique_id_by_companyidSM_date


class SocialMediaViewSet(viewsets.ViewSet, APIView):
    permission_classes = (IsAuthenticated,)

    @action(methods=["GET"], detail=False,
            url_path="socialMedia-score/(?P<pk>\\d+)")
    def get_socialMedia_score(self, request, pk):
        """
        Get Social Media KPI's.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.start_date = self.query_params.get("start_date", None)
        self.end_date = self.query_params.get("end_date", None)
        self.sm_end_date = self.query_params.get("sm_end_date", None)

        start_date = start_date_values(self.start_date, self.end_date)
        end_date = end_date_values(self.end_date)
        sm_end_date = end_date_values(self.sm_end_date)

        company_id = get_company_id(pk)

        socialMedia_global_last = get_data_last_by_company_id_table(
            Social_media,
            company_id,
            sm_end_date
        )
        socialMedia_score_last = get_data_by_range(
            pk,
            company_id,
            end_date
        )

        if not socialMedia_global_last or not socialMedia_score_last:
            return not_found('No website data for this project', '')

        socialMedia_score_start = get_data_by_range(
            pk,
            company_id,
            start_date
        )

        socialMedia_global_start = get_data_last_by_company_id_table(
            Social_media,
            company_id,
            start_date
        )

        socialMedia_score_dict = {}

        socialMedia_score_dict["sm_last_score"] = \
            socialMedia_score_last["sm_score"]
        socialMedia_score_dict["engagement_rate"] = \
            socialMedia_global_last["global_engagement_rate"]
        socialMedia_score_dict["total_followers"] = \
            round(float(socialMedia_global_last["total_followers"])) \
            if socialMedia_global_last["total_followers"] is not None \
            else socialMedia_global_last["total_followers"]
        socialMedia_score_dict["total_interactions"] = \
            round(
            float(socialMedia_global_last["total_average_interactions"])) \
            if\
            socialMedia_global_last["total_average_interactions"] is not None \
            else socialMedia_global_last["total_average_interactions"]
        socialMedia_score_dict["total_clicks"] = \
            round(float(socialMedia_global_last["total_clicks"])) \
            if socialMedia_global_last["total_clicks"] is not None \
            else socialMedia_global_last["total_clicks"]

        if not socialMedia_global_start or not socialMedia_score_start:
            socialMedia_score_dict["sm_last_score_month"] = None
            socialMedia_score_dict["engagement_rate_month"] = None
            socialMedia_score_dict["total_followers_month"] = None
            socialMedia_score_dict["total_interactions_month"] = None
            socialMedia_score_dict["total_clicks_month"] = None
        else:
            socialMedia_score_dict["sm_last_score_month"] = \
                socialMedia_score_start["sm_score"]
            socialMedia_score_dict["engagement_rate_month"] = \
                socialMedia_global_start["global_engagement_rate"]
            socialMedia_score_dict["total_followers_month"] = \
                round(float(socialMedia_global_last["total_followers"])) \
                if socialMedia_global_last["total_followers"] is not None \
                else socialMedia_global_last["total_followers"]
            socialMedia_score_dict["total_interactions_month"] = \
                round(
                float(socialMedia_global_last["total_average_interactions"])) \
                if\
                socialMedia_global_last["total_average_interactions"]\
                is not None \
                else socialMedia_global_last["total_average_interactions"]
            socialMedia_score_dict["total_clicks_month"] = \
                round(float(socialMedia_global_last["total_clicks"])) \
                if socialMedia_global_last["total_clicks"] is not None \
                else socialMedia_global_last["total_clicks"]

        return http_ok(socialMedia_score_dict)

    @action(methods=["GET"], detail=False,
            url_path="socialMedia-score/(?P<pk>\\d+)/direct-competitors")
    def get_socialMedia_direct_competitors(self, request, pk):
        """
        Get Social Media Direct Competitors.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.end_date = self.query_params.get("end_date", None)
        end_full_date = end_date_values(self.end_date)
        self.sm_end_date = self.query_params.get("sm_end_date", None)

        direct_competitors_list = []

        direct_competitors = get_data_group_by_range(pk, end_full_date)

        count = check_competitors(pk)

        company_project_id = get_company_id(pk)

        for companies in direct_competitors:
            temp = {}
            company_data_id = companies["company_id"]

            company_data = get_primary_table_by_companyid(
                Social_media, company_data_id)

            if company_data:
                for company in company_data:
                    company_id = company_data_id
                    temp["company_id"] = company_id
                    temp["company_url"] = get_company_url_by_id(company_id)
                    temp["social_media_score"] = companies["sm_score"]
                    temp["engagement_rate"] = company["global_engagement_rate"]
                    temp["total_followers"] = \
                        round(float(company["total_followers"])) \
                        if company["total_followers"] is not None \
                        else company["total_followers"]
                    temp["total_interactions"] = \
                        round(float(company["total_average_interactions"])) \
                        if company["total_average_interactions"] is not None \
                        else company["total_average_interactions"]
                    temp["total_clicks"] = \
                        round(float(company["total_clicks"])) \
                        if company["total_clicks"] is not None \
                        else company["total_clicks"]
                    temp["check_company"] = isCompanyProjectID(
                        company_id, company_project_id)

                    # Get social traffic and organic traffic
                    # from api_website_traffic table
                    # website_data = get_primary_table_by_companyid(
                    # Website, company_id).last()
                    website_data = get_primary_by_companyid_date(
                        Website,
                        company_data_id,
                        end_full_date
                    ).first()
                    website_id = website_data["website_id"]
                    traffic_data_query = get_secondary_by_primaryid(
                        Website_traffic,
                        website_id).last()
                    temp["social_traffic"] = \
                        traffic_data_query["social_traffic"]

            if temp:
                direct_competitors_list.append(temp)

        return http_ok(direct_competitors_list[0:(11 - count)])

    @action(methods=["GET"], detail=False,
            url_path="facebook-score/(?P<pk>\\d+)")
    def get_facebook_score(self, request, pk):
        """
        Get Facebook Media KPI's.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.start_date = self.query_params.get("start_date", None)
        self.end_date = self.query_params.get("end_date", None)

        start_date = start_date_values(self.start_date, self.end_date)
        end_date = end_date_values(self.end_date)

        company_id = get_company_id(pk)

        facebook_url = get_socialUrl_by_company_id(company_id, 'facebook_url')

        socialMedia_global_last = get_data_by_range(
            pk,
            company_id,
            end_date
        )

        socialMedia_global_start = get_data_by_range(
            pk,
            company_id,
            start_date
        )

        if socialMedia_global_start:
            unique_month_id = get_unique_id_by_companyidSM_date(
                Social_media,
                company_id,
                start_date
            )
            facebook_data_month = get_secondary_sm_by_primaryid(
                Facebook, unique_month_id)

        facebook_data = None

        if socialMedia_global_last:
            unique_id = get_unique_id_by_companyidSM_date(
                Social_media,
                company_id,
                end_date
            )
            facebook_data = get_secondary_sm_by_primaryid(
                Facebook, unique_id)

        if not facebook_data:
            return not_found('No data for this project', '')

        facebook_score_dict = {}

        facebook_score_dict["facebook_url"] = facebook_url
        facebook_score_dict["facebook_score"] = \
            socialMedia_global_last["sm_facebook_score"]
        facebook_score_dict["total_followers"] = \
            facebook_data["followers"]
        facebook_score_dict["total_likes"] = \
            facebook_data["likes"]
        facebook_score_dict["average_likes"] = \
            round(float(facebook_data["avg_post_likes"])) \
            if facebook_data["avg_post_likes"] is not None \
            else facebook_data["avg_post_likes"]
        facebook_score_dict["average_shares"] = \
            round(float(facebook_data["avg_post_shares"])) \
            if facebook_data["avg_post_shares"] is not None \
            else facebook_data["avg_post_shares"]
        facebook_score_dict["average_comments"] = \
            round(float(facebook_data["avg_post_comments"])) \
            if facebook_data["avg_post_comments"] is not None \
            else facebook_data["avg_post_comments"]
        facebook_score_dict["engagement_rate"] = \
            facebook_data["fb_engagement_rate"]

        if not socialMedia_global_start or not facebook_data_month:
            facebook_score_dict["facebook_score_month"] = None
            facebook_score_dict["total_followers_month"] = None
            facebook_score_dict["total_likes_month"] = None
            facebook_score_dict["average_likes_month"] = None
            facebook_score_dict["average_shares_month"] = None
            facebook_score_dict["average_comments_month"] = None
            facebook_score_dict["engagement_rate_month"] = None
        else:
            facebook_score_dict["facebook_score_month"] = \
                socialMedia_global_start["sm_facebook_score"]
            facebook_score_dict["total_followers_month"] = \
                facebook_data_month["followers"]
            facebook_score_dict["total_likes_month"] = \
                facebook_data_month["likes"]
            facebook_score_dict["average_likes_month"] = \
                round(float(facebook_data["avg_post_likes"])) \
                if facebook_data["avg_post_likes"] is not None \
                else facebook_data["avg_post_likes"]
            facebook_score_dict["average_shares_month"] = \
                round(float(facebook_data["avg_post_shares"])) \
                if facebook_data["avg_post_shares"] is not None \
                else facebook_data["avg_post_shares"]
            facebook_score_dict["average_comments_month"] = \
                round(float(facebook_data["avg_post_comments"])) \
                if facebook_data["avg_post_comments"] is not None \
                else facebook_data["avg_post_comments"]
            facebook_score_dict["engagement_rate_month"] = \
                facebook_data_month["fb_engagement_rate"]

        return http_ok(facebook_score_dict)

    @action(methods=["GET"], detail=False,
            url_path="facebook-score/(?P<pk>\\d+)/direct-competitors")
    def get_facebook_direct_competitors(self, request, pk):
        """
        Get Facebook Direct Competitors.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.end_date = self.query_params.get("end_date", None)

        end_date = end_date_values(self.end_date)

        direct_competitors_list = []

        direct_competitors = get_data_group_by_range(pk, end_date)

        count = check_competitors(pk)

        company_project_id = get_company_id(pk)

        for companies in direct_competitors:
            temp = {}

            company_data_id = companies["company_id"]
            unique_id = get_unique_id_by_companyidSM_date(
                Social_media,
                company_data_id,
                end_date
            )
            social_data = get_secondaries_sm_by_primaryid(
                Facebook, unique_id)

            if social_data:
                for company in social_data:
                    company_id = company_data_id
                    temp["company_id"] = company_id
                    temp["company_url"] = get_company_url_by_id(company_id)
                    temp["facebook_score"] = companies["sm_facebook_score"]
                    temp["total_followers"] = company["followers"]
                    temp["total_likes"] = company["likes"]
                    temp["avg._likes"] = \
                        round(float(company["avg_post_likes"])) \
                        if company["avg_post_likes"] is not None \
                        else company["avg_post_likes"]
                    temp["avg._shares"] = \
                        round(float(company["avg_post_shares"])) \
                        if company["avg_post_shares"] is not None \
                        else company["avg_post_shares"]
                    temp["avg._comments"] = \
                        round(float(company["avg_post_comments"])) \
                        if company["avg_post_comments"] is not None \
                        else company["avg_post_comments"]
                    temp["social_url"] = get_socialUrl_by_company_id(
                        company_id, 'facebook_url'
                    )
                    temp["engagement_rate"] = company["fb_engagement_rate"]

                    temp["check_company"] = isCompanyProjectID(
                        company_id, company_project_id)

            if temp:
                direct_competitors_list.append(temp)

        return http_ok(direct_competitors_list[0:(11 - count)])

    @action(methods=["GET"], detail=False,
            url_path="instagram-score/(?P<pk>\\d+)")
    def get_instagram_score(self, request, pk):
        """
        Get Instagram Media KPI's.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.start_date = self.query_params.get("start_date", None)
        self.end_date = self.query_params.get("end_date", None)

        start_date = start_date_values(self.start_date, self.end_date)
        end_date = end_date_values(self.end_date)

        company_id = get_company_id(pk)

        instagram_url = get_socialUrl_by_company_id(
            company_id, 'instagram_url')

        socialMedia_global_last = get_data_by_range(
            pk,
            company_id,
            end_date
        )

        socialMedia_global_start = get_data_by_range(
            pk,
            company_id,
            start_date
        )
        if socialMedia_global_start:
            unique_month_id = get_unique_id_by_companyidSM_date(
                Social_media,
                company_id,
                start_date
            )

            instagram_data_month = get_secondary_sm_by_primaryid(
                Instagram, unique_month_id)

        if socialMedia_global_last:
            unique_id = get_unique_id_by_companyidSM_date(
                Social_media,
                company_id,
                end_date
            )

            instagram_data = get_secondary_sm_by_primaryid(
                Instagram, unique_id)

        instagram_score_dict = {}

        if not instagram_data:
            return not_found('No data for this project', '')

        instagram_score_dict["instagram_url"] = instagram_url
        instagram_score_dict["instagram_score"] = \
            socialMedia_global_last["sm_instagram_score"]
        instagram_score_dict["total_followers"] = \
            instagram_data["followers"]
        instagram_score_dict["total_posts"] = \
            instagram_data["posts"]
        instagram_score_dict["average_likes"] = \
            round(float(instagram_data["avg_post_likes"])) \
            if instagram_data["avg_post_likes"] is not None \
            else instagram_data["avg_post_likes"]
        instagram_score_dict["average_shares"] = ""
        instagram_score_dict["average_comments"] = \
            round(float(instagram_data["avg_post_comments"])) \
            if instagram_data["avg_post_comments"] is not None \
            else instagram_data["avg_post_comments"]
        instagram_score_dict["engagement_rate"] = \
            instagram_data["insta_engagement_rate"]

        if not socialMedia_global_start or not instagram_data_month:
            instagram_score_dict["instagram_score_month"] = None
            instagram_score_dict["total_followers_month"] = None
            instagram_score_dict["total_posts_month"] = None
            instagram_score_dict["average_likes_month"] = None
            instagram_score_dict["average_shares_month"] = None
            instagram_score_dict["average_comments_month"] = None
            instagram_score_dict["engagement_rate_month"] = None
        else:
            instagram_score_dict["instagram_score_month"] = \
                socialMedia_global_last["sm_instagram_score"]
            instagram_score_dict["total_followers_month"] = \
                instagram_data_month["followers"]
            instagram_score_dict["total_posts_month"] = \
                instagram_data_month["posts"]
            instagram_score_dict["average_likes_month"] = \
                round(float(instagram_data["avg_post_likes"])) \
                if instagram_data["avg_post_likes"] is not None \
                else instagram_data["avg_post_likes"]
            instagram_score_dict["average_shares_month"] = ""
            instagram_score_dict["average_comments_month"] = \
                round(float(instagram_data["avg_post_comments"])) \
                if instagram_data["avg_post_comments"] is not None \
                else instagram_data["avg_post_comments"]
            instagram_score_dict["engagement_rate_month"] = \
                instagram_data_month["insta_engagement_rate"]

        return http_ok(instagram_score_dict)

    @action(methods=["GET"], detail=False,
            url_path="instagram-score/(?P<pk>\\d+)/direct-competitors")
    def get_instagram_direct_competitors(self, request, pk):
        """
        Get Instagram Media Direct Competitors.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.end_date = self.query_params.get("end_date", None)

        end_date = end_date_values(self.end_date)

        direct_competitors_list = []

        direct_competitors = get_data_group_by_range(pk, end_date)

        count = check_competitors(pk)

        company_project_id = get_company_id(pk)

        for companies in direct_competitors:
            temp = {}
            company_data_id = companies["company_id"]

            unique_id = get_unique_id_by_companyidSM_date(
                Social_media,
                company_data_id,
                end_date
            )
            social_data = get_secondaries_sm_by_primaryid(
                Instagram, unique_id)

            if social_data:
                for company in social_data:
                    company_id = company_data_id
                    temp["company_id"] = company_id
                    temp["company_url"] = get_company_url_by_id(company_id)
                    temp["instagram_score"] = companies["sm_instagram_score"]
                    temp["total_followers"] = company["followers"]
                    temp["total_posts"] = company["posts"]
                    temp["avg._likes"] = \
                        round(float(company["avg_post_likes"])) \
                        if company["avg_post_likes"] is not None \
                        else company["avg_post_likes"]
                    temp["avg._comments"] = \
                        round(float(company["avg_post_comments"])) \
                        if company["avg_post_comments"] is not None \
                        else company["avg_post_comments"]
                    temp["social_url"] = get_socialUrl_by_company_id(
                        company_id, 'instagram_url'
                    )
                    temp["engagement_rate"] = \
                        company["insta_engagement_rate"]
                    temp["check_company"] = isCompanyProjectID(
                        company_id, company_project_id)

            if temp:
                direct_competitors_list.append(temp)
        print("IG Direct Competitors: ", direct_competitors_list)

        return http_ok(direct_competitors_list[0:(11 - count)])

    @action(methods=["GET"], detail=False,
            url_path="twitter-score/(?P<pk>\\d+)")
    def get_twitter_score(self, request, pk):
        """
        Get Twitter Media KPI's.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.start_date = self.query_params.get("start_date", None)
        self.end_date = self.query_params.get("end_date", None)

        start_full_date = start_date_values(self.start_date, self.end_date)
        end_date = end_date_values(self.end_date)

        company_id = get_company_id(pk)

        twitter_url = get_socialUrl_by_company_id(company_id, 'twitter_url')

        socialMedia_global_last = get_data_by_range(
            pk,
            company_id,
            end_date
        )

        socialMedia_global_start = get_data_by_range(
            pk,
            company_id,
            start_full_date
        )

        if socialMedia_global_start:
            unique_month_id = get_unique_id_by_companyidSM_date(
                Social_media,
                company_id,
                start_full_date
            )
            twitter_data_month = get_secondary_sm_by_primaryid(
                Twitter, unique_month_id)

        if socialMedia_global_last:
            unique_id = get_unique_id_by_companyidSM_date(
                Social_media,
                company_id,
                end_date
            )
            twitter_data = get_secondary_sm_by_primaryid(
                Twitter, unique_id)

        if not twitter_data:
            return not_found('No data for this project', '')

        twitter_score_dict = {}

        twitter_score_dict["twitter_url"] = twitter_url
        twitter_score_dict["twitter_score"] = \
            socialMedia_global_last["sm_twitter_score"]
        twitter_score_dict["total_followers"] = \
            twitter_data["followers_count"]
        twitter_score_dict["total_following"] = \
            twitter_data["following_count"]
        twitter_score_dict["average_retweets"] = \
            round(float(twitter_data["avg_retweet_count"])) \
            if twitter_data["avg_retweet_count"] is not None \
            else twitter_data["avg_retweet_count"]
        twitter_score_dict["average_replies"] = \
            round(float(twitter_data["avg_reply_count"])) \
            if twitter_data["avg_reply_count"] is not None \
            else twitter_data["avg_reply_count"]
        twitter_score_dict["average_likes"] = \
            round(float(twitter_data["avg_likes_count"])) \
            if twitter_data["avg_likes_count"] is not None \
            else twitter_data["avg_likes_count"]
        twitter_score_dict["engagement_rate"] = \
            twitter_data["twitter_engagement_rate"]

        if not socialMedia_global_start or not twitter_data_month:
            twitter_score_dict["twitter_score_month"] = None
            twitter_score_dict["total_followers_month"] = None
            twitter_score_dict["total_following_month"] = None
            twitter_score_dict["average_retweets_month"] = None
            twitter_score_dict["average_replies_month"] = None
            twitter_score_dict["average_likes_month"] = None
            twitter_score_dict["engagement_rate_month"] = None
        else:
            twitter_score_dict["twitter_score_month"] = \
                socialMedia_global_start["sm_twitter_score"]
            twitter_score_dict["total_followers_month"] = \
                twitter_data_month["followers_count"]
            twitter_score_dict["total_following_month"] = \
                twitter_data_month["following_count"]
            twitter_score_dict["average_retweets_month"] = \
                round(float(twitter_data["avg_retweet_count"])) \
                if twitter_data["avg_retweet_count"] is not None \
                else twitter_data["avg_retweet_count"]
            twitter_score_dict["average_replies_month"] = \
                round(float(twitter_data["avg_reply_count"])) \
                if twitter_data["avg_reply_count"] is not None \
                else twitter_data["avg_reply_count"]
            twitter_score_dict["average_likes_month"] = \
                round(float(twitter_data["avg_likes_count"])) \
                if twitter_data["avg_likes_count"] is not None \
                else twitter_data["avg_likes_count"]
            twitter_score_dict["engagement_rate_month"] = \
                twitter_data_month["twitter_engagement_rate"]

        return http_ok(twitter_score_dict)

    @action(methods=["GET"], detail=False,
            url_path="twitter-score/(?P<pk>\\d+)/direct-competitors")
    def get_twitter_direct_competitors(self, request, pk):
        """
        Get Twitter Media Direct Competitors.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.end_date = self.query_params.get("end_date", None)

        end_date = end_date_values(self.end_date)

        direct_competitors_list = []

        direct_competitors = get_data_group_by_range(pk, end_date)

        count = check_competitors(pk)

        company_project_id = get_company_id(pk)

        for companies in direct_competitors:
            temp = {}
            company_data_id = companies["company_id"]

            unique_id = get_unique_id_by_companyidSM_date(
                Social_media,
                company_data_id,
                end_date
            )
            social_data = get_secondaries_sm_by_primaryid(
                Twitter, unique_id)
            if social_data:
                for company in social_data:
                    company_id = company_data_id
                    temp["company_id"] = company_id
                    temp["company_url"] = get_company_url_by_id(company_id)
                    temp["twitter_score"] = companies["sm_twitter_score"]
                    temp["total_followers"] = company["followers_count"]
                    temp["total_following"] = company["following_count"]
                    temp["avg._retweets"] = \
                        round(float(company["avg_retweet_count"])) \
                        if company["avg_retweet_count"] is not None \
                        else company["avg_retweet_count"]
                    temp["avg._replies"] = \
                        round(float(company["avg_reply_count"])) \
                        if company["avg_reply_count"] is not None \
                        else company["avg_reply_count"]
                    temp["avg._likes"] = \
                        round(float(company["avg_likes_count"])) \
                        if company["avg_likes_count"] is not None \
                        else company["avg_likes_count"]
                    temp["social_url"] = get_socialUrl_by_company_id(
                        company_id, 'twitter_url'
                    )
                    temp["engagement_rate"] = \
                        company["twitter_engagement_rate"]

                    temp["check_company"] = isCompanyProjectID(
                        company_id, company_project_id)

            if temp:
                direct_competitors_list.append(temp)

        return http_ok(direct_competitors_list[0:(11 - count)])

    @action(methods=["GET"], detail=False,
            url_path="youtube-score/(?P<pk>\\d+)")
    def get_youtube_score(self, request, pk):
        """
        Get Youtube Media KPI's.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.start_date = self.query_params.get("start_date", None)
        self.end_date = self.query_params.get("end_date", None)

        start_date = start_date_values(self.start_date, self.end_date)
        end_date = end_date_values(self.end_date)

        company_id = get_company_id(pk)

        youtube_url = get_socialUrl_by_company_id(company_id, 'youtube_url')

        socialMedia_global_last = get_data_by_range(
            pk,
            company_id,
            end_date
        )

        socialMedia_global_start = get_data_by_range(
            pk,
            company_id,
            start_date
        )

        if socialMedia_global_start:
            unique_month_id = get_unique_id_by_companyidSM_date(
                Social_media,
                company_id,
                start_date
            )
            youtube_data_month = get_secondary_sm_by_primaryid(
                Youtube, unique_month_id)

        if socialMedia_global_last:
            unique_id = get_unique_id_by_companyidSM_date(
                Social_media,
                company_id,
                end_date
            )
            youtube_data = get_secondary_sm_by_primaryid(
                Youtube, unique_id)

        if not youtube_data:
            return not_found('No data for this project', '')

        youtube_score_dict = {}

        youtube_score_dict["youtube_url"] = youtube_url
        youtube_score_dict["youtube_score"] = \
            socialMedia_global_last["sm_youtube_score"]
        youtube_score_dict["total_videos"] = youtube_data["video_count"]
        youtube_score_dict["total_views"] = youtube_data["view_count"]
        youtube_score_dict["subcribers"] = youtube_data["subscriber_count"]
        youtube_score_dict["likes"] = youtube_data["like_count"]
        youtube_score_dict["comments"] = youtube_data["comment_count"]
        youtube_score_dict["engagement_rate"] = \
            youtube_data["youtube_engagement_rate"]

        if not socialMedia_global_start or not youtube_data_month:
            youtube_score_dict["youtube_score_month"] = None
            youtube_score_dict["total_videos_month"] = None
            youtube_score_dict["total_views_month"] = None
            youtube_score_dict["subcribers_month"] = None
            youtube_score_dict["likes_month"] = None
            youtube_score_dict["comments_month"] = None
            youtube_score_dict["engagement_rate_month"] = None
        else:
            youtube_score_dict["youtube_score_month"] = \
                socialMedia_global_start["sm_youtube_score"]
            youtube_score_dict["total_videos_month"] = \
                youtube_data_month["video_count"]
            youtube_score_dict["total_views_month"] = \
                youtube_data_month["view_count"]
            youtube_score_dict["subcribers_month"] = \
                youtube_data_month["subscriber_count"]
            youtube_score_dict["likes_month"] = \
                youtube_data_month["like_count"]
            youtube_score_dict["comments_month"] = \
                youtube_data_month["comment_count"]
            youtube_score_dict["engagement_rate_month"] = \
                youtube_data_month["youtube_engagement_rate"]

        return http_ok(youtube_score_dict)

    @action(methods=["GET"], detail=False,
            url_path="youtube-score/(?P<pk>\\d+)/direct-competitors")
    def get_youtube_direct_competitors(self, request, pk):
        """
        Get Youtube Media Direct Competitors.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.end_date = self.query_params.get("end_date", None)

        end_date = end_date_values(self.end_date)

        direct_competitors_list = []

        direct_competitors = get_data_group_by_range(pk, end_date)

        count = check_competitors(pk)

        company_project_id = get_company_id(pk)

        for companies in direct_competitors:
            temp = {}
            company_data_id = companies["company_id"]

            unique_id = get_unique_id_by_companyidSM_date(
                Social_media,
                company_data_id,
                end_date
            )
            social_data = get_secondaries_sm_by_primaryid(
                Youtube, unique_id)
            if social_data:
                for company in social_data:
                    company_id = company_data_id
                    temp["company_id"] = company_id
                    temp["company_url"] = get_company_url_by_id(company_id)
                    temp["youtube_score"] = companies["sm_youtube_score"]
                    temp["total_videos"] = company["video_count"]
                    temp["total_views"] = company["view_count"]
                    temp["subscribers"] = company["subscriber_count"]
                    temp["likes"] = company["like_count"]
                    temp["comments"] = company["comment_count"]
                    temp["social_url"] = get_socialUrl_by_company_id(
                        company_id, 'youtube_url'
                    )
                    temp["engagement_rate"] = \
                        company["youtube_engagement_rate"]

                    temp["check_company"] = isCompanyProjectID(
                        company_id, company_project_id)

            if temp:
                direct_competitors_list.append(temp)

        return http_ok(direct_competitors_list[0:(11 - count)])


def social_media_direct_competitors_dict(
        company_data,
        company_score,
        company_project_id):

    temp = {}
    company_id = company_data["company_id"]
    temp["company_id"] = company_id
    temp["company_url"] = get_company_url_by_id(company_id)
    temp["social_media_score"] = company_score
    temp["global_engagement_rate"] = company_data["global_engagement_rate"]
    temp["total_followers"] = company_data["total_followers"]
    temp["total_average_interactions"] = \
        company_data["total_average_interactions"]
    temp["check_company"] = isCompanyProjectID(
        company_id, company_project_id
    )

    return temp
