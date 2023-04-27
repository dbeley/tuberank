from rest_framework import routers
from django.urls import include, path
from ratings import views, html_views

router = routers.DefaultRouter()
router.register(r"channels", views.ChannelViewSet, basename="channels")
router.register(r"videos", views.VideoViewSet, basename="videos")
router.register(
    r"channel-ratings", views.ChannelRatingViewSet, basename="channel-ratings"
)
router.register(r"video-ratings", views.VideoRatingViewSet, basename="video-ratings")
urlpatterns = [
    path("", include(router.urls)),
    path("channels_html", html_views.ChannelList.as_view(), name="channels_html"),
    path("videos_html/<int:pk>", html_views.VideoList.as_view(), name="videos_html"),
    path(
        "channel_rating_html/<int:pk>",
        html_views.ChannelRatingDetail.as_view(),
        name="channel_rating_html",
    ),
    path(
        "video_rating_html/<int:pk>",
        html_views.VideoRatingDetail.as_view(),
        name="video_rating_html",
    ),
]
