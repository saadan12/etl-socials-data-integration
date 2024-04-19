# Create your tests here.
from .auth import LoginTokenCase

from rest_framework import status
from rest_framework.test import APITestCase
APITestCase.maxDiff = None


class PerformanceTestCase(APITestCase, LoginTokenCase):

    # Performance recommendations

    def test_get_performance_recommends_get(self):
        LoginTokenCase.setUp(self)
        response = self.client.get('/performance/performance/recommends/1/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_performance_recommends_post(self):
        LoginTokenCase.setUp(self)
        response = self.client.post('/performance/performance/recommends/1/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_performance_recommends_put(self):
        LoginTokenCase.setUp(self)
        response = self.client.put('/performance/performance/recommends/1/')
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_get_performance_recommends_delete(self):
        LoginTokenCase.setUp(self)
        response = self.client.delete('/performance/performance/recommends/1/')
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_get_performance_recommends_unauthorized(self):
        response = self.client.post('/performance/performance/recommends/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Performance calc

    def test_get_performance_calc_put(self):
        LoginTokenCase.setUp(self)
        response = self.client.put('/performance/performance/calc/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_performance_calc_post(self):
        LoginTokenCase.setUp(self)
        response = self.client.post('/performance/performance/calc/')
        self.assertEqual(
            response.status_codestatus.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_performance_calc_get(self):
        LoginTokenCase.setUp(self)
        response = self.client.get('/performance/performance/calc/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_performance_calc_delete(self):
        LoginTokenCase.setUp(self)
        response = self.client.delete('/performance/performance/calc/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    # Performance calc project

    def test_get_performance_calc_project_post(self):
        LoginTokenCase.setUp(self)
        response = self.client.post('/performance/performance/calc-project/1/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_performance_calc_project_get(self):
        LoginTokenCase.setUp(self)
        response = self.client.get('/performance/performance/calc-project/1/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_performance_calc_project_delete(self):
        LoginTokenCase.setUp(self)
        response = self.client.delete(
            '/performance/performance/calc-project/1/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
