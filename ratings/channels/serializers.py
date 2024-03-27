from rest_framework import serializers

from ratings.models.channels import Channel, ChannelRating, ChannelSnapshot
from ratings.serializers import CustomRatingField


class ChannelSerializer(serializers.ModelSerializer):
    last_snapshot = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    ratings_count = serializers.SerializerMethodField()
    indexed_videos_count = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    def get_last_snapshot(self, obj: Channel) -> dict[str, str]:
        return ChannelSnapshotSerializer(obj.last_snapshot).data

    def get_average_rating(self, obj: Channel) -> float:
        return obj.average_rating

    def get_ratings_count(self, obj: Channel) -> int:
        return obj.ratings.count()

    def get_indexed_videos_count(self, obj):
        return obj.indexed_videos_count

    def get_url(self, obj: Channel) -> str:
        return obj.url

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
            "url",
        ]


class ChannelSerializerWithRatings(ChannelSerializer):
    ratings = serializers.SerializerMethodField()

    def get_ratings(self, obj: Channel):
        return ChannelRatingSerializer(obj.ratings, many=True).data

    class Meta(ChannelSerializer.Meta):
        model = Channel
        fields = ChannelSerializer.Meta.fields + ["ratings"]


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
