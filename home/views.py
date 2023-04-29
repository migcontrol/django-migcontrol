from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.views.generic import TemplateView
from django_ratelimit.decorators import ratelimit

from . import forms


class NewsletterSignup(CreateView):

    form_class = forms.NewsletterSignupForm
    template_name = "home/newsletter_signup.html"

    @method_decorator(ratelimit(key="ip", rate="10/d", block=True))
    @method_decorator(ratelimit(key="ip", rate="5/h", block=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("newsletter_valid")


class NewsletterSignupValid(TemplateView):
    template_name = "home/newsletter_signup.html"

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c["valid"] = True
        return c
