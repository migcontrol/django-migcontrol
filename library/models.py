from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.edit_handlers import InlinePanel
from wagtail.core import blocks
from wagtail.core.fields import RichTextField
from wagtail.core.fields import StreamField
from wagtail.core.models.i18n import TranslatableMixin
from wagtail.core.templatetags.wagtailcore_tags import richtext
from wagtail.images import get_image_model_string
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.snippets.models import register_snippet


@register_snippet
class RegionSnippet(TranslatableMixin, models.Model):

    name = models.CharField(
        verbose_name=_("region name"),
        help_text=_("Some geographical area, may intersect with other areas"),
        max_length=255,
    )

    panels = [
        FieldPanel("name"),
    ]

    def __str__(self):
        return f"{self.name}"


@register_snippet
class TopicSnippet(TranslatableMixin, models.Model):

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


@register_snippet
class IndustrySnippet(TranslatableMixin, models.Model):

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


@register_snippet
class BusinessCategorySnippet(TranslatableMixin, models.Model):

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


@register_snippet
class BusinessPageSourceSnippet(TranslatableMixin, models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Source Name"))
    url = models.URLField(max_length=512, verbose_name=_("URL"), null=True, blank=True)
    page_link = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        verbose_name=_("Internal page"),
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel("title", classname="title full"),
        FieldPanel("url"),
        FieldPanel("page_link"),
    ]

    def __str__(self):
        return f"{self.title} ({self.url})"


class LibraryIndexPage(Page):
    template = "library/index.html"

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
        from .forms import LibraryFilterForm

        context = super().get_context(request)

        filter_form = LibraryFilterForm(request.GET)

        qs = self.get_children().live().type(MediaPage).order_by("title").specific()

        if filter_form.is_valid():
            qs = filter_form.apply_filter(qs)

        context["filter_form"] = filter_form
        context["media_pages"] = qs
        return context


class MediaPageRegion(models.Model):
    page = ParentalKey(
        "library.MediaPage", on_delete=models.CASCADE, related_name="regions"
    )
    region = models.ForeignKey(
        "library.RegionSnippet", on_delete=models.CASCADE, related_name="media"
    )

    panels = [
        FieldPanel("region"),
    ]

    class Meta:
        unique_together = ("page", "region")


class MediaPageTopic(models.Model):
    page = ParentalKey(
        "library.MediaPage", on_delete=models.CASCADE, related_name="topics"
    )
    topic = models.ForeignKey(
        "library.TopicSnippet", on_delete=models.CASCADE, related_name="media"
    )

    panels = [
        FieldPanel("topic"),
    ]

    class Meta:
        unique_together = ("page", "topic")


class MediaPage(Page):

    body = RichTextField()

    feature_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=("feature image"),
    )

    authors = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
        verbose_name=_("authors"),
    )

    full_title = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
        verbose_name=_("full title"),
    )

    publisher = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
        verbose_name=_("publisher or journal"),
    )

    year = models.PositiveSmallIntegerField(
        default=timezone.now().year,
        blank=True,
        null=True,
        verbose_name=_("year of publication"),
    )

    media_type = models.CharField(
        max_length=128,
        verbose_name=_("media type"),
        blank=True,
        null=True,
    )

    link = models.URLField(
        max_length=1024,
        blank=True,
        null=True,
        verbose_name=_("Link (URL)"),
    )

    media_topics = models.ManyToManyField(
        TopicSnippet, through=MediaPageTopic, blank=True
    )
    media_regions = models.ManyToManyField(
        RegionSnippet, through=MediaPageRegion, blank=True
    )

    def get_display_country(self):
        return ", ".join(map(lambda c: c.name, self.country))

    def get_display_locations(self):
        return ", ".join(str(ll.location) for ll in self.locations.all())

    def get_body(self):  # noqa: max-complexity=11
        body = richtext(self.body)
        return str(body)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        FieldPanel("authors"),
        FieldPanel("full_title"),
        FieldPanel("publisher"),
        FieldPanel("year"),
        FieldPanel("media_type"),
        FieldPanel("link"),
        InlinePanel("regions", label="regions"),
        InlinePanel("topics", label="topics"),
    ]


