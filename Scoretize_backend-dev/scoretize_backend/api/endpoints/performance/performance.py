from ...views import viewsets, APIView, IsAuthenticated, \
    action, http_ok, start_date_values, \
    end_date_values, Performance, Q, \
    bad_request
import json


class PerformanceInfo(viewsets.ViewSet, APIView):
    permission_classes = (IsAuthenticated,)

    @action(methods=["GET"], detail=False, url_path="recommends/(?P<pk>\\d+)")
    def get_recommendations(self, request, pk):
        """
        Endpoint to GET the Performance KPIs.
        Start-date / End-date.
        """

        self.query_params = self.request.query_params
        self.start_date = self.query_params.get("start_date", None)
        self.end_date = self.query_params.get("end_date", None)

        start_full_date = start_date_values(self.start_date, self.end_date)
        end_full_date = end_date_values(self.end_date)

        performance = Performance.objects.filter(
            Q(project=pk) &
            Q(performance_date__range=(
                start_full_date,
                end_full_date
            ))
        )

        if not performance:
            return bad_request(
                'no data',
                'no data',
                'no data'
            )

        performanceDict = performance.values().last()
        performanceInfo = {}

        websitePerformance = {}
        seoPerformance = {}
        paidPerformance = {}
        socialPerformance = {}
        facebookBreakdown = {}
        instagramBreakdown = {}
        # twitterBreakdown = {}
        youtubeBreakdown = {}

        for key, value in performanceDict.items():
            if key != 'id':
                if 'web' in key:
                    websitePerformance[key] = \
                        (float(value) * website_weights[key])
                if 'seo' in key:
                    seoPerformance[key] = (float(value) * seo_weights[key])
                if 'paid' in key and 'web' not in key:
                    paidPerformance[key] = \
                        (float(value) * paid_weights[key])
                if 'social' in key:
                    socialPerformance[key] = \
                        value
                if 'facebook' in key:
                    facebookBreakdown[key] = \
                        (float(value) * facebook_weights[key])
                if 'instagram' in key:
                    instagramBreakdown[key] = \
                        (float(value) * instagram_weights[key])
                """
                if 'twitter' in key:
                    twitterBreakdown[key] = \
                        (float(value) * twitter_weights[key])
                """
                if 'youtube' in key:
                    youtubeBreakdown[key] = \
                        (float(value) * youtube_weights[key])

        websitePerformance = sort_dict_by_value_asc(websitePerformance)
        seoPerformance = sort_dict_by_value_asc(seoPerformance)
        paidPerformance = sort_dict_by_value_asc(paidPerformance)
        socialPerformance = sort_dict_by_value_asc(socialPerformance)
        socialPerformance["facebook"] = \
            first_three_values(sort_dict_by_value_asc(facebookBreakdown))
        """
        socialPerformance["twitter"] = \
            first_three_values(sort_dict_by_value_asc(twitterBreakdown))
        """
        socialPerformance["youtube"] = \
            first_three_values(sort_dict_by_value_asc(youtubeBreakdown))
        socialPerformance["instagram"] = \
            first_three_values(sort_dict_by_value_asc(instagramBreakdown))

        performanceInfo["website"] = \
            first_three_values(websitePerformance)
        performanceInfo["seo"] = \
            first_three_values(seoPerformance)
        performanceInfo["paid"] = \
            first_three_values(paidPerformance)
        performanceInfo["social"] = socialPerformance

        import os

        BASE_DIR = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        with open(
            BASE_DIR + '/performance/recomendations.json'
        ) as f:
            data = json.load(f)

        socialPerformance["social_engagement_rate"] = \
            data["social"]["social_engagement_rate"]
        socialPerformance["social_total_followers"] = \
            data["social"]["social_total_followers"]
        socialPerformance["social_total_interactions"] = \
            data["social"]["social_total_interactions"]
        socialPerformance["web_social_traffic"] = \
            data["social"]["web_social_traffic"]

        for key, value in socialPerformance["instagram"].items():
            socialPerformance["instagram"][key] = data["instagram"][key]
        """
        for key, value in socialPerformance["twitter"].items():
            socialPerformance["twitter"][key] = data["twitter"][key]
        """
        for key, value in socialPerformance["facebook"].items():
            socialPerformance["facebook"][key] = data["facebook"][key]
        for key, value in socialPerformance["youtube"].items():
            socialPerformance["youtube"][key] = data["youtube"][key]

        for key, value in performanceInfo["website"].items():
            performanceInfo["website"][key] = data["website"][key]
        for key, value in performanceInfo["seo"].items():
            performanceInfo["seo"][key] = data["seo"][key]
        for key, value in performanceInfo["paid"].items():
            performanceInfo["paid"][key] = data["paid"][key]

        performanceInfo["social"] = socialPerformance

        return http_ok(performanceInfo)


def sort_dict_by_value_asc(d):
    return {k: v for k, v in sorted(d.items(),
            key=lambda item: item[1], reverse=False)}


def first_three_values(d):
    return dict(list(d.items())[:3])


instagram_weights = {
    "instagram_total_followers": 0.2,
    "instagram_total_posts": 0.2,
    "instagram_avg_likes": 0.3,
    "instagram_avg_comments": 0.3
}

"""
twitter_weights = {
    "twitter_tweet_count": 0.1,
    "twitter_total_followers": 0.2,
    "twitter_total_following": 0.1,
    "twitter_avg_retweets": 0.3,
    "twitter_avg_replies": 0.2,
    "twitter_avg_likes": 0.1
}
"""

youtube_weights = {
    "youtube_total_videos": 0.2,
    "youtube_subscriber_count": 0.3,
    "youtube_total_views": 0.3,
    "youtube_total_likes": 0.2,
}

facebook_weights = {
    "facebook_total_page_likes": 0.15,
    "facebook_total_followers": 0.10,
    "facebook_avg_post_likes": 0.2,
    "facebook_avg_post_shares": 0.3,
    "facebook_avg_post_comments": 0.25,
}

website_weights = {
    "web_monthly_traffic": 0.1,
    "web_avg_time": 0.15,
    "web_bounce_rate": 0.1,
    "web_pages_visit": 0.15,
    "web_organic_traffic": 0,
    "web_direct_traffic": 0,
    "web_paid_traffic": 0,
    "web_referred_traffic": 0.1,
    "web_mail_traffic": 0,
    "web_social_traffic": 0,
    "web_desktop_page_speed": 0.2,
    "web_mobile_page_speed": 0.2,
}

seo_weights = {
    "seo_organic_traffic": 0.20,
    "seo_w_authority": 0.25,
    "seo_total_keywords": 0.15,
    "seo_avg_organic_rank": 0.10,
    "seo_backlinks": 0.2,
    "seo_referring_domains": 0.1,
}

paid_weights = {
    "paid_paid_traffic": 0.2,
    "paid_paid_keywords": 0.1,
    "paid_est_ppc_budget": 0.25,
    "paid_est_cpc_links": 0.45,
}
