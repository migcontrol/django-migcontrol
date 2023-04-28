import re

from django import template
from django.contrib.staticfiles import finders
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.utils import translation
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail
from wagtail.core.models import Site
from wagtail.core.templatetags.wagtailcore_tags import pageurl
from wagtail.models import Page


register = template.Library()


@register.simple_tag(takes_context=False)
def page_url_localized_fallback(localized_page, target_language):
    if (
        localized_page.locale.language_code != target_language
        and localized_page.get_parent()
    ):
        return page_url_localized_fallback(
            localized_page.get_parent().localized, target_language
        )
    return localized_page.url


@register.simple_tag(takes_context=True)
def slugurl_localized(context, slug):
    """
    A language-aware version of Wagtail's slugurl tag

    Returns the URL for the page that has the given slug.

    First tries to find a page on the current site. If that fails or a request
    is not available in the context, then returns the URL for the first page
    that matches the slug on any site.
    """
    page = None
    try:
        site = Site.find_for_request(context["request"])
        current_site = site
    except KeyError:
        # No site object found - allow the fallback below to take place.
        pass
    else:
        if current_site is not None:
            page = Page.objects.in_site(current_site).filter(slug=slug).first()

    # If no page is found, fall back to searching the whole tree.
    if page is None:
        page = Page.objects.filter(slug=slug).first()

    if page:
        # call pageurl() instead of page.relative_url() here so we get the ``accepts_kwarg`` logic
        return pageurl(context, page.localized)


class StaticPath(str):
    def __new__(cls, path: str, storage: FileSystemStorage):
        obj = super().__new__(cls, path)
        obj.storage = storage
        return obj


storage = FileSystemStorage(location="/")


@register.simple_tag(takes_context=False)
def get_static_thumbnail(file_: str, geometry, *args, **kwargs):
    disk_path = finders.find(file_)
    if disk_path:
        return get_thumbnail(
            StaticPath(disk_path, storage),
            geometry,
            *args,
            **kwargs,
        )


@register.simple_tag(takes_context=True)
def get_site_root(context):
    # This returns a core.Page. The main menu needs to have the site.root_page
    # defined else will return an object attribute error ('str' object has no
    # attribute 'get_children')
    return Site.find_for_request(context["request"]).root_page.localized


@register.simple_tag(takes_context=False)
def get_page_by_slug(parent, slug):
    # This returns a core.Page. The main menu needs to have the site.root_page
    # defined else will return an object attribute error ('str' object has no
    # attribute 'get_children')
    return parent.get_children().get(slug=slug)


@register.simple_tag(takes_context=True)
def richtext_footnotes(context, html):
    """
    example: {% richtext_footnotes page.body|richtext %}

    html: already processed richtext field html
    Assumes "page" in context.
    """
    FIND_FOOTNOTE_TAG = re.compile(r'<footnote id="(.*?)">.*?</footnote>')

    if not isinstance(context.get("page"), Page):
        return html

    page = context["page"]
    if not hasattr(page, "footnotes_list"):
        page.footnotes_list = []
    footnotes = {str(footnote.uuid): footnote for footnote in page.footnotes.all()}

    def replace_tag(match):
        try:
            index = process_footnote(match.group(1), page)
        except (KeyError, ValidationError):
            return ""
        else:
            return f'<a href="#footnote-{index}" id="footnote-source-{index}"><sup>[{index}]</sup></a>'

    def process_footnote(footnote_id, page):
        footnote = footnotes[footnote_id]
        if footnote not in page.footnotes_list:
            page.footnotes_list.append(footnote)
        # Add 1 to the index as footnotes are indexed starting at 1 not 0.
        return page.footnotes_list.index(footnote) + 1

    return mark_safe(FIND_FOOTNOTE_TAG.sub(replace_tag, html))


# Retrieves the top menu items - the immediate children of the parent page
# The has_menu_children method is necessary because the bootstrap menu requires
# a dropdown class to be applied to a parent
@register.simple_tag(takes_context=True)
def get_menu(context, page=None, ignore_show=False, specific=True):
    if page:
        root_page = page
    else:
        language = translation.get_language()
        root_page = Page.objects.get(depth=3, slug=language)  # @UndefinedVariable

    children = root_page.get_children().filter(live=True, show_in_menus=True)

    if specific:
        children = children

    if not ignore_show:
        children = children.filter(show_in_menus=True)
    return children.specific()


@register.simple_tag(takes_context=False)
def get_sub_menus(page, fixed_level=None, maxdepth=2, specific=True):
    maxdepth = maxdepth or 2
    pages = (
        page.get_ancestors(inclusive=True).filter(live=True).filter(depth__gt=maxdepth)
    )
    if fixed_level:
        pages = pages.filter(depth=fixed_level)
    return pages.specific()


@register.filter("startswith")
def startswith(text, starts):
    return text.startswith(starts)


@register.filter()
def migcontrol_relative_url_path(url_path, locale_id):

    url_parts = url_path.split("/")
    url_parts = [""] + [locale_id] + url_parts[2:]
    return "/".join(url_parts)
