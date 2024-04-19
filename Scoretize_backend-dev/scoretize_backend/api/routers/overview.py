from rest_framework.routers import DefaultRouter
from api.endpoints.overview.overview import OverviewViewSet

router = DefaultRouter()
router.register(r'overview', OverviewViewSet, basename="overview")

urlpatterns = router.urls
