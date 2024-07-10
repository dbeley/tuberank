from django.contrib.auth.models import User
from rest_framework import serializers

from ratings.models import VideoRating, ChannelRating, VideoViewing, Channel


class UserSerializer(serializers.ModelSerializer):
    number_channels_ratings = serializers.SerializerMethodField()
    number_videos_ratings = serializers.SerializerMethodField()
    number_videos_viewed = serializers.SerializerMethodField()

    def get_number_channels_ratings(self, obj: User):
        return ChannelRating.objects.filter(user=obj).count()

    def get_number_videos_ratings(self, obj: User):
        return VideoRating.objects.filter(user=obj).count()

    def get_number_videos_viewed(self, obj: User):
        return VideoViewing.objects.filter(user=obj).count()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "number_videos_ratings",
            "number_videos_viewed",
            "number_channels_ratings",
        ]


class MostWatchedChannelSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    def get_count(self, obj: Channel):
        return obj.videos.count()

    def get_name(self, obj: Channel):
        return obj.last_snapshot.name_en

    def get_thumbnail_url(self, obj: Channel):
        return obj.last_snapshot.thumbnail_url

    class Meta:
        model = Channel
        fields = [
            "id",
            "name",
            "count",
            "thumbnail_url",
        ]