class BusinessIndexPage(Page):
    template = "library/business/index.html"

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
        context["business_pages"] = (
            self.get_children().live().type(BusinessPage).specific()
        )
        return context


class BusinessPageRegion(models.Model):
    page = ParentalKey(
        "library.BusinessPage",
        on_delete=models.CASCADE,
        related_name="businesspage_regions",
    )
    region = models.ForeignKey(
        "library.RegionSnippet", on_delete=models.CASCADE, related_name="businesses"
    )

    panels = [
        FieldPanel("region"),
    ]

    class Meta:
        unique_together = ("page", "region")


class BusinessPageIndustry(models.Model):
    page = ParentalKey(
        "library.BusinessPage",
        on_delete=models.CASCADE,
        related_name="businesspage_industries",
    )
    industry = models.ForeignKey(
        "library.IndustrySnippet", on_delete=models.CASCADE, related_name="businesses"
    )

    panels = [
        FieldPanel("industry"),
    ]

    class Meta:
        unique_together = ("page", "industry")


class BusinessPageBusinessCategory(models.Model):
    page = ParentalKey(
        "library.BusinessPage",
        on_delete=models.CASCADE,
        related_name="businesspage_categories",
    )
    business_category = models.ForeignKey(
        "library.BusinessCategorySnippet",
        on_delete=models.CASCADE,
        related_name="businesses",
    )

    panels = [
        FieldPanel("business_category"),
    ]

    class Meta:
        unique_together = ("page", "business_category")


class BusinessPageBusinessPageSource(models.Model):
    page = ParentalKey(
        "library.BusinessPage",
        on_delete=models.CASCADE,
        related_name="businesspage_sources",
    )
    businesspage_source = models.ForeignKey(
        "library.BusinessPageSourceSnippet",
        on_delete=models.CASCADE,
        related_name="businesses",
    )

    panels = [
        FieldPanel("businesspage_source"),
    ]

    class Meta:
        unique_together = ("page", "businesspage_source")


class BusinessPage(Page):
    template = "library/business/business_page.html"

    organization_type = models.CharField(
        verbose_name=_("organization type"),
        blank=True,
        null=True,
        max_length=255,
    )

    country_jurisdiction = CountryField(
        verbose_name=_("country"),
        blank=True,
        default="",
        help_text=_(
            "Home country/jurisdiction of the organization (where it's registered)"
        ),
    )

    city_jurisdiction = models.CharField(
        verbose_name=_("city"),
        blank=True,
        null=True,
        help_text=_(
            "Home city/jurisdiction of the organization (where it's registered)"
        ),
        max_length=512,
    )

    branches = RichTextField(
        blank=True,
        verbose_name=_("Branches (subsidiaries)"),
        help_text=_(
            "Use this to name other brands or country offices owned by the same company. This text is free-form for now and until there is a desired data model for mapping branches."
        ),
    )

    regions = models.ManyToManyField(
        RegionSnippet, through=BusinessPageRegion, blank=True
    )

    industries = models.ManyToManyField(
        IndustrySnippet, through=BusinessPageIndustry, blank=True
    )

    business_categories = models.ManyToManyField(
        BusinessCategorySnippet, through=BusinessPageBusinessCategory, blank=True
    )

    sources = models.ManyToManyField(
        BusinessPageSourceSnippet, through=BusinessPageBusinessPageSource, blank=True
    )

    about = RichTextField(
        blank=True,
    )
    eu_border_contribution = RichTextField(
        blank=True,
    )

    website = models.URLField(blank=True, null=True)

    authors = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
        verbose_name=_("authors"),
    )

    content_panels = Page.content_panels + [
        FieldPanel("organization_type"),
        FieldPanel("country_jurisdiction"),
        FieldPanel("city_jurisdiction"),
        FieldPanel("about"),
        FieldPanel("eu_border_contribution"),
        FieldPanel("website"),
        InlinePanel("businesspage_regions", label=_("Regions")),
        InlinePanel("businesspage_industries", label=_("Industries")),
        InlinePanel("businesspage_categories", label=_("Business categories")),
        InlinePanel("businesspage_sources", label=_("Sources")),
    ]

    meta_panels = Page.promote_panels + ["authors"]
