from rest_framework.routers import DefaultRouter
from api.endpoints.project.project import ManageProject
from api.endpoints.project.project import ActiveProject

router = DefaultRouter()
router.register(r'project', ManageProject, basename="project")
router.register(r'project', ActiveProject, basename="project")

urlpatterns = router.urls
