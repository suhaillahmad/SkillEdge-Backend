# Generated by Django 4.1.2 on 2022-10-24 20:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0004_alter_newuserregistration_otp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newuserregistration",
            name="otp",
            field=models.PositiveIntegerField(
                blank=True,
                null=True,
                validators=[django.core.validators.MaxValueValidator(9999)],
            ),
        ),
    ]
