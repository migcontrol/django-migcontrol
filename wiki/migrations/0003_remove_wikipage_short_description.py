# Generated by Django 3.2.13 on 2022-07-20 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0002_wikiindexpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wikipage',
            name='short_description',
        ),
    ]