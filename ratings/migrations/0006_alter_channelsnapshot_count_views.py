# Generated by Django 4.2 on 2023-05-06 17:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ratings", "0005_videolistitem_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="channelsnapshot",
            name="count_views",
            field=models.BigIntegerField(blank=True, default=0, null=True),
        ),
    ]