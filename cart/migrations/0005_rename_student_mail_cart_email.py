# Generated by Django 4.1.2 on 2022-11-09 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0004_cart_courses"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cart",
            old_name="student_mail",
            new_name="email",
        ),
    ]
