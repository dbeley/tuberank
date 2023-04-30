from django.contrib.auth.models import User
from django.db import models

from ratings import enums


class UserTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_creation = models.DateTimeField(auto_now_add=True)
    state = models.PositiveIntegerField(choices=enums.TagState.choices())

    def __str__(self):
        return f"{self.pk} - {self.name} - {self.user} - {self.state}"
