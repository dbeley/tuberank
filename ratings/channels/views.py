import logging
from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import F, Max, Count, Avg
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings import enums
from ratings.channels.serializers import (
    ChannelRatingSerializer,
    ChannelSerializer,
    ChannelSerializerWithRatings,
)
from ratings.models.channels import Channel, ChannelRating, ChannelSnapshot
from ratings.models.videos import Video
from ratings.videos.serializers import VideoSerializer
from ratings.yt_import import create_video_snapshot


logger = logging.getLogger(__name__)


def _get_user_rating_for_channel(user: User, channel: Channel) -> ChannelRating | None:
    if ChannelRating.objects.filter(
        channel=channel,
        user=user,
    ).exists():
        return ChannelRating.objects.get(channel=channel, user=user)
    return None


class ChannelDetailsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "channels/channel_details.html"

    def get(self, request, pk):
        channel = get_object_or_404(Channel, pk=pk)
        videos = (
            Video.objects.filter(channel=channel)
            .annotate(
                num_ratings=Count("ratings"),
                avg_rating=Avg("ratings__rating"),
                count_views=Max("snapshots__count_views"),
            )
            .order_by("-date_publication")
        )
        if sort_method := request.GET.get("sort_by"):
            if sort_method not in enums.SortingChoices.choices():
                return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
            match sort_method:
                case enums.SortingChoices.OLDEST.value:
                    videos = videos.order_by("date_publication")
                case enums.SortingChoices.MOST_VIEWED.value:
                    videos = videos.order_by("-count_views")
                case enums.SortingChoices.LEAST_VIEWED.value:
                    videos = videos.order_by("count_views")
                case enums.SortingChoices.MOST_RATED.value:
                    videos = videos.order_by("-num_ratings")
                case enums.SortingChoices.BEST_RATED.value:
                    videos = videos.filter(avg_rating__isnull=False).order_by(
                        "-avg_rating"
                    )
                case enums.SortingChoices.NEWEST.value:
                    videos = videos.order_by("-date_publication")
        else:
            videos = videos.order_by("-date_publication")
        paginator = Paginator(videos, 8)
        videos = paginator.get_page(request.GET.get("page", 1))
        if request.META.get("HTTP_HX_REQUEST"):
            return Response(
                {
                    "videos": VideoSerializer(videos, many=True).data,
                    "videos_page": videos,
                },
                template_name="channels/channel_details_partial.html",
            )
        return Response(
            {
                "channel": ChannelSerializerWithRatings(channel).data,
                "videos": VideoSerializer(videos, many=True).data,
                "videos_page": videos,
            }
        )


class ChannelListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "channels/channel_list.html"

    def get(self, request):
        channels = Channel.objects.annotate(
            name=F("snapshots__name_en"),
            count_subscribers=Max("snapshots__count_subscribers"),
            count_views=Max("snapshots__count_views"),
            count_videos_indexed=Count("videos"),
            avg_rating=Avg(F("ratings__rating")),
        ).order_by("-count_videos_indexed")
        if sort_method := request.GET.get("sort_by"):
            if sort_method not in enums.SortingChoices.choices():
                return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
            match sort_method:
                case enums.SortingChoices.MOST_VIDEOS_INDEXED.value:
                    channels = channels.order_by("-count_videos_indexed")
                case enums.SortingChoices.NAME_ASC.value:
                    channels = channels.order_by("name")
                case enums.SortingChoices.NAME_DESC.value:
                    channels = channels.order_by("-name")
                case enums.SortingChoices.MOST_VIEWED.value:
                    channels = channels.order_by("-count_views")
                case enums.SortingChoices.LATEST_INDEXED.value:
                    channels = channels.order_by("-id")
                case enums.SortingChoices.BEST_RATED.value:
                    channels = channels.filter(avg_rating__isnull=False).order_by(
                        "-avg_rating"
                    )
                case enums.SortingChoices.MOST_SUBSCRIBERS.value:
                    channels = channels.order_by("-count_subscribers")
        paginator = Paginator(channels, 12)
        channels = paginator.get_page(request.GET.get("page", 1))
        if request.META.get("HTTP_HX_REQUEST"):
            return Response(
                {
                    "channels": ChannelSerializer(channels, many=True).data,
                    "channels_page": channels,
                },
                template_name="channels/channel_list_partial.html",
            )
        return Response(
            {
                "channels": ChannelSerializer(channels, many=True).data,
                "channels_page": channels,
            }
        )


class ChannelRatingDetailView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "channels/channel_rating.html"

    def get(self, request, pk):
        channel = get_object_or_404(Channel, pk=pk)
        channel_rating = _get_user_rating_for_channel(
            user=request.user, channel=channel
        )
        if not channel_rating:
            channel_rating = ChannelRating(channel=channel, user=request.user)
        serializer = ChannelRatingSerializer(channel_rating)
        return Response(
            {"serializer": serializer, "channel": ChannelSerializer(channel).data}
        )

    def post(self, request, pk):
        if not request.user.is_authenticated:
            raise PermissionDenied()
        channel = get_object_or_404(Channel, pk=pk)
        channel_rating = ChannelRating(channel=channel, user=request.user)
        serializer = ChannelRatingSerializer(channel_rating, data=request.data)
        if not serializer.is_valid():
            return Response(
                {"serializer": serializer, "channel": ChannelSerializer(channel).data}
            )
        ChannelRating.objects.update_or_create(
            channel=channel,
            user=request.user,
            defaults={
                **serializer.validated_data,
            },
        )
        return redirect("channel_details", pk=channel.id)


class ChannelRefreshView(APIView):
    def get(self, _, pk):
        channel = get_object_or_404(Channel, pk=pk)
        videos = Video.objects.filter(channel=channel)
        latest_snapshot = ChannelSnapshot.objects.filter(channel=channel).latest(
            "date_creation"
        )
        if datetime.now().date() != latest_snapshot.date_creation.date():
            for index, video in enumerate(videos, 1):
                create_video_snapshot(video.yt_id, skip_channel_snapshot=index != 1)
        else:
            logger.warning(
                "Skipping snapshot creation for channel %s, the latest one is too recent",
                channel.pk,
            )
        return redirect("channel_details", pk=channel.id)
