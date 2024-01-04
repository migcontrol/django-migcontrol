from django import forms
from django.conf import settings
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from . import models


class LibraryFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["region"].label_from_instance = self.region_label_from_instance
        self.fields["topic"].label_from_instance = self.topic_label_from_instance

    language = forms.ChoiceField(
        required=False,
        label=_("Language"),
        choices=[
            ("", _("All languages")),
        ]
        + settings.LANGUAGES,
    )
    region = forms.ModelChoiceField(
        queryset=models.RegionSnippet.objects.all().order_by('name'),
        required=False,
        label=_("Region"),
    )
    topic = forms.ModelChoiceField(
        queryset=models.TopicSnippet.objects.all().order_by('name'),
        required=False,
        label=_("Topic"),
    )

    search_query = forms.CharField(
        required=False,
        label=_("Search description and title"),
    )

    order_by = forms.ChoiceField(
        choices=[
            ("title", _("Title")),
            ("-year", _("Year published")),
        ],
        initial="title",
        required=False,
    )

    @staticmethod
    def region_label_from_instance(obj):
        return obj.name

    @staticmethod
    def topic_label_from_instance(obj):
        return obj.name

    def apply_filter(self, qs):
        cd = self.cleaned_data
        if not cd:
            return qs

        if cd["topic"]:
            qs = qs.filter(topics__topic=cd["topic"])

        if cd["region"]:
            qs = qs.filter(regions__region=cd["region"])

        if cd["language"]:
            qs = qs.filter(locale__language_code=cd["language"])

        if cd["search_query"]:
            qs = qs.filter(
                Q(title__icontains=cd["search_query"])
                | Q(body__icontains=cd["search_query"])
            )

        if cd["order_by"]:
            qs = qs.order_by(cd["order_by"])

        return qs
