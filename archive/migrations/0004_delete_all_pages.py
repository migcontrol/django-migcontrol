from django.db import migrations


def delete_all(apps, schema_editor):
    # Get models
    ContentType = apps.get_model('contenttypes.ContentType')
    from wagtail.core.models import Page  # noqa

    # Create content type for archiveindexpage model
    archiveindex_content_type, __ = ContentType.objects.get_or_create(
        model='archiveindexpage', app_label='archive')

    Page.objects.filter(
        content_type__model=archiveindex_content_type.model,
        content_type__app_label=archiveindex_content_type.app_label,
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_homepage_body'),
        ('blog', '0012_alter_blogpage_body_mixed'),
        ('library', '0005_create_businessindex'),
        ('archive', '0003_remove_archivepage_short_description'),
        ('wagtailsearch', '0006_customise_indexentry'),
        ('wagtailforms', '0001_initial'),
        ('wagtailredirects', '0001_initial'),
        ('wagtail_footnotes', '0001_initial'),
        ('wagtail_localize', '0015_translationcontext_field_path'),
        ('wiki', '0003_remove_wikipage_short_description'),
    ]

    operations = [
        migrations.RunPython(delete_all),
    ]
