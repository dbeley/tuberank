from django.core.paginator import Paginator
from django.db.models import Avg, Count, Max, F
from django.http import HttpResponseRedirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings import enums
from ratings.models import UserTag
from ratings.models.videos import Video
from ratings.tags.serializers import SimpleUserTagSerializer
from ratings.tags.views import get_active_tags
from ratings.videos.serializers import SimpleVideoSerializer


class ChartsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "charts.html"

    def get(self, request):
        tags_data = SimpleUserTagSerializer(
            get_active_tags().order_by("name"), many=True
        ).data
        videos = Video.objects.annotate(
            num_ratings=Count("ratings"),
            avg_rating=Avg(F("ratings__rating")),
            count_views=Max(F("snapshots__count_views")),
        )
        if sort_method := request.GET.get("sort_by"):
            if sort_method not in enums.SortingChoices.choices():
                return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
            elif sort_method == enums.SortingChoices.NEWEST.value:
                videos = videos.order_by("-date_publication")
            elif sort_method == enums.SortingChoices.OLDEST.value:
                videos = videos.order_by("date_publication")
            elif sort_method == enums.SortingChoices.MOST_VIEWED.value:
                videos = videos.order_by("-count_views")
            elif sort_method == enums.SortingChoices.LEAST_VIEWED.value:
                videos = videos.order_by("count_views")
            elif sort_method == enums.SortingChoices.MOST_RATED.value:
                videos = videos.order_by("-num_ratings")
            elif sort_method == enums.SortingChoices.BEST_RATED.value:
                videos = videos.filter(avg_rating__isnull=False).order_by("-avg_rating")
            else:
                # default sort
                videos = videos.filter(avg_rating__isnull=False).order_by("-avg_rating")
        else:
            # default
            videos = videos.filter(avg_rating__isnull=False).order_by("-avg_rating")

        if selected_tag := request.GET.get("tag"):
            tag = UserTag.objects.get(name=selected_tag)
            videos = videos.filter(tags__in=[tag])

        paginator = Paginator(videos, 12)
        page = paginator.get_page(request.GET.get("page", 1))
        videos_data = SimpleVideoSerializer(page, many=True).data
        if request.META.get("HTTP_HX_REQUEST"):
            return Response(
                {
                    "videos": videos_data,
                    "page": page,
                },
                template_name="charts_partial.html",
            )
        return Response(
            {
                "videos": videos_data,
                "page": page,
                "tags": tags_data,
                "selected_sort_method": sort_method,
                "selected_tag": selected_tag,
            }
        )
