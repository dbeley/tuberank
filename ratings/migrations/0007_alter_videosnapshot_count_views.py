# Generated by Django 4.2 on 2023-05-06 17:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ratings", "0006_alter_channelsnapshot_count_views"),
    ]

    operations = [
        migrations.AlterField(
            model_name="videosnapshot",
            name="count_views",
            field=models.BigIntegerField(blank=True, default=0, null=True),
        ),
    ]