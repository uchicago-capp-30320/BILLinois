import logging
import sys

from django.core.management.base import BaseCommand
from django.utils import timezone
from ...models import UserNotificationQueue

logger = logging.getLogger("email_notifications")


class Command(BaseCommand):
    """
    Remove users who have received email notifications from the UserNotificationQueue table.
    """

    def handle(self, **kwargs):
        """
        Remove users who have received email notifications from the UserNotificationQueue table.
        """

        try:
            UserNotificationQueue.objects.filter(is_notified=True).delete()

        except Exception as e:
            logger.error(f"Error while removing users from notification queue: {e}")
            sys.exit(1)

        logger.info(f"Removed users who have received email notifications at {timezone.now()}")
