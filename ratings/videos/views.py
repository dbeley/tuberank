from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings import enums
from ratings.models.tags import UserTag
from ratings.models.lists import VideoList, VideoListItem
from ratings.models.videos import Video, VideoRating, VideoViewing
from ratings.tags.serializers import UserTagSerializer
from ratings.videos.serializers import VideoRatingSerializer


def _add_video_to_list(video_pk: int, list_pk: int):
    list = VideoList.objects.get(pk=list_pk)
    video = Video.objects.get(pk=video_pk)
    VideoListItem.objects.create(list=list, video=video, order=1)


def _get_user_lists(user: User) -> QuerySet[VideoList]:
    return VideoList.objects.filter(user=user)


def _get_user_rating_for_video(user: User, video: Video) -> VideoRating | None:
    if VideoRating.objects.filter(
        video=video,
        user=user,
    ).exists():
        return VideoRating.objects.get(video=video, user=user)
    return None


class VideoRatingDetailView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "videos/video_rating.html"

    def get(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        video_rating = _get_user_rating_for_video(user=request.user, video=video)
        if not video_rating:
            video_rating = VideoRating(video=video, user=request.user)
        serializer = VideoRatingSerializer(video_rating)
        return Response({"serializer": serializer, "video": video})

    def post(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        video_rating = VideoRating(video=video, user=request.user)
        serializer = VideoRatingSerializer(video_rating, data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer, "video": video})
        VideoRating.objects.update_or_create(
            video=video,
            user=request.user,
            defaults={
                **serializer.validated_data,
            },
        )
        return redirect("video_details", pk=video.id)


class VideoViewingView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "videos/video_viewing.html"

    def get(self, request, pk):
        try:
            video = get_object_or_404(Video, pk=pk)
        except Video.DoesNotExist:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
        return Response({"video": video})

    def post(self, request, pk):
        try:
            video = get_object_or_404(Video, pk=pk)
        except Video.DoesNotExist:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
        VideoViewing.objects.create(
            user=request.user,
            video=video,
            state=enums.ViewingState.VIEWED,
        )
        return redirect("video_details", pk=video.id)


class VideoDetailsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "videos/video_details.html"

    def get(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        user_lists = _get_user_lists(request.user)
        return Response({"video": video, "user_lists": user_lists})

    def post(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        user_lists = _get_user_lists(request.user)
        if "name" in request.data:
            serializer = UserTagSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"video": video, "user_lists": user_lists})
            tag, created = UserTag.objects.get_or_create(
                name=serializer.validated_data.get("name"),
                defaults={"user": self.request.user, "state": enums.TagState.VALIDATED},
            )
            video.tags.add(tag)
        elif "list_pk" in request.data:
            _add_video_to_list(video_pk=video.pk, list_pk=request.data.get("list_pk"))
        return Response({"video": video, "user_lists": user_lists})
