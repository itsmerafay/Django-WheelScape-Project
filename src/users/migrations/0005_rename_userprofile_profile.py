# Generated by Django 5.0.1 on 2024-02-01 13:49

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_userprofile_location'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserProfile',
            new_name='Profile',
        ),
    ]
