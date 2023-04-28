from django.urls import path
from rest_framework import routers

from ratings import html_views, views

router = routers.DefaultRouter()
router.register(r"channels", views.ChannelViewSet, basename="channels")
router.register(r"videos", views.VideoViewSet, basename="videos")
router.register(
    r"channel-ratings", views.ChannelRatingViewSet, basename="channel-ratings"
)
router.register(r"video-ratings", views.VideoRatingViewSet, basename="video-ratings")
urlpatterns = [
    # path("", include(router.urls)),
    path("", html_views.HomepageView.as_view(), name="homepage"),
    path(
        "video_rating/<int:pk>",
        html_views.VideoRatingDetailView.as_view(),
        name="video_rating",
    ),
    path(
        "video/<int:pk>",
        html_views.VideoDetailsView.as_view(),
        name="video_details",
    ),
    path(
        "search",
        html_views.VideoSearchView.as_view(),
        name="search",
    ),
]
