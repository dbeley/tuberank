from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Avg, Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings.models.videos import Video
from ratings.models.channels import Channel
from ratings.charts import charts
from ratings.videos.serializers import VideoSerializer
from ratings.channels.serializers import ChannelSerializer
from ratings.yt_import import (
    create_video_snapshot_from_url,
    TooManyResultException,
    NoResultException,
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
        if video_page_query_param := request.GET.get("page"):
            video_page = video_paginator.get_page(video_page_query_param)
            return Response(
                {
                    "videos": VideoSerializer(video_page, many=True).data,
                    "query": query,
                    "video_page": video_page,
                },
                template_name="search/video_results.html",
            )
        video_page = video_paginator.get_page(request.GET.get("page", 1))
        channel_queryset = Channel.objects.filter(
            Q(snapshots__name_en__icontains=query)
        ).distinct()
        channel_paginator = Paginator(channel_queryset, 4)
        if channel_page_query_param := request.GET.get("page_c"):
            channel_page = channel_paginator.get_page(channel_page_query_param)
            return Response(
                {
                    "channels": ChannelSerializer(channel_page, many=True).data,
                    "query": query,
                    "channel_page": channel_page,
                },
                template_name="search/channel_results.html",
            )
        channel_page = channel_paginator.get_page(request.GET.get("page_c", 1))
        print(channel_page)
        return Response(
            {
                "channels": ChannelSerializer(channel_page, many=True).data,
                "videos": VideoSerializer(video_page, many=True).data,
                "query": query,
                "channel_page": channel_page,
                "video_page": video_page,
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


class ImportVideoView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "import_video.html"

    def get(self, request):
        print(request.__dict__)
        return Response()

    def post(self, request):
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
                finally:
                    success.append(f"The import for item {url} finished successfully.")
        return Response({"success": success, "errors": errors})
