from ...views import viewsets, APIView, IsAuthenticated, \
    action, is_user_project, \
    end_date_values, \
    check_competitors, get_company_id, \
    get_secondary_by_primaryid, http_ok, \
    not_found, Website, Website_traffic, Company_wise_scores, \
    isCompanyProjectID, \
    get_company_url_by_id, \
    get_primary_by_companyid_date, start_date_values, \
    build_graph_dict, \
    br_project_not_user, get_data_last_by_company_id_table, \
    get_data_by_range, get_date_string, \
    get_previous_month, set_to_last_day_of_month, \
    get_scores_by_company_project_filterDate, \
    get_data_group_by_range, get_start_date_from_project_date

from django.db.models import Q


def getAllWebDates(pk):
    allWebDates = Company_wise_scores.objects.filter(
        Q(project=pk) & Q(website_score__gt=0)
    ).order_by('initial_date').values_list(
        'initial_date', flat=True).distinct()
    return allWebDates


class WebsiteViewSet(viewsets.ViewSet, APIView):
    permission_classes = (IsAuthenticated,)

    @action(methods=["GET"], detail=False,
            url_path="website-score/(?P<pk>\\d+)")
    def get_website_score(self, request, pk):
        """
        Get Website KPI's.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params

        self.end_date = self.query_params.get("end_date", None)
        end_date = end_date_values(self.end_date)
        self.web_end_date = self.query_params.get("web_end_date", None)
        web_end_date = end_date_values(self.web_end_date)

        self.start_date = self.query_params.get("start_date", None)
        start_date = start_date_values(self.start_date, self.end_date)

        company_id = get_company_id(pk)

        website_global_last = get_data_last_by_company_id_table(
            Website,
            company_id,
            web_end_date
        )
        website_score_last = get_data_by_range(
            pk,
            company_id,
            end_date
        )

        if not website_global_last or not website_score_last:
            return not_found('No website data for this project', '')

        website_global_start = get_data_last_by_company_id_table(
            Website,
            company_id,
            start_date
        )
        website_score_start = get_data_by_range(
            pk,
            company_id,
            start_date
        )

        global_score_dict = {}

        global_score_dict["website_last_score"] = \
            website_score_last["website_score"]
        global_score_dict["total_traffic"] = \
            website_global_last["monthly_traffic"]
        global_score_dict["page_per_visit"] = \
            website_global_last["pages_visit"]
        global_score_dict["bounce_rate"] = \
            website_global_last["bounce_rate"]
        global_score_dict["mobile_performance"] = \
            website_global_last["mobile_page_speed"]
        global_score_dict["desktop_performance"] = \
            website_global_last["desktop_page_speed"]
        global_score_dict["visit_duration"] = \
            website_global_last["avg_TimeOnSite"]

        if not website_global_start or not website_score_start:
            global_score_dict["website_last_score_month"] = None
            global_score_dict["total_traffic_month"] = None
            global_score_dict["page_per_visit_month"] = None
            global_score_dict["bounce_rate_month"] = None
            global_score_dict["mobile_performance_month"] = None
            global_score_dict["desktop_performance_month"] = None
            global_score_dict["visit_duration_month"] = None
        else:
            global_score_dict["website_last_score_month"] = \
                website_score_start["website_score"]
            global_score_dict["total_traffic_month"] = \
                website_global_start["monthly_traffic"]
            global_score_dict["page_per_visit_month"] = \
                website_global_start["pages_visit"]
            global_score_dict["bounce_rate_month"] = \
                website_global_start["bounce_rate"]
            global_score_dict["mobile_performance_month"] = \
                website_global_start["mobile_page_speed"]
            global_score_dict["desktop_performance_month"] = \
                website_global_start["desktop_page_speed"]
            global_score_dict["visit_duration_month"] = \
                website_global_start["avg_TimeOnSite"]

        return http_ok(global_score_dict)

    @action(methods=["GET"], detail=False,
            url_path="website-score/(?P<pk>\\d+)/evolution")
    def get_website_score_evolution(self, request, pk):
        """
        Get Website Score Evolution.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.start_date = self.query_params.get("start_date", None)
        self.end_date = self.query_params.get("end_date", None)

        start_full_date = get_start_date_from_project_date(pk, self.start_date)
        end_full_date = end_date_values(self.end_date)

        companies_dict = {}

        competitors = get_data_group_by_range(pk, end_full_date)

        for company in competitors:

            company_id = company["company_id"]

            website_score = get_scores_by_company_project_filterDate(
                company_id,
                pk,
                end_full_date,
                start_full_date
            )

            evolution_score = build_graph_dict(website_score, "website_score")

            company_name = get_company_url_by_id(company_id)
            companies_dict[company_name] = evolution_score

        return http_ok(companies_dict)

    @action(methods=["GET"], detail=False,
            url_path="website-score-all-dates/(?P<pk>\\d+)/evolution")
    def get_website_score_evolution_all_dates(self, request, pk):
        """
        Get Website Score Evolution.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.start_date = self.query_params.get("start_date", None)
        self.end_date = self.query_params.get("end_date", None)

        start_full_date = get_start_date_from_project_date(pk, self.start_date)
        end_full_date = end_date_values(self.end_date)

        company_id = get_company_id(pk)

        allWebEvScores = []
        entries = getAllWebDates(pk)
        for initial_date in entries:
            current_month = set_to_last_day_of_month(initial_date)
            current_month_string = get_date_string(current_month)
            previous_month = set_to_last_day_of_month(
                get_previous_month(initial_date))
            previous_month_string = get_date_string(
                previous_month)
            start_full_date = get_start_date_from_project_date(
                pk, previous_month_string)
            end_full_date = end_date_values(current_month_string)

            companies_dict = {}

            competitors = get_data_group_by_range(pk, end_full_date)

            for company in competitors:

                company_id = company["company_id"]

                website_score = get_scores_by_company_project_filterDate(
                    company_id,
                    pk,
                    end_full_date,
                    start_full_date
                )

                evolution_score = build_graph_dict(
                    website_score, "website_score")

                company_name = get_company_url_by_id(company_id)
                companies_dict[company_name] = evolution_score
            if companies_dict != {}:
                allWebEvScores.append(companies_dict)

        return http_ok(allWebEvScores)

    @action(methods=["GET"], detail=False,
            url_path="website-score/(?P<pk>\\d+)/traffic-country")
    def get_website_traffic_country(self, request, pk):
        """
        Get Website Traffic per Country
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.end_date = self.query_params.get("end_date", None)
        self.query_params = self.request.query_params
        self.web_end_date = self.query_params.get("web_end_date", None)

        web_end_date = end_date_values(self.web_end_date)

        traffic_sources_dict = {}

        company_id = get_company_id(pk)

        website = get_data_last_by_company_id_table(
            Website,
            company_id,
            web_end_date
        )

        if not website:
            return not_found('No Website data for this project', '')

        website_id = website["website_id"]

        traffic_data_query = get_secondary_by_primaryid(
            Website_traffic, website_id)

        if not traffic_data_query:
            return not_found('No Website_traffic data for this project', '')

        else:
            traffic_data = traffic_data_query.first()
            traffic_sources_dict["company_id"] = company_id

            traffic_sources_dict["total_traffic_website"] = \
                traffic_data["direct_traffic"] + \
                traffic_data["organic_traffic"] + \
                traffic_data["paid_traffic"] + \
                traffic_data["social_traffic"] + \
                traffic_data["reffered_traffic"] + \
                traffic_data["mail_traffic"]

            traffic_sources_dict["country_first"] = \
                traffic_data["country_first"]
            traffic_sources_dict["country_second"] = \
                traffic_data["country_second"]
            traffic_sources_dict["country_third"] = \
                traffic_data["country_third"]
            traffic_sources_dict["country_forth"] = \
                traffic_data["country_forth"]
            traffic_sources_dict["country_fifth"] = \
                traffic_data["country_fifth"]

            traffic_sources_dict["country_value_first"] = \
                traffic_data["country_value_first"]
            traffic_sources_dict["country_value_second"] = \
                traffic_data["country_value_second"]
            traffic_sources_dict["country_value_third"] = \
                traffic_data["country_value_third"]
            traffic_sources_dict["country_value_forth"] = \
                traffic_data["country_value_forth"]
            traffic_sources_dict["country_value_fifth"] = \
                traffic_data["country_value_fifth"]

            return http_ok(traffic_sources_dict)

    @action(methods=["GET"], detail=False,
            url_path="website-score/(?P<pk>\\d+)/direct-competitors")
    def get_website_score_evolution_competitors(self, request, pk):
        """
        Get Website Direct Competitors.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.end_date = self.query_params.get("end_date", None)
        end_date = end_date_values(self.end_date)
        self.web_end_date = self.query_params.get("web_end_date", None)
        web_end_date = end_date_values(self.web_end_date)

        direct_competitors_list = []

        direct_competitors = get_data_group_by_range(pk, end_date)

        count = check_competitors(pk)

        company_project_id = get_company_id(pk)

        for companies in direct_competitors:
            company_data_id = companies["company_id"]
            company_data = get_primary_by_companyid_date(
                Website,
                company_data_id,
                web_end_date
            ).first()

            temp = website_direct_competitors_dict(
                company_data,
                companies["website_score"],
                company_project_id
            )

            direct_competitors_list.append(temp)

        return http_ok(direct_competitors_list[0:(11 - count)])

    @action(methods=["GET"], detail=False,
            url_path="website-score/(?P<pk>\\d+)/traffic-sources/graph")
    def get_traffic_sources_graph(self, request, pk):
        """
        Get Website Traffic Sources.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.end_date = self.query_params.get("end_date", None)
        self.web_end_date = self.query_params.get("web_end_date", None)

        web_end_date = end_date_values(self.web_end_date)

        traffic_sources_dict = {}

        company_id = get_company_id(pk)

        website = get_data_last_by_company_id_table(
            Website,
            company_id,
            web_end_date
        )

        if not website:
            return not_found('No Website data for this project', '')

        website_id = website["website_id"]

        traffic_data_query = get_secondary_by_primaryid(
            Website_traffic, website_id)

        if not traffic_data_query:
            return not_found('No Website_traffic data for this project', '')

        else:
            traffic_data = traffic_data_query[0]
            traffic_sources_dict["company_id"] = company_id
            traffic_sources_dict["direct_traffic"] = \
                traffic_data["direct_traffic"]
            traffic_sources_dict["paid_traffic"] = traffic_data["paid_traffic"]
            traffic_sources_dict["organic_traffic"] = \
                traffic_data["organic_traffic"]
            traffic_sources_dict["social_traffic"] = \
                traffic_data["social_traffic"]
            traffic_sources_dict["reffered_traffic"] = \
                traffic_data["reffered_traffic"]
            traffic_sources_dict["mail_traffic"] = traffic_data["mail_traffic"]

            return http_ok(traffic_sources_dict)

    @action(methods=["GET"], detail=False,
            url_path="website-score/(?P<pk>\\d+)/social-sources")
    def get_website_social_sources(self, request, pk):
        """
        Get Website Social Sources.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.end_date = self.query_params.get("end_date", None)
        self.web_end_date = self.query_params.get("web_end_date", None)

        web_end_date = end_date_values(self.web_end_date)

        traffic_sources_dict = {}

        company_id = get_company_id(pk)

        website = get_data_last_by_company_id_table(
            Website,
            company_id,
            web_end_date
        )

        if not website:
            return not_found('No Website data for this project', '')

        website_id = website["website_id"]

        traffic_data_query = get_secondary_by_primaryid(
            Website_traffic, website_id)

        if not traffic_data_query:
            return not_found('No Website_traffic data for this project', '')

        else:
            traffic_data = traffic_data_query.first()
            traffic_sources_dict["company_id"] = company_id
            traffic_sources_dict["total_traffic"] = \
                traffic_data["direct_traffic"] + \
                traffic_data["organic_traffic"] + \
                traffic_data["paid_traffic"] + \
                traffic_data["social_traffic"] + \
                traffic_data["reffered_traffic"] + traffic_data["mail_traffic"]

            traffic_sources_dict["social_traffic"] = \
                traffic_data["social_traffic"]

            traffic_sources_dict["social_first"] = \
                traffic_data["social_first"]
            traffic_sources_dict["social_second"] = \
                traffic_data["social_second"]
            traffic_sources_dict["social_third"] = \
                traffic_data["social_third"]
            traffic_sources_dict["social_value_first"] = \
                traffic_data["social_value_first"]
            traffic_sources_dict["social_value_second"] = \
                traffic_data["social_value_second"]
            traffic_sources_dict["social_value_third"] = \
                traffic_data["social_value_third"]

            return http_ok(traffic_sources_dict)

    @action(methods=["GET"], detail=False,
            url_path="website-score/(?P<pk>\\d+)/traffic-sources/competitors")
    def get_traffic_sources(self, request, pk):
        """
        Get Website Traffic Sources Direct Competitors.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.end_date = self.query_params.get("end_date", None)
        self.query_params = self.request.query_params
        self.web_end_date = self.query_params.get("web_end_date", None)

        end_date = end_date_values(self.end_date)
        web_end_date = end_date_values(self.web_end_date)

        direct_competitors_list = []

        direct_competitors = get_data_group_by_range(pk, end_date)

        count = check_competitors(pk)

        company_project_id = get_company_id(pk)

        for companies in direct_competitors:
            temp = {}

            company_id = companies["company_id"]

            website_company_data = get_primary_by_companyid_date(

                Website, company_id, web_end_date)

            if (len(website_company_data) > 0):
                current_website_id = website_company_data[0]["website_id"]

                company_data = get_secondary_by_primaryid(
                    Website_traffic, current_website_id)

                if company_data:
                    for company in company_data:
                        temp["company_id"] = company_id
                        temp["company_url"] = get_company_url_by_id(company_id)
                        temp["direct_traffic"] = company["direct_traffic"]
                        temp["paid_traffic"] = company["paid_traffic"]
                        temp["organic_traffic"] = company["organic_traffic"]
                        temp["social_traffic"] = company["social_traffic"]
                        temp["reffered_traffic"] = company["reffered_traffic"]
                        temp["mail_traffic"] = company["mail_traffic"]

                        temp["check_company"] = isCompanyProjectID(
                            company_id, company_project_id)

                    direct_competitors_list.append(temp)

        return http_ok(direct_competitors_list[0:(11 - count)])


