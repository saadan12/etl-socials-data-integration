import sys
import os
import calendar
from datetime import datetime
from ...model.model_website import Website
from ...model.seo_data import Seo
from django.db.models import Q
from ...model.social_media_data import Social_media
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.identity import ClientSecretCredential
from ...views import viewsets, APIView, IsAuthenticated, \
    action, get_sector_by_name, bad_request, \
    get_company_by_url, CompanySerializer, \
    IntegrityError, get_company_id_by_url, \
    ProjectSerializer, Response, status, \
    UserProjectSerializer, Users, \
    UserProject, Company_wise_scores, \
    Account, Project, Company, \
    send_mail_for_project_confirmation, \
    send_mail_for_email_verification, \
    send_mail_for_project_fail, \
    random_with_N_digits, add_https_to_urls, \
    add_competitors_to_dict, \
    check_competitors_length, \
    check_dupes
from api.endpoints.account.account import AccountProperties


class ManageProject(viewsets.ViewSet, APIView):
    permission_classes = (IsAuthenticated,)

    @action(methods=["POST"], detail=False, url_path="create-project")
    def createProject(self, request):
        """
        Create a new Project.
        """
        # Check if max_num_account_projects is equal
        # to num_active_account_projects
        account_properties_view = AccountProperties()
        account_info = account_properties_view.getNumAccountProjects(request)
        max_num_account_projects = \
            account_info.data["data"]["max_num_account_projects"]
        num_active_account_projects = \
            account_info.data["data"]["num_active_account_projects"]

        # Compare max_num_account_projects and num_active_account_projects
        if max_num_account_projects == num_active_account_projects:
            return Response({
                'error': 'Cannot create the project',
                'message':
                'Number of active projects exceeds the maximum allowed.',
                'data': ''
            }, status=status.HTTP_400_BAD_REQUEST,
                content_type='application/json')
        else:
            # Declare dicts
            project_dict = {}
            user_project = {}

            ETL_dict = {}
            # Inputs needed to create a project
            project_dict["name"] = request.data["name"].lower()

            request.data["sector_name"] = request.data["sector_name"].lower()
            request.data["subcategory"] = request.data["subcategory"].lower()

            # Check if sector and subcategory exists in Scoretize DB
            sector_check = get_sector_by_name(
                request.data["sector_name"],
                request.data["subcategory"]
            )

            if not sector_check:
                return bad_request(
                    'Sector does not exist',
                    'Sector does not exist',
                    ''
                )

            # Fill the FK sector_id inside Project table
            project_dict["sector"] = sector_check.values_list(
                'id', flat=True).first()

            company_array = []
            company_id_array = []

            # All competitors inside a list. Check number of competitors
            competitors_naked = list(filter(None, request.data["competitors"]))

            if not check_competitors_length(competitors_naked):
                return bad_request(
                    'Competitors should be between 2 and 10',
                    'Competitors should be between 2 and 10',
                    ''
                )

            # Add https to Company URL and append to 'Company_array'
            request.data["company_url"] = add_https_to_urls(
                [request.data["company_url"]])[0]
            company_array.append(request.data["company_url"])

            # Add https to Competitors list and append to 'Company_array'
            competitors = []
            competitors = add_https_to_urls(competitors_naked)
            for competitor in competitors:
                company_array.append(competitor)

            # Check no duplicated URLs (Company and competitors
            # cannot be the same)
            if not check_dupes(company_array):
                return bad_request('Duplicated URLs', 'Duplicated URLs', '')

            new_company_array = []

            # Check if we have data for current month for each URL
            for company in company_array:
                if get_company_by_url(company):
                    (check_Website,
                        check_Seo,
                        check_SocialMedia) = check_current_month_data(company)
                    if not check_Website \
                            or not check_Seo \
                            or not check_SocialMedia:
                        new_company_array.append(company)
                if not get_company_by_url(company):
                    new_company_array.append(company)
            print(len(new_company_array))
            print(len(company_array))

            if 'test' not in sys.argv:
                if len(new_company_array) == len(company_array):
                    print(True)
                else:
                    print(False)

            # Store non-existent companies inside Company table
            for company in company_array:
                company_check = get_company_by_url(company)
                if not company_check:
                    company_dict = {}
                    company_dict["url"] = company
                    companySerializer = CompanySerializer(data=company_dict)

                    if not companySerializer.is_valid(raise_exception=True):
                        return bad_request(
                            'URLs does not exist',
                            'There has been an error',
                            ''
                        )
                    try:
                        companySerializer.save()

                    except IntegrityError as e:
                        return bad_request(
                            e,
                            'There has been an error',
                            ''
                        )
                    else:
                        pass

            # Values for Project table (IDs)
            project_dict["company"] = get_company_id_by_url(
                request.data["company_url"])

            project_dict = add_competitors_to_dict(competitors, project_dict)
            project_dict["is_active"] = 0
            projectSerializer = ProjectSerializer(data=project_dict)

            if not projectSerializer.is_valid(raise_exception=True):
                return Response({
                    'error': 'Cannot create the project',
                    'message': 'There has been an error',
                    'data': ''
                }, status=status.HTTP_400_BAD_REQUEST,
                    content_type='application/json')

            try:
                projectSerializer.save()

            except IntegrityError as e:
                return Response({
                    'error': e,
                    'message': 'There has been an error',
                    'data': ''
                }, status=status.HTTP_400_BAD_REQUEST)

            # Storing data inside User-Project intermediate table
            user_project["user"] = request.user.id
            user_project["project"] = projectSerializer.data["id"]

            userProjectSerializer = UserProjectSerializer(data=user_project)

            if not userProjectSerializer.is_valid(raise_exception=True):
                return Response({
                    'error': 'Cannot create the project',
                    'message': 'There has been an error',
                    'data': ''
                }, status=status.HTTP_400_BAD_REQUEST,
                    content_type='application/json')

            try:
                userProjectSerializer.save()

            except IntegrityError as e:
                return Response({
                    'error': e,
                    'message': 'There has been an error',
                    'data': ''
                }, status=status.HTTP_400_BAD_REQUEST)

            new_company_id_array = []
            company_id_array.append(project_dict["company"])

            for company in new_company_array:
                company_id = Company.objects.filter(
                    url=company).values('id').first()
                new_company_id_array.append(company_id['id'])

            for key in project_dict:
                if 'competitor_' in key:
                    company_id_array.append(project_dict[key])

            # Connection Name used on ETL to handle containers
            connection_name = 'tkf-' + str(user_project["project"])

            # Declare dict/list, generate and store non-repeated uuidss
            uuid_dict = {}
            uuid_list = []
            new_uuid_dict = {}

            for company_id in company_id_array:
                uuid_list.append(company_id)

            # Store URLs in order to send to the ETL
            counter = 0
            for company in company_array:
                uuid_dict[company] = uuid_list[counter]
                counter += 1

            for company in new_company_array:
                if company in company_array:
                    pos = company_array.index(company)
                    new_uuid_dict[company] = uuid_list[pos]

            # ETL Dictionary
            ETL_dict["client_id"] = project_dict["company"]
            ETL_dict["project_id"] = user_project["project"]
            ETL_dict["sector_id"] = project_dict["sector"]
            ETL_dict["site_list"] = company_array
            ETL_dict["new_site_list"] = new_company_array
            ETL_dict["company_id"] = company_id_array
            ETL_dict["new_company_id"] = new_company_id_array
            ETL_dict["container_name"] = connection_name
            ETL_dict["timestamp"] = datetime.today().strftime('%Y-%m-%d')
            ETL_dict["unique_ids"] = uuid_dict
            ETL_dict["new_unique_ids"] = new_uuid_dict

            print(ETL_dict)
            if 'test' not in sys.argv:
                ETL_call(ETL_dict)
                return Response({
                    'error': '',
                    'message': 'Successful request',
                    'data': project_dict,
                    'response_ETL': 'Success'
                }, status=status.HTTP_200_OK)

            else:
                return Response({
                    'error': '',
                    'message': 'Successful request',
                    'data': project_dict,
                    'response_ETL': 'OK'
                }, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, url_path="get-projects")
    def get_all_projects(self, request):
        """
        Get all projects for a user.
        """
        user_project = UserProject.objects.filter(
            user=request.user.id).values_list('project', flat=True)
        projects_array = []
        user_account_id = Users.objects.filter(
            id=request.user.id).values_list()[0][2]
        account_data = Account.objects.filter(
            id=user_account_id).values()[0]
        account_dict = {}
        account_dict["name"] = account_data["name"]
        account_dict["public_id"] = account_data["public_id"]

        projects_array.append(account_dict)

        for project in user_project:
            if project is not None:
                project_temp = Project.objects.filter(
                    id=project).values().last()
                project_score_temp = Company_wise_scores.objects.filter(
                    Q(project=project) & Q(
                        company_id=project_temp["company_id"])).values(
                    'global_score').last()
                project_all_dates_temp = Company_wise_scores.objects.filter(
                    project=project).order_by('initial_date').values_list(
                    'initial_date', flat=True).distinct()
                project_first_date_temp = Company_wise_scores.objects.filter(
                    project=project).order_by('initial_date').values(
                    'initial_date').first()
                project_last_date_temp = Company_wise_scores.objects.filter(
                    project=project).order_by('initial_date').values(
                    'initial_date').last()
                project_website_dates_temp = \
                    Company_wise_scores.objects.filter(
                        Q(project=project)
                    ).order_by('initial_date').values_list(
                        'initial_date', flat=True).distinct()
                project_seo_dates_temp = Company_wise_scores.objects.filter(
                    Q(project=project)
                ).order_by('initial_date').values_list(
                    'initial_date', flat=True).distinct().last()
                project_sm_dates_temp = Company_wise_scores.objects.filter(
                    Q(project=project)
                ).order_by('initial_date').values_list(
                    'initial_date', flat=True).distinct().last()
                if project_score_temp is not None:
                    project_temp["global_score"] = \
                        project_score_temp["global_score"]
                else:
                    project_temp["global_score"] = None
                if project_all_dates_temp is not None:
                    project_temp["all_dates"] = \
                        [date.date() for date in project_all_dates_temp]
                else:
                    project_temp["all_dates"] = [datetime.today()]
                if project_first_date_temp is not None:
                    project_temp["initial_date"] = \
                        project_first_date_temp["initial_date"].date(
                    )
                else:
                    project_temp["initial_date"] = datetime.today()
                if project_last_date_temp is not None:
                    project_temp["last_date"] = \
                        project_last_date_temp["initial_date"].date(
                    )
                else:
                    project_temp["last_date"] = datetime.today()
                if project_website_dates_temp is not None:
                    project_temp["website_dates"] = \
                        [date.date() for date in project_website_dates_temp]
                else:
                    project_temp["website_dates"] = [datetime.today()]
                if project_seo_dates_temp is not None:
                    project_temp["seo_dates"] = \
                        [date.date() for date in [project_seo_dates_temp]]
                else:
                    project_temp["seo_dates"] = [datetime.today()]
                if project_sm_dates_temp is not None:
                    project_temp["sm_dates"] = \
                        [date.date() for date in [project_sm_dates_temp]]
                else:
                    project_temp["sm_dates"] = [datetime.today()]
                projects_array.append(project_temp)

        if not projects_array:
            return Response({
                'error': '',
                'message': "You don't have any projects yet.",
                'data': []
            }, status=status.HTTP_200_OK)

        return Response({
            'error': '',
            'message': 'Successful request',
            'data': projects_array
        }, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, url_path="get-project/(?P<pk>\\w+)")
    def get_project_by_id(self, request, pk):
        """
        Get Project data by ID.
        """
        project_dict = {}
        project = Project.objects.filter(id=pk)
        project_dict["id"] = project.values_list('id', flat=True).first()
        project_dict["sector_id"] = project.values_list(
            'sector_id', flat=True).first()
        project_dict["name"] = project.values_list('name', flat=True).first()

        project_dict["company_name"] = Company.objects.filter(
            id=project.values_list(
                'company_id', flat=True).first()).values_list(
            'url', flat=True).first()
        competitors_temp = project.values_list()[0][5:15]
        competitors_name_temp = []

        for competitor in competitors_temp:
            if competitor is not None:
                competitors_name_temp.append(Company.objects.filter(
                    id=competitor).values_list('url', flat=True).first())

        project_dict["competitors_name"] = competitors_name_temp

        return Response({
            'error': '',
            'message': 'Successful request',
            'data': project_dict
        }, status=status.HTTP_200_OK)

    @action(methods=["PUT"], detail=False,
            url_path="update-project/(?P<pk>\\w+)")
    def updateProject(self, request, pk):
        """
        Disable (is_active=3) or Enable (is_active=1) a project.
        """
        project = Project.objects.filter(id=pk)
        activate_project = request.data['activate']
        if activate_project:
            account_properties_view = AccountProperties()
            account_info = account_properties_view.getNumAccountProjects(
                request)
            max_num_account_projects = \
                account_info.data["data"]["max_num_account_projects"]
            num_active_account_projects = \
                account_info.data["data"]["num_active_account_projects"]

            # Compare max_num_account_projects and num_active_account_projects
            if max_num_account_projects == num_active_account_projects:
                return Response({
                    'error': 'Cannot activate the project',
                    'message':
                    'Number of active projects exceeds the maximum allowed.',
                    'data': ''
                }, status=status.HTTP_400_BAD_REQUEST,
                    content_type='application/json')
            else:
                project.update(is_active=1)
                return Response({
                    'error': '',
                    'message': 'Successful request',
                    'data': 'activate'
                }, status=status.HTTP_200_OK)
        elif not activate_project:
            project.update(is_active=3)
            return Response({
                'error': '',
                'message': 'Successful request',
                'data': 'deactivate'
            }, status=status.HTTP_200_OK)

    @action(methods=["PUT"], detail=False,
            url_path="archive-project/(?P<pk>\\w+)")
    def archiveProject(self, request, pk):
        """
        Archive a project. is_active=5
        """
        project = Project.objects.filter(id=pk)
        project.update(is_active=5)
        return Response({
            'error': '',
            'message': 'Successful request',
            'data': ''
        }, status=status.HTTP_200_OK)


