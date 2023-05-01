from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import permissions, views
from rest_framework.response import Response

from ratings import enums
from ratings.models.tags import UserTag
from ratings.models.videos import Video
from ratings.tags.serializers import UserTagSerializer
from ratings.videos.serializers import VideoSerializer


class UserTagView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(
            UserTagSerializer(
                UserTag.objects.filter(state=enums.TagState.VALIDATED), many=True
            )
        )


class UserTagVideoView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, video_pk):
        video = get_object_or_404(Video.objects.all(), pk=video_pk)
        return Response(UserTagSerializer(video.tags, many=True))

    def post(self, request, video_pk):
        serializer = UserTagSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError("Payload invalid")
        video = get_object_or_404(Video.objects.all(), pk=request.data.get("video_id"))
        tag, created = UserTag.objects.get_or_create(
            name=request.data.get("name"),
            defaults={"user": self.request.user, "state": enums.TagState.VALIDATED},
        )
        video.tags.add(tag)
        return Response(UserTagSerializer(tag).data)


class UserTagOverviewView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, name):
        tag = get_object_or_404(UserTag.objects.all(), name=name)
        return Response(
            VideoSerializer(Video.objects.filter(tags__contains=tag), many=True)
        )
