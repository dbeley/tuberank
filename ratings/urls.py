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
    path("html", html_views.HomepageView.as_view(), name="homepage"),
    path(
        "videos_html/<int:pk>", html_views.VideoListView.as_view(), name="videos_html"
    ),
    path(
        "channel_rating_html/<int:pk>",
        html_views.ChannelRatingDetailView.as_view(),
        name="channel_rating_html",
    ),
    path(
        "video_rating_html/<int:pk>",
        html_views.VideoRatingDetailView.as_view(),
        name="video_rating_html",
    ),
    path(
        "subscribe",
        html_views.SubscribeView.as_view(),
        name="subscribe",
    ),
]
