from django.db.models import Count, QuerySet
from django.shortcuts import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings import enums
from ratings.models.tags import UserTag
from ratings.videos.serializers import SimpleVideoSerializer


def get_active_tags() -> QuerySet[UserTag]:
    return (
        UserTag.objects.annotate(num_videos=Count("video"))
        .filter(num_videos__gt=0, state=enums.TagState.VALIDATED)
        .all()
    )


class UserTagOverviewView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tags/tag_overview.html"

    def get(self, _, name):
        tag = get_object_or_404(UserTag, name=name)
        videos = tag.video_set.all()
        videos_data = SimpleVideoSerializer(videos, many=True).data
        return Response({"tag": tag, "videos": videos_data})


class TagsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tags/tags.html"

    def get(self, _):
        return Response({"tags": get_active_tags().order_by("-num_videos")})
