from django.db.models import Q
from ...views import viewsets, APIView, IsAuthenticated, Response, \
    action, Users, \
    UserProject, Project
import json


class AccountProperties(viewsets.ViewSet, APIView):
    permission_classes = (IsAuthenticated,)

    @action(methods=["GET"], detail=False, url_path="num-account-projects")
    def getNumAccountProjects(self, request):
        response = Response()

        user = request.user

        # Validate that a user_id has been passed to endpoint
        if user is None:
            # Response for no user
            response.data = {
                "error": "No user found with given token",
                "data": None
            }
        else:
            # Get stripe subscription plan from account associated with user
            # Read from account_properties json file to get
            # maximum number of projects per account based on stripe
            # subscription plan
            user_id = user.id
            account_id = user.account_id
            print("account_id: ", account_id)
            account_properties_file = open(
                "api/endpoints/account/account_properties.json")
            all_account_data = json.load(account_properties_file)
            # stripe_subscription_plan = account.stripe_SubscriptionPlan
            stripe_subscription_plan = 1
            current_account_data = all_account_data[str(
                stripe_subscription_plan)]
            max_num_account_projects = current_account_data["max_num_projects"]

            # Unique set of project ids
            # Users may have share projects, so  it must be a set
            account_project_ids = set()

            # Get all user_ids for users that use this account
            users_of_account = Users.objects.filter(
                account_id=account_id).all()
            user_ids_of_account = [user.id for user in users_of_account]

            # Get all project ids for each and add to set
            for current_user_id in user_ids_of_account:
                user_project_ids = UserProject.objects.filter(
                    user=current_user_id).values_list('project_id', flat=True)
                account_project_ids.update(user_project_ids)

            # Filter down user projects to unique active projects for account
            active_account_projects = Project.objects.filter(
                Q(id__in=account_project_ids) & Q(is_active=1))
            # Get number of unique active projects for account
            num_active_account_projects = active_account_projects.count()

            response.data = {
                "error": None,
                "data": {
                    "user_id": user_id,
                    "account_id": account_id,
                    "stripe_subscription_plan": stripe_subscription_plan,
                    "max_num_account_projects": max_num_account_projects,
                    "num_active_account_projects": num_active_account_projects
                }
            }

        return response

    @action(methods=["GET"], detail=False, url_path="num-account-users")
    def getNumAccountUsers(self, request):
        response = Response()

        user = request.user

        # Validate that a user_id has been passed to endpoint
        if user is None:
            # Response for no user
            response.data = {
                "error": "No user found with given token",
                "data": None
            }
        else:
            # Get stripe subscription plan from account associated with user
            # Read from account_properties json file to get
            # maximum number of users per account based on stripe
            # subscription plan
            user_id = user.id
            account_id = user.account_id

            account_properties_file = open(
                "api/endpoints/account/account_properties.json")
            all_account_data = json.load(account_properties_file)
            # stripe_subscription_plan = account.stripe_SubscriptionPlan
            stripe_subscription_plan = 1
            current_account_data = all_account_data[str(
                stripe_subscription_plan)]
            max_num_account_users = current_account_data["max_num_users"]

            # Get number of users sharing account
            users_of_account = Users.objects.filter(
                account_id=account_id).all()
            num_current_account_users = users_of_account.count()

            response.data = {
                "error": None,
                "data": {
                    "user_id": user_id,
                    "account_id": account_id,
                    "stripe_subscription_plan": stripe_subscription_plan,
                    "max_num_account_users": max_num_account_users,
                    "num_current_account_users": num_current_account_users
                }
            }
        return response
