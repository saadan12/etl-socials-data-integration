from rest_framework.routers import DefaultRouter
from api.endpoints.socialMedia import SocialMediaViewSet

router = DefaultRouter()
router.register(r'socialMedia', SocialMediaViewSet, basename="socialMedia")

urlpatterns = router.urls
