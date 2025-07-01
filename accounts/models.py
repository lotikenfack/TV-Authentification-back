from django.db import models
from django.utils.timezone import now
from datetime import timedelta, datetime
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

class AccessKey(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    credential_validity_days = models.IntegerField(default=7)
    cumulative_usage_quota_minutes = models.IntegerField(default=240)
    first_login_time = models.DateTimeField(null=True, blank=True)
    last_active_time = models.DateTimeField(null=True, blank=True)
    total_minutes_used = models.IntegerField(default=0)
    current_session_start_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    invalidated_at = models.DateTimeField(null=True, blank=True)
    grace_period_end_time = models.DateTimeField(null=True, blank=True)
    scheduled_for_deletion = models.DateTimeField(null=True, blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_quota_exceeded(self):
        return self.total_minutes_used >= self.cumulative_usage_quota_minutes

    @property
    def has_credential_expired(self):
        if self.first_login_time:
            expiry_date = self.first_login_time + timedelta(days=self.credential_validity_days)
            return now() > expiry_date
        return False

    @property
    def should_be_deleted(self):
        return self.scheduled_for_deletion and now() > self.scheduled_for_deletion

    def invalidate_key(self, reason=None):
        self.is_active = False
        self.invalidated_at = now()
        self.grace_period_end_time = now() + timedelta(hours=12)
        self.scheduled_for_deletion = now() + timedelta(days=1)
        self.save()

    def revalidate_key(self):
        self.is_active = True
        self.total_minutes_used = 0
        self.invalidated_at = None
        self.grace_period_end_time = None
        self.scheduled_for_deletion = None
        self.save()