class ActiveProject(viewsets.ViewSet, APIView):

    @action(methods=["PUT"], detail=False,
            url_path="active-project/(?P<pk>\\w+)")
    def enableProject(self, request, pk):
        """
        Active project. Endpoint called by ETL.
        """
        project = Project.objects.filter(id=pk)
        project_id = project.values().first()["id"]
        user_id = UserProject.objects.filter(project_id=project_id).values(
        ).first()["user_id"]
        user = Users.objects.filter(id=user_id).values().first()
        user_email = user["email"]
        user_name = user["name"]
        project.update(is_active=1)
        send_mail_for_project_confirmation(
            to_emails=[user_email], name=[user_name]
        )
        return Response({
            'error': '',
            'message': 'Successful request',
            'data': ''
        }, status=status.HTTP_200_OK)

    @action(methods=["PUT"], detail=False,
            url_path="failed-project/(?P<pk>\\w+)")
    def failedProject(self, request, pk):
        """
        Called if new project fails [ETL]
        """
        project = Project.objects.filter(id=pk)
        project_id = project.values().first()["id"]
        user_id = UserProject.objects.filter(project_id=project_id).values(
        ).first()["user_id"]
        user = Users.objects.filter(id=user_id).values().first()
        user_email = user["email"]
        user_name = user["name"]
        project.update(is_active=2)
        send_mail_for_project_fail(
            to_emails=[user_email], name=[user_name]
        )
        return Response({
            'error': '',
            'message': 'Successful request',
            'data': ''
        }, status=status.HTTP_200_OK)

    @action(methods=["PUT"], detail=False,
            url_path="test-project/(?P<pk>\\w+)")
    def testProject(self, request, pk):
        """
        Not used endpoint
        """
        project = Project.objects.filter(id=pk)
        project_id = project.values().first()["id"]
        user_id = UserProject.objects.filter(project_id=project_id).values(
        ).first()["user_id"]
        user = Users.objects.filter(id=user_id).values().first()
        user_email = user["email"]
        user_name = user["name"]
        project.update(is_active=1)
        send_mail_for_email_verification(
            to_emails=[user_email], name=[user_name]
        )
        return Response({
            'error': '',
            'message': 'Successful request',
            'data': ''
        }, status=status.HTTP_200_OK)


