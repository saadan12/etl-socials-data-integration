from rest_framework.routers import DefaultRouter
from api.endpoints.settings.userType import UserTypeRegister

router = DefaultRouter()
router.register(r'user_type', UserTypeRegister, basename="settings")

urlpatterns = router.urls
