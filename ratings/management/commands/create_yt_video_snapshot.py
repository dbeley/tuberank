from django.core.management.base import BaseCommand
from ratings import yt_import


class Command(BaseCommand):
    help = "Import youtube video"

    def add_arguments(self, parser):
        parser.add_argument("-u", "--urls", type=str, help="URLs separated by comma")

    def handle(self, *args, **kwargs):
        urls = kwargs["urls"]
        if not all(["youtube" in url for url in urls.split(",")]):
            raise ValueError("Invalid urls")

        for url in urls.split(","):
            print("Importing %s", url)
            yt_import.create_video_snapshot_from_url(url)
