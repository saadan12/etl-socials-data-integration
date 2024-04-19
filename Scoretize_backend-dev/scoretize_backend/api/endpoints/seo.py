from ..views import viewsets, APIView, IsAuthenticated, \
    action, is_user_project, \
    start_date_values, end_date_values, \
    get_company_id, \
    Seo, Company_wise_scores, \
    http_ok, isCompanyProjectID, build_graph_dict, \
    get_company_url_by_id, Website, Website_traffic, \
    get_scores_by_company_project_filterDate, \
    get_primary_table_by_companyid, \
    get_secondary_by_primaryid, check_competitors, \
    not_found, \
    get_data_group_by_range, get_start_date_from_project_date, \
    br_project_not_user, get_data_last_by_company_id_table, \
    get_data_by_range, get_previous_month, \
    set_to_last_day_of_month, get_date_string
from django.db.models import Q


def getAllSeoDates(pk):
    allSeoDates = Company_wise_scores.objects.filter(
        Q(project=pk) & Q(seo_score__gt=0)
    ).order_by('initial_date').values_list(
        'initial_date', flat=True).distinct()
    return allSeoDates


class SeoviewViewSet(viewsets.ViewSet, APIView):
    permission_classes = (IsAuthenticated,)

    @action(methods=["GET"], detail=False,
            url_path="seo-score/(?P<pk>\\d+)")
    def get_seo_score(self, request, pk):
        """
        Get Seo KPI's.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params

        self.end_date = self.query_params.get("end_date", None)
        end_date = end_date_values(self.end_date)

        self.start_date = self.query_params.get("start_date", None)
        start_date = start_date_values(self.start_date, self.end_date)

        self.web_end_date = self.query_params.get("web_end_date", None)
        web_end_date = end_date_values(self.web_end_date)

        self.seo_end_date = self.query_params.get("seo_end_date", None)
        seo_end_date = end_date_values(self.seo_end_date)

        company_id = get_company_id(pk)

        seo_global_last = get_data_last_by_company_id_table(
            Seo,
            company_id,
            seo_end_date
        )
        seo_score_last = get_data_by_range(
            pk,
            company_id,
            end_date
        )

        if not seo_global_last or not seo_score_last:
            return not_found('No website data for this project', '')

        website_temp_last = get_data_last_by_company_id_table(
            Website,
            company_id,
            web_end_date
        )
        website_last = get_secondary_by_primaryid(
            Website_traffic, website_temp_last["website_id"]).first()

        if not website_last:
            return not_found('No Website data for this project', '')

        seo_global_start = get_data_last_by_company_id_table(
            Seo,
            company_id,
            start_date
        )
        seo_score_start = get_data_by_range(
            pk,
            company_id,
            start_date
        )

        seo_score_dict = {}

        seo_score_dict["seo_last_score"] = seo_score_last["seo_score"]
        seo_score_dict["organic_traffic"] = seo_global_last["organic_traffic"]
        seo_score_dict["web_authority"] = seo_global_last["web_authority"]
        seo_score_dict["total_keywords"] = seo_global_last["total_keywords"]
        seo_score_dict["backlinks"] = seo_global_last["backlinks"]
        seo_score_dict["referring_domains"] = \
            seo_global_last["referring_domains"]
        seo_score_dict["referal_traffic"] = \
            website_last["reffered_traffic"]
        seo_score_dict["avg_organic_rank"] = \
            seo_global_last["avg_organic_rank"]
        # Add refering Domains and Backlinks

        if not seo_global_start or not seo_score_start:
            seo_score_dict["seo_last_score_month"] = None
            seo_score_dict["organic_traffic_month"] = None
            seo_score_dict["web_authority_month"] = None
            seo_score_dict["total_keywords_month"] = None
            seo_score_dict["backlinks_month"] = None
            seo_score_dict["referring_domains_month"] = None
            seo_score_dict["reffered_traffic_month"] = None
            seo_score_dict["avg_organic_rank_month"] = None
        else:
            # website_start = get_secondary_by_primaryid(
            #     Website_traffic, website_temp_start["website_id"])[0]
            seo_score_dict["seo_last_score_month"] = \
                seo_score_start["seo_score"]
            seo_score_dict["organic_traffic_month"] = \
                seo_global_start["organic_traffic"]
            seo_score_dict["web_authority_month"] = \
                seo_global_start["web_authority"]
            seo_score_dict["total_keywords_month"] = \
                seo_global_start["total_keywords"]
            seo_score_dict["backlinks_month"] = \
                seo_global_start["backlinks"]
            seo_score_dict["referring_domains_month"] = \
                seo_global_start["referring_domains"]
            # seo_score_dict["reffered_traffic_month"] = \
            #     website_start["reffered_traffic"]
            seo_score_dict["avg_organic_rank_month"] = \
                seo_global_start["avg_organic_rank"]

        return http_ok(seo_score_dict)

    @action(methods=["GET"], detail=False,
            url_path="seo-score/(?P<pk>\\d+)/evolution")
    def get_seo_score_evolution(self, request, pk):
        """
        Get Seo score evolution.
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
            company_name = get_company_url_by_id(company_id)

            seo_score = get_scores_by_company_project_filterDate(
                company_id,
                pk,
                end_full_date,
                start_full_date
            )

            evolution_score = build_graph_dict(seo_score, "seo_score")

            companies_dict[company_name] = evolution_score

        return http_ok(companies_dict)

    @action(methods=["GET"], detail=False,
            url_path="seo-score/(?P<pk>\\d+)/evolution-all-dates")
    def get_seo_score_evolution_all_dates(self, request, pk):
        """
        Get Seo score evolution.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.start_date = self.query_params.get("start_date", None)
        self.end_date = self.query_params.get("end_date", None)

        start_full_date = get_start_date_from_project_date(pk, self.start_date)
        end_full_date = end_date_values(self.end_date)

        company_id = get_company_id(pk)

        allSeoEvScores = []
        entries = getAllSeoDates(pk)
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
                company_name = get_company_url_by_id(company_id)

                seo_score = get_scores_by_company_project_filterDate(
                    company_id,
                    pk,
                    end_full_date,
                    start_full_date
                )

                evolution_score = build_graph_dict(seo_score, "seo_score")

                companies_dict[company_name] = evolution_score
            if companies_dict != {}:
                allSeoEvScores.append(companies_dict)

        return http_ok(allSeoEvScores)

    @action(methods=["GET"], detail=False,
            url_path="seo-score/(?P<pk>\\d+)/traffic-evolution")
    def get_seo_score_traffic_evolution(self, request, pk):
        """
        Get Seo Traffic Evolution.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.start_date = self.query_params.get("start_date", None)
        self.end_date = self.query_params.get("end_date", None)

        start_full_date = get_start_date_from_project_date(pk, self.start_date)
        end_full_date = end_date_values(self.end_date)

        total_list = {}

        company_id = get_company_id(pk)

        seo_score = get_primary_table_by_companyid(
            Seo, company_id).filter(
            initial_date__range=(start_full_date, end_full_date))

        organic_list = build_graph_dict(seo_score, "organic_traffic")
        paid_list = build_graph_dict(seo_score, "paid_traffic")

        total_list["organic"] = organic_list
        total_list["paid"] = paid_list

        return http_ok(total_list)

    @action(methods=["GET"], detail=False,
            url_path="seo-score/(?P<pk>\\d+)/traffic-evolution-all-dates")
    def get_seo_score_traffic_evolution_all_dates(self, request, pk):
        """
        Get Seo Traffic Evolution.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.start_date = self.query_params.get("start_date", None)
        self.end_date = self.query_params.get("end_date", None)

        start_full_date = get_start_date_from_project_date(pk, self.start_date)
        end_full_date = end_date_values(self.end_date)

        company_id = get_company_id(pk)

        allSeoTrafficEvScores = []
        entries = getAllSeoDates(pk)
        for initial_date in entries:
            # initial_date = entry["initial_date"]
            current_month = set_to_last_day_of_month(initial_date)
            current_month_string = get_date_string(current_month)
            previous_month = set_to_last_day_of_month(
                get_previous_month(initial_date))
            previous_month_string = get_date_string(
                previous_month)
            start_full_date = get_start_date_from_project_date(
                pk, previous_month_string)
            end_full_date = end_date_values(current_month_string)

            total_list = {}

            # company_id = get_company_id(pk)

            seo_score = get_primary_table_by_companyid(
                Seo, company_id).filter(
                initial_date__range=(start_full_date, end_full_date))

            organic_list = build_graph_dict(seo_score, "organic_traffic")
            paid_list = build_graph_dict(seo_score, "paid_traffic")

            total_list["organic"] = organic_list
            total_list["paid"] = paid_list

            if total_list != {}:
                allSeoTrafficEvScores.append(total_list)

        return http_ok(allSeoTrafficEvScores)

    @action(methods=["GET"], detail=False,
            url_path="seo-score/(?P<pk>\\d+)/keywords-graph")
    def get_seo_score_keywords_graph(self, request, pk):
        """
        Get Seo Score Keywords Graph.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.start_date = self.query_params.get("start_date", None)
        self.end_date = self.query_params.get("end_date", None)

        start_full_date = start_date_values(self.start_date, self.end_date)
        end_full_date = end_date_values(self.end_date)

        companies_dict = {}

        competitors = get_data_group_by_range(pk, end_full_date)

        for company in competitors:
            temp_dict = {}

            company_id = company["company_id"]

            seo_score = get_primary_table_by_companyid(
                Seo, company_id).order_by('initial_date').filter(
                initial_date__range=(start_full_date, end_full_date))

            keywords_list = build_graph_dict(seo_score, "total_keywords")
            traffic_cost_list = build_graph_dict(seo_score, "paid_keywords")

            temp_dict["keywords"] = keywords_list
            temp_dict["traffic_cost"] = traffic_cost_list

            company_name = get_company_url_by_id(company_id)

            companies_dict[company_name] = temp_dict

        return http_ok(companies_dict)

    @action(methods=["GET"], detail=False,
            url_path="seo-score/(?P<pk>\\d+)/keywords-graph-all-dates")
    def get_seo_score_keywords_graph_all_dates(self, request, pk):
        """
        Get Seo Score Keywords Graph.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.start_date = self.query_params.get("start_date", None)
        self.end_date = self.query_params.get("end_date", None)

        start_full_date = start_date_values(self.start_date, self.end_date)
        end_full_date = end_date_values(self.end_date)

        company_id = get_company_id(pk)

        allSeoKeywords = []
        entries = getAllSeoDates(pk)
        for initial_date in entries:
            # initial_date = entry["initial_date"]
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
                temp_dict = {}

                company_id = company["company_id"]

                seo_score = get_primary_table_by_companyid(
                    Seo, company_id).order_by('initial_date').filter(
                    initial_date__range=(start_full_date, end_full_date))
                keywords_list = build_graph_dict(seo_score, "total_keywords")
                traffic_cost_list = build_graph_dict(
                    seo_score, "paid_keywords")

                temp_dict["keywords"] = keywords_list
                temp_dict["traffic_cost"] = traffic_cost_list

                company_name = get_company_url_by_id(company_id)

                companies_dict[company_name] = temp_dict

            if companies_dict != {}:
                allSeoKeywords.append(companies_dict)

        return http_ok(allSeoKeywords)

    @action(methods=["GET"], detail=False,
            url_path="seo-score/(?P<pk>\\d+)/direct-competitors")
    def get_seo_score_competitors(self, request, pk):
        """
        Get Seo Direct Competitors.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.end_date = self.query_params.get("end_date", None)
        self.web_end_date = self.query_params.get("web_end_date", None)
        self.seo_end_date = self.query_params.get("seo_end_date", None)

        # end_date = end_date_values(self.end_date)
        web_end_date = end_date_values(self.web_end_date)
        seo_end_date = end_date_values(self.seo_end_date)

        direct_competitors_list = []

        direct_competitors = get_data_group_by_range(pk, seo_end_date)

        count = check_competitors(pk)

        company_project_id = get_company_id(pk)

        for companies in direct_competitors:
            temp = {}
            company_data_id = companies["company_id"]
            company_data = get_primary_table_by_companyid(Seo, company_data_id)

            website_temp_last = get_data_last_by_company_id_table(
                Website,
                company_data_id,
                web_end_date
            )

            website_last = get_secondary_by_primaryid(
                Website_traffic,
                website_temp_last["website_id"]
            )

            if company_data and website_last:
                for company in company_data:
                    company_id = company_data_id
                    temp["company_id"] = company_id
                    temp["company_url"] = get_company_url_by_id(company_id)
                    temp["seo_score"] = companies["seo_score"]
                    temp["organic_traffic"] = company["organic_traffic"]
                    temp["web_authority"] = company["web_authority"]
                    temp["total_keywords"] = company["total_keywords"]
                    temp["avg_keywords_search"] = \
                        company["avg_keywords_search"]
                    temp["referred_traffic"] = \
                        website_last[0]["reffered_traffic"]
                    temp["backlinks"] = company["backlinks"]
                    temp["referring_domains"] = company["referring_domains"]
                    temp["avg_organic_rank"] = company["avg_organic_rank"]

                    temp["check_company"] = isCompanyProjectID(
                        company_id, company_project_id)

                # temp["check_company"] = int(company_id) == company_project_id
            direct_competitors_list.append(temp)
        return http_ok(direct_competitors_list[0:(11 - count)])


def seo_direct_competitors_dict(company_data,
                                company_score,
                                company_project_id):
    temp = {}
    company_id = company_data["company_id"]
    temp["company_id"] = company_id
    temp["company_url"] = get_company_url_by_id(company_id)
    temp["seo_score"] = company_score
    temp["organic_traffic"] = company_data["organic_traffic"]
    temp["web_authority"] = company_data["web_authority"]
    temp["total_keywords"] = company_data["total_keywords"]
    temp["backlinks"] = company_data["backlinks"]
    temp["referring_domains"] = company_data["referring_domains"]
    temp["avg_organic_rank"] = company_data["avg_organic_rank"]
    temp["check_company"] = isCompanyProjectID(
        company_id, company_project_id
    )

    return temp
