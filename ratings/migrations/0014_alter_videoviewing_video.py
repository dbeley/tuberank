# Generated by Django 4.2.11 on 2024-03-18 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("ratings", "0013_remove_videolistitem_unique_rank_in_list"),
    ]

    operations = [
        migrations.AlterField(
            model_name="videoviewing",
            name="video",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="viewings",
                to="ratings.video",
            ),
        ),
    ]
