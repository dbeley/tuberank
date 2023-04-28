from datetime import datetime, timezone

from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings.models import Channel, ChannelRating, Video, VideoRating
from ratings.serializers import (
    ChannelRatingSerializer,
    ChannelSerializer,
    VideoRatingSerializer,
    VideoSerializer,
    UserSerializer,
)


class HomepageView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "homepage.html"

    def get(self, request):
        channels = ChannelSerializer(Channel.objects.order_by("-id")[0:10], many=True)
        best_videos = VideoSerializer(
            Video.objects.annotate(avg_rating=Avg("ratings__rating")).order_by(
                "-avg_rating"
            )[0:10],
            many=True,
        )

        return Response(
            {
                "channels": channels.data,
                "best_videos": best_videos.data,
            }
        )


class ChannelRatingDetailView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "channel_rating_detail.html"

    def get(self, request, pk):
        channel = get_object_or_404(Channel, pk=pk)
        channel_rating = ChannelRating(channel=channel, user=request.user)
        serializer = ChannelRatingSerializer(channel_rating)
        return Response({"serializer": serializer, "channel": channel})

    def post(self, request, pk):
        channel = get_object_or_404(Channel, pk=pk)
        channel_rating = ChannelRating(channel=channel, user=request.user)
        serializer = ChannelRatingSerializer(channel_rating, data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer, "channel": channel})
        ChannelRating.objects.update_or_create(
            channel=channel,
            user=request.user,
            defaults={
                "date_publication": datetime.now(timezone.utc),
                **serializer.validated_data,
            },
        )
        return redirect("html")


class VideoListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "video_list.html"

    def get(self, request, pk):
        channel = get_object_or_404(Channel, pk=pk)
        queryset = (
            Video.objects.filter(channel=channel).order_by("-date_publication").all()
        )
        videos = VideoSerializer(queryset, many=True)
        return Response({"videos": videos.data[:]})


class VideoRatingDetailView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "video_rating_detail.html"

    def get(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
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
                "date_publication": datetime.now(timezone.utc),
                **serializer.validated_data,
            },
        )
        return redirect("videos_html", pk=video.channel_id)


class SubscribeView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "subscribe.html"

    def get(self, request):
        serializer = UserSerializer()
        return Response({"serializer": serializer})

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer})
        serializer.save()
        return redirect("homepage")
