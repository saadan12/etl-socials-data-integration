from rest_framework.routers import DefaultRouter
from api.endpoints.settings.sector import SectorRegister

router = DefaultRouter()
router.register(r'sector', SectorRegister, basename="settings")

urlpatterns = router.urls
