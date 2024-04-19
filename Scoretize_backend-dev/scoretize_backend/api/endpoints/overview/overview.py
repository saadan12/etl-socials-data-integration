from ...views import viewsets, APIView, IsAuthenticated, action
from ...views import end_date_values
from ...views import http_ok, get_scores_by_company_project_filterDate
from ...views import build_graph_dict
from ...views import get_company_id
from ...views import get_start_date_from_project_date
from ...views import is_user_project
from ...views import br_project_not_user


class OverviewViewSet(viewsets.ViewSet, APIView):
    permission_classes = (IsAuthenticated,)

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

        company_id = get_company_id(pk)

        website_score = get_scores_by_company_project_filterDate(
            company_id,
            pk,
            end_full_date,
            start_full_date
        )

        evolution_score = build_graph_dict(website_score, "website_score")

        return http_ok(evolution_score)

    @action(methods=["GET"], detail=False,
            url_path="seo-score/(?P<pk>\\d+)/evolution")
    def get_seo_score_evolution(self, request, pk):
        """
        Get Seo Score Evolution.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.start_date = self.query_params.get("start_date", None)
        self.end_date = self.query_params.get("end_date", None)

        start_full_date = get_start_date_from_project_date(pk, self.start_date)
        end_full_date = end_date_values(self.end_date)

        company_id = get_company_id(pk)

        seo_score = get_scores_by_company_project_filterDate(
            company_id,
            pk,
            end_full_date,
            start_full_date
        )

        evolution_score = build_graph_dict(seo_score, "seo_score")

        return http_ok(evolution_score)

    @action(methods=["GET"], detail=False,
            url_path="paid-media/(?P<pk>\\d+)/evolution")
    def get_searchAds_score_evolution(self, request, pk):
        """
        Get Search Ads / Paid Media Score Evolution.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.start_date = self.query_params.get("start_date", None)
        self.end_date = self.query_params.get("end_date", None)

        start_full_date = get_start_date_from_project_date(pk, self.start_date)
        end_full_date = end_date_values(self.end_date)

        company_id = get_company_id(pk)

        searchAds_score = get_scores_by_company_project_filterDate(
            company_id,
            pk,
            end_full_date,
            start_full_date
        )

        evolution_score = build_graph_dict(searchAds_score, "searchAds_score")

        return http_ok(evolution_score)

    @action(methods=["GET"], detail=False,
            url_path="socialMedia-score/(?P<pk>\\d+)/evolution")
    def get_socialMedia_score_evolution(self, request, pk):
        """
        Get Social Media Score Evolution.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.start_date = self.query_params.get("start_date", None)
        self.end_date = self.query_params.get("end_date", None)

        start_full_date = get_start_date_from_project_date(pk, self.start_date)
        end_full_date = end_date_values(self.end_date)

        company_id = get_company_id(pk)

        socialMedia_score = get_scores_by_company_project_filterDate(
            company_id,
            pk,
            end_full_date,
            start_full_date
        )

        evolution_score = build_graph_dict(socialMedia_score, "sm_score")

        return http_ok(evolution_score)
