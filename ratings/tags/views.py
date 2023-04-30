from django.db.models import QuerySet, Count
from django.shortcuts import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings import enums
from ratings.models.tags import UserTag


def _get_validated_tags() -> QuerySet[UserTag]:
    return UserTag.objects.filter(state=enums.TagState.VALIDATED).all()


class UserTagOverviewView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tags/tag_overview.html"

    def get(self, request, name):
        tag = get_object_or_404(UserTag, name=name)
        videos = tag.video_set.all()
        return Response({"tag": tag, "videos": videos})


class TagsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tags/tags.html"

    def get(self, request):
        tags = (
            _get_validated_tags()
            .annotate(num_videos=Count("video"))
            .order_by("-num_videos")
        )
        return Response({"tags": tags})