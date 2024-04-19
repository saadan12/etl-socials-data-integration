from rest_framework.routers import DefaultRouter
from api.endpoints.chronTrigger import ChronTriggerViewSet

router = DefaultRouter()

router.register(r'chron', ChronTriggerViewSet, basename="chron")

urlpatterns = router.urls
