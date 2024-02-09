from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.gis.db.models import PointField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from mapwidgets import GooglePointFieldWidget


@admin.register(get_user_model())
class UserAdmin(BaseUserAdmin):
    formfield_overrides = {PointField: {"widget": GooglePointFieldWidget}}
    ordering = ["-created_at"]
    date_hierarchy = "created_at"
    list_filter = ["is_active", "is_staff", "is_superuser", "country_code"]

    list_display = ["email", "username"]

    search_fields = ["email", "email"]

    fieldsets = (
        (_("Primary Info"), {"fields": ("email", "username", "password")}),
        (
            _("Personal Info"),
            {"fields": ("first_name", "last_name", "dob", "bio")},
        ),
        (_("Location"), {"fields": ("country_code", "coordinates")}),
        ((_("Permissions")), {"fields": ("is_active", "is_staff", "is_superuser")}),
        (_("Important dates"), {"fields": ("last_login", "created_at", "updated_at")}),
    )
    readonly_fields = ["created_at", "updated_at"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "country_code",
                    "password1",
                    "password2",
                    "coordinates",
                ),
            },
        ),
    )
