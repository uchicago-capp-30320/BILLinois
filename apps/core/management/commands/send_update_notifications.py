import logging
import os

from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.template.loader import render_to_string

from ...models import UserNotificationQueue, FavoritesTable, BillsTable, UpdatesMockDjango
from ....accounts.models import User

FROM_EMAIL = os.getenv("FROM_EMAIL")

logger = logging.getLogger("email_notifications")


class Command(BaseCommand):
    """
    Send bill update notifications to users.
    """

    def get_bill_data(self, bill):
        """
        Get the data of a bill for a given bill ID.

        Args:
            bill_id (str): The ID of the bill.

        Returns:
            dict: A dictionary containing bill information.
        """

        latest_update = UpdatesMockDjango.objects.filter(bill_id=bill)

        bill_data = (
            BillsTable.objects.filter(bill_id=bill)
            .annotate(
                updated_at=latest_update.values("date"),
                update_description=latest_update.values("description"),
            )
            .get()
        )

        bill_data = {
            "title": bill_data.title,
            "summary": bill_data.summary,
            "updated_at": bill_data.updated_at,
            "update_description": bill_data.update_description,
        }

        return bill_data

    def create_email_body(self, context_data):
        """
        Create the email body.

        Args:
            context_data (dict): The context data to render the email body
        """

        text_content = render_to_string(
            "email/notification.txt",
            context=context_data,
        )

        html_content = render_to_string(
            "email/notification.html",
            context=context_data,
        )

        return text_content, html_content

    def send_email(self, user, text_content, html_content):
        """
        Send notification email to the user.

        Args:
            user (User): The user to send the email to.
            text_content (str): The plain text content of the email.
            html_content (str): The HTML content of the email.

        Returns:
            bool: True if the email was sent successfully, False otherwise.
        """

        msg = EmailMultiAlternatives(
            "Your Bill Updates",
            text_content,
            FROM_EMAIL,
            [user.email],
        )

        msg.attach_alternative(html_content, "text/html")

        try:
            msg.send()

        except Exception as e:
            logger.error(f"Error sending email to {user.email}: {e}")
            return False

        return True

    def handle(self, **kwargs):
        users_to_notify = (
            User.objects.filter(usernotificationqueue__is_notified=False)
            .select_related("usernotificationqueue")
            .all()
        )

        for user in users_to_notify:
            queue = user.usernotificationqueue

            bills = []

            # Bills to notify is an array of bill IDs
            for bill in queue.bills_to_notify:
                bills.append(self.get_bill_data(bill))

            context_data = {
                "full_name": user.full_name,
                "number_of_notifications": queue.number_of_notifications,
                "bills": bills,
            }

            text_content, html_content = self.create_email_body(context_data)

            success = self.send_email(user, text_content, html_content)

            if success:
                queue.is_notified = True
                queue.save()
                logger.info(f"Email sent to {user.email} at {timezone.now()}")
