from ratings.models import Channel
from googleapiclient.discovery import build
import json
import os


YOUTUBE_DEVELOPER_KEY = os.environ["YOUTUBE_DEVELOPER_KEY"]


def _get_channel_information_from_id(channel_id: str):
    with build("youtube", "v3", developerKey=YOUTUBE_DEVELOPER_KEY) as service:
        response = json.dumps(
            service.channels().list(part="statistics", id=channel_id).execute()
        )
    return response
