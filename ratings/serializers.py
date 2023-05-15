from django.contrib.auth.models import User
from rest_framework import serializers

from core.utils import get_human_readable_duration
from ratings.models import VideoViewing, VideoSnapshot
from django.template.defaultfilters import date as _date


class CustomRatingField(serializers.CharField):
    def to_representation(self, value: int) -> str:
        return str(value / 2)

    def to_internal_value(self, data: str) -> int:
        return int(float(data) * 2)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")


class PartialViewingVideoSnapshotSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()

    def get_duration(self, obj):
        return get_human_readable_duration(obj.duration)

    class Meta:
        model = VideoSnapshot
        fields = ("thumbnail_url", "title_en", "duration")


class ViewingSerializer(serializers.ModelSerializer):
    video_last_snapshot = serializers.SerializerMethodField()
    channel_name = serializers.SerializerMethodField()
    date_creation = serializers.SerializerMethodField()

    def get_video_last_snapshot(self, obj: VideoViewing):
        return PartialViewingVideoSnapshotSerializer(obj.video.last_snapshot).data

    def get_channel_name(self, obj: VideoViewing) -> str:
        return obj.video.channel.last_snapshot.name_en

    def get_date_creation(self, obj: VideoViewing) -> str:
        return _date(obj.date_creation, "j M Y, G:i")

    class Meta:
        model = VideoViewing
        fields = ("date_creation", "video_id", "channel_name", "video_last_snapshot")
