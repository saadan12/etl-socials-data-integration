from ..views import viewsets, APIView, IsAuthenticated, \
    action, is_user_project, \
    start_date_values, \
    get_company_id, not_found, \
    http_ok, isCompanyProjectID, \
    check_competitors, get_company_url_by_id, \
    get_data_by_range, \
    br_project_not_user, get_data_group_by_range, \
    end_date_values


class GlobalViewSet(viewsets.ViewSet, APIView):
    permission_classes = (IsAuthenticated,)

    @action(methods=["GET"],
            detail=False,
            url_path="global-score/(?P<pk>\\d+)")
    def get_global_score(self, request, pk):
        """
        Get Global Score data for 2 months.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params

        self.end_date = self.query_params.get("end_date", None)
        end_date = end_date_values(self.end_date)

        self.start_date = self.query_params.get("start_date", None)
        start_date = start_date_values(self.start_date, self.end_date)

        company_id = get_company_id(pk)

        website_score_last = get_data_by_range(pk, company_id, end_date)
        website_score_start = get_data_by_range(pk, company_id, start_date)

        if not website_score_last:
            return not_found('No Website data for this project', '')

        global_score_duo = {}

        global_score_duo["global_score"] = website_score_last["global_score"]

        if not website_score_start:
            global_score_duo["global_score_month"] = None
        else:
            global_score_duo["global_score_month"] = \
                website_score_start["global_score"]

        return http_ok(global_score_duo)

    @action(methods=["GET"], detail=False,
            url_path="global-score/(?P<pk>\\d+)/direct-competitors")
    def get_global_score_competitors(self, request, pk):
        """
        Get Direct Competitors for a month.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.end_date = self.query_params.get("end_date", None)
        end_date = end_date_values(self.end_date)

        global_score_dict = {}

        direct_competitors_list = []

        direct_competitors = get_data_group_by_range(pk, end_date)

        count = check_competitors(pk)

        company_project_id = get_company_id(pk)

        for companies in direct_competitors:
            temp = global_direct_competitors_dict(
                companies,
                company_project_id
            )

            direct_competitors_list.append(temp)

        global_score_dict["direct_competitors"] = direct_competitors_list[0:(
            11 - count)]

        return http_ok(global_score_dict)


def global_direct_competitors_dict(
    companies,
    company_project_id
):
    temp = {}
    company_temp_id = companies["company_id"]
    temp["company_id"] = company_temp_id
    temp["company_url"] = get_company_url_by_id(company_temp_id)
    temp["global_score"] = companies["global_score"]
    temp["website_score"] = companies["website_score"]
    temp["seo_score"] = companies["seo_score"]
    temp["sm_score"] = companies["sm_score"]
    # temp["searchAds_score"] = companies["searchAds_score"]
    temp["check_company"] = isCompanyProjectID(
        company_temp_id, company_project_id)

    return temp
