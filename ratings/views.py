from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from ratings.serializers import UserSerializer, ChannelSerializer
from ratings.models import Channel


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChannelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Channel.objects.all().order_by("-date_creation")
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticated]
