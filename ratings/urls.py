from django.urls import path

import ratings.channels.views
import ratings.charts.views
import ratings.lists.views
import ratings.tags.views
import ratings.videos.views
from ratings import views

urlpatterns = [
    path("", views.HomepageView.as_view(), name="homepage"),
    path("login", views.LoginView.as_view(), name="login"),
    path("signup", views.SignupView.as_view(), name="signup"),
    path("user/<str:username>", views.ProfileView.as_view(), name="profile"),
    path(
        "channels/list",
        ratings.channels.views.ChannelListView.as_view(),
        name="channel_list",
    ),
    path(
        "channel/<int:pk>",
        ratings.channels.views.ChannelDetailsView.as_view(),
        name="channel_details",
    ),
    path(
        "video/<int:pk>/rate",
        ratings.videos.views.VideoRatingDetailView.as_view(),
        name="video_rating",
    ),
    path(
        "video/<int:pk>/view",
        ratings.videos.views.VideoViewingView.as_view(),
        name="video_viewing",
    ),
    path(
        "video/<int:pk>",
        ratings.videos.views.VideoDetailsView.as_view(),
        name="video_details",
    ),
    path(
        "search",
        views.SearchView.as_view(),
        name="search",
    ),
    path(
        "charts",
        ratings.charts.views.ChartsView.as_view(),
        name="charts",
    ),
    path("lists", ratings.lists.views.VideoListView.as_view(), name="lists"),
    path(
        "list/<int:pk>",
        ratings.lists.views.VideoListDetailsView.as_view(),
        name="list_details",
    ),
    path(
        "list/<int:pk>/delete",
        ratings.lists.views.VideoListDeleteView.as_view(),
        name="list_delete",
    ),
    path(
        "list/<int:list_pk>/delete/<int:video_pk>",
        ratings.lists.views.VideoListDeleteItemView.as_view(),
        name="list_delete_item",
    ),
    path(
        "tags",
        ratings.tags.views.TagsView.as_view(),
        name="tags",
    ),
    path(
        "tags/<str:name>",
        ratings.tags.views.UserTagOverviewView.as_view(),
        name="tag_overview",
    ),
    path(
        "tags/<str:tag_name>/delete/<int:video_pk>",
        ratings.tags.views.UserTagDeleteItemView.as_view(),
        name="tag_delete_item",
    ),
    path(
        "import-video",
        ratings.views.ImportVideoView.as_view(),
        name="import_video",
    ),
]
