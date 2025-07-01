from django.contrib import admin
from .models import AccessKey

@admin.register(AccessKey)
class AccessKeyAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_active', 'total_minutes_used', 'credential_validity_days', 'cumulative_usage_quota_minutes')
    actions = ['revalidate_key']

    def revalidate_key(self, request, queryset):
        for access_key in queryset:
            access_key.revalidate_key()
        self.message_user(request, "Selected keys have been revalidated.")
    revalidate_key.short_description = "Revalidate selected keys"
