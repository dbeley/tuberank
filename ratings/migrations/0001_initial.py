# Generated by Django 4.2 on 2023-05-04 17:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Channel",
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
                ("yt_id", models.CharField(max_length=24, unique=True)),
                (
                    "date_creation",
                    models.DateTimeField(verbose_name="date of channel creation"),
                ),
                ("description", models.TextField(blank=True, max_length=5000)),
            ],
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
                ("name", models.CharField(max_length=50, unique=True)),
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
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Video",
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
                ("yt_id", models.CharField(max_length=11, unique=True)),
                (
                    "date_publication",
                    models.DateTimeField(verbose_name="date of video publication"),
                ),
                (
                    "channel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="videos",
                        to="ratings.channel",
                    ),
                ),
                ("tags", models.ManyToManyField(blank=True, to="ratings.usertag")),
            ],
        ),
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
        migrations.CreateModel(
            name="VideoViewing",
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
                ("date_creation", models.DateTimeField(auto_now_add=True)),
                (
                    "state",
                    models.PositiveIntegerField(
                        choices=[("Watching", 0), ("Viewed", 1)]
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="viewings",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "video",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="viewings",
                        to="ratings.video",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="VideoSnapshot",
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
                ("title_en", models.CharField(max_length=100)),
                ("count_views", models.IntegerField(blank=True, default=0, null=True)),
                ("count_likes", models.IntegerField(blank=True, default=0, null=True)),
                (
                    "count_comments",
                    models.IntegerField(blank=True, default=0, null=True),
                ),
                ("date_creation", models.DateTimeField(auto_now_add=True)),
                ("description", models.TextField(blank=True, max_length=5000)),
                ("thumbnail_url", models.CharField(max_length=100)),
                (
                    "category",
                    models.PositiveIntegerField(
                        blank=True,
                        choices=[
                            ("Film & Animation", 1),
                            ("Autos & Vehicles", 2),
                            ("Music", 10),
                            ("Pets & Animals", 15),
                            ("Sports", 17),
                            ("Travel & Events", 19),
                            ("Gaming", 20),
                            ("People & Blogs", 22),
                            ("Comedy", 23),
                            ("Entertainment", 24),
                            ("News & Politics", 25),
                            ("How-to & Styles", 26),
                            ("Education", 27),
                            ("Science & Technology", 28),
                            ("Non-profits & Activism", 29),
                        ],
                        null=True,
                    ),
                ),
                ("duration", models.IntegerField(blank=True, null=True)),
                (
                    "video",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="snapshots",
                        to="ratings.video",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="VideoRating",
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
                (
                    "rating",
                    models.PositiveIntegerField(
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
                ("date_creation", models.DateTimeField(auto_now_add=True)),
                ("review_title", models.TextField(blank=True, max_length=100)),
                ("review_body", models.TextField(blank=True, max_length=5000)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="video_ratings",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "video",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ratings",
                        to="ratings.video",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="VideoListRating",
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
                        related_name="ratings",
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
            name="ChannelSnapshot",
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
                ("name_en", models.CharField(max_length=20)),
                (
                    "count_subscribers",
                    models.IntegerField(blank=True, default=0, null=True),
                ),
                ("count_views", models.IntegerField(blank=True, default=0, null=True)),
                ("count_videos", models.IntegerField(blank=True, default=0, null=True)),
                ("date_creation", models.DateTimeField(auto_now_add=True)),
                ("custom_url", models.CharField(blank=True, max_length=24)),
                ("description", models.TextField(blank=True, max_length=5000)),
                ("thumbnail_url", models.CharField(max_length=100)),
                (
                    "channel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="snapshots",
                        to="ratings.channel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ChannelRating",
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
                (
                    "rating",
                    models.PositiveIntegerField(
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
                ("date_creation", models.DateTimeField(auto_now_add=True)),
                ("review_title", models.TextField(blank=True, max_length=100)),
                ("review_body", models.TextField(blank=True, max_length=5000)),
                (
                    "channel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ratings",
                        to="ratings.channel",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="channel_ratings",
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
        migrations.AddConstraint(
            model_name="videorating",
            constraint=models.UniqueConstraint(
                fields=("user", "video"), name="unique_user_rating_video"
            ),
        ),
        migrations.AddConstraint(
            model_name="videolistitem",
            constraint=models.UniqueConstraint(
                fields=("list", "video"), name="unique_video_in_list"
            ),
        ),
        migrations.AddConstraint(
            model_name="videolist",
            constraint=models.UniqueConstraint(
                fields=("user", "name"), name="unique_user_video_list_by_name"
            ),
        ),
        migrations.AddConstraint(
            model_name="channelrating",
            constraint=models.UniqueConstraint(
                fields=("user", "channel"), name="unique_user_rating_channel"
            ),
        ),
    ]
