from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models import Avg
from ratings import enums


class Channel(models.Model):
    yt_id = models.CharField(max_length=24, unique=True)
    date_creation = models.DateTimeField("date of channel creation")
    description = models.TextField(max_length=5000, blank=True)

    def __str__(self):
        return f"{self.pk} - {self.yt_id} - {self.date_creation}"

    @property
    def last_snapshot(self):
        return self.snapshots.last()

    @property
    def average_rating(self):
        return round(self.ratings.aggregate(avg=Avg("rating"))["avg"] or 0, 2)

    @property
    def indexed_videos_count(self):
        return Video.objects.filter(channel=self).count()


class Video(models.Model):
    yt_id = models.CharField(max_length=11, unique=True)
    channel = models.ForeignKey(
        Channel, related_name="videos", on_delete=models.CASCADE
    )
    date_publication = models.DateTimeField("date of video publication")

    def __str__(self):
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


class ChannelSnapshot(models.Model):
    name_en = models.CharField(max_length=20)
    channel = models.ForeignKey(
        Channel, related_name="snapshots", on_delete=models.CASCADE
    )
    count_subscribers = models.IntegerField(default=0, blank=True, null=True)
    count_views = models.IntegerField(default=0, blank=True, null=True)
    count_videos = models.IntegerField(default=0, blank=True, null=True)
    date_creation = models.DateTimeField("date of snapshot creation")
    custom_url = models.CharField(max_length=24, blank=True)
    description = models.TextField(max_length=5000, blank=True)
    thumbnail_url = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.pk} - {self.name_en} - {self.date_creation}"


class VideoSnapshot(models.Model):
    title_en = models.CharField(max_length=100)
    video = models.ForeignKey(Video, related_name="snapshots", on_delete=models.CASCADE)
    count_views = models.IntegerField(default=0, blank=True, null=True)
    count_likes = models.IntegerField(default=0, blank=True, null=True)
    count_comments = models.IntegerField(default=0, blank=True, null=True)
    date_creation = models.DateTimeField("date of snapshot creation")
    description = models.TextField(max_length=5000, blank=True)
    thumbnail_url = models.CharField(max_length=100)
    category = models.PositiveIntegerField(
        choices=enums.Category.choices(), blank=True, null=True
    )
    duration = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.pk} - {self.title_en} - {self.date_creation}"


class ChannelRating(models.Model):
    rating = models.PositiveIntegerField(
        choices=enums.Rating.choices(),
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    user = models.ForeignKey(
        User, related_name="channel_ratings", on_delete=models.CASCADE
    )
    channel = models.ForeignKey(
        Channel, related_name="ratings", on_delete=models.CASCADE
    )
    date_publication = models.DateTimeField("date of rating publication")
    review_title = models.TextField(max_length=100, blank=True)
    review_body = models.TextField(max_length=5000, blank=True)

    def __str__(self):
        return (
            f"{self.pk} - {self.user} - {self.channel.yt_id} - {self.date_publication}"
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "channel"], name="unique_user_rating_channel"
            )
        ]


class VideoRating(models.Model):
    rating = models.PositiveIntegerField(
        choices=enums.Rating.choices(),
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    user = models.ForeignKey(
        User, related_name="video_ratings", on_delete=models.CASCADE
    )
    video = models.ForeignKey(Video, related_name="ratings", on_delete=models.CASCADE)
    date_publication = models.DateTimeField("date of rating publication")
    review_title = models.TextField(max_length=100, blank=True)
    review_body = models.TextField(max_length=5000, blank=True)

    def __str__(self):
        return f"{self.pk} - {self.user} - {self.video.yt_id} - {self.date_publication}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "video"], name="unique_user_rating_video"
            )
        ]


class VideoViewing(models.Model):
    video = models.ForeignKey(
        Video, related_name="viewings", on_delete=models.DO_NOTHING
    )
    user = models.ForeignKey(User, related_name="viewings", on_delete=models.CASCADE)
    date_creation = models.DateTimeField("date of video viewing creation")
    state = models.PositiveIntegerField(
        choices=enums.ViewingState.choices(),
    )

    def __str__(self):
        return f"{self.pk} - {self.user} - {self.video.yt_id} - {self.date_creation}"
