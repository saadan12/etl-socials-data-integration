# Create your tests here.
from .auth import LoginTokenCase

from rest_framework import status
from rest_framework.test import APITestCase
APITestCase.maxDiff = None


class CSVTestCase(APITestCase, LoginTokenCase):

    # Export CSV Scores

    def test_export_csv_scores_get(self):
        LoginTokenCase.setUp(self)
        response = self.client.get(
            '/export/data/csv/scores/1?'
            'start_date=2023-07-31&end_date=2023-08-31')
        self.assertEqual(response.status_code,
                         status.HTTP_301_MOVED_PERMANENTLY)

    def test_export_csv_scores_post(self):
        LoginTokenCase.setUp(self)
        response = self.client.post('/export/data/csv/scores/1/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_export_csv_scores_put(self):
        LoginTokenCase.setUp(self)
        response = self.client.put('/export/data/csv/scores/1/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_export_csv_scores_delete(self):
        LoginTokenCase.setUp(self)
        response = self.client.delete('/export/data/csv/scores/1/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_export_csv_scores_unauthorized(self):
        response = self.client.get('/export/data/csv/scores/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Export CSV Website

    def test_export_csv_web_get(self):
        LoginTokenCase.setUp(self)
        response = self.client.get(
            '/export/data/csv/website/1?'
            'start_date=2023-07-31&end_date=2023-08-31')
        self.assertEqual(response.status_code,
                         status.HTTP_301_MOVED_PERMANENTLY)

    def test_export_csv_web_post(self):
        LoginTokenCase.setUp(self)
        response = self.client.post('/export/data/csv/website/1/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_export_csv_web_put(self):
        LoginTokenCase.setUp(self)
        response = self.client.put('/export/data/csv/website/1/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_export_csv_web_delete(self):
        LoginTokenCase.setUp(self)
        response = self.client.delete('/export/data/csv/website/1/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_export_csv_web_unauthorized(self):
        response = self.client.get('/export/data/csv/website/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Export CSV SEO

    def test_export_csv_seo_get(self):
        LoginTokenCase.setUp(self)
        response = self.client.get(
            '/export/data/csv/seo/1?start_date=2023-07-31&end_date=2023-08-31')
        self.assertEqual(response.status_code,
                         status.HTTP_301_MOVED_PERMANENTLY)

    def test_export_csv_seo_post(self):
        LoginTokenCase.setUp(self)
        response = self.client.post('/export/data/csv/seo/1/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_export_csv_seo_put(self):
        LoginTokenCase.setUp(self)
        response = self.client.put('/export/data/csv/seo/1/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_export_csv_seo_delete(self):
        LoginTokenCase.setUp(self)
        response = self.client.delete('/export/data/csv/seo/1/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_export_csv_seo_unauthorized(self):
        response = self.client.get('/export/data/csv/seo/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Export CSV Social Media

    def test_export_csv_sm_get(self):
        LoginTokenCase.setUp(self)
        response = self.client.get(
            '/export/data/csv/sm/1?start_date=2023-07-31&end_date=2023-08-31')
        self.assertEqual(response.status_code,
                         status.HTTP_301_MOVED_PERMANENTLY)

    def test_export_csv_sm_post(self):
        LoginTokenCase.setUp(self)
        response = self.client.post('/export/data/csv/sm/1/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_export_csv_sm_put(self):
        LoginTokenCase.setUp(self)
        response = self.client.put('/export/data/csv/sm/1/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_export_csv_sm_delete(self):
        LoginTokenCase.setUp(self)
        response = self.client.delete('/export/data/csv/sm/1/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_export_csv_sm_unauthorized(self):
        response = self.client.get('/export/data/csv/sm/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
