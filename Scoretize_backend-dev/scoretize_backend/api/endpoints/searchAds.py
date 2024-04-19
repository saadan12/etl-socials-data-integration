from ..views import viewsets, APIView, IsAuthenticated, action, \
    is_user_project, start_date_values, \
    end_date_values, get_company_id, \
    Seo, not_found, \
    http_ok, \
    check_competitors, \
    get_primary_table_by_companyid, \
    get_company_url_by_id, isCompanyProjectID, \
    br_project_not_user, \
    get_data_last_by_company_id_table, \
    get_data_by_range, get_data_group_by_range


class SearchAdsviewViewSet(viewsets.ViewSet, APIView):
    permission_classes = (IsAuthenticated,)

    @action(methods=["GET"], detail=False,
            url_path="paid-media/(?P<pk>\\d+)")
    def get_searchAds_score(self, request, pk):
        """
        Get Search Ads / Paid Media KPI's.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params

        self.end_date = self.query_params.get("end_date", None)
        end_date = end_date_values(self.end_date)

        self.start_date = self.query_params.get("start_date", None)
        start_date = start_date_values(self.start_date, self.end_date)

        company_id = get_company_id(pk)

        searchAds_global_last = get_data_last_by_company_id_table(
            Seo,
            company_id,
            end_date
        )
        searchAds_score_last = get_data_by_range(
            pk,
            company_id,
            end_date
        )

        if not searchAds_global_last or not searchAds_score_last:
            return not_found('No website data for this project', '')

        searchAds_global_start = get_data_last_by_company_id_table(
            Seo,
            company_id,
            start_date
        )
        searchAds_score_start = get_data_by_range(
            pk,
            company_id,
            start_date
        )

        searchAds_score_dict = {}

        searchAds_score_dict["searchAds_last_score"] = \
            searchAds_score_last["searchAds_score"]
        searchAds_score_dict["paid_traffic"] = \
            searchAds_global_last["paid_traffic"]
        searchAds_score_dict["estimated_CPC"] = \
            searchAds_global_last["estimatedCPC"]
        searchAds_score_dict["paid_keywords"] = \
            searchAds_global_last["paid_keywords"]
        searchAds_score_dict["estimated_ppc_budget"] = \
            searchAds_global_last["estm_ppc_budget"]

        if not searchAds_score_start:
            searchAds_score_dict["searchAds_last_score_month"] = None
        else:
            searchAds_score_dict["searchAds_last_score_month"] = \
                searchAds_score_start["searchAds_score"]

        if not searchAds_global_start or not searchAds_score_start:
            searchAds_score_dict["searchAds_last_score_month"] = None
            searchAds_score_dict["paid_traffic_month"] = None
            searchAds_score_dict["estimated_CPC_month"] = None
            searchAds_score_dict["paid_keywords_month"] = None
            searchAds_score_dict["estimated_ppc_budget_month"] = None
        else:
            searchAds_score_dict["paid_traffic_month"] = \
                searchAds_global_start["paid_traffic"]
            searchAds_score_dict["estimated_CPC_month"] = \
                searchAds_global_start["estimatedCPC"]
            searchAds_score_dict["paid_keywords_month"] = \
                searchAds_global_start["paid_keywords"]
            searchAds_score_dict["estimated_ppc_budget_month"] = \
                searchAds_global_start["estm_ppc_budget"]

        return http_ok(searchAds_score_dict)

    @action(methods=["GET"], detail=False,
            url_path="paid-media/(?P<pk>\\d+)/direct-competitors")
    def get_searchAds_direct_competitors(self, request, pk):
        """
        Get Direct Competitors on Search Ads / Paid Media.
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

            company_data = get_primary_table_by_companyid(Seo, company_data_id)

            for company in company_data:
                company_id = company_data_id
                temp["company_id"] = company_id
                temp["company_url"] = get_company_url_by_id(company_id)
                temp["paid_media_score"] = companies["searchAds_score"]
                temp["paid_traffic"] = company["paid_traffic"]
                temp["estimated_CPC"] = company["estimatedCPC"]
                temp["paid_keywords"] = company["paid_keywords"]
                temp["estm_ppc_budget"] = company["estm_ppc_budget"]

                temp["check_company"] = isCompanyProjectID(
                    company_id, company_project_id)

            direct_competitors_list.append(temp)

        return http_ok(direct_competitors_list[0:(11 - count)])


def paid_media_direct_competitors_dict(
        company_data,
        company_score,
        company_project_id):
    temp = {}
    company_id = company_data["company_id"]
    temp["company_id"] = company_id
    temp["company_url"] = get_company_url_by_id(company_id)
    temp["paid_media_score"] = company_score
    temp["paid_traffic"] = company_data["paid_traffic"]
    temp["estimatedCPC"] = company_data["estimatedCPC"]
    temp["paid_keywords"] = company_data["paid_keywords"]
    temp["estm_ppc_budget"] = company_data["estm_ppc_budget"]
    temp["check_company"] = isCompanyProjectID(
        company_id, company_project_id
    )

    return temp
