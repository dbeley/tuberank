from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers

from ratings.channels.serializers import ChannelSerializer
from ratings.models.videos import Video, VideoRating, VideoSnapshot
from ratings.serializers import CustomRatingField


class VideoSerializer(serializers.ModelSerializer):
    last_snapshot = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    ratings_count = serializers.SerializerMethodField()
    channel = ChannelSerializer(read_only=True)
    date_publication = serializers.SerializerMethodField()

    def get_last_snapshot(self, obj: Video) -> dict[str, str]:
        return VideoSnapshotSerializer(obj.last_snapshot).data

    def get_title(self, obj: Video) -> str:
        last_snapshot = obj.last_snapshot
        return last_snapshot.title_en

    def get_ratings_count(self, obj: Video) -> int:
        return obj.ratings.count()

    def get_date_publication(self, obj: Video) -> str:
        return naturaltime(obj.date_publication)

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
    class Meta:
        model = VideoSnapshot
        fields = [
            "title_en",
            "count_views",
            "count_likes",
            "count_comments",
            "date_creation",
            "description",
            "duration",
            "thumbnail_url",
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
