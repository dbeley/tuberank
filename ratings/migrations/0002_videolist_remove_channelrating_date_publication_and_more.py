# Generated by Django 4.2 on 2023-04-30 11:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("ratings", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="VideoList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True, max_length=5000)),
                ("date_creation", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="channelrating",
            name="date_publication",
        ),
        migrations.RemoveField(
            model_name="videorating",
            name="date_publication",
        ),
        migrations.AddField(
            model_name="channelrating",
            name="date_creation",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="videorating",
            name="date_creation",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="channelrating",
            name="rating",
            field=models.PositiveIntegerField(
                choices=[
                    ("0", 0),
                    ("0.5", 1),
                    ("1", 2),
                    ("1.5", 3),
                    ("2", 4),
                    ("2.5", 5),
                    ("3", 6),
                    ("3.5", 7),
                    ("4", 8),
                    ("4.5", 9),
                    ("5", 10),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="channelsnapshot",
            name="date_creation",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="videorating",
            name="rating",
            field=models.PositiveIntegerField(
                choices=[
                    ("0", 0),
                    ("0.5", 1),
                    ("1", 2),
                    ("1.5", 3),
                    ("2", 4),
                    ("2.5", 5),
                    ("3", 6),
                    ("3.5", 7),
                    ("4", 8),
                    ("4.5", 9),
                    ("5", 10),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="videosnapshot",
            name="date_creation",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="videoviewing",
            name="date_creation",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name="VideoListReaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("liked", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "list",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ratings.videolist",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="VideoListItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("order", models.PositiveIntegerField()),
                (
                    "list",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ratings.videolist",
                    ),
                ),
                (
                    "video",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="ratings.video"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="videolist",
            name="videos",
            field=models.ManyToManyField(
                through="ratings.VideoListItem", to="ratings.video"
            ),
        ),
        migrations.CreateModel(
            name="UserTag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("date_creation", models.DateTimeField(auto_now_add=True)),
                (
                    "state",
                    models.PositiveIntegerField(
                        choices=[("In validation", 0), ("Validated", 1)]
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="channel",
            name="tags",
            field=models.ManyToManyField(blank=True, to="ratings.usertag"),
        ),
        migrations.AddField(
            model_name="video",
            name="tags",
            field=models.ManyToManyField(blank=True, to="ratings.usertag"),
        ),
    ]