from .auth import LoginTokenCase
from rest_framework import status
from rest_framework.test import APITestCase


class ProjectTestCase(APITestCase, LoginTokenCase):

    def test_projectActivation(self):
        LoginTokenCase.setUp(self)
        response = self.client.put(
            '/project/project/active-project/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_projectActivationFail(self):
        LoginTokenCase.setUp(self)
        response = self.client.put(
            '/project/project/failed-project/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_getProjectByID(self):
        LoginTokenCase.setUp(self)
        response = self.client.get(
            '/project/project/get-project/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_getAllProjects(self):
        LoginTokenCase.setUp(self)
        response = self.client.get(
            '/project/project/get-projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_archiveProject(self):
        LoginTokenCase.setUp(self)
        response = self.client.put(
            '/project/project/archive-project/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'error': '',
            'message': 'Successful request',
            'data': ''
        })

    def test_archive_project_post(self):
        LoginTokenCase.setUp(self)
        response = self.client.post('/project/project/archive-project/1/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_archive_project_get(self):
        LoginTokenCase.setUp(self)
        response = self.client.get('/project/project/archive-project/1/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_archive_project_delete(self):
        LoginTokenCase.setUp(self)
        response = self.client.delete('/project/project/archive-project/1/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_archive_project_unauthorized(self):
        response = self.client.post('/project/project/archive-project/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_project_enable(self):
        LoginTokenCase.setUp(self)
        payload = {
            'activate': True,
        }
        url = '/project/project/update-project/1/'
        response = self.client.put(url, data=payload, format='json')
        if response.status_code == status.HTTP_200_OK:
            self.assertEqual(response.data, {
                'error': '',
                'message': 'Successful request',
                'data': 'activate'
            })

        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            self.assertEqual(response.data, {
                'error': 'Cannot activate the project',
                'message':
                'Number of active projects exceeds the maximum allowed.',
                'data': ''
            })

    def test_update_project_disable(self):
        LoginTokenCase.setUp(self)
        payload = {
            'activate': False,
        }
        url = '/project/project/update-project/1/'
        response = self.client.put(url, data=payload, format='json')
        if response.status_code == status.HTTP_200_OK:
            self.assertEqual(response.data, {
                'error': '',
                'message': 'Successful request',
                'data': 'deactivate'
            })
        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            self.assertEqual(response.data, {
                'error': 'Cannot deactivate the project',
                'message':
                'Number of active projects exceeds the maximum allowed.',
                'data': ''
            })

    def test_update_project_post(self):
        LoginTokenCase.setUp(self)
        response = self.client.post('/project/project/update-project/1/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_project_get(self):
        LoginTokenCase.setUp(self)
        response = self.client.get('/project/project/update-project/1/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_project_delete(self):
        LoginTokenCase.setUp(self)
        response = self.client.delete('/project/project/update-project/1/')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_project_unauthorized(self):
        response = self.client.post('/project/project/update-project/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
