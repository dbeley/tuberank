from django.core.paginator import Paginator
from django.db.models import Avg, Count, Max, F
from django.http import HttpResponseRedirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings.models import UserTag
from ratings.models.videos import Video
from ratings.tags.views import get_active_tags


class ChartsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "charts.html"

    def get(self, request):
        tags = get_active_tags().order_by("name")
        videos = Video.objects.annotate(
            num_ratings=Count("ratings"),
            avg_rating=Avg(F("ratings__rating")),
            count_views=Max(F("snapshots__count_views")),
        )
        if sort_method := request.GET.get("sort_by"):
            if sort_method not in [
                "newest",
                "oldest",
                "views_count",
                "views_count_desc",
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
            elif sort_method == "views_count_desc":
                videos = videos.order_by("count_views")
            elif sort_method == "ratings_count":
                videos = videos.order_by("-num_ratings")
            elif sort_method == "rating":
                videos = videos.filter(avg_rating__isnull=False).order_by("-avg_rating")
        else:
            # default
            videos = videos.filter(avg_rating__isnull=False).order_by("-avg_rating")

        if selected_tag := request.GET.get("tag"):
            tag = UserTag.objects.get(name=selected_tag)
            videos = videos.filter(tags__in=[tag])

        paginator = Paginator(videos, 12)
        videos = paginator.get_page(request.GET.get("page", 1))
        if request.META.get("HTTP_HX_REQUEST"):
            return Response(
                {
                    "videos": videos,
                },
                template_name="charts_partial.html",
            )
        return Response(
            {
                "videos": videos,
                "tags": tags,
                "selected_sort_method": sort_method,
                "selected_tag": selected_tag,
            }
        )
