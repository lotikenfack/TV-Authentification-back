from celery import shared_task
from .models import AccessKey
from datetime import datetime

@shared_task
def invalidate_expired_keys():
    keys = AccessKey.objects.filter(is_active=True)
    for key in keys:
        if key.is_quota_exceeded or key.has_credential_expired:
            key.invalidate_key()

@shared_task
def delete_scheduled_keys():
    keys = AccessKey.objects.filter(is_active=False, scheduled_for_deletion__lte=datetime.now())
    keys.delete()
