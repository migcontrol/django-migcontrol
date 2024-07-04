# Generated by Django 3.2.18 on 2024-04-24 19:00

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtail_footnotes.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_blogcategory_translationmixin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogindexpage',
            name='body',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='full title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())], blank=True, help_text='The main contents of the page', use_json_field=True, verbose_name='body'),
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='body_mixed',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='full title')), ('paragraph', wagtail_footnotes.blocks.RichTextBlockWithFootnotes()), ('image', wagtail.images.blocks.ImageChooserBlock())], blank=True, help_text='Avoiding this at first because data might be hard to migrate?', use_json_field=True, verbose_name='body (mixed)'),
        ),
    ]