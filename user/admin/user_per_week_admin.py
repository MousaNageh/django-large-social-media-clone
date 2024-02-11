from django.contrib import admin
from user.models import UserPerWeek



@admin.register(UserPerWeek)
class UserPerWeekAdmin(admin.ModelAdmin):
    list_display = ("week", "user_number", "counties")
    list_per_page = 12

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
