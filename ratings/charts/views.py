from django.core.paginator import Paginator
from django.db.models import Count, Avg, Max
from django.http import HttpResponseRedirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings.models import UserTag
from ratings.models.videos import Video
from ratings.tags.views import _get_validated_tags


class ChartsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "charts.html"

    def get(self, request):
        tags = _get_validated_tags().order_by("name")
        videos = Video.objects.annotate(
            num_ratings=Count("ratings"),
            avg_rating=Avg("ratings__rating"),
            count_views=Max("snapshots__count_views"),
        ).order_by("-num_ratings")
        if sort_method := request.GET.get("sort_by"):
            if sort_method not in [
                "newest",
                "oldest",
                "views_count",
                "ratings_count",
                "rating",
            ]:
                return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
            elif sort_method == "newest":
                videos = videos.order_by("-date_publication")
            elif sort_method == "oldest":
                videos = videos.order_by("date_publication")
            elif sort_method == "views_count":
                videos = videos.order_by("-count_views")
            elif sort_method == "ratings_count":
                # default sorting mechanism
                # videos = videos.order_by("-num_ratings")
                pass
            elif sort_method == "rating":
                videos = videos.order_by("-avg_rating")
        if selected_tag := request.GET.get("tag"):
            tag = UserTag.objects.get(name=selected_tag)
            videos = videos.filter(tags__in=[tag])

        paginator = Paginator(videos, 12)
        page = paginator.get_page(request.GET.get("page", 1))
        return Response(
            {
                "videos": page,
                "page": page,
                "tags": tags,
                "selected_sort_method": sort_method,
                "selected_tag": selected_tag,
            }
        )
