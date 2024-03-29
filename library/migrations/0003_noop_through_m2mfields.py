# Generated by Django 3.2.14 on 2022-08-04 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_create_libraryindex'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediapage',
            name='media_regions',
            field=models.ManyToManyField(blank=True, through='library.MediaPageRegion', to='library.RegionSnippet'),
        ),
        migrations.AddField(
            model_name='mediapage',
            name='media_topics',
            field=models.ManyToManyField(blank=True, through='library.MediaPageTopic', to='library.TopicSnippet'),
        ),
    ]
