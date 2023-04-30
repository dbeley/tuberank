from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponseRedirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings.models.videos import Video


class ChartsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "charts.html"

    def get(self, request):
        videos = Video.objects.annotate(num_ratings=Count("ratings")).all()
        sort_method = request.GET.get("sort_by")
        if sort_method:
            if sort_method not in [
                "newest",
                "oldest",
                "views_count",
                "ratings_count",
                "rating",
            ]:
                return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
            if sort_method == "newest":
                videos = videos.order_by("date_publication")
            if sort_method == "oldest":
                videos = videos.order_by("-date_publication")
            # if sort_method == "views_count":
            #     videos = videos.order_by("last_snapshot__count_views")
            if sort_method == "ratings_count":
                videos = videos.order_by("-num_ratings")
            # if sort_method == "rating":
            #     videos = videos.order_by("average_rating")

        paginator = Paginator(videos, 8)
        page = paginator.get_page(request.GET.get("page", 1))
        return Response({"videos": page, "page": page})
