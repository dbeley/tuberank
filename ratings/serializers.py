from django.contrib.auth.models import User
from rest_framework import serializers
from ratings.models import (
    Channel,
    ChannelSnapshot,
    ChannelRating,
    Video,
    VideoSnapshot,
    VideoRating,
)
from django.db.models import Avg


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class VideoSerializer(serializers.ModelSerializer):
    last_snapshot = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    def get_last_snapshot(self, obj):
        last_snapshot = obj.snapshots.last()
        return VideoSnapshotSerializer(last_snapshot).data

    def get_title(self, obj):
        last_snapshot = obj.snapshots.last()
        return last_snapshot.title_en

    def get_average_rating(self, obj):
        return obj.ratings.aggregate(avg=Avg("rating"))["avg"]

    class Meta:
        model = Video
        fields = [
            "pk",
            "yt_id",
            "date_publication",
            "title",
            "last_snapshot",
            "average_rating",
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

    class Meta:
        model = VideoRating
        fields = [
            "rating",
            "video",
            "date_publication",
            "review_title",
            "review_body",
        ]


class ChannelSerializer(serializers.ModelSerializer):
    last_snapshot = serializers.SerializerMethodField()
    videos = VideoSerializer(many=True, read_only=True)

    def get_last_snapshot(self, obj):
        last_snapshot = obj.snapshots.last()
        return ChannelSnapshotSerializer(last_snapshot).data

    class Meta:
        model = Channel
        fields = ["pk", "yt_id", "date_creation", "last_snapshot", "videos"]


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
