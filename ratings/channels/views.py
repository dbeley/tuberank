from django.core.paginator import Paginator
from django.db.models import F, Max, Count, Avg
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings.models.channels import Channel
from ratings.models.videos import Video


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
            if sort_method not in [
                "newest",
                "oldest",
                "views_count",
                "views_count_desc",
                "ratings_count",
                "rating",
            ]:
                return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
            elif sort_method == "newest":
                # default sorting mechanism
                # videos = videos.order_by("-date_publication")
                pass
            elif sort_method == "oldest":
                videos = videos.order_by("date_publication")
            elif sort_method == "views_count":
                videos = videos.order_by("-count_views")
            elif sort_method == "views_count_desc":
                videos = videos.order_by("count_views")
            elif sort_method == "ratings_count":
                videos = videos.order_by("-num_ratings")
            elif sort_method == "rating":
                videos = videos.order_by("-avg_rating")
        paginator = Paginator(videos, 8)
        page = paginator.get_page(request.GET.get("page", 1))
        if request.META.get("HTTP_HX_REQUEST"):
            return Response(
                {"videos": page},
                template_name="channels/channel_details_partial.html",
            )
        return Response(
            {
                "channel": channel,
                "videos": page,
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
        ).order_by("-count_subscribers")
        if sort_method := request.GET.get("sort_by"):
            if sort_method not in [
                "most_subscribers",
                "name_asc",
                "name_desc",
                "views_count",
                "latest_indexed",
            ]:
                return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
            if sort_method == "most_subscribers":
                # default sorting mechanism
                # channels = channels.order_by("-count_subscribers")
                pass
            elif sort_method == "name_asc":
                channels = channels.order_by("name")
            elif sort_method == "name_desc":
                channels = channels.order_by("-name")
            elif sort_method == "views_count":
                channels = channels.order_by("-count_views")
            elif sort_method == "latest_indexed":
                channels = channels.order_by("-id")
        paginator = Paginator(channels, 12)
        page = paginator.get_page(request.GET.get("page", 1))
        if request.META.get("HTTP_HX_REQUEST"):
            return Response(
                {"channels": page},
                template_name="channels/channel_list_partial.html",
            )
        return Response(
            {
                "channels": page,
            }
        )
