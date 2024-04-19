from rest_framework.routers import DefaultRouter
from api.endpoints.globalv import GlobalViewSet

router = DefaultRouter()
router.register(r'global', GlobalViewSet, basename="global")

urlpatterns = router.urls
