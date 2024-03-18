from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg

from ratings import enums


class Video(models.Model):
    yt_id = models.CharField(max_length=11, unique=True)
    channel = models.ForeignKey(
        "ratings.Channel", related_name="videos", on_delete=models.CASCADE
    )
    date_publication = models.DateTimeField("date of video publication")
    tags = models.ManyToManyField("ratings.UserTag", blank=True)

    def __str__(self) -> str:
        return f"{self.pk} - {self.yt_id} - {self.date_publication}"

    @property
    def last_snapshot(self):
        return self.snapshots.last()

    @property
    def average_rating(self) -> int:
        return round(self.ratings.aggregate(avg=Avg("rating"))["avg"] or 0, 2)

    @property
    def url(self) -> str:
        return f"https://www.youtube.com/watch?v={self.yt_id}"


class VideoSnapshot(models.Model):
    title_en = models.CharField(max_length=100)
    video = models.ForeignKey(
        "ratings.Video", related_name="snapshots", on_delete=models.CASCADE
    )
    count_views = models.BigIntegerField(default=0, blank=True, null=True)
    count_likes = models.IntegerField(default=0, blank=True, null=True)
    count_comments = models.IntegerField(default=0, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=5000, blank=True)
    thumbnail_url = models.CharField(max_length=200)
    category = models.PositiveIntegerField(
        choices=enums.Category.choices(), blank=True, null=True
    )
    duration = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.pk} - {self.title_en} - {self.date_creation}"


class VideoRating(models.Model):
    rating = models.PositiveIntegerField(
        choices=enums.Rating.choices(),
    )
    user = models.ForeignKey(
        User, related_name="video_ratings", on_delete=models.CASCADE
    )
    video = models.ForeignKey(
        "ratings.Video", related_name="ratings", on_delete=models.CASCADE
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    review_title = models.TextField(max_length=100, blank=True)
    review_body = models.TextField(max_length=5000, blank=True)

    def __str__(self) -> str:
        return f"{self.pk} - {self.user.username} - {self.rating} - {self.video.yt_id}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "video"], name="unique_user_rating_video"
            )
        ]


class VideoViewing(models.Model):
    video = models.ForeignKey(
        "ratings.Video", related_name="viewings", on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, related_name="viewings", on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    state = models.PositiveIntegerField(
        choices=enums.ViewingState.choices(),
    )

    def __str__(self) -> str:
        return f"{self.pk} - {self.user.pk} - {self.date_creation}"
