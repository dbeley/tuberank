from rest_framework import serializers

from ratings.models.lists import VideoList


class VideoListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=5000, required=False)

    class Meta:
        model = VideoList
        fields = ["name", "description"]
