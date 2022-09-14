from uuid import uuid4
from django.db import migrations


def create_businessindex(apps, schema_editor):
    # Get models
    BusinessIndexPage = apps.get_model('library.BusinessIndexPage')
    ContentType = apps.get_model('contenttypes.ContentType')
    Locale = apps.get_model('wagtailcore.Locale')
    from wagtail.core.models import Page  # noqa

    # Create content type for libraryindexpage model
    businessindex_content_type, __ = ContentType.objects.get_or_create(
        model='businessindexpage', app_label='library')
    libraryindex_content_type, __ = ContentType.objects.get_or_create(
        model='libraryindexpage', app_label='library')

    translation_key = uuid4()

    # Create a new homepage
    for locale in Locale.objects.all():
        library = Page.objects.get(
            locale__language_code=locale.language_code,
            depth=3,
            content_type__model=libraryindex_content_type.model,
            content_type__app_label=libraryindex_content_type.app_label,
        )
        libraryindex = BusinessIndexPage(
            title="Border Business",
            draft_title="Border Business",
            slug='business',
            content_type=businessindex_content_type,
            locale=locale,
            translation_key=translation_key,
            path=library.path + "0001",
            depth=3,
            numchild=0,
            url_path=library.url_path + "business/",
            live=True,
            show_in_menus=True,
        )

        library.add_child(instance=libraryindex)


def remove_businessindex(apps, schema_editor):
    # Get models
    BusinessIndexPage = apps.get_model('library.BusinessIndexPage')

    # Delete BlogIndexPage
    # Page and Site objects CASCADE
    BusinessIndexPage.objects.filter(slug="business").delete()


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_businesses'),
    ]

    operations = [
        migrations.RunPython(create_businessindex, remove_businessindex),
    ]
