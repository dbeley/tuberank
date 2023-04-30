from datetime import datetime, timezone
from django.core.exceptions import ValidationError

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Avg, Q, Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings.models import (
    Channel,
    ChannelRating,
    Video,
    VideoRating,
    VideoViewing,
    UserTag,
)
from ratings.charts import charts
from ratings import enums
from ratings.serializers import (
    ChannelSerializer,
    ChannelRatingSerializer,
    VideoSerializer,
    VideoRatingSerializer,
    ProfileSerializer,
    UserTagSerializer,
)


class HomepageView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "homepage.html"

    def get(self, request):
        latest_videos = Video.objects.order_by("-id")[0:4]
        best_videos = Video.objects.annotate(
            avg_rating=Avg("ratings__rating")
        ).order_by("-avg_rating")[0:8]
        number_of_users = User.objects.count()
        number_of_channels = Channel.objects.count()
        number_of_videos = Video.objects.count()

        return Response(
            {
                "latest_videos": latest_videos,
                "best_videos": best_videos,
                "number_of_users": number_of_users,
                "number_of_channels": number_of_channels,
                "number_of_videos": number_of_videos,
            }
        )


class SearchView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "search/search.html"

    def get(self, request):
        query = request.GET.get("q")
        if not query:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
        video_queryset = Video.objects.filter(
            Q(snapshots__title_en__icontains=query)
        ).distinct()
        video_paginator = Paginator(video_queryset, 9)
        video_page = video_paginator.get_page(request.GET.get("page", 1))
        channel_queryset = Channel.objects.filter(
            Q(snapshots__name_en__icontains=query)
        ).distinct()
        channel_paginator = Paginator(channel_queryset, 4)
        channel_page = channel_paginator.get_page(request.GET.get("page_c", 1))
        return Response(
            {
                "channels": ChannelSerializer(channel_page, many=True).data,
                "videos": VideoSerializer(video_page, many=True).data,
                "query": query,
                "channel_page": channel_page,
                "video_page": video_page,
            }
        )


class PartialChannelSearchView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "search/channel_results.html"

    def get(self, request):
        query = request.GET.get("q")
        if not query:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
        channel_queryset = Channel.objects.filter(
            Q(snapshots__name_en__icontains=query)
        ).distinct()
        channel_paginator = Paginator(channel_queryset, 4)
        channel_page = channel_paginator.get_page(request.GET.get("page_c", 1))
        return Response(
            {
                "channels": ChannelSerializer(channel_page, many=True).data,
                "query": query,
                "channel_page": channel_page,
            }
        )


class PartialVideoSearchView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "search/video_results.html"

    def get(self, request):
        query = request.GET.get("q")
        if not query:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
        video_queryset = Video.objects.filter(
            Q(snapshots__title_en__icontains=query)
        ).distinct()
        video_paginator = Paginator(video_queryset, 9)
        video_page = video_paginator.get_page(request.GET.get("page", 1))
        return Response(
            {
                "videos": VideoSerializer(video_page, many=True).data,
                "query": query,
                "video_page": video_page,
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
        return Response({"video": video})

    def post(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        serializer = UserTagSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"video": video})
        tag, created = UserTag.objects.get_or_create(
            name=serializer.validated_data.get("name"),
            defaults={"user": self.request.user, "state": enums.TagState.VALIDATED},
        )
        video.tags.add(tag)
        return Response({"video": video})


class UserTagOverviewView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tag_overview.html"

    def get(self, request, name):
        tag = get_object_or_404(UserTag, name=name)
        videos = tag.video_set.all()
        return Response({"tag": tag, "videos": videos})


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
                "channel": channel,
                "videos": page,
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
                "channels": page,
            }
        )


class LoginView(APIView):
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("homepage")
        return render(request, "registration/login.html", {"form": form})

    def get(self, request):
        form = AuthenticationForm()
        return render(request, "registration/login.html", {"form": form})


class SignupView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


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
        page = paginator.get_page(request.GET.get("page", 1))
        return Response(
            {
                "user": user,
                "ratings_labels": chart_data["ratings_labels"],
                "ratings_data": chart_data["ratings_data"],
                "viewings": page,
            }
        )


class PartialProfileView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "profile/profile_timeframe.html"

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
        paginator = Paginator(user.viewings.order_by("-date_creation"), 10)
        page = paginator.get_page(request.GET.get("page", 1))
        return Response(
            {
                "user": user,
                "viewings": page,
            }
        )


class ChartsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "charts.html"

    def get(self, request):
        videos = Video.objects.annotate(num_ratings=Count("ratings")).all()
        sort_method = request.GET.get("sort_by")
        if sort_method:
            if sort_method not in [
                "newest",
                "oldest",
                "views_count",
                "ratings_count",
                "rating",
            ]:
                return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
            if sort_method == "newest":
                videos = videos.order_by("date_publication")
            if sort_method == "oldest":
                videos = videos.order_by("-date_publication")
            # if sort_method == "views_count":
            #     videos = videos.order_by("last_snapshot__count_views")
            if sort_method == "ratings_count":
                videos = videos.order_by("-num_ratings")
            # if sort_method == "rating":
            #     videos = videos.order_by("average_rating")

        paginator = Paginator(videos, 8)
        page = paginator.get_page(request.GET.get("page", 1))
        return Response({"videos": page, "page": page})
