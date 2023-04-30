from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings import enums
from ratings.models.tags import UserTag
from ratings.models.lists import VideoList
from ratings.models.videos import Video, VideoRating, VideoViewing
from ratings.lists.serializers import VideoListSerializer
from ratings.tags.serializers import UserTagSerializer
from ratings.videos.serializers import VideoRatingSerializer


class VideoRatingDetailView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "video_rating.html"

    def get(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        if not VideoRating.objects.filter(
            video=video,
            user=request.user,
        ).exists():
            video_rating = VideoRating(video=video, user=request.user)
        else:
            video_rating = VideoRating.objects.get(video=video, user=request.user)
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
    template_name = "video_viewing.html"

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
    template_name = "video_details.html"

    def get(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        video_lists = VideoList.objects.filter(user=request.user)
        return Response({"video": video, "video_lists": video_lists})

    def post(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        video_lists = VideoList.objects.filter(user=request.user)
        serializer = UserTagSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"video": video})
        tag, created = UserTag.objects.get_or_create(
            name=serializer.validated_data.get("name"),
            defaults={"user": self.request.user, "state": enums.TagState.VALIDATED},
        )
        video.tags.add(tag)
        return Response({"video": video, "video_lists": video_lists})


class VideoListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "lists.html"

    def get(self, request):
        user_lists = VideoList.objects.filter(user=request.user)
        popular_lists = VideoList.objects.annotate(
            num_ratings=Count("ratings")
        ).order_by("-num_ratings")[0:8]
        return Response({"user_lists": user_lists, "popular_lists": popular_lists})

    def post(self, request):
        serializer = VideoListSerializer(data=request.data)
        if not serializer.is_valid():
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
        VideoList.objects.create(
            user=request.user,
            **serializer.validated_data,
        )
        user_lists = VideoList.objects.filter(user=request.user)
        popular_lists = VideoList.objects.annotate(
            num_ratings=Count("ratings")
        ).order_by("-num_ratings")[0:8]
        return Response({"user_lists": user_lists, "popular_lists": popular_lists})
