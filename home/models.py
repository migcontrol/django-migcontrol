from bs4 import BeautifulSoup
from django.db import models  # noqa
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.admin.panels import InlinePanel
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Orderable
from wagtail.models import Page
from wagtail.snippets.models import register_snippet

from home.fields import CarouselBlog
from home.fields import CarouselPage
from home.fields import CarouselRaw
from home.fields import FeatureBlock
from home.fields import OrganizationsCardBlock
from home.fields import SectionCardBlock
from migcontrol.utils import get_toc


class HomePage(Page):
    """
    This is the landing page
    """

    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="full title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("feature", FeatureBlock()),
            (
                "carousel",
                blocks.StreamBlock(
                    [
                        ("blog", CarouselBlog()),
                        ("page", CarouselPage()),
                        ("raw", CarouselRaw()),
                    ],
                    template="home/blocks/carousel.html",
                ),
            ),
            (
                "section_cards",
                blocks.StreamBlock(
                    [
                        ("section", SectionCardBlock()),
                    ],
                    template="home/blocks/section_cards.html",
                ),
            ),
            ("organizations_card", OrganizationsCardBlock()),
        ],
        use_json_field=True,
        verbose_name="body",
        blank=True,
        help_text="The main contents of the page",
    )

    content_panels = [
        FieldPanel("title", classname="full title"),
        FieldPanel("body"),
    ]


class ArticleBase(models.Model):
    """
    This mixin can be reused in Page models of other applications that need
    the same structure.
    """

    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="full title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
        ],
        verbose_name="body",
        blank=True,
        help_text="The main contents of the page",
        use_json_field=True,
    )
    content_panels = [
        FieldPanel("title", classname="full title"),
        FieldPanel("body"),
        FieldPanel("hide_toc"),
    ]

    hide_toc = models.BooleanField(
        default=False,
        verbose_name="Hide Table of Contents",
    )

    class Meta:
        abstract = True

    def get_toc(self):
        """
        [(name, [*children])]
        """
        return get_toc(self.get_body())

    def get_body(self):
        body = "".join([str(f.value) for f in self.body])

        # Now let's add some id=... attributes to all h{1,2,3,4,5}
        soup = BeautifulSoup(body, "html5lib")

        # Beautiful soup unfortunately adds some noise to the structure, so we
        # remove this again - see:
        # https://stackoverflow.com/questions/21452823/beautifulsoup-how-should-i-obtain-the-body-contents
        for attr in ["head", "html", "body"]:
            if hasattr(soup, attr):
                getattr(soup, attr).unwrap()

        for element in soup.find_all(["h1", "h2", "h3", "h4", "h5"]):
            element["id"] = "header-" + slugify(element.text, allow_unicode=True)

        return str(soup)


class Article(ArticleBase, Page):
    """
    We are using this model as a default article page. This covers the following
    page types:

    * Landing page
    * About page
    * Contact page
    * Donate page
    * Subscribe page
    * Data protection page
    * Imprint page
    """

    pass


class Organization(models.Model):

    name = models.CharField(max_length=512)

    website = models.URLField(
        max_length=1024,
    )

    def __str__(self):
        return f"Organization: {self.name}"


# The real model which combines the abstract model, an
# Orderable helper class, and what amounts to a ForeignKey link
# to the model we want to add related links to (BookPage)
class OrganizationRelation(Orderable, Organization):
    page = ParentalKey(
        "OrganizationCollection", on_delete=models.CASCADE, related_name="organizations"
    )


@register_snippet
class OrganizationCollection(ClusterableModel):
    name = models.CharField(
        max_length=128,
        help_text=_(
            "Name this something, i.e. 'collaborators shown on the main landing page'"
        ),
        unique=True,
    )

    def __str__(self):
        return f"Organization Collection: {self.name}"

    class Meta:
        verbose_name = _("Organization collection")
        verbose_name_plural = _("Organization collections")

    panels = [
        FieldPanel("name"),
        InlinePanel("organizations", heading=_("Organizations")),
    ]


class NewsletterSignup(models.Model):
    """
    Register newsletter signups.
    The list is processed manually according to privacy policy.
    """

    email = models.EmailField()
    opt_out = models.BooleanField(
        default=False,
        help_text=_(
            "Check this box if a user indicates that they do not want the newsletter "
            "so we can avoid sending it to them in the future. However,"
            "remember that deleting a user's email is preferable in most cases."
        ),
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel("email"),
        FieldPanel("opt_out"),
    ]
