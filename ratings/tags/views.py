from django.db.models import Count, QuerySet, Avg
from django.shortcuts import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings import enums
from ratings.models.tags import UserTag


def get_active_tags() -> QuerySet[UserTag]:
    return (
        UserTag.objects.annotate(num_videos=Count("video"))
        .filter(num_videos__gt=0, state=enums.TagState.VALIDATED)
        .all()
    )


class UserTagOverviewView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tags/tag_overview.html"

    def get(self, request, name):
        tag = get_object_or_404(UserTag, name=name)
        videos = tag.video_set.annotate(
            avg_rating=Avg("ratings__rating"), num_ratings=Count("ratings")
        )
        best_videos = videos.filter(avg_rating__isnull=False).order_by("-avg_rating")[
            0:8
        ]
        popular_videos = videos.order_by("-num_ratings")[0:4]
        return Response(
            {
                "tag": tag,
                "videos": videos.all(),
                "best_videos": best_videos,
                "popular_videos": popular_videos,
            }
        )


class TagsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tags/tags.html"

    def get(self, request):
        return Response({"tags": get_active_tags().order_by("-num_videos")})
