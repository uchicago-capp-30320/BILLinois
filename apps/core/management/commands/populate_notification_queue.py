import logging
import sys
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Count
from django.contrib.postgres.aggregates import ArrayAgg
from ...models import UserNotificationQueue, FavoritesTable, BillsTable, UpdatesMockDjango
from ....accounts.models import User

logger = logging.getLogger("to_email_queue")


class Command(BaseCommand):
    def handle(self, **kwargs):
        """
        Populate the UserNotificationQueue table with data.
        """

        favorite_updates = (
            FavoritesTable.objects.filter(bill_id__in=UpdatesMockDjango.objects.values("bill_id"))
            .select_related("accounts.user")
            .values("user_id")
            .annotate(
                number_of_notifications=Count("bill_id"),
                bills_to_notify=ArrayAgg("bill_id"),
            )
        )

        # Make list of users to notify for bulk insert into UserNotificationQueue.
        # Only include users who are subscribed to notifications.
        users_to_notify = [
            UserNotificationQueue(
                user_id=User.objects.filter(is_subscribed=True).get(id=favorite["user_id"]),
                number_of_notifications=favorite["number_of_notifications"],
                bills_to_notify=favorite["bills_to_notify"],
                is_notified=False,
            )
            for favorite in favorite_updates
        ]

        logger.info(f"Pushing users to notification queue at {timezone.now()}")

        try:
            UserNotificationQueue.objects.bulk_create(
                users_to_notify,
                unique_fields=["user_id"],
                update_conflicts=True,
                update_fields=["number_of_notifications", "bills_to_notify", "is_notified"],
            )
            logger.info(f"Finished pushing users to notification queue at {timezone.now()}")

        except Exception as e:
            logger.error(f"Error while pushing users to notification queue: {e}")

            # Return an error to indicate failure
            sys.exit(1)
