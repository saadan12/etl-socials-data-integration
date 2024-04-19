from ..models import Seo, Website, Website_traffic
from ..models import Social_media, Facebook, Instagram
from ..models import Twitter, Youtube, Company_wise_scores
from ..models import Users, User_Type, UserProject, Account


class LoginTokenCase():
    # Testing Login & auth inside endpoints.
    def __init__(self):
        print("Login token case initialised")

    def setUp(self):
        self.account = Account.objects.create(
            name='TKF',
            public_id=111111
        )
        # Shoud have id 1
        self.user_type1 = User_Type.objects.create(
            name='Basic User',
            description='Basic User'
        )
        self.user_type2 = User_Type.objects.create(
            name='Admin',
            description='Admin'
        )
        self.user_type3 = User_Type.objects.create(
            name='Keenfolks',
            description='Keenfolks'
        )
        self.user = Users.objects.create_user(
            name="Testers",
            surname="Testers",
            email="testers@testing.com",
            password="123456tT*",
            account_id=1,
            user_type_id=1
        )
        self.access_token = self.client.post('/user/user/login/', {
            'email': 'testers@testing.com',
            'password': '123456tT*'}).data.get("data").get("access")
        self.api_authentication()
        self.project()
        self.user_project()

    def project(self):
        self.setUpSectors()
        self.project = self.client.post(
            '/project/project/create-project/', {
                "name": "Walmart0",
                "sector_name": "law and government",
                "subcategory": "immigration and visas",
                "company_url": "walmart.com",
                "competitors": ["ebay.com",
                                "mangakakalot.com",
                                "etsy.com",
                                "aliexpress.com",
                                "amazon.de"
                                ]}, format='json')
        self.seo = Seo.objects.create(company_id=1)
        self.website = Website.objects.create(company_id=1)
        self.website_traffic = Website_traffic.objects.create(website_id=1)
        self.social_media = Social_media.objects.create(company_id=1)
        self.social_media_facebook = Facebook.objects.create(social_media_id=1)
        self.social_media_instagram = Instagram.objects.create(
            social_media_id=1)
        self.social_media_twitter = Twitter.objects.create(social_media_id=1)
        self.social_media_youtube = Youtube.objects.create(social_media_id=1)
        self.scores = Company_wise_scores.objects.create(
            project_id=1, company_id=1,
            global_score=1, website_score=1, sm_score=1,
            sm_facebook_score=1, sm_instagram_score=1,
            sm_youtube_score=1, sm_twitter_score=1,
            seo_score=1, searchAds_score=1)

    def setUpSectors(self):
        response = self.client.post(
            '/sector/sector/postSectors/', format='json')
        return response

    def user_project(self):
        self.user_project = UserProject.objects.create(
            user_id=1,
            project_id=1
        )

    def api_authentication(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
