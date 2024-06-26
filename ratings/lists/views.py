from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Count, QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from rest_framework.exceptions import PermissionDenied
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings.lists.serializers import VideoListSerializer
from ratings.models import Video
from ratings.models.lists import VideoList, VideoListItem


def _get_user_lists(user: User) -> QuerySet[VideoList]:
    return VideoList.objects.filter(user=user)


def _get_popular_lists() -> QuerySet[VideoList]:
    return VideoList.objects.annotate(num_ratings=Count("ratings")).order_by(
        "-num_ratings"
    )


class VideoListDetailsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "lists/list_details.html"

    def get(self, request, pk):
        video_list = get_object_or_404(VideoList, pk=pk)
        return Response(
            {
                "list": video_list,
            }
        )

    def post(self, request, pk):
        if not request.user.is_authenticated:
            raise PermissionDenied()
        video_list = get_object_or_404(VideoList, pk=pk, user=request.user)
        if "description" in request.data:
            video_list.description = request.data.get("description")
            video_list.save()
        else:
            for item in video_list.items.all():
                if request.data.get(f"description{item.rank}"):
                    item.description = request.data[f"description{item.rank}"]
                    item.save()
        return redirect("list_details", pk=pk)


class VideoListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "lists/lists.html"

    def get(self, request):
        user_lists = None
        if request.user.is_authenticated:
            user_lists = _get_user_lists(request.user)
        popular_lists = _get_popular_lists()[0:8]
        return Response({"user_lists": user_lists, "popular_lists": popular_lists})

    def post(self, request):
        if not request.user.is_authenticated:
            raise PermissionDenied()
        serializer = VideoListSerializer(data=request.data)
        if not serializer.is_valid():
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
        VideoList.objects.create(
            user=request.user,
            **serializer.validated_data,
        )
        user_lists = _get_user_lists(request.user)
        popular_lists = _get_popular_lists()[0:8]
        return Response({"user_lists": user_lists, "popular_lists": popular_lists})


class VideoListDeleteView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "lists/lists.html"

    def get(self, request, pk):
        if not request.user.is_authenticated:
            raise PermissionDenied()
        try:
            video_list = VideoList.objects.get(pk=pk, user=request.user)
        except VideoList.DoesNotExist:
            raise ValidationError("List not found")
        video_list.delete()
        return redirect("lists")


class VideoListDeleteItemView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "lists/list_details.html"

    def get(self, request, list_pk, video_pk):
        if not request.user.is_authenticated:
            raise PermissionDenied()
        video_list = get_object_or_404(VideoList, pk=list_pk, user=request.user)
        video = get_object_or_404(Video, pk=video_pk)
        video_list.videos.remove(video)
        return redirect("list_details", pk=list_pk)


class VideoListReorderView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "lists/list_details_sortable.html"

    def get(self, request, pk):
        if not request.user.is_authenticated:
            raise PermissionDenied()
        video_list = get_object_or_404(VideoList, pk=pk)
        return Response(
            {
                "list": video_list,
            }
        )

    def post(self, request, pk):
        data = dict(request.data.lists())
        parsed_data = [
            {"id": element.split(": ")[0], "order": element.split(": ")[1]}
            for element in data.get("item")
        ]
        items = []
        for new_rank, item in enumerate(parsed_data, 1):
            list_item = VideoListItem.objects.get(pk=item.get("id"))
            list_item.rank = new_rank
            items.append(list_item)
        with transaction.atomic():
            [item.save() for item in items]
        current_list = VideoList.objects.get(pk=pk)
        return Response(
            {"list": current_list, "sortable": True},
            template_name="lists/list_details_partial.html",
        )
