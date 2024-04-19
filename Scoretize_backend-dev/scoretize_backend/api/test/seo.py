# from django.test import TestCase
from .auth import LoginTokenCase
from rest_framework import status
from rest_framework.test import APITestCase


class SeoTestCase(APITestCase, LoginTokenCase):

    # SEO Testing Endpoint
    def test_seo_score(self):
        LoginTokenCase.setUp(self)
        response = self.client.get('/seo/seo/seo-score/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_seo_score_evolution(self):
        LoginTokenCase.setUp(self)
        response = self.client.get('/seo/seo/seo-score/1/evolution/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_seo_score_traffic_evolution(self):
        LoginTokenCase.setUp(self)
        response = self.client.get('/seo/seo/seo-score/1/traffic-evolution/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_seo_score_keywords(self):
        LoginTokenCase.setUp(self)
        response = self.client.get('/seo/seo/seo-score/1/keywords-graph/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_seo_score_direct_competitors(self):
        LoginTokenCase.setUp(self)
        response = self.client.get('/seo/seo/seo-score/1/direct-competitors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_seo_score_evolution_dates(self):
        LoginTokenCase.setUp(self)
        query_params = {
            'start_date': '2023-08-01',
            'end_date': '2023-09-30',
        }
        url = '/seo/seo/seo-score/1/evolution-all-dates/'
        response = self.client.get(url, data=query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['data']
        self.assertIsInstance(data, list)
        for item in data:
            self.assertIsInstance(item, dict)

    def test_get_seo_score_evolution_dates_post(self):
        LoginTokenCase.setUp(self)
        response = self.client.post(
            '/seo/seo/seo-score/1/evolution-all-dates/')
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_get_seo_score_evolution_dates_put(self):
        LoginTokenCase.setUp(self)
        response = self.client.put('/seo/seo/seo-score/1/evolution-all-dates/')
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_get_seo_score_evolution_dates_delete(self):
        LoginTokenCase.setUp(self)
        response = self.client.delete(
            '/seo/seo/seo-score/1/evolution-all-dates/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_get_seo_score_evolution_dates_unauthorized(self):
        response = self.client.post(
            '/seo/seo/seo-score/1/evolution-all-dates/'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_seo_score_traffic_evolution_dates(self):
        LoginTokenCase.setUp(self)
        query_params = {
            'start_date': '2023-08-01',
            'end_date': '2023-09-30',
        }
        url = '/seo/seo/seo-score/1/traffic-evolution-all-dates/'
        response = self.client.get(url, data=query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        data = response.data['data']
        self.assertIsInstance(data, list)

        for item in data:
            self.assertIsInstance(item, dict)
            self.assertIn('organic', item)
            self.assertIn('paid', item)

            organic_data = item['organic']
            self.assertIsInstance(organic_data, list)

            for organic_item in organic_data:
                self.assertIsInstance(organic_item, dict)
                self.assertIn('initial_date', organic_item)
                self.assertIn('organic_traffic', organic_item)

            paid_data = item['paid']
            self.assertIsInstance(paid_data, list)

            for paid_item in paid_data:
                self.assertIsInstance(paid_item, dict)
                self.assertIn('initial_date', paid_item)
                self.assertIn('paid_traffic', paid_item)

    def test_get_seo_score_traffic_evolution_dates_post(self):
        LoginTokenCase.setUp(self)
        response = self.client.post(
            '/seo/seo/seo-score/1/traffic-evolution-all-dates/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_get_seo_score_traffic_evolution_dates_put(self):
        LoginTokenCase.setUp(self)
        response = self.client.put(
            '/seo/seo/seo-score/1/traffic-evolution-all-dates/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_get_seo_score_traffic_evolution_dates_delete(self):
        LoginTokenCase.setUp(self)
        response = self.client.delete(
            '/seo/seo/seo-score/1/traffic-evolution-all-dates/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_seo_score_traffic_evolution_dates_unauthorized(self):
        response = self.client.post(
            '/seo/seo/seo-score/1/traffic-evolution-all-dates/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_seo_score_keywords_graph_dates(self):
        LoginTokenCase.setUp(self)
        query_params = {
            'start_date': '2023-08-01',
            'end_date': '2023-09-30',
        }
        url = '/seo/seo/seo-score/1/keywords-graph-all-dates/'
        response = self.client.get(url, data=query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(response.data, dict)
        self.assertIn('data', response.data)
        data = response.data['data']
        self.assertIsInstance(data, list)

        for item in data:
            self.assertIsInstance(item, dict)
            keywords_data = item.get('keywords', [])
            self.assertIsInstance(keywords_data, list)

            for keywords_item in keywords_data:
                self.assertIsInstance(keywords_item, dict)
                self.assertIn('initial_date', keywords_item)
                self.assertIn('total_keywords', keywords_item)

            traffic_cost_data = item.get('traffic_cost', [])
            self.assertIsInstance(traffic_cost_data, list)

            for traffic_cost_item in traffic_cost_data:
                self.assertIsInstance(traffic_cost_item, dict)
                self.assertIn('initial_date', traffic_cost_item)
                self.assertIn('paid_keywords', traffic_cost_item)

    def test_get_seo_score_keywords_graph_dates_post(self):
        LoginTokenCase.setUp(self)
        response = self.client.post(
            '/seo/seo/seo-score/1/keywords-graph-all-dates/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_seo_score_keywords_graph_dates_put(self):
        LoginTokenCase.setUp(self)
        response = self.client.put(
            '/seo/seo/seo-score/1/keywords-graph-all-dates/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_seo_score_keywords_graph_dates_delete(self):
        LoginTokenCase.setUp(self)
        response = self.client.delete(
            '/seo/seo/seo-score/1/keywords-graph-all-dates/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_seo_score_keywords_graph_dates_unauthorized(self):
        response = self.client.post(
            '/seo/seo/seo-score/1/keywords-graph-all-dates/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
