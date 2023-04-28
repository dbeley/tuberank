from django.core.management.base import BaseCommand
from ratings import yt_import
import logging
from ratings.yt_import import NoResultException

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import youtube video"

    def add_arguments(self, parser):
        parser.add_argument("-u", "--urls", type=str, help="URLs separated by comma")
        parser.add_argument(
            "-f",
            "--file",
            type=str,
            help="File containing either youtube urls or youtube ids (one per line). Lines starting with # are ignored.",
        )

    def handle(self, *args, **kwargs):
        urls = kwargs["urls"]
        filename = kwargs["file"]
        if not urls and not filename:
            raise ValueError("Please specify youtube urls (--urls) or a file (--file).")

        if urls:
            if not all(["youtube" in url for url in urls.split(",")]):
                raise ValueError("Invalid urls")
            urls = urls.split(",")

        if filename:
            with open(filename, "r") as f:
                urls = [line for line in f.readlines() if not line.startswith("#")]

        total_urls = len(urls)
        for index, url in enumerate(urls, 1):
            logger.warning("[%s/%s] Importing %s", index, total_urls, url)
            try:
                yt_import.create_video_snapshot_from_url(url)
            except NoResultException:
                logger.warning("No result found for %s. Skipping.", url)
