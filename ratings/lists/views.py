from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings.lists.serializers import VideoListSerializer
from ratings.models import VideoList

from ratings.models.lists import VideoList


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
        user_lists = VideoList.objects.filter(user=request.user)
        popular_lists = VideoList.objects.annotate(
            num_ratings=Count("ratings")
        ).order_by("-num_ratings")[0:8]
        return Response({"user_lists": user_lists, "popular_lists": popular_lists})

    def post(self, request):
        serializer = VideoListSerializer(data=request.data)
        if not serializer.is_valid():
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
        VideoList.objects.create(
            user=request.user,
            **serializer.validated_data,
        )
        user_lists = VideoList.objects.filter(user=request.user)
        popular_lists = VideoList.objects.annotate(
            num_ratings=Count("ratings")
        ).order_by("-num_ratings")[0:8]
        return Response({"user_lists": user_lists, "popular_lists": popular_lists})