def check_current_month_data(company):
    company_id = Company.objects.filter(
        url=company).values('id').first()["id"]
    now = datetime.now()
    days_in_month = calendar.monthrange(
        now.year,
        now.month,
    )[1]
    first_day = datetime(now.year, now.month, 1)
    last_day = datetime(now.year,
                        now.month,
                        days_in_month
                        )
    check_Website = Website.objects.filter(Q(
        initial_date__range=[first_day, last_day]
    ) & Q(
        company_id=company_id)
    ).values().last()
    check_Seo = Seo.objects.filter(Q(
        initial_date__range=[first_day, last_day]
    ) & Q(
        company_id=company_id)
    ).values().last()
    check_SocialMedia = Social_media.objects.filter(Q(
        initial_date__range=[first_day, last_day]) & Q(
        company_id=company_id)
    ).values().last()
    return check_Website, check_Seo, check_SocialMedia


def check_uuid_by_company_id(company_id):
    now = datetime.now()
    first_day = datetime(now.year, now.month, 1)
    last_day = datetime(now.year,
                        now.month,
                        calendar.monthrange(now.year, now.month)[1])
    check_uuid_website = Website.objects.filter(Q(
        initial_date__range=[first_day, last_day]) & Q(
        company_id=company_id)).values().last()
    check_uuid_seo = Seo.objects.filter(Q(
        initial_date__range=[first_day, last_day]) & Q(
        company_id=company_id)).values().last()
    check_uuid_sm = Social_media.objects.filter(Q(
        initial_date__range=[first_day, last_day]) & Q(
        company_id=company_id)).values().last()
    if check_uuid_website and \
        check_uuid_seo and \
            check_uuid_sm:
        return check_uuid_website
    else:
        return None


