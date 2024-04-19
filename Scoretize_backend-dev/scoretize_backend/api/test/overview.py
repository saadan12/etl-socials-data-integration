# from django.test import TestCase
from .auth import LoginTokenCase
from rest_framework import status
from rest_framework.test import APITestCase


class OverviewTestCase(APITestCase, LoginTokenCase):

    # SEO Testing Endpoint
    def test_overview_score(self):
        LoginTokenCase.setUp(self)
        response = self.client.get('/global/global/global-score/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_overview_direct_competitors(self):
        LoginTokenCase.setUp(self)
        response = self.client.get(
            '/global/global/global-score/1/direct-competitors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
