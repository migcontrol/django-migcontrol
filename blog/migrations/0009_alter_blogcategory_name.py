# Generated by Django 3.2.13 on 2022-06-02 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_remove_blogpage_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcategory',
            name='name',
            field=models.CharField(max_length=80, verbose_name='Category Name'),
        ),
    ]
