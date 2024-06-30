from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponseRedirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings.charts import charts
from ratings.models import VideoViewing, Channel

from ratings.users.serializers import UserSerializer


class UserListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "users/user_list.html"

    def get(self, request):
        users = User.objects.filter(username__isnull=False, is_superuser=False)
        return Response({"users": UserSerializer(users, many=True).data})


class ProfileView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "profile/profile.html"

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
        chart_data = charts.get_ratings_chart_for_user(user)
        paginator = Paginator(user.viewings.order_by("-date_creation"), 10)
        if page_query_param := request.GET.get("page"):
            page = paginator.get_page(page_query_param)
            return Response(
                {
                    "user": user,
                    "viewings": page,
                },
                template_name="profile/profile_timeframe.html",
            )
        page = paginator.get_page(1)
        most_watched_channel_dict = (
            VideoViewing.objects.filter(user=user)
            .values("video__channel_id")
            .annotate(count=Count("video__channel_id"))
            .order_by("-count")[:8]
        )
        most_watched_channels = []
        for channel_dict in most_watched_channel_dict:
            channel = Channel.objects.get(pk=channel_dict.get("video__channel_id"))
            most_watched_channels.append(
                {
                    "id": channel.pk,
                    "name": channel.last_snapshot.name_en,
                    "count": channel_dict.get("count"),
                    "thumbnail_url": channel.last_snapshot.thumbnail_url,
                }
            )
        return Response(
            {
                "user": user,
                "ratings_labels": chart_data["ratings_labels"],
                "ratings_data": chart_data["ratings_data"],
                "viewings": page,
                "most_watched_channels": most_watched_channels,
            }
        )


class ProfileVideosRatingsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "profile/profile_videos_ratings.html"

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
        return Response(
            {
                "user": user,
            }
        )


class ProfileChannelsRatingsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "profile/profile_channels_ratings.html"

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
        return Response(
            {
                "user": user,
            }
        )
