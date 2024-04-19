from rest_framework.routers import DefaultRouter
from api.endpoints.website.website import WebsiteViewSet

router = DefaultRouter()

router.register(r'website', WebsiteViewSet, basename="website")

urlpatterns = router.urls
