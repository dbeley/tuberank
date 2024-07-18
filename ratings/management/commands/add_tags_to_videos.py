import logging

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models import Q

from ratings.models import Video
from ratings.videos.views import _add_video_to_tag

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Apply tags to several videos"

    def add_arguments(self, parser):
        parser.add_argument(
            "-t", "--tags", type=str, help="Tags to apply, separated by comma."
        )
        parser.add_argument(
            "-s",
            "--search_query",
            type=str,
            help=("Search query to filter videos."),
        )

    def handle(self, *args, **kwargs):
        tags = kwargs["tags"]
        search_query = kwargs["search_query"]

        video_queryset = Video.objects.filter(
            Q(snapshots__title_en__icontains=search_query)
            | Q(yt_id__icontains=search_query)
        ).distinct()

        admin_user = (
            User.objects.filter(Q(is_staff=True) | Q(is_superuser=True))
            .order_by("id")
            .first()
        )

        for tag_name in tags.split(","):
            for video in video_queryset:
                _add_video_to_tag(tag_name, video, admin_user)
