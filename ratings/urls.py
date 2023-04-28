from django.urls import path

from ratings import views

urlpatterns = [
    path("", views.HomepageView.as_view(), name="homepage"),
    path(
        "video_rating/<int:pk>",
        views.VideoRatingDetailView.as_view(),
        name="video_rating",
    ),
    path(
        "channel-list",
        views.ChannelListView.as_view(),
        name="channel_list",
    ),
    path(
        "video/<int:pk>",
        views.VideoDetailsView.as_view(),
        name="video_details",
    ),
    path(
        "channel/<int:pk>",
        views.ChannelDetailsView.as_view(),
        name="channel_details",
    ),
    path(
        "search",
        views.SearchView.as_view(),
        name="search",
    ),
]
