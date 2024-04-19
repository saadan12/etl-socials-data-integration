# from django.test import TestCase
from .auth import LoginTokenCase
from rest_framework import status
from rest_framework.test import APITestCase
# ACTIVATE ENDPOINTS WHEN NEW DB IS CREATEDSS


class WebsiteTestCase(APITestCase, LoginTokenCase):

    # SEO Testing Endpoint
    def test_website_score(self):
        LoginTokenCase.setUp(self)
        response = self.client.get('/website/website/website-score/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_website_score_evolution(self):
        LoginTokenCase.setUp(self)
        response = self.client.get(
            '/overview/overview/website-score/1/evolution/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_website_score_direct_competitors(self):
        LoginTokenCase.setUp(self)
        response = self.client.get(
            '/website/website/website-score/1/direct-competitors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_website_social_sources(self):
        LoginTokenCase.setUp(self)
        response = self.client.get(
            '/website/website/website-score/1/social-sources/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_website_traffic_sources_graph(self):
        LoginTokenCase.setUp(self)
        response = self.client.get(
            '/website/website/website-score/1/traffic-sources/graph/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_website_traffic_country(self):
        LoginTokenCase.setUp(self)
        response = self.client.get(
            '/website/website/website-score/1/traffic-country/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_website_score_evolution_all_dates(self):
        LoginTokenCase.setUp(self)
        query_params = {
            'start_date': '2023-08-01',
            'end_date': '2023-09-30'
        }
        url = '/website/website/website-score-all-dates/1/evolution/'
        response = self.client.get(url, data=query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn('data', response.data)
        data_list = response.data['data']
        self.assertIsInstance(data_list, list)

        for item in data_list:
            self.assertIsInstance(item, dict)
            website_score = item.get('website_score', [])
            self.assertIsInstance(website_score, list)

            for score_item in website_score:
                self.assertIsInstance(score_item, dict)
                self.assertIn('initial_date', score_item)
                self.assertIn('website_score', score_item)

    def test_get_website_score_evolution_all_dates_post(self):
        LoginTokenCase.setUp(self)
        response = self.client.post(
            '/website/website/website-score-all-dates/1/evolution/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_website_score_evolution_all_dates_put(self):
        LoginTokenCase.setUp(self)
        response = self.client.put(
            '/website/website/website-score-all-dates/1/evolution/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_website_score_evolution_all_dates_delete(self):
        LoginTokenCase.setUp(self)
        response = self.client.delete(
            '/website/website/website-score-all-dates/1/evolution/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_website_score_evolution_all_dates_unauthorized(self):
        response = self.client.post(
            '/website/website/website-score-all-dates/1/evolution/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_website_traffic_sources(self):
        LoginTokenCase.setUp(self)
        query_params = {
            'end_date': '2023-07-31',      # Replace with a valid end date
            'web_end_date': '2023-07-31',  # Replace with a valid web end date
        }
        url = '/website/website/website-score/1/traffic-sources/competitors/'
        response = self.client.get(url, data=query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn('data', response.data)

    def test_website_traffic_sources_post(self):
        LoginTokenCase.setUp(self)
        response = self.client.post(
            '/website/website/website-score/1/traffic-sources/competitors/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_website_traffic_sources_put(self):
        LoginTokenCase.setUp(self)
        response = self.client.put(
            '/website/website/website-score/1/traffic-sources/competitors/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_website_traffic_sources_delete(self):
        LoginTokenCase.setUp(self)
        response = self.client.delete(
            '/website/website/website-score/1/traffic-sources/competitors/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_website_traffic_sources_unauthorized(self):
        response = self.client.post(
            '/website/website/website-score/1/traffic-sources/competitors/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
