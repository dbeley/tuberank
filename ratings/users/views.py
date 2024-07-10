from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponseRedirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings.charts import charts
from ratings.models import Channel

from ratings.users.serializers import UserSerializer, MostWatchedChannelSerializer


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
        video_chart_data = charts.get_video_ratings_chart_for_user(user)
        channel_chart_data = charts.get_channel_ratings_chart_for_user(user)

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

        most_watched_channels = (
            Channel.objects.filter(videos__viewings__user=user)
            .annotate(view_count=Count("videos__viewings"))
            .order_by("-view_count")
        )
        return Response(
            {
                "user": user,
                "video_ratings_labels": video_chart_data["ratings_labels"],
                "video_ratings_data": video_chart_data["ratings_data"],
                "channel_ratings_labels": channel_chart_data["ratings_labels"],
                "channel_ratings_data": channel_chart_data["ratings_data"],
                "viewings": page,
                "most_watched_channels": MostWatchedChannelSerializer(
                    most_watched_channels, many=True
                ).data,
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
