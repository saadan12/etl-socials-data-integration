from .auth import LoginTokenCase
from rest_framework import status
from rest_framework.test import APITestCase

# ACTIVATE ENDPOINTS WHEN NEW DB IS CREATED


class SocialMediaTestCase(APITestCase, LoginTokenCase):

    # SEO Testing Endpoint
    def test_socialMedia_score(self):
        LoginTokenCase.setUp(self)
        response = self.client.get(
            '/socialMedia/socialMedia/socialMedia-score/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_socialMedia_score_evolution(self):
        LoginTokenCase.setUp(self)
        response = self.client.get(
            '/overview/overview/socialMedia-score/1/evolution/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_socialMedia_direct_competitors(self):
        LoginTokenCase.setUp(self)
        response = self.client.get(
            '/socialMedia/socialMedia/socialMedia-score/1/direct-competitors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_socialMedia_facebook_direct_competitors(self):
        LoginTokenCase.setUp(self)
        response = self.client.get(
            '/socialMedia/socialMedia/facebook-score/1/direct-competitors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_socialMedia_instagram_direct_competitors(self):
        LoginTokenCase.setUp(self)
        response = self.client.get(
            '/socialMedia/socialMedia/instagram-score/1/direct-competitors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_socialMedia_twitter_direct_competitors(self):
        LoginTokenCase.setUp(self)
        response = self.client.get(
            '/socialMedia/socialMedia/twitter-score/1/direct-competitors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_socialMedia_youtube_direct_competitors(self):
        LoginTokenCase.setUp(self)
        response = self.client.get(
            '/socialMedia/socialMedia/youtube-score/1/direct-competitors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
