# Generated by Django 4.2.16 on 2024-11-07 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_otp_is_used'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
