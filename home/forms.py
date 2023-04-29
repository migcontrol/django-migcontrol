from django import forms

from . import models


class NewsletterSignupForm(forms.ModelForm):
    class Meta:
        model = models.NewsletterSignup
        fields = ["email"]
