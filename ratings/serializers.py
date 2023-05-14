from django.contrib.auth.models import User
from rest_framework import serializers


class CustomRatingField(serializers.CharField):
    def to_representation(self, value: int) -> str:
        return str(value / 2)

    def to_internal_value(self, data: str) -> int:
        return int(float(data) * 2)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
