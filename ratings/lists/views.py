from django.shortcuts import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings.models.lists import VideoList


class VideoListDetailsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "list_details.html"

    def get(self, request, pk):
        list = get_object_or_404(VideoList, pk=pk)
        return Response(
            {
                "list": list,
            }
        )
