# Generated by Django 4.2.16 on 2024-11-07 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
            ],
        ),
    ]