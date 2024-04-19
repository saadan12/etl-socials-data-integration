# Create your tests here.
from ..test.auth import LoginTokenCase

from rest_framework import status
from rest_framework.test import APITestCase


class AccountTestCase(APITestCase, LoginTokenCase):

    def test_get_account_projects_get(self):
        LoginTokenCase.setUp(self)
        response = self.client.get('/account/account/num-account-projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_account_projects_post(self):
        LoginTokenCase.setUp(self)
        response = self.client.post('/account/account/num-account-projects/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_account_projects_info(self):
        LoginTokenCase.setUp(self)
        response = self.client.get('/account/account/num-account-projects/')
        self.assertEqual(response.data,
                         {
                             "error": None,
                             "data": {
                                 "user_id": 1,
                                 "account_id": 1,
                                 "stripe_subscription_plan": 1,
                                 "max_num_account_projects": 10,
                                 "num_active_account_projects": 0
                             }

                         }
                         )

    def test_get_account_projects_info_unauthorized(self):
        response = self.client.get('/account/account/num-account-projects/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_account_users_get(self):
        LoginTokenCase.setUp(self)
        response = self.client.get('/account/account/num-account-users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_account_users_post(self):
        LoginTokenCase.setUp(self)
        response = self.client.post('/account/account/num-account-users/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_account_users_info(self):
        LoginTokenCase.setUp(self)
        response = self.client.get('/account/account/num-account-users/')
        self.assertEqual(response.data,
                         {
                             "error": None,
                             "data": {
                                 "user_id": 1,
                                 "account_id": 1,
                                 "stripe_subscription_plan": 1,
                                 "max_num_account_users": 10,
                                 "num_current_account_users": 1
                             }
                         }
                         )

    def test_get_account_users_info_unauthorized(self):
        response = self.client.get('/account/account/num-account-users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
