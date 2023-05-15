from rest_framework import serializers

from core.utils import get_human_readable_duration
from ratings.channels.serializers import ChannelSerializer, SimpleChannelSerializer
from ratings.models.videos import Video, VideoRating, VideoSnapshot
from ratings.serializers import CustomRatingField
from django.template.defaultfilters import date as _date


class SimpleVideoSerializer(serializers.ModelSerializer):
    last_snapshot = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    ratings_count = serializers.SerializerMethodField()
    date_publication = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    channel = serializers.SerializerMethodField()

    def get_last_snapshot(self, obj: Video) -> dict[str, str]:
        return VideoSnapshotSerializer(obj.last_snapshot).data

    def get_title(self, obj: Video) -> str:
        last_snapshot = obj.last_snapshot
        return last_snapshot.title_en

    def get_average_rating(self, obj: Video) -> float:
        return round(obj.average_rating / 2, 2)

    def get_ratings_count(self, obj: Video) -> int:
        return obj.ratings.count() or 0

    def get_date_publication(self, obj: Video) -> str:
        return _date(obj.date_publication)

    def get_url(self, obj: Video) -> str:
        return obj.url

    def get_channel(self, obj: Video):
        return SimpleChannelSerializer(obj.channel).data

    class Meta:
        model = Video
        fields = [
            "id",
            "yt_id",
            "date_publication",
            "title",
            "last_snapshot",
            "average_rating",
            "ratings_count",
            "url",
            "channel",
        ]


class VideoSerializer(serializers.ModelSerializer):
    last_snapshot = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    ratings_count = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    channel = ChannelSerializer(read_only=True)

    def get_last_snapshot(self, obj: Video) -> dict[str, str]:
        return VideoSnapshotSerializer(obj.last_snapshot).data

    def get_title(self, obj: Video) -> str:
        last_snapshot = obj.last_snapshot
        return last_snapshot.title_en

    def get_average_rating(self, obj: Video) -> float:
        return obj.average_rating

    def get_ratings_count(self, obj: Video) -> int:
        return obj.ratings.count()

    def get_url(self, obj: Video) -> str:
        return obj.url

    class Meta:
        model = Video
        fields = [
            "id",
            "yt_id",
            "date_publication",
            "title",
            "last_snapshot",
            "average_rating",
            "ratings_count",
            "url",
            "channel",
        ]


class VideoSnapshotSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()

    def get_duration(self, obj):
        return get_human_readable_duration(obj.duration)

    class Meta:
        model = VideoSnapshot
        fields = [
            "title_en",
            "count_views",
            "count_likes",
            "count_comments",
            "date_creation",
            "description",
            "thumbnail_url",
            "duration",
        ]


class VideoRatingSerializer(serializers.ModelSerializer):
    date_creation = serializers.DateTimeField(read_only=True)
    video = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    rating = CustomRatingField()

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = VideoRating
        fields = [
            "rating",
            "video",
            "date_creation",
            "review_title",
            "review_body",
            "username",
        ]
