from ratings.models import Channel, Video
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
        return Response({"channels": channels.data[:]})


class ChannelRatingDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "channel_rating_detail.html"

    def get(self, request, pk):
        channel = get_object_or_404(Channel, pk=pk)
        serializer = ChannelRatingSerializer(channel)
        return Response({"serializer": serializer, "channel": channel})

    def post(self, request, pk):
        channel = get_object_or_404(Channel, pk=pk)
        serializer = ChannelRatingSerializer(channel, data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer, "channel": channel})
        serializer.save(
            user=self.request.user, date_publication=datetime.now(timezone.utc)
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
        serializer = VideoRatingSerializer(video)
        return Response({"serializer": serializer, "video": video})

    def post(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        serializer = VideoRatingSerializer(video, data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer, "video": video})
        serializer.save(
            user=self.request.user, date_publication=datetime.now(timezone.utc)
        )
        return redirect("videos_html")
