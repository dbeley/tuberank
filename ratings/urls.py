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
        "video/<int:pk>",
        views.VideoDetailsView.as_view(),
        name="video_details",
    ),
    path(
        "search",
        views.VideoSearchView.as_view(),
        name="search",
    ),
]
