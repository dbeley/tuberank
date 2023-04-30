from django.shortcuts import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings.models.tags import UserTag


class UserTagOverviewView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tag_overview.html"

    def get(self, request, name):
        tag = get_object_or_404(UserTag, name=name)
        videos = tag.video_set.all()
        return Response({"tag": tag, "videos": videos})
