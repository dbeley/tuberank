from rest_framework import serializers

from ratings.models.channels import Channel, ChannelRating, ChannelSnapshot
from ratings.serializers import CustomRatingField


class SimpleChannelSerializer(serializers.ModelSerializer):
    last_snapshot = serializers.SerializerMethodField()

    def get_last_snapshot(self, obj: Channel) -> dict[str, str]:
        return ChannelSnapshotSerializer(obj.last_snapshot).data

    class Meta:
        model = Channel
        fields = [
            "id",
            "yt_id",
            "date_creation",
            "description",
            "last_snapshot",
        ]


class ChannelSerializer(serializers.ModelSerializer):
    last_snapshot = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    ratings_count = serializers.SerializerMethodField()
    indexed_videos_count = serializers.SerializerMethodField()

    def get_last_snapshot(self, obj: Channel) -> dict[str, str]:
        return ChannelSnapshotSerializer(obj.last_snapshot).data

    def get_average_rating(self, obj: Channel) -> float:
        return obj.average_rating

    def get_ratings_count(self, obj: Channel) -> int:
        return obj.ratings.count()

    def get_indexed_videos_count(self, obj):
        return obj.indexed_videos_count

    class Meta:
        model = Channel
        fields = [
            "id",
            "yt_id",
            "date_creation",
            "description",
            "last_snapshot",
            "average_rating",
            "ratings_count",
            "indexed_videos_count",
        ]


class ChannelSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelSnapshot
        fields = [
            "name_en",
            "count_subscribers",
            "count_views",
            "count_videos",
            "date_creation",
            "custom_url",
            "description",
            "thumbnail_url",
        ]


class ChannelRatingSerializer(serializers.ModelSerializer):
    date_publication = serializers.DateTimeField(read_only=True)
    channel = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    rating = CustomRatingField()

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = ChannelRating
        fields = [
            "rating",
            "channel",
            "date_publication",
            "review_title",
            "review_body",
            "username",
        ]
