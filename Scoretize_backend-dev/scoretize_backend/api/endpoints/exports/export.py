from ...views import viewsets, APIView, IsAuthenticated, \
    action, \
    HttpResponse, \
    is_user_project, br_project_not_user, \
    start_date_values, \
    end_date_values, \
    get_companies_id, \
    Company_wise_scores, Q, Seo, \
    Website, Website_traffic, \
    Social_media, Instagram, \
    Facebook, Twitter, Youtube, \
    not_found
import csv


class ExportDataViewSet(viewsets.ViewSet, APIView):
    permission_classes = (IsAuthenticated,)

    @action(methods=["GET"], detail=False, url_path="csv/scores/(?P<pk>\\d+)")
    def export_csv_scores(self, request, pk):
        """
        Exports scores in csv format.
        """
        if not is_user_project(request.user.id, pk):
            return br_project_not_user()

        self.query_params = self.request.query_params
        self.start_date = self.query_params.get("start_date", None)
        self.end_date = self.query_params.get("end_date", None)

        start_full_date = start_date_values(self.start_date, self.end_date)
        end_full_date = end_date_values(self.end_date)

        # Company wise scores
        response = HttpResponse(
            content_type='text/csv;charset=UTF-8',
            headers={
                'Content-Disposition': 'attachment; filename="scores.csv"'
            },
        )

        company_table = Company_wise_scores.objects.filter(
            Q(project_id=pk) &
            Q(initial_date__range=(start_full_date, end_full_date))
        ).order_by('initial_date').values()

        if not company_table:
            return not_found(
                'No data for selected date',
                'No data for selected date'
            )
        writer = csv.writer(response, delimiter=',')
        writer.writerow(['scores'])

        column_names = []
        for value in company_table[0]:
            if value == 'initial_date':
                value = 'date'
            column_names.append(value)
        writer.writerow(column_names)

        for company in company_table:
            store_values = []
            for key, value in company.items():
                if key == 'initial_date':
                    value = value.strftime('%Y-%m-%d')
                store_values.append(value)
            writer.writerow(store_values)

        return response

    @action(methods=["GET"], detail=False, url_path="csv/seo/(?P<pk>\\d+)")
    def export_csv_seo(self, request, pk):
        """
        Exports SEO data in csv format.
        """
        self.query_params = self.request.query_params
        self.start_date = self.query_params.get("start_date", None)
        self.end_date = self.query_params.get("end_date", None)

        start_full_date = start_date_values(self.start_date, self.end_date)
        end_full_date = end_date_values(self.end_date)

        companies_id = get_companies_id(pk)

        seo_response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="seo.csv"'},
        )

        seo_data = []

        for company_id in companies_id:
            seo_table = Seo.objects.filter(
                Q(company_id=company_id) &
                Q(initial_date__range=(start_full_date, end_full_date))
            ).order_by('initial_date').values().last()
            seo_data.append(seo_table)

        writer = csv.writer(seo_response, delimiter=',')
        writer.writerow(['seo'])

        if not seo_data[0]:
            return not_found(
                'No data for selected date',
                'No data for selected date'
            )

        column_names = []
        for key, value in seo_data[0].items():
            if key == 'initial_date':
                key = 'date'
            column_names.append(key)
        writer.writerow(column_names)

        for company in seo_data:
            store_values = []
            for key, value in company.items():
                if key == 'initial_date':
                    value = value.strftime('%Y-%m-%d')
                store_values.append(value)
            writer.writerow(store_values)

        return seo_response

    @action(methods=["GET"], detail=False, url_path="csv/website/(?P<pk>\\d+)")
    def export_csv_website(self, request, pk):
        """
        Exports Website data in csv format.
        """
        self.query_params = self.request.query_params
        self.start_date = self.query_params.get("start_date", None)
        self.end_date = self.query_params.get("end_date", None)

        start_full_date = start_date_values(self.start_date, self.end_date)
        end_full_date = end_date_values(self.end_date)

        companies_id = get_companies_id(pk)

        website_response = HttpResponse(
            content_type='text/csv',
            headers={
                'Content-Disposition': 'attachment; filename="website.csv"'
            },
        )

        website_data = []
        website_ids = []
        website_traffic_data = []

        for company_id in companies_id:
            website_table = Website.objects.filter(
                Q(company_id=company_id) &
                Q(initial_date__range=(start_full_date, end_full_date))
            ).order_by('initial_date').values().last()
            website_data.append(website_table)
            if not website_table:
                return not_found(
                    'No data for selected date',
                    'No data for selected date'
                )
            website_ids.append(website_table["website_id"])

        writer = csv.writer(website_response, delimiter=',')
        writer.writerow(['website'])

        if not website_data[0]:
            return not_found(
                'No data for selected date',
                'No data for selected date'
            )

        column_names = []
        for key, value in website_data[0].items():
            if key == 'initial_date':
                key = 'date'
            column_names.append(key)
        writer.writerow(column_names)

        for company in website_data:
            store_values = []
            for key, value in company.items():
                if key == 'initial_date':
                    value = value.strftime('%Y-%m-%d')
                store_values.append(value)
            writer.writerow(store_values)

        writer.writerow(['website_traffic'])

        for website_id in website_ids:
            website_traffic = Website_traffic.objects.filter(
                website_id=website_id
            ).values().last()
            website_traffic_data.append(website_traffic)

        if not website_traffic_data[0]:
            return not_found(
                'No data for selected date',
                'No data for selected date'
            )

        column_names = []
        for key, value in website_traffic_data[0].items():
            if key != 'id':
                column_names.append(key)
        writer.writerow(column_names)

        for company in website_traffic_data:
            store_values = []
            for key, value in company.items():
                if key != 'id':
                    if key == 'initial_date':
                        value = value.strftime('%Y-%m-%d')
                    store_values.append(value)
            writer.writerow(store_values)

        return website_response

    @action(methods=["GET"], detail=False, url_path="csv/sm/(?P<pk>\\d+)")
    def export_csv_sm(self, request, pk):
        """
        Exports Social Media data in csv format.
        """
        self.query_params = self.request.query_params
        self.start_date = self.query_params.get("start_date", None)
        self.end_date = self.query_params.get("end_date", None)

        start_full_date = start_date_values(self.start_date, self.end_date)
        end_full_date = end_date_values(self.end_date)

        companies_id = get_companies_id(pk)

        sm_response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="sm.csv"'},
        )

        sm_data = []
        sm_ids = []

        for company_id in companies_id:
            sm_table = Social_media.objects.filter(
                Q(company_id=company_id) &
                Q(initial_date__range=(start_full_date, end_full_date))
            ).order_by('initial_date').values().last()
            sm_data.append(sm_table)
            if not sm_table:
                return not_found(
                    'No data for selected date',
                    'No data for selected date'
                )
            sm_ids.append(sm_table["social_id"])

        writer = csv.writer(sm_response, delimiter=',')
        writer.writerow(['social_media'])

        if not sm_data[0]:
            return not_found(
                'No data for selected date',
                'No data for selected date'
            )

        column_names = []
        for key, value in sm_data[0].items():
            if key == 'initial_date':
                key = 'date'
            column_names.append(key)
        writer.writerow(column_names)

        for company in sm_data:
            store_values = []
            for key, value in company.items():
                if key == 'initial_date':
                    value = value.strftime('%Y-%m-%d')
                store_values.append(value)
            writer.writerow(store_values)

        writer.writerow(['sm_instagram'])

        sm_instagram_data = []

        for sm_id in sm_ids:
            sm_instagram = Instagram.objects.filter(
                social_media_id=sm_id
            ).values().last()
            sm_instagram_data.append(sm_instagram)

        column_names = []
        for key, value in sm_instagram_data[0].items():
            if key != 'id':
                column_names.append(key)
        writer.writerow(column_names)

        for company in sm_instagram_data:
            store_values = []
            for key, value in company.items():
                if key != 'id':
                    store_values.append(value)
            writer.writerow(store_values)

        writer.writerow(['sm_facebook'])

        sm_facebook_data = []

        for sm_id in sm_ids:
            sm_facebook = Facebook.objects.filter(
                social_media_id=sm_id
            ).values().last()
            sm_facebook_data.append(sm_facebook)

        column_names = []
        for key, value in sm_facebook_data[0].items():
            if key != 'id':
                column_names.append(key)
        writer.writerow(column_names)

        for company in sm_facebook_data:
            store_values = []
            for key, value in company.items():
                if key != 'id':
                    store_values.append(value)
            writer.writerow(store_values)

        writer.writerow(['sm_twitter'])

        sm_twitter_data = []

        for sm_id in sm_ids:
            sm_twitter = Twitter.objects.filter(
                social_media_id=sm_id
            ).values().last()
            sm_twitter_data.append(sm_twitter)

        column_names = []
        for key, value in sm_twitter_data[0].items():
            if key != 'id':
                column_names.append(key)
        writer.writerow(column_names)

        for company in sm_twitter_data:
            store_values = []
            for key, value in company.items():
                if key != 'id':
                    store_values.append(value)
            writer.writerow(store_values)

        writer.writerow(['sm_youtube'])
        sm_youtube_data = []
        for sm_id in sm_ids:
            sm_youtube = Youtube.objects.filter(
                social_media_id=sm_id
            ).values().last()
            sm_youtube_data.append(sm_youtube)

        column_names = []
        for key, value in sm_youtube_data[0].items():
            if key != 'id':
                column_names.append(key)
        writer.writerow(column_names)

        for company in sm_youtube_data:
            store_values = []
            for key, value in company.items():
                if key != 'id':
                    store_values.append(value)
            writer.writerow(store_values)

        return sm_response
