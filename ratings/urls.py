from rest_framework import routers
from ratings import views

router = routers.DefaultRouter()
router.register(r"channels", views.ChannelViewSet, basename="channels")
router.register(r"videos", views.VideoViewSet, basename="videos")
router.register(
    r"channel-ratings", views.ChannelRatingViewSet, basename="channel-ratings"
)
router.register(r"video-ratings", views.VideoRatingViewSet, basename="video-ratings")
urlpatterns = router.urls
