from django.db import models
from django.contrib.auth.models import User


class Channel(models.Model):
    name_en = models.CharField(max_length=20)
    yt_id = models.CharField(max_length=24)
    date_creation = models.DateTimeField("date of channel creation")


class Video(models.Model):
    yt_id = models.CharField(max_length=11)
    date_publication = models.DateTimeField("date of video publication")
    title_en = models.CharField(max_length=100)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)


class ChannelSnapshot(models.Model):
    count_subscribers = models.IntegerField(default=0)
    count_views = models.IntegerField(default=0)
    date_creation = models.DateTimeField("date of snapshot creation")
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)


class VideoSnapshot(models.Model):
    count_views = models.IntegerField(default=0)
    date_creation = models.DateTimeField("date of snapshot creation")
    video = models.ForeignKey(Video, on_delete=models.CASCADE)


class ChannelRating(models.Model):
    rating = models.IntegerField(min_value=0, max_value=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_publication = models.DateTimeField("date of rating publication")
    review_title = models.TextField(max_length=100, blank=True)
    review_body = models.TextField(max_length=5000, blank=True)


class VideoRating(models.Model):
    rating = models.IntegerField(min_value=0, max_value=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_publication = models.DateTimeField("date of rating publication")
    review_title = models.TextField(max_length=100, blank=True)
    review_body = models.TextField(max_length=5000, blank=True)
