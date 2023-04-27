from ratings.models import Channel, Video, ChannelRating, VideoRating
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from ratings.serializers import (
    ChannelSerializer,
    ChannelRatingSerializer,
    VideoSerializer,
    VideoRatingSerializer,
)
from datetime import datetime, timezone
from django.shortcuts import redirect


class ChannelList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "channel_list.html"

    def get(self, request):
        queryset = Channel.objects.all()
        channels = ChannelSerializer(queryset, many=True)
        best_channels = ChannelSerializer(
            sorted(queryset, key=lambda obj: obj.average_rating, reverse=True),
            many=True,
        )
        return Response(
            {"channels": channels.data[:], "best_channels": best_channels.data[:]}
        )


class ChannelRatingDetail(APIView):
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
        return redirect("channels_html")


class VideoList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "video_list.html"

    def get(self, request, pk):
        channel = get_object_or_404(Channel, pk=pk)
        queryset = Video.objects.filter(channel=channel).all()
        videos = VideoSerializer(queryset, many=True)
        return Response({"videos": videos.data[:]})


class VideoRatingDetail(APIView):
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
