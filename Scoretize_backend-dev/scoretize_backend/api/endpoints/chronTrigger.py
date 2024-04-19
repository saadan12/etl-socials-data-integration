from ..views import viewsets, APIView, IsAuthenticated, \
    action, Project, get_company_url_by_id, \
    Response, \
    status, Users, \
    Company, \
    Facebook, Instagram, Twitter, \
    Youtube, get_company_by_url
from .project.project import ETL_update, check_current_month_data, \
    generate_non_repeated_uuid, check_uuid_by_company_id
from datetime import datetime
import sys
import time


class ChronTriggerViewSet(viewsets.ViewSet, APIView):
    permission_classes = (IsAuthenticated,)

    @action(methods=["GET"], detail=False, url_path="company-scrapping")
    def send_chron_trigger(self, request):
        """
        Temp endpoint. Does nothing.
        """
        users = Users.objects.values('email', 'name')

        for user in users:
            print(user)

        return Response({
            'error': '',
            'message': 'Successful request',
            'data': 'project_dict',
            'response_ETL': 'OK'
        }, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, url_path="update-projects")
    def send_companies_scrapping(self, request):
        """
        Updates all projects.
        """
        projects = Project.objects.all().values()
        for project in projects:
            if project["is_active"] == 3:
                pass
            else:
                project_dict = {}
                companies_url_array = []
                companies_id_array = []

                project_dict["client_id"] = project["company_id"]
                project_dict["project_id"] = project["id"]
                project_dict["sector_id"] = project["sector_id"]

                company = competitor = get_company_url_by_id(
                    project["company_id"])
                companies_url_array.append(company)
                companies_id_array.append(project["company_id"])

                for key, value in project.items():
                    if "competitor" in key and value is not None:
                        competitor = get_company_url_by_id(value)
                        companies_url_array.append(competitor)
                        companies_id_array.append(value)

                new_company_array = []
                new_company_id_array = []

                # Check if we have data for current month for each URL
                for company in companies_url_array:
                    if get_company_by_url(company):
                        (check_Website,
                            check_Seo,
                            check_SocialMedia) = check_current_month_data(
                            company
                        )
                        if not check_Website \
                                or not check_Seo \
                                or not check_SocialMedia:
                            new_company_array.append(company)

                for company in new_company_array:
                    company_id = Company.objects.filter(
                        url=company).values('id').first()
                    new_company_id_array.append(int(company_id['id']))

                connection_name = 'tkf-' + str(project["id"])

                uuid_dict = {}
                uuid_list = []
                new_uuid_dict = {}

                for company_id in companies_id_array:
                    check_uuid = check_uuid_by_company_id(company_id)
                    if check_uuid:
                        unique = check_uuid['website_id']
                        uuid_list.append(unique)
                    else:
                        unique = generate_non_repeated_uuid(company_id)
                        uuid_list.append(unique)

                counter = 0
                for company in companies_url_array:
                    uuid_dict[company] = uuid_list[counter]
                    counter += 1

                for company in new_company_array:
                    if company in companies_url_array:
                        pos = companies_url_array.index(company)
                        new_uuid_dict[company] = uuid_list[pos]

                project_dict["site_list"] = companies_url_array
                project_dict["new_site_list"] = new_company_array
                project_dict["company_id"] = companies_id_array
                project_dict["new_company_id"] = new_company_id_array
                project_dict["container_name"] = connection_name
                project_dict["timestamp"] = datetime.today(
                ).strftime('%Y-%m-%d')
                project_dict["unique_ids"] = uuid_dict
                project_dict["new_unique_ids"] = new_uuid_dict

                if 'test' not in sys.argv:
                    ETL_update(project_dict)

                time.sleep(60)

        return Response({
            'error': '',
            'message': 'Successful request',
            'data': 'project_dict',
            'response_ETL': 'OK'
        }, status=status.HTTP_200_OK)

    @action(methods=["GET"],
            detail=False,
            url_path="update-project/(?P<pk>\\d+)")
    def force_company_update(self, request, pk):
        """
        Update an specific project.
        """
        projects = Project.objects.filter(id=pk).values()
        for project in projects:
            if project["is_active"]:
                project_dict = {}
                companies_url_array = []
                companies_id_array = []

                project_dict["client_id"] = project["company_id"]
                project_dict["project_id"] = project["id"]
                project_dict["sector_id"] = project["sector_id"]

                company = competitor = get_company_url_by_id(
                    project["company_id"])
                companies_url_array.append(company)
                companies_id_array.append(project["company_id"])

                for key, value in project.items():
                    if "competitor" in key and value is not None:
                        competitor = get_company_url_by_id(value)
                        companies_url_array.append(competitor)
                        companies_id_array.append(value)

                connection_name = 'tkf-' + str(pk)

                uuid_dict = {}
                uuid_list = []
                new_uuid_dict = {}

                for company_id in companies_id_array:
                    unique = generate_non_repeated_uuid(company_id)
                    uuid_list.append(unique)

                counter = 0
                for company in companies_url_array:
                    uuid_dict[company] = uuid_list[counter]
                    counter += 1

                for company in companies_url_array:
                    pos = companies_url_array.index(company)
                    new_uuid_dict[company] = uuid_list[pos]

                project_dict["site_list"] = companies_url_array
                project_dict["new_site_list"] = companies_url_array
                project_dict["company_id"] = companies_id_array
                project_dict["new_company_id"] = companies_id_array
                project_dict["container_name"] = connection_name
                project_dict["timestamp"] = datetime.today(
                ).strftime('%Y-%m-%d')
                project_dict["unique_ids"] = uuid_dict
                project_dict["new_unique_ids"] = new_uuid_dict

                # project_id = project["id"]
                # user_id = UserProject.objects.filter(
                #     project_id=project_id).values(
                #     ).first()["user_id"]
                # user = Users.objects.filter(id=user_id).values().first()
                # user_email = user["email"]
                # user_name = user["name"]
                # project_name = project["name"]

                if 'test' not in sys.argv:
                    ETL_update(project_dict)
            else:
                pass

        return Response({
            'error': '',
            'message': 'Successful request',
            'data': 'project_dict',
            'response_ETL': 'OK'
        }, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, url_path="update-engagement-rate")
    def update_engagement_rate(self, request):
        """
        Recalculates engagement rate for all Social Media.
        """
        facebook_data = Facebook.objects.all()
        for company in facebook_data:
            avg_post = company.avg_post_likes
            followers = company.followers
            if avg_post and followers:
                engagement_rate = ((avg_post / followers)*100)
            else:
                engagement_rate = 0
            company = Facebook.objects.filter(id=company.id)
            company.update(fb_engagement_rate=engagement_rate)

        instagram_data = Instagram.objects.all()
        for company in instagram_data:
            avg_post = company.avg_post_likes
            followers = company.followers
            if avg_post and followers:
                engagement_rate = ((avg_post / followers)*100)
            else:
                engagement_rate = 0
            company = Instagram.objects.filter(id=company.id)
            company.update(insta_engagement_rate=engagement_rate)

        twitter_data = Twitter.objects.all()
        for company in twitter_data:
            avg_likes = company.avg_likes_count
            followers = company.followers_count
            if avg_likes and followers:
                engagement_rate = ((avg_likes / followers)*100)
            else:
                engagement_rate = 0
            company = Twitter.objects.filter(id=company.id)
            company.update(twitter_engagement_rate=engagement_rate)

        Youtube_data = Youtube.objects.all()
        for company in Youtube_data:
            like_count = company.like_count
            video_count = company.video_count
            if like_count and video_count:
                avg_interations = (like_count/video_count)
            suscribers = company.subscriber_count
            if avg_interations and suscribers:
                engagement_rate = ((avg_interations / suscribers)*100)
            else:
                engagement_rate = 0
            company = Youtube.objects.filter(id=company.id)
            company.update(youtube_engagement_rate=engagement_rate)

        return Response({
            'error': '',
            'message': 'Successful request',
            'data': 'project_dict',
            'response_ETL': 'OK'
        }, status=status.HTTP_200_OK)
