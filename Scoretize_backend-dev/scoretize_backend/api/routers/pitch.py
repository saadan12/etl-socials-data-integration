from rest_framework.routers import DefaultRouter
from api.endpoints.pitch.pitch import PitchDeck
from api.endpoints.pitch.pitch_input import PitchInput

router = DefaultRouter()

router.register(r'pitch', PitchDeck, basename="pitch")
router.register(r'pitch', PitchInput, basename="pitch")

urlpatterns = router.urls
