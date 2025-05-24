import logging
import sys
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db.models import Count
from django.contrib.postgres.aggregates import ArrayAgg
from ...models import (
    UserNotificationQueue,
    FavoritesTable,
    UpdatesMockDjango,
    UpdatesTable,
    MostRecentUpload,
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
        
        current_date = datetime.now(tz=ZoneInfo("America/Chicago")).date()
        most_recent_date = MostRecentUpload.objects.latest(
                "last_upload_date").last_upload_date

        logger.info(f"Current date: {current_date}")
        # Check if bills have successfully been uploaded today. If not, exit.
        if not debug and current_date != most_recent_date:
            logger.error("Most recent upload date does not match the current date.")

            print(f"current_date: {repr(current_date)}")
            print(f"most_recent_date: {repr(most_recent_date)}")
            print(f"Equal? {current_date == most_recent_date}")


            sys.exit(1)

        favorite_updates = (
            FavoritesTable.objects.filter(
                bill_id__in=updates_table.objects.values(
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
