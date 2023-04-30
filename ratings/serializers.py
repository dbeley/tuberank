from django.contrib.auth.models import User
from rest_framework import serializers
from ratings.models import (
    Channel,
    ChannelSnapshot,
    ChannelRating,
    Video,
    VideoSnapshot,
    VideoRating,
    VideoViewing,
    UserTag,
)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")


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

    class Meta:
        model = ChannelRating
        fields = [
            "rating",
            "channel",
            "date_publication",
            "review_title",
            "review_body",
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


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    video_ratings_count = serializers.SerializerMethodField()
    channel_ratings_count = serializers.SerializerMethodField()
    video_ratings = VideoRatingSerializer(
        source="video_ratings", many=True, read_only=True
    )
    channel_ratings = ChannelRatingSerializer(
        source="channel_ratings", many=True, read_only=True
    )

    def get_video_ratings_count(self, obj: User) -> int:
        return obj.video_ratings.count()

    def get_channel_ratings_count(self, obj: User) -> int:
        return obj.channel_ratings.count()

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "video_ratings_count",
            "channel_ratings_count",
            "video_ratings",
            "channel_ratings",
        )

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data["password"])
            user.save()
        except KeyError:
            pass
        return user


class UserTagSerializer(serializers.ModelSerializer):
    video_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)

    def validate_name(self, value: str) -> str:
        return value.replace(" ", "-").lower()

    class Meta:
        model = UserTag
        fields = ["name", "video_id"]
