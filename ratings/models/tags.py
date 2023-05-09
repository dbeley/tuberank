from django.contrib.auth.models import User
from django.db import models

from ratings import enums


class UserTag(models.Model):
    name = models.CharField(max_length=25, unique=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_creation = models.DateTimeField(auto_now_add=True)
    state = models.PositiveIntegerField(choices=enums.TagState.choices())

    def __str__(self):
        return f"{self.pk} - {self.name} - {self.user} - {self.state}"


class UserTagVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(
        "ratings.UserTag", related_name="votes", on_delete=models.CASCADE
    )
    vote = models.IntegerField(choices=enums.TagVote.choices())
    video = models.ForeignKey("ratings.Video", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "tag", "video"], name="unique_vote_by_tag_user_video"
            )
        ]
