# Generated by Django 4.2.1 on 2023-05-09 23:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ratings", "0011_alter_usertagvote_vote"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usertag",
            name="name",
            field=models.CharField(max_length=25, unique=True),
        ),
    ]
