from rest_framework.routers import DefaultRouter
from api.endpoints.seo import SeoviewViewSet

router = DefaultRouter()
router.register(r'seo', SeoviewViewSet, basename="seo")

urlpatterns = router.urls
