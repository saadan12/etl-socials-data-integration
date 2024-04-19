from rest_framework.routers import DefaultRouter
from api.endpoints.searchAds import SearchAdsviewViewSet

router = DefaultRouter()
router.register(r'paid-media', SearchAdsviewViewSet, basename="paid-media")

urlpatterns = router.urls
