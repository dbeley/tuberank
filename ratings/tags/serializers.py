from rest_framework import serializers

from ratings.models.tags import UserTag


class UserTagSerializer(serializers.ModelSerializer):
    video_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)

    def validate_name(self, value: str) -> str:
        return value.replace(" ", "-").lower()

    class Meta:
        model = UserTag
        fields = ["name", "video_id"]
