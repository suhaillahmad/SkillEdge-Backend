# Generated by Django 4.1.2 on 2022-11-06 19:36

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0004_alter_lessons_lesson"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lessons",
            name="lesson",
            field=cloudinary.models.CloudinaryField(max_length=255),
        ),
    ]