def generate_non_repeated_uuid(company_id):
    new_check_uuid_website = True
    new_check_uuid_seo = True
    new_check_uuid_sm = True
    while new_check_uuid_website or new_check_uuid_seo or new_check_uuid_sm:
        unique = int(str(company_id) + str(
            random_with_N_digits(9 - len(str(company_id)))))
        new_check_uuid_website = Website.objects.filter(website_id=unique)
        new_check_uuid_seo = Seo.objects.filter(seo_id=unique)
        new_check_uuid_sm = Social_media.objects.filter(social_id=unique)
    return unique


def ETL_call(ETL_dict):
    if not ETL_dict["new_site_list"]:
        try:
            credentials = ClientSecretCredential(
                client_id='6abdc6fb-f717-45d3-a1e0-84e804be58ec',
                client_secret='HW68Q~.VgLY4G4UP8L4ND_Vu60cI~0YOUz_IdddV',
                tenant_id='0382225c-93b8-4c82-b547-47fd564d990c')
            adf_client = DataFactoryManagementClient(
                credentials,
                os.environ['DF_MANAGEMENT_CLIENT'])
            run_response = adf_client.pipelines.create_run(
                os.environ['RESOURCE_GROUP'],
                os.environ['DF_PIPELINE'],
                "Score-Load-Control",
                parameters={'function_dictionary': ETL_dict})
            print(run_response)
        except IntegrityError as e:
            return Response({
                e
            })
    else:
        try:
            credentials = ClientSecretCredential(
                client_id='6abdc6fb-f717-45d3-a1e0-84e804be58ec',
                client_secret='HW68Q~.VgLY4G4UP8L4ND_Vu60cI~0YOUz_IdddV',
                tenant_id='0382225c-93b8-4c82-b547-47fd564d990c')
            adf_client = DataFactoryManagementClient(
                credentials,
                os.environ['DF_MANAGEMENT_CLIENT'])
            run_response = adf_client.pipelines.create_run(
                os.environ['RESOURCE_GROUP'],
                os.environ['DF_PIPELINE'],
                "Control",
                parameters={'function_dictionary': ETL_dict})
            print(run_response)
        except IntegrityError as e:
            return Response({
                e
            })


