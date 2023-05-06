# Generated by Django 4.2 on 2023-05-05 10:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ratings", "0003_rename_order_videolistitem_rank"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="videolistitem",
            name="unique_order_in_list",
        ),
        migrations.AddConstraint(
            model_name="videolistitem",
            constraint=models.UniqueConstraint(
                fields=("list", "rank"), name="unique_rank_in_list"
            ),
        ),
    ]