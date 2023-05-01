from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Count, QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings.lists.serializers import VideoListSerializer
from ratings.models.lists import VideoList


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
        list = get_object_or_404(VideoList, pk=pk)
        return Response(
            {
                "list": list,
            }
        )


class VideoListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "lists/lists.html"

    def get(self, request):
        user_lists = _get_user_lists(request.user)
        popular_lists = _get_popular_lists()[0:8]
        return Response({"user_lists": user_lists, "popular_lists": popular_lists})

    def post(self, request):
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
        try:
            video_list = VideoList.objects.get(pk=pk, user=request.user)
        except VideoList.DoesNotExist:
            raise ValidationError("List not found")
        video_list.delete()
        user_lists = _get_user_lists(request.user)
        popular_lists = _get_popular_lists()[0:8]
        return Response({"user_lists": user_lists, "popular_lists": popular_lists})
