import pycountry
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.gis.db.models import PointField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from mapwidgets import GooglePointFieldWidget

from user.models import UserActivity


class UserActivityInline(admin.StackedInline):
    readonly_fields = ['created_at', 'country', 'user']
    model = UserActivity

    @staticmethod
    def country(instance):
        if instance:
            return pycountry.countries.get(alpha_2=instance.country_code).name

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(get_user_model())
class UserAdmin(BaseUserAdmin):
    inlines = [UserActivityInline]
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
