from django.urls import path

from ratings import views

urlpatterns = [
    path("", views.HomepageView.as_view(), name="homepage"),
    path("login", views.LoginView.as_view(), name="login"),
    path("signup", views.SignupView.as_view(), name="signup"),
    path("user/<str:username>", views.ProfileView.as_view(), name="profile"),
    path(
        "user/<str:username>/timeframe",
        views.PartialProfileView.as_view(),
        name="profile_timeframe",
    ),
    path(
        "channels/list",
        views.ChannelListView.as_view(),
        name="channel_list",
    ),
    path(
        "channel/<int:pk>",
        views.ChannelDetailsView.as_view(),
        name="channel_details",
    ),
    path(
        "video/<int:pk>/rate",
        views.VideoRatingDetailView.as_view(),
        name="video_rating",
    ),
    path(
        "video/<int:pk>/view",
        views.VideoViewingView.as_view(),
        name="video_viewing",
    ),
    path(
        "video/<int:pk>",
        views.VideoDetailsView.as_view(),
        name="video_details",
    ),
    path(
        "search/channels",
        views.PartialChannelSearchView.as_view(),
        name="search_channels",
    ),
    path(
        "search/videos",
        views.PartialVideoSearchView.as_view(),
        name="search_videos",
    ),
    path(
        "search",
        views.SearchView.as_view(),
        name="search",
    ),
    path(
        "charts",
        views.ChartsView.as_view(),
        name="charts",
    ),
]
