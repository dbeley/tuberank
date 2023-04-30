from rest_framework import serializers

from ratings.channels.serializers import ChannelSerializer
from ratings.models.videos import Video, VideoSnapshot, VideoRating


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
        ]


class VideoRatingSerializer(serializers.ModelSerializer):
    date_publication = serializers.DateTimeField(read_only=True)
    video = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    rating = serializers.IntegerField()

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = VideoRating
        fields = [
            "rating",
            "video",
            "date_publication",
            "review_title",
            "review_body",
            "username",
        ]