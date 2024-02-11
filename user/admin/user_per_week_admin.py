import pycountry
from django.contrib import admin
from user.models import UserPerWeek
from django.utils.html import format_html, mark_safe
from django.utils.translation import gettext_lazy as _


@admin.register(UserPerWeek)
class UserPerWeekAdmin(admin.ModelAdmin):
    list_display = ("week", "user_number", "counties_for_users")
    list_per_page = 8
    date_hierarchy = "week"
    readonly_fields = ["counties_for_users"]

    @staticmethod
    def counties_for_users(instance):
        html = ""
        if instance:
            html = f"""
            <table class="table table-dark table-bordered">
                  <tr scope="row">
                    <th scope="col">{_("country code")}</th>
                    <th scope="col">{_("country")}</th>
                    <th scope="col">{_("number of users")}</th>
                  </tr>
            """
            for item in instance.counties:
                country = pycountry.countries.get(alpha_2=list(item.keys())[0])
                if country:
                    country = country.name
                else:
                    country = ""
                html += f"""
                    <tr scope="row"> 
                        <td >{list(item.keys())[0]}</td>
                        <td>{country}</td>
                        <td>{list(item.values())[0]}</td>
                      </tr>
                """
            html += "</table>"

        return mark_safe(format_html(html))

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
