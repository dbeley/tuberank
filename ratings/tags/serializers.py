from rest_framework import serializers

from ratings.models.tags import UserTag


class UserTagSerializer(serializers.ModelSerializer):
    video_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=25)

    class Meta:
        model = UserTag
        fields = ["name", "video_id"]
