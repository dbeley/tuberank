from django.contrib.auth.models import User
from django.db import models

from ratings.models.videos import Video


class VideoList(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=5000, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    videos = models.ManyToManyField(Video, through="VideoListItem")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"], name="unique_user_video_list_by_name"
            )
        ]


class VideoListItem(models.Model):
    video = models.ForeignKey("ratings.Video", on_delete=models.CASCADE)
    list = models.ForeignKey(
        "ratings.VideoList", related_name="items", on_delete=models.CASCADE
    )
    rank = models.PositiveIntegerField()
    description = models.TextField(max_length=5000, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["list", "video"],
                name="unique_video_in_list",
            ),
            models.UniqueConstraint(
                fields=["list", "rank"],
                name="unique_rank_in_list",
            ),
        ]


class VideoListRating(models.Model):
    list = models.ForeignKey(
        "ratings.VideoList", related_name="ratings", on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
