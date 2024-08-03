from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Avg, Q, Count
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from rest_framework.exceptions import PermissionDenied
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings.channels.serializers import ChannelSerializer
from ratings.models.channels import Channel
from ratings.models.videos import Video
from ratings.videos.serializers import VideoSerializer
from ratings.yt_import import (
    NoResultException,
    TooManyResultException,
    create_video_snapshot_from_url,
)


class HomepageView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "homepage.html"

    def get(self, request):
        latest_videos = Video.objects.order_by("-id")[0:20]
        paginator = Paginator(latest_videos, 4)
        latest_videos = paginator.get_page(request.GET.get("page", 1))
        if request.META.get("HTTP_HX_REQUEST"):
            return Response(
                {
                    "latest_videos": VideoSerializer(latest_videos, many=True).data,
                    "latest_videos_page": latest_videos,
                },
                template_name="homepage_partial.html",
            )
        videos = Video.objects.annotate(
            avg_rating=Avg("ratings__rating"), num_ratings=Count("ratings")
        )
        best_videos = videos.filter(avg_rating__isnull=False).order_by(
            "-avg_rating", "num_ratings"
        )[0:8]
        two_weeks_ago = timezone.now() - timezone.timedelta(weeks=2)

        # Get videos with recent activity in the last two weeks
        trending_videos = (
            Video.objects.filter(ratings__date_creation__gte=two_weeks_ago)
            .annotate(avg_rating=Avg("ratings__rating"), num_ratings=Count("ratings"))
            .order_by("-avg_rating", "-num_ratings")
            .filter(avg_rating__isnull=False, avg_rating__gt=3)
        )[0:8]
        popular_videos = videos.order_by("-num_ratings")[0:4]

        return Response(
            {
                "latest_videos": VideoSerializer(latest_videos, many=True).data,
                "latest_videos_page": latest_videos,
                "trending_videos": VideoSerializer(trending_videos, many=True).data,
                "best_videos": VideoSerializer(best_videos, many=True).data,
                "popular_videos": VideoSerializer(popular_videos, many=True).data,
                "number_of_users": User.objects.count(),
                "number_of_channels": Channel.objects.count(),
                "number_of_videos": Video.objects.count(),
            }
        )


class SearchView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "search/search.html"

    def get(self, request):
        query = request.GET.get("q")
        if not query:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
        if query.startswith("https://") and "youtube.com" in query:
            query = (
                query.strip()
                .split("youtube.com/watch?v=")[-1]
                .rsplit("&list=")[0]
                .rsplit("&pp=")[0]
            )
        video_queryset = Video.objects.filter(
            Q(snapshots__title_en__icontains=query) | Q(yt_id__icontains=query)
        ).distinct()
        video_paginator = Paginator(video_queryset, 9)
        if video_page_query_param := request.GET.get("page"):
            video_page = video_paginator.get_page(video_page_query_param)
            return Response(
                {
                    "videos": VideoSerializer(video_page, many=True).data,
                    "video_page": video_page,
                    "query": query,
                },
                template_name="search/video_results.html",
            )
        video_page = video_paginator.get_page(1)

        channel_queryset = Channel.objects.filter(
            Q(snapshots__name_en__icontains=query)
            | Q(snapshots__custom_url__icontains=query)
            | Q(yt_id__icontains=query)
        ).distinct()
        channel_paginator = Paginator(channel_queryset, 4)
        if channel_page_query_param := request.GET.get("page_c"):
            channel_page = channel_paginator.get_page(channel_page_query_param)
            return Response(
                {
                    "channels": ChannelSerializer(channel_page, many=True).data,
                    "channel_page": channel_page,
                    "query": query,
                },
                template_name="search/channel_results.html",
            )
        channel_page = channel_paginator.get_page(1)
        video_results_count = video_queryset.count()
        channel_results_count = channel_queryset.count()
        return Response(
            {
                "results_count": video_results_count + channel_results_count,
                "channels": ChannelSerializer(channel_page, many=True).data,
                "channel_page": channel_page,
                "videos": VideoSerializer(video_page, many=True).data,
                "video_page": video_page,
                "query": query,
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


class ImportVideoView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "import_video.html"

    def get(self, request):
        if not request.user.is_authenticated:
            raise PermissionDenied()
        return Response()

    def post(self, request):
        if not request.user.is_authenticated:
            raise PermissionDenied()
        errors = []
        success = []
        if urls := request.data.get("urls"):
            urls_list = urls.split("\n")
            for url in urls_list:
                try:
                    create_video_snapshot_from_url(url)
                except TooManyResultException:
                    errors.append(
                        f"The import for item {url} failed with an error: more than one result found"
                    )
                except NoResultException:
                    errors.append(
                        f"The import for item {url} failed with an error: no result found"
                    )
                except Exception as err:
                    errors.append(
                        f"The import for item {url} failed with an error: {str(err)}"
                    )
                else:
                    success.append(f"The import for item {url} finished successfully.")
        return Response({"success": success, "errors": errors})


class AboutView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "about.html"

    def get(self, request):
        return Response()
