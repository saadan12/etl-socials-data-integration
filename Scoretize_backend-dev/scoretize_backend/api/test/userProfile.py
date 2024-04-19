# Create your tests here.
import json
from .auth import LoginTokenCase

from rest_framework import status
from rest_framework.test import APITestCase
APITestCase.maxDiff = None


class UserProfileTestCase(APITestCase, LoginTokenCase):

    # Get user profile

    def test_get_user_profile_get(self):
        LoginTokenCase.setUp(self)
        response = self.client.get('/user/profile/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_profile_get_content(self):
        LoginTokenCase.setUp(self)
        response = self.client.get('/user/profile/users-account/')
        response_dict = response.data
        response_dict["data"] = response_dict["data"]
        response_dict_data = dict(response_dict["data"][0])
        password = response_dict_data["password"]
        lastLogin = response_dict_data["last_login"]
        dateJoined = response_dict_data["date_joined"]
        stripeEndDate = response_dict_data["stripe_endDate"]
        expected_data = {
            "error": "",
            "message": "Successful request",
            "data": [{
                "id": 1,
                "email": "testers@testing.com",
                "password": password,
                "name": "Testers",
                "surname": "Testers",
                "phone": "",
                "photo": "",
                "is_superuser": False,
                "is_staff": False,
                "is_active": True,
                "is_emailMarketing": True,
                "last_login": lastLogin,
                "date_joined": dateJoined,
                "stripe_id": None,
                "stripe_isActive": False,
                "stripe_endDate": stripeEndDate,
                "stripe_subscriptionID": None,
                "stripe_subscriptionPlan": "",
                "is_termsOfServicePrivacyPolicy": True,
                "user_type": 1,
                "account": 1,
                "groups": [],
                "user_permissions": []
            }]
        }
        self.assertEqual(json.dumps(response.data), json.dumps(expected_data))

    def test_get_user_profile_post(self):
        LoginTokenCase.setUp(self)
        response = self.client.post('/user/profile/profile/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_user_profile_put(self):
        LoginTokenCase.setUp(self)
        response = self.client.put('/user/profile/profile/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_user_profile_unathorized(self):
        response = self.client.post('/user/profile/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Edit user profile

    def test_edit_user_profile_pswd_correct_put(self):
        LoginTokenCase.setUp(self)
        put_body = {
            "data": {
                "id": 1,
                "email": "testers@testing.com",
                "password": "pbkdf2_sha256$320000$XSVeCxmlZRUu6HzeDQ80go$\
                vPXKJKjpLfPVFWCRSWn3g9/oyuTer6PZ3c+hiy++cqk=",
                "name": "Testers",
                "surname": "Testers",
                "phone": "",
                "photo": "",
                "is_superuser": False,
                "is_staff": False,
                "is_active": True,
                "is_emailMarketing": True,
                "last_login": "2023-09-18T10:17:34.748527",
                "date_joined": "2023-08-27T11:21:16.074536",
                "stripe_id": None,
                "stripe_isActive": False,
                "stripe_endDate": "2023-08-27T11:21:16.323419",
                "stripe_subscriptionID": None,
                "stripe_subscriptionPlan": "Free",
                "is_termsOfServicePrivacyPolicy": True,
                "user_type": 2,
                "account": 1,
                "groups": [],
                "user_permissions": []
            },
            "password": {
                "old_password": "123456tT*",
                "new_password": "123456rR*",
                "new_password_confirm": "123456rR*"
            }
        }
        response = self.client.put('/user/profile/edit-profile/',
                                   put_body, format='json')

        expected_data = {
            "error": "",
            "message": "Successful request",
            "data": {
                "email": "testers@testing.com",
                "name": "Testers",
                "surname": "Testers",
                "is_emailMarketing": True
            }
        }
        self.assertEqual(json.dumps(response.data), json.dumps(expected_data))

    def test_edit_user_profile_old_pswd_incorrect_put(self):
        LoginTokenCase.setUp(self)
        put_body = {
            "data": {
                "id": 1,
                "email": "testers@testing.com",
                "password": "pbkdf2_sha256$320000$XSVeCxmlZRUu6HzeDQ80go$\
                vPXKJKjpLfPVFWCRSWn3g9/oyuTer6PZ3c+hiy++cqk=",
                "name": "Testers",
                "surname": "Testers",
                "phone": "",
                "photo": "",
                "is_superuser": False,
                "is_staff": False,
                "is_active": True,
                "is_emailMarketing": True,
                "last_login": "2023-09-18T10:17:34.748527",
                "date_joined": "2023-08-27T11:21:16.074536",
                "stripe_id": None,
                "stripe_isActive": False,
                "stripe_endDate": "2023-08-27T11:21:16.323419",
                "stripe_subscriptionID": None,
                "stripe_subscriptionPlan": "Free",
                "is_termsOfServicePrivacyPolicy": True,
                "user_type": 2,
                "account": 1,
                "groups": [],
                "user_permissions": []
            },
            "password": {
                "old_password": "123456rR*",
                "new_password": "123456rT*",
                "new_password_confirm": "123456rJ*"
            }
        }
        response = self.client.put('/user/profile/edit-profile/',
                                   put_body, format='json')

        expected_data = {
            "error": "An error happened when updating the user",
            "message": "An error happened when updating the user",
            "data": {
                "old_password": [
                    "Incorrect current password"
                ]
            }
        }

        self.assertEqual(json.dumps(response.data), json.dumps(expected_data))

    def test_edit_user_profile_new_pswds_mismatch_put(self):
        LoginTokenCase.setUp(self)
        put_body = {
            "data": {
                "id": 1,
                "email": "testers@testing.com",
                "password": "pbkdf2_sha256$320000$XSVeCxmlZRUu6HzeDQ80go$\
                vPXKJKjpLfPVFWCRSWn3g9/oyuTer6PZ3c+hiy++cqk=",
                "name": "Testers",
                "surname": "Testers",
                "phone": "",
                "photo": "",
                "is_superuser": False,
                "is_staff": False,
                "is_active": True,
                "is_emailMarketing": True,
                "last_login": "2023-09-18T10:17:34.748527",
                "date_joined": "2023-08-27T11:21:16.074536",
                "stripe_id": None,
                "stripe_isActive": False,
                "stripe_endDate": "2023-08-27T11:21:16.323419",
                "stripe_subscriptionID": None,
                "stripe_subscriptionPlan": "Free",
                "is_termsOfServicePrivacyPolicy": True,
                "user_type": 2,
                "account": 1,
                "groups": [],
                "user_permissions": []
            },
            "password": {
                "old_password": "123456tT*",
                "new_password": "123456rR*",
                "new_password_confirm": "123456rT*"
            }
        }
        response = self.client.put('/user/profile/edit-profile/',
                                   put_body, format='json')

        expected_data = {
            "error": "An error happened when updating the user",
            "message": "An error happened when updating the user",
            "data": {
                "non_field_errors": [
                    "Your password and confirmation password do not match."
                ]
            }
        }

        self.assertEqual(json.dumps(response.data), json.dumps(expected_data))

    def test_edit_user_profile_weak_new_pswd_put(self):
        LoginTokenCase.setUp(self)
        put_body = {
            "data": {
                "id": 1,
                "email": "testers@testing.com",
                "password": "pbkdf2_sha256$320000$XSVeCxmlZRUu6HzeDQ80go$\
                vPXKJKjpLfPVFWCRSWn3g9/oyuTer6PZ3c+hiy++cqk=",
                "name": "Testers",
                "surname": "Testers",
                "phone": "",
                "photo": "",
                "is_superuser": False,
                "is_staff": False,
                "is_active": True,
                "is_emailMarketing": True,
                "last_login": "2023-09-18T10:17:34.748527",
                "date_joined": "2023-08-27T11:21:16.074536",
                "stripe_id": None,
                "stripe_isActive": False,
                "stripe_endDate": "2023-08-27T11:21:16.323419",
                "stripe_subscriptionID": None,
                "stripe_subscriptionPlan": "Free",
                "is_termsOfServicePrivacyPolicy": True,
                "user_type": 2,
                "account": 1,
                "groups": [],
                "user_permissions": []
            },
            "password": {
                "old_password": "123456tT*",
                "new_password": "123456rR",
                "new_password_confirm": "123456rR"
            }
        }
        response = self.client.put('/user/profile/edit-profile/',
                                   put_body, format='json')

        expected_data = {
            "error": "An error happened when updating the user",
            "message": "An error happened when updating the user",
            "data": {
                "new_password": [
                    "Password must have at least one uppercase, one "
                    "lowercase, one numerical digit and a character like "
                    "!@#$&*+_- with a minimum length of 8 chars."
                ],
                "new_password_confirm": [
                    "Password must have at least one uppercase, one "
                    "lowercase, one numerical digit and a character like "
                    "!@#$&*+_- with a minimum length of 8 chars."
                ]
            }
        }

        self.assertEqual(json.dumps(response.data), json.dumps(expected_data))

    def test_edit_user_profile_get(self):
        LoginTokenCase.setUp(self)
        response = self.client.get('/user/profile/edit-profile/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_edit_user_profile_post(self):
        LoginTokenCase.setUp(self)
        response = self.client.post('/user/profile/edit-profile/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_edit_user_profile_delete(self):
        LoginTokenCase.setUp(self)
        response = self.client.delete('/user/profile/edit-profile/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_edit_user_profile_unauthorized(self):
        response = self.client.put('/user/profile/edit-profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Delete user profile

    def test_delete_user_profile_post(self):
        LoginTokenCase.setUp(self)
        response = self.client.get('/user/profile/delete-profile/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_user_profile_get(self):
        LoginTokenCase.setUp(self)
        response = self.client.get('/user/profile/delete-profile/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_user_profile_unauthorized(self):
        response = self.client.post('/user/profile/delete-profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Get all user profile

    def test_get_all_users_get(self):
        LoginTokenCase.setUp(self)
        response = self.client.get('/user/profile/users-account/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_users_get_content(self):
        LoginTokenCase.setUp(self)
        response = self.client.get('/user/profile/users-account/')
        password = response.data['data'][0]['password']
        lastLogin = response.data['data'][0]['last_login']
        dateJoined = response.data['data'][0]['date_joined']
        stripeEndDate = response.data['data'][0]['stripe_endDate']

        expected_data = {
            "error": "",
            "message": "Successful request",
            "data": [
                {
                    "id": 1,
                    "email": "testers@testing.com",
                    "password": password,
                    "name": "Testers",
                    "surname": "Testers",
                    "phone": "",
                    "photo": "",
                    "is_superuser": False,
                    "is_staff": False,
                    "is_active": True,
                    "is_emailMarketing": True,
                    "last_login": lastLogin,
                    "date_joined": dateJoined,
                    "stripe_id": None,
                    "stripe_isActive": False,
                    "stripe_endDate": stripeEndDate,
                    "stripe_subscriptionID": None,
                    "stripe_subscriptionPlan": "",
                    "is_termsOfServicePrivacyPolicy": True,
                    "user_type": 1,
                    "account": 1,
                    "groups": [],
                    "user_permissions": []
                }
            ]
        }
        self.assertEqual(json.dumps(response.data), json.dumps(expected_data))

    def test_get_all_users_post(self):
        LoginTokenCase.setUp(self)
        response = self.client.post('/user/profile/users-account/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_all_users_put(self):
        LoginTokenCase.setUp(self)
        response = self.client.put('/user/profile/users-account/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_all_users_delete(self):
        LoginTokenCase.setUp(self)
        response = self.client.delete('/user/profile/users-account/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_all_users_unauthorized(self):
        response = self.client.get('/user/profile/users-account/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
