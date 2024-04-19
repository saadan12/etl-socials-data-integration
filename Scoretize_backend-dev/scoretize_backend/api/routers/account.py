from rest_framework.routers import DefaultRouter
from api.endpoints.account.account import AccountProperties

router = DefaultRouter()

router.register(r'account', AccountProperties, basename="account")

urlpatterns = router.urls
