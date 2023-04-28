from datetime import datetime, timezone

from django.db.models import Avg, Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings.models import Channel, Video, VideoRating
from ratings.serializers import (
    ChannelSerializer,
    VideoSerializer,
    VideoRatingSerializer,
)


class HomepageView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "homepage.html"

    def get(self, request):
        channels = ChannelSerializer(Channel.objects.order_by("-id")[0:8], many=True)
        latest_videos = VideoSerializer(
            Video.objects.order_by("-id")[0:4],
            many=True,
        )
        best_videos = VideoSerializer(
            Video.objects.annotate(avg_rating=Avg("ratings__rating")).order_by(
                "-avg_rating"
            )[0:8],
            many=True,
        )

        return Response(
            {
                "channels": channels.data,
                "latest_videos": latest_videos.data,
                "best_videos": best_videos.data,
            }
        )


class SearchView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "search.html"

    def get(self, request):
        query = request.GET.get("q")
        if not query:
            return redirect("homepage")
        queryset = Video.objects.filter(
            Q(snapshots__title_en__icontains=query)
            | Q(channel__snapshots__name_en__icontains=query)
        ).distinct()
        paginator = Paginator(queryset, 9)
        page = paginator.get_page(request.GET.get("page", 1))
        return Response(
            {
                "videos": VideoSerializer(page, many=True).data,
                "query": query,
                "page": page,
            }
        )


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
                "date_publication": datetime.now(timezone.utc),
                **serializer.validated_data,
            },
        )
        return redirect("video_details", pk=video.id)


class VideoDetailsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "video_details.html"

    def get(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        serializer = VideoSerializer(video)
        ratings = VideoRatingSerializer(video.ratings.all(), many=True)
        return Response({"video": serializer.data, "selected_ratings": ratings.data})


class ChannelDetailsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "channel_details.html"

    def get(self, request, pk):
        channel = get_object_or_404(Channel, pk=pk)
        videos = Video.objects.filter(channel=channel)
        paginator = Paginator(videos, 8)
        page = paginator.get_page(request.GET.get("page", 1))
        return Response(
            {
                "channel": ChannelSerializer(channel).data,
                "videos": VideoSerializer(page, many=True).data,
                "page": page,
            }
        )


class ChannelListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "channel_list.html"

    def get(self, request):
        channels = Channel.objects.all()
        paginator = Paginator(channels, 12)
        page = paginator.get_page(request.GET.get("page", 1))
        return Response(
            {
                "channels": ChannelSerializer(page, many=True).data,
                "page": page,
            }
        )
