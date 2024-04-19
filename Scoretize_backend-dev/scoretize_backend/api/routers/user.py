from rest_framework.routers import DefaultRouter
from api.endpoints.register.register import UserRegister
from api.endpoints.register.login import Login
from api.endpoints.profile.userProfile import UserProfileViewSet

router = DefaultRouter()

router.register(r'user', Login, basename="user")
router.register(r'register', UserRegister, basename="user")
router.register(r'profile', UserProfileViewSet, basename="user")


urlpatterns = router.urls