def ETL_update(ETL_dict):
    print(ETL_dict)
    if not ETL_dict["new_site_list"]:
        try:
            credentials = ClientSecretCredential(
                client_id='6abdc6fb-f717-45d3-a1e0-84e804be58ec',
                client_secret='HW68Q~.VgLY4G4UP8L4ND_Vu60cI~0YOUz_IdddV',
                tenant_id='0382225c-93b8-4c82-b547-47fd564d990c')
            adf_client = DataFactoryManagementClient(
                credentials,
                os.environ['DF_MANAGEMENT_CLIENT'])
            run_response = adf_client.pipelines.create_run(
                os.environ['RESOURCE_GROUP'],
                os.environ['DF_PIPELINE'],
                "Score-Load-Control-Update",
                parameters={'function_dictionary': ETL_dict})
            print(run_response)
        except IntegrityError as e:
            return Response({
                e
            })
    else:
        try:
            credentials = ClientSecretCredential(
                client_id='6abdc6fb-f717-45d3-a1e0-84e804be58ec',
                client_secret='HW68Q~.VgLY4G4UP8L4ND_Vu60cI~0YOUz_IdddV',
                tenant_id='0382225c-93b8-4c82-b547-47fd564d990c')
            adf_client = DataFactoryManagementClient(
                credentials,
                os.environ['DF_MANAGEMENT_CLIENT'])
            run_response = adf_client.pipelines.create_run(
                os.environ['RESOURCE_GROUP'],
                os.environ['DF_PIPELINE'],
                "Control-Update",
                parameters={'function_dictionary': ETL_dict})
            print(run_response)
        except IntegrityError as e:
            return Response({
                e
            })


def ETL_social_links(ETL_dict):
    try:
        credentials = ClientSecretCredential(
            client_id='6abdc6fb-f717-45d3-a1e0-84e804be58ec',
            client_secret='HW68Q~.VgLY4G4UP8L4ND_Vu60cI~0YOUz_IdddV',
            tenant_id='0382225c-93b8-4c82-b547-47fd564d990c')
        adf_client = DataFactoryManagementClient(
            credentials,
            os.environ['DF_MANAGEMENT_CLIENT'])
        run_response = adf_client.pipelines.create_run(
            os.environ['RESOURCE_GROUP'],
            os.environ['DF_PIPELINE'],
            "Control-SM",
            parameters={'function_dictionary': ETL_dict})
        print(run_response)
    except IntegrityError as e:
        return Response({
            e
        })


def check_company_ids(company_id_array, projects):
    project_id = str(projects.get('company_id'))
    return project_id in map(str, company_id_array) if project_id else False
