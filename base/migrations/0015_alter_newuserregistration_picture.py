# Generated by Django 4.1.3 on 2022-11-12 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0014_alter_newuserregistration_wallet"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newuserregistration",
            name="picture",
            field=models.ImageField(
                default="images/defaultProfilePicture_jkvski.png", upload_to="images"
            ),
        ),
    ]
