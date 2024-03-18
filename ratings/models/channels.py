from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg

from ratings import enums
from ratings.models.videos import Video


class Channel(models.Model):
    yt_id = models.CharField(max_length=24, unique=True)
    date_creation = models.DateTimeField("date of channel creation")
    description = models.TextField(max_length=5000, blank=True)
    tags = models.ManyToManyField("ratings.UserTag", blank=True)

    def __str__(self) -> str:
        return f"{self.pk} - {self.yt_id} - {self.date_creation}"

    @property
    def last_snapshot(self):
        return self.snapshots.last()

    @property
    def average_rating(self) -> float:
        return round(self.ratings.aggregate(avg=Avg("rating"))["avg"] or 0, 2)

    @property
    def indexed_videos_count(self) -> int:
        return Video.objects.filter(channel=self).count()

    @property
    def url(self) -> str:
        if last_snapshot := self.last_snapshot:
            if custom_url := last_snapshot.custom_url:
                return f"https://www.youtube.com/{custom_url}"
        return ""


class ChannelSnapshot(models.Model):
    name_en = models.CharField(max_length=50)
    channel = models.ForeignKey(
        "ratings.Channel", related_name="snapshots", on_delete=models.CASCADE
    )
    count_subscribers = models.IntegerField(default=0, blank=True, null=True)
    count_views = models.BigIntegerField(default=0, blank=True, null=True)
    count_videos = models.IntegerField(default=0, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    custom_url = models.CharField(max_length=24, blank=True)
    description = models.TextField(max_length=5000, blank=True)
    thumbnail_url = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.pk} - {self.name_en} - {self.date_creation}"


class ChannelRating(models.Model):
    rating = models.PositiveIntegerField(
        choices=enums.Rating.choices(),
    )
    user = models.ForeignKey(
        User, related_name="channel_ratings", on_delete=models.CASCADE
    )
    channel = models.ForeignKey(
        "ratings.Channel", related_name="ratings", on_delete=models.CASCADE
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    review_title = models.TextField(max_length=100, blank=True)
    review_body = models.TextField(max_length=5000, blank=True)

    def __str__(self) -> str:
        return (
            f"{self.pk} - {self.user.username} - {self.rating} - {self.channel.yt_id}"
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "channel"], name="unique_user_rating_channel"
            )
        ]
