from bs4 import BeautifulSoup
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.edit_handlers import InlinePanel
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models.i18n import TranslatableMixin
from wagtail.images import get_image_model_string
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.snippets.models import register_snippet

from migcontrol.utils import get_toc


@register_snippet
class WikiCategorySnippet(TranslatableMixin, models.Model):

    name = models.CharField(
        verbose_name=_("topic name"),
        help_text=_("A topic for the library, can intersect with other topics"),
        max_length=255,
    )

    panels = [
        FieldPanel("name"),
    ]

    def __str__(self):
        return f"{self.name}"


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
        FieldPanel("body"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["wiki_pages"] = (
            self.get_children()
            .live()
            .type(WikiPage)
            .specific()
            .values(
                "title",
                "url_path",
                "locale__language_code",
                "wikipage__wiki_categories__wiki_category__name",
            )
            .order_by("wikipage__wiki_categories__wiki_category__name", "title")
        )
        return context


class WikiPageWikiCategory(models.Model):
    page = ParentalKey(
        "wiki.WikiPage",
        on_delete=models.CASCADE,
        related_name="wiki_categories",
    )
    wiki_category = models.ForeignKey(
        "wiki.WikiCategorySnippet",
        on_delete=models.CASCADE,
        related_name="wikipages",
    )

    panels = [
        FieldPanel("wiki_category"),
    ]

    class Meta:
        unique_together = ("page", "wiki_category")


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

    description = StreamField(
        [
            ("heading", blocks.CharBlock(form_classname="title")),
            (
                "rich_text",
                blocks.RichTextBlock(
                    features=[
                        "h1",
                        "h2",
                        "h3",
                        "h4",
                        "h5",
                        "h6",
                        "bold",
                        "italic",
                        "ol",
                        "ul",
                        "hr",
                        "link",
                        "document-link",
                        "image",
                        "embed",
                        "footnotes",
                        "code",
                        "superscript",
                        "subscript",
                        "strikethrough",
                        "blockquote",
                    ]
                ),
            ),
            ("table", TableBlock()),
            ("image", ImageChooserBlock()),
        ],
        use_json_field=True,
    )
    # RichTextField(
    #     features=[
    #         "h1",
    #         "h2",
    #         "h3",
    #         "h4",
    #         "h5",
    #         "h6",
    #         "bold",
    #         "italic",
    #         "ol",
    #         "ul",
    #         "hr",
    #         "link",
    #         "document-link",
    #         "image",
    #         "embed",
    #         "footnotes",
    #         "code",
    #         "superscript",
    #         "subscript",
    #         "strikethrough",
    #         "blockquote",
    #     ]
    # )

    def get_display_country(self):
        return ", ".join(map(lambda c: c.name, self.country))

    content_panels = Page.content_panels + [
        FieldPanel("country"),
        InlinePanel("wiki_categories", label=_("Wiki categories")),
        FieldPanel("description"),
        FieldPanel("authors"),
        InlinePanel("footnotes", label="Footnotes"),
    ]

    def get_toc(self):
        """
        [(name, [*children])]
        """
        return get_toc(self.get_body())

    def get_body(self, context=None):  # noqa: max-complexity=11
        context = context or {}
        body = str(self.description.render_as_block(context=context))

        # Now let's add some id=... attributes to all h{1,2,3,4,5}
        soup = BeautifulSoup(body, "html5lib")

        # Beautiful soup unfortunately adds some noise to the structure, so we
        # remove this again - see:
        # https://stackoverflow.com/questions/21452823/beautifulsoup-how-should-i-obtain-the-body-contents
        for attr in ["head", "html", "body"]:
            if hasattr(soup, attr):
                getattr(soup, attr).unwrap()

        # Now let's add some id=... attributes to all h{1,2,3,4,5}
        for element in soup.find_all(["h1", "h2", "h3", "h4", "h5"]):
            element["id"] = "header-" + slugify(element.text, allow_unicode=True)

        return str(soup)
