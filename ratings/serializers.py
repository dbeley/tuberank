from django.contrib.auth.models import User
from rest_framework import serializers
from ratings.models import Channel, ChannelSnapshot


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class ChannelSerializer(serializers.HyperlinkedModelSerializer):
    last_snapshot = serializers.SerializerMethodField()

    def get_last_snapshot(self, obj):
        last_snapshot = obj.snapshots.last()
        return ChannelSnapshotSerializer(last_snapshot).data

    class Meta:
        model = Channel
        fields = ["yt_id", "date_creation", "last_snapshot"]


class ChannelSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelSnapshot
        fields = [
            "count_subscribers",
            "count_views",
            "count_videos",
            "date_creation",
            "custom_url",
            "description",
            "thumbnail_url",
        ]
