# Generated by Django 5.0.3 on 2024-05-18 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0008_userlibrary_state"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="UserLibrary",
            new_name="ProfileLibrary",
        ),
    ]
