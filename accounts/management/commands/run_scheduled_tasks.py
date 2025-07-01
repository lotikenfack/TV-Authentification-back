from django.core.management.base import BaseCommand
from accounts.models import AccessKey
from datetime import datetime

class Command(BaseCommand):
    help = 'Run scheduled tasks for AccessKey management'

    def handle(self, *args, **kwargs):
        # Invalidate expired or quota-exceeded keys
        keys = AccessKey.objects.filter(is_active=True)
        for key in keys:
            if key.is_quota_exceeded or key.has_credential_expired:
                key.invalidate_key()

        # Delete keys scheduled for deletion
        keys_to_delete = AccessKey.objects.filter(is_active=False, scheduled_for_deletion__lte=datetime.now())
        keys_to_delete.delete()

        self.stdout.write(self.style.SUCCESS('Scheduled tasks executed successfully'))
