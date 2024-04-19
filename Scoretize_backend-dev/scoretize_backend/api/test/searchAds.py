# from django.test import TestCase
from .auth import LoginTokenCase
from rest_framework import status
from rest_framework.test import APITestCase


class SearchAdsTestCase(APITestCase, LoginTokenCase):

    def test_searchAds_score(self):
        LoginTokenCase.setUp(self)
        response = self.client.get('/paid-media/paid-media/paid-media/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_searchAds_score_evolution(self):
        LoginTokenCase.setUp(self)
        response = self.client.get(
            '/overview/overview/paid-media/1/evolution/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_searchAds_score_direct_competitors(self):
        LoginTokenCase.setUp(self)
        response = self.client.get(
            '/paid-media/paid-media/paid-media/1/direct-competitors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
