# Generated by Django 5.0.1 on 2024-02-01 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_rename_userprofile_profile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]