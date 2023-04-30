import configparser
import logging
import isodate
import os
from dataclasses import dataclass
from datetime import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from ratings.models import Channel, ChannelSnapshot, Video, VideoSnapshot

logger = logging.getLogger(__name__)


class TooManyResultException(Exception):
    pass


class NoResultException(Exception):
    pass


def get_secret(BASE_DIR, config_file):
    try:
        CONFIG = configparser.RawConfigParser()
        CONFIG.read(os.path.join(BASE_DIR, config_file))
        return CONFIG["django"]["YOUTUBE_DEVELOPER_KEY"]
    except Exception as err:
        logger.warning("Error with the config file: %s", err)
        return os.environ.get("YOUTUBE_DEVELOPER_KEY", "")


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YOUTUBE_DEVELOPER_KEY = get_secret(BASE_DIR, "secret.ini")


@dataclass
class ChannelDataClass:
    title: str
    description: str
    date_creation: datetime
    custom_url: str
    yt_id: str
    count_subscribers: int
    count_views: int
    count_videos: int
    thumbnail_url: str


def _get_channel_response_from_id(channel_id: str):
    with build("youtube", "v3", developerKey=YOUTUBE_DEVELOPER_KEY) as service:
        try:
            response = (
                service.channels()
                .list(part="snippet,statistics", id=channel_id)
                .execute()
            )
        except HttpError:
            return None
        if response.get("pageInfo").get("totalResults") > 1:
            raise TooManyResultException()
        if response.get("pageInfo").get("totalResults") == 0:
            raise NoResultException()
    return response


def _get_channel_data_class_from_id(channel_id: str) -> ChannelDataClass:
    response = _get_channel_response_from_id(channel_id)
    data = response["items"][0]
    return ChannelDataClass(
        title=data["snippet"]["title"],
        description=data["snippet"]["description"],
        date_creation=data["snippet"]["publishedAt"],
        custom_url=data["snippet"].get("customUrl", ""),
        yt_id=data["id"],
        count_subscribers=data["statistics"]["subscriberCount"],
        count_views=data["statistics"]["viewCount"],
        count_videos=data["statistics"]["videoCount"],
        thumbnail_url=_get_thumbnail_data(data["snippet"]["thumbnails"]),
    )


def create_channel_snapshot(channel_id: str) -> None:
    """
    Will create a Channel Snapshot. If the Channel doesn't exist, it will create it.
    """
    data = _get_channel_data_class_from_id(channel_id)
    if not Channel.objects.filter(yt_id=channel_id).exists():
        logger.warning("Channel %s not found. Creating it.", channel_id)
        channel = Channel(yt_id=data.yt_id, date_creation=data.date_creation)
        channel.save()

    channel = Channel.objects.get(yt_id=channel_id)

    snapshot = ChannelSnapshot(
        name_en=data.title,
        channel=channel,
        count_subscribers=data.count_subscribers,
        count_views=data.count_views,
        count_videos=data.count_videos,
        custom_url=data.custom_url,
        description=data.description,
        thumbnail_url=data.thumbnail_url,
    )
    snapshot.save()


def _get_video_response_from_id(video_id: str):
    with build("youtube", "v3", developerKey=YOUTUBE_DEVELOPER_KEY) as service:
        try:
            response = (
                service.videos()
                .list(part="snippet,statistics,contentDetails", id=video_id)
                .execute()
            )
        except HttpError:
            return None
        if response.get("pageInfo").get("totalResults") > 1:
            raise TooManyResultException()
        if response.get("pageInfo").get("totalResults") == 0:
            raise NoResultException()
    return response


@dataclass
class VideoDataClass:
    title: str
    description: str
    date_publication: datetime
    channel_id: str
    yt_id: str
    count_views: int
    count_likes: int
    count_comments: int
    thumbnail_url: str
    category_id: int
    duration: int


def _parse_youtube_duration(duration: str) -> int:
    return isodate.parse_duration(duration).total_seconds()


def _get_video_data_class_from_id(video_id: str) -> VideoDataClass:
    response = _get_video_response_from_id(video_id)
    data = response["items"][0]
    return VideoDataClass(
        title=data["snippet"]["title"],
        yt_id=data["id"],
        channel_id=data["snippet"]["channelId"],
        date_publication=data["snippet"]["publishedAt"],
        count_views=data["statistics"].get("viewCount"),
        count_likes=data["statistics"].get("likeCount"),
        count_comments=data["statistics"].get("commentCount"),
        description=data["snippet"]["description"],
        thumbnail_url=_get_thumbnail_data(data["snippet"]["thumbnails"]),
        category_id=data["snippet"].get("categoryId"),
        duration=_parse_youtube_duration(data["contentDetails"].get("duration")),
    )


def _get_thumbnail_data(data: dict) -> str:
    if thumbnail := data.get("standard"):
        return thumbnail["url"]
    elif thumbnail := data.get("medium"):
        return thumbnail["url"]
    elif thumbnail := data.get("default"):
        return thumbnail["url"]
    elif thumbnail := data.get("high"):
        return thumbnail["url"]
    elif thumbnail := data.get("maxres"):
        return thumbnail["url"]
    return None


def create_video_snapshot_from_url(url: str) -> None:
    video_id = url.strip().split("https://www.youtube.com/watch?v=")[-1]
    logger.info("Creating video snapshot for video id %s", video_id)
    create_video_snapshot(video_id)


def create_video_snapshot(video_id: str) -> None:
    """
    Will create a Video Snapshot. If the associated Channel doesn't exist, it will create it.
    """
    data = _get_video_data_class_from_id(video_id)

    if not Channel.objects.filter(yt_id=data.channel_id).exists():
        logger.warning("Channel %s not found. Creating it.", data.channel_id)
        create_channel_snapshot(data.channel_id)
    channel = Channel.objects.get(yt_id=data.channel_id)

    if not Video.objects.filter(yt_id=video_id).exists():
        logger.warning("Video %s not found. Creating it.", video_id)
        video = Video(
            yt_id=data.yt_id, date_publication=data.date_publication, channel=channel
        )
        video.save()
    video = Video.objects.get(yt_id=video_id)

    snapshot = VideoSnapshot(
        title_en=data.title,
        video=video,
        count_views=data.count_views,
        count_likes=data.count_likes,
        count_comments=data.count_comments,
        description=data.description,
        thumbnail_url=data.thumbnail_url,
        category=data.category_id,
        duration=data.duration,
    )
    snapshot.save()
