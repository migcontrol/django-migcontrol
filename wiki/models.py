from bs4 import BeautifulSoup
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import RichTextField
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.core.templatetags.wagtailcore_tags import richtext
from wagtail.images import get_image_model_string
from wagtail.images.blocks import ImageChooserBlock

from migcontrol.utils import get_toc


class WikiIndexPage(Page):
    template = "wiki/index.html"

    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="full title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
        ],
        verbose_name="body",
        blank=True,
        help_text="The main contents of the page",
    )
    content_panels = [
        FieldPanel("title", classname="full title"),
        StreamFieldPanel("body"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["wiki_pages"] = self.get_children().live().type(WikiPage)
        return context


class WikiPage(Page):

    wordpress_post_id = models.PositiveSmallIntegerField(
        blank=True, null=True, editable=False
    )

    country = CountryField(
        verbose_name=_("country"),
        blank=True,
        multiple=True,
        default="",
    )

    short_description = models.TextField(blank=True, null=True)

    authors = models.CharField(
        blank=True,
        null=True,
        verbose_name="author(s)",
        max_length=255,
        help_text="Mention author(s) by the name to be displayed",
    )

    header_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=("Header image"),
    )

    description = RichTextField()

    def get_display_country(self):
        return ", ".join(map(lambda c: c.name, self.country))

    content_panels = Page.content_panels + [
        FieldPanel("country"),
        FieldPanel("short_description"),
        FieldPanel("description"),
    ]

    def get_toc(self):
        """
        [(name, [*children])]
        """
        return get_toc(self.get_body())

    def get_body(self):
        body = richtext(self.description)

        # Now let's add some id=... attributes to all h{1,2,3,4,5}
        soup = BeautifulSoup(body, "html5lib")

        # Beautiful soup unfortunately adds some noise to the structure, so we
        # remove this again - see:
        # https://stackoverflow.com/questions/21452823/beautifulsoup-how-should-i-obtain-the-body-contents
        for attr in ["head", "html", "body"]:
            if hasattr(soup, attr):
                getattr(soup, attr).unwrap()

        for element in soup.find_all(["h1", "h2", "h3", "h4", "h5"]):
            element["id"] = "header-" + slugify(element.text)

        return str(soup)