def website_direct_competitors_dict(company_data,
                                    company_score,
                                    company_project_id):

    temp = {}
    if company_data is not None:
        company_id = company_data["company_id"]
        temp["company_id"] = company_id
        temp["company_url"] = get_company_url_by_id(company_id)
        temp["website_score"] = company_score
        temp["monthly_traffic"] = company_data["monthly_traffic"]
        temp["pages_visit"] = company_data["pages_visit"]
        temp["bounce_rate"] = company_data["bounce_rate"]
        temp["mobile_performance"] = company_data["mobile_page_speed"]
        temp["desktop_performance"] = company_data["desktop_page_speed"]
        temp["check_company"] = isCompanyProjectID(
            company_id, company_project_id
        )
        temp["avg_time"] = company_data["avg_TimeOnSite"]

        # Get Mail traffic, social traffic,
        # organic traffic and reffered traffic
        # from api_website_traffic table
        website_id = company_data["website_id"]
        traffic_data_query = get_secondary_by_primaryid(
            Website_traffic,
            website_id
        ).last()
        temp["mail_traffic"] = traffic_data_query["mail_traffic"]
        temp["social_traffic"] = traffic_data_query["social_traffic"]
        temp["organic_traffic"] = traffic_data_query["organic_traffic"]
        temp["referred_traffic"] = traffic_data_query["reffered_traffic"]

    return temp
