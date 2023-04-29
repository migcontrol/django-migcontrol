from wagtail.contrib.modeladmin.options import ModelAdmin
from wagtail.contrib.modeladmin.options import modeladmin_register

from .models import NewsletterSignup


class NewsletterSignupAdmin(ModelAdmin):
    model = NewsletterSignup
    menu_label = "Newsletter"  # ditch this to use verbose_name_plural from model
    menu_icon = "tick-inverse"  # change as required
    menu_order = 500  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = (
        False  # or True to exclude pages of this type from Wagtail's explorer view
    )
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ("email", "opt_out", "created")
    list_filter = ("opt_out",)
    search_fields = ("email",)


# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(NewsletterSignupAdmin)
