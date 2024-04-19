from rest_framework.routers import DefaultRouter
from api.endpoints.performance.performanceCalc import PerformanceCalc

router = DefaultRouter()

router.register(r'performance', PerformanceCalc, basename="performance")

urlpatterns = router.urls
