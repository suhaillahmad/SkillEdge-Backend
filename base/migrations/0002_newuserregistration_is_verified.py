# Generated by Django 4.1.2 on 2022-10-24 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="newuserregistration",
            name="is_verified",
            field=models.BooleanField(default=False),
        ),
    ]
