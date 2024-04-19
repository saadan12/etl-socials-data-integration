from rest_framework.routers import DefaultRouter
from api.endpoints.performance.performance import PerformanceInfo

router = DefaultRouter()

router.register(r'performance', PerformanceInfo, basename="performance")

urlpatterns = router.urls
