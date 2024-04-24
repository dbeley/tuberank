from django.contrib.auth.models import User
from rest_framework import serializers

from ratings.models import VideoRating, ChannelRating, VideoViewing


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
