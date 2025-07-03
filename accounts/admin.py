from django import forms
from .models import AccessKey

class AccessKeyAdminForm(forms.ModelForm):
    class Meta:
        model = AccessKey
        fields = '__all__'

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and not password.startswith('pbkdf2_'):
            # Only hash if not already hashed
            return self.instance.set_password(password) or self.instance.password
        return password

    def save(self, commit=True):
        instance = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password and not password.startswith('pbkdf2_'):
            instance.set_password(password)
        if commit:
            instance.save()
        return instance

from django.contrib import admin
from .models import AccessKey

@admin.register(AccessKey)
class AccessKeyAdmin(admin.ModelAdmin):
    form = AccessKeyAdminForm
    list_display = ('username', 'is_active', 'total_minutes_used', 'credential_validity_days', 'cumulative_usage_quota_minutes')
    actions = ['revalidate_key']

    def revalidate_key(self, request, queryset):
        for access_key in queryset:
            access_key.revalidate_key()
        self.message_user(request, "Selected keys have been revalidated.")
    revalidate_key.short_description = "Revalidate selected keys"
