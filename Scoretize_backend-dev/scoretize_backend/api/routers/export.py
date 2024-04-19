from rest_framework.routers import DefaultRouter
from api.endpoints.exports.export import ExportDataViewSet

router = DefaultRouter()
router.register(r'data', ExportDataViewSet, basename="export")

urlpatterns = router.urls
