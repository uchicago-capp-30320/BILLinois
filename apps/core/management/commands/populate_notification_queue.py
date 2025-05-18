import logging
import sys
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Count
from django.contrib.postgres.aggregates import ArrayAgg
from ...models import (
    UserNotificationQueue,
    FavoritesTable,
    BillsTable,
    UpdatesMockDjango,
    UpdatesTable,
)
from ....accounts.models import User

logger = logging.getLogger("to_email_queue")


class Command(BaseCommand):
    def add_arguments(self, parser):
        """
        Add a debug command line argument.
        """
        parser.add_argument(
            "--DEBUG",
            action="store_true",
            help="Run the command in debug mode.",
        )

    def handle(self, *args, **options):
        """
        Populate the UserNotificationQueue table with data.
        """

        debug = options.get("DEBUG")
        if debug == 1:
            updates_table = UpdatesMockDjango
        else:
            updates_table = UpdatesTable

        # We only want to notify users who have bill updates within the last 24 hours.
        # This is to avoid sending notifications for old updates.
        time_threshold = timezone.now() - timezone.timedelta(days=1)

        favorite_updates = (
            FavoritesTable.objects.filter(
                bill_id__in=updates_table.objects.filter(date__gte=time_threshold).values(
                    "bill_id"
                ),
                user_id__in=User.objects.filter(is_subscribed=True).values("id"),
            )
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
