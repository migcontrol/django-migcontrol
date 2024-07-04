# Generated by Django 3.2.18 on 2024-04-24 19:00

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtail.snippets.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20230429_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='body',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='full title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())], blank=True, help_text='The main contents of the page', use_json_field=True, verbose_name='body'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='full title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('feature', wagtail.blocks.StructBlock([('headline', wagtail.blocks.CharBlock()), ('sub_headline', wagtail.blocks.CharBlock()), ('description', wagtail.blocks.RichTextBlock()), ('read_more', wagtail.blocks.PageChooserBlock())])), ('carousel', wagtail.blocks.StreamBlock([('blog', wagtail.blocks.StructBlock([('latest_blog_post', wagtail.blocks.BooleanBlock(required=False)), ('blog_post', wagtail.blocks.PageChooserBlock(page_type=['blog.BlogPage'], required=False))])), ('page', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('page', wagtail.blocks.PageChooserBlock())])), ('raw', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('headline', wagtail.blocks.CharBlock()), ('description', wagtail.blocks.RichTextBlock()), ('read_more', wagtail.blocks.PageChooserBlock())]))], template='home/blocks/carousel.html')), ('section_cards', wagtail.blocks.StreamBlock([('section', wagtail.blocks.StructBlock([('headline', wagtail.blocks.CharBlock()), ('description', wagtail.blocks.RichTextBlock()), ('read_more', wagtail.blocks.PageChooserBlock())]))], template='home/blocks/section_cards.html')), ('organizations_card', wagtail.blocks.StructBlock([('headline', wagtail.blocks.CharBlock()), ('sub_headline', wagtail.blocks.CharBlock()), ('organizations', wagtail.snippets.blocks.SnippetChooserBlock('home.OrganizationCollection'))]))], blank=True, help_text='The main contents of the page', use_json_field=True, verbose_name='body'),
        ),
    ]