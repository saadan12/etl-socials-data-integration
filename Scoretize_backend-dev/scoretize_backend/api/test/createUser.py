# Create your tests here.
from django.contrib.auth import get_user_model

from ..test.auth import LoginTokenCase
from rest_framework import status
from rest_framework.test import APITestCase


class UsersManagersTests(APITestCase, LoginTokenCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(TypeError):
            User.objects.create_user(password='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='super@user.com', password='foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)

    def test_setUpSectors(self):
        LoginTokenCase.setUp(self)
        response = LoginTokenCase.setUpSectors(self)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_register(self):
        correct_data = {
            "email": "testuser@scoretize.com",
            "password": "Foo!2023",
            "name": "John",
            "surname": "Doe",
            "account_name": "TestAccount",
            "stripe_subscriptionPlan": 1
        }
        incorrect_data = {
            "email": "invalid_email",
            "password": "12345",
            "name": "",
            "surname": "Doe",
            "account_name": "TestAccount",
            "stripe_subscriptionPlan": "invalid_value"
        }
        url = '/user/register/create-profile/'

        response = self.client.post(url, correct_data, format='json')
        self.assertIn(response.status_code, [
                      status.HTTP_200_OK, status.HTTP_201_CREATED])
        self.assertEqual(response.data['data'], 'Verify your email')

        response_incorrect = self.client.post(
            url, incorrect_data, format='json')
        self.assertEqual(response_incorrect.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_post_register_get(self):
        response = self.client.get('/user/register/create-profile/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_register_put(self):
        response = self.client.put('/user/register/create-profile/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_register_delete(self):
        response = self.client.delete('/user/register/create-profile/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_active_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='alejandra.elsin@thekeenfolks.com',
            name='tester',
            password='foo',
            is_active=False
        )

        self.assertEqual(user.email, 'alejandra.elsin@thekeenfolks.com')
        url_user_activation = "/user/register/active-profile/"

        response = self.client.get(f"{url_user_activation}?email={user.email}")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        user.refresh_from_db()
        self.assertTrue(user.is_active)

        response = self.client.get(f"{url_user_activation}?email={user.email}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data
        self.assertEqual(response_data['error'], '')
        self.assertEqual(response_data['message'], 'User already verified')
        self.assertEqual(response_data['data'], '')

    def test_active_user_post(self):
        response = self.client.post("/user/register/active-profile/")
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_active_user_put(self):
        response = self.client.put("/user/register/active-profile/")
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_active_user_delete(self):
        response = self.client.delete("/user/register/active-profile/")
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
