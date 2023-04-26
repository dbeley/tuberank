from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from ratings.serializers import (
    UserSerializer,
    ChannelSerializer,
    ChannelRatingSerializer,
    VideoSerializer,
    VideoRatingSerializer,
)
from ratings.models import Channel, Video, ChannelRating, VideoRating
from datetime import datetime, timezone


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChannelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Channel.objects.all().order_by("-date_creation")
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChannelRatingViewSet(viewsets.ModelViewSet):
    serializer_class = ChannelRatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChannelRating.objects.filter(user=user).order_by("date_publication")

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user, date_publication=datetime.now(timezone.utc)
        )


class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.all().order_by("-date_publication")
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]


class VideoRatingViewSet(viewsets.ModelViewSet):
    serializer_class = VideoRatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return VideoRating.objects.filter(user=user).order_by("date_publication")

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user, date_publication=datetime.now(timezone.utc)
        )
