# Generated by Django 3.2.14 on 2022-09-14 21:06

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_create_businessindex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesspagebusinesscategory',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='businesspage_categories', to='library.businesspage'),
        ),
        migrations.AlterField(
            model_name='businesspagebusinesspagesource',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='businesspage_sources', to='library.businesspage'),
        ),
        migrations.AlterField(
            model_name='businesspageindustry',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='businesspage_industries', to='library.businesspage'),
        ),
        migrations.AlterField(
            model_name='businesspageregion',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='businesspage_regions', to='library.businesspage'),
        ),
        migrations.AlterField(
            model_name='businesspagesourcesnippet',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Source Name'),
        ),
    ]