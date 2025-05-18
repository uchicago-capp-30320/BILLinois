from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from django.utils import timezone
from ...models import UpdatesMockDjango, ActionsMockDjango, BillsTable, BillsMockDjango


class Command(BaseCommand):
    help = "Insert a mock update into the updates_mock table."

    def add_arguments(self, parser):
        parser.add_argument(
            "category",
            type=str,
            help="The category of the update to insert.",
            default="reading-1",
        )

    def handle(self, **kwargs):
        category = kwargs["category"] if "category" in kwargs else "reading-1"

        action_string = get_random_string(length=10)

        bill, _ = BillsMockDjango.objects.get_or_create(
            bill_id="ocd-bill/18dc955e-de21-493b-b981-d829840c2ac7",
            defaults={
                "title": "NUTELLA DAY",
                "number": "HR 87",
                "summary": "Declares February 5, 2025 as Nutella Day in the State of Illinois to honor Ferrero's significant investments in the State, the many employees who contribute to its success, and the joy that Nutella spreads throughout our communities.",
                "status": "Assigned to State Government Administration Committee",
                "state": "IL",
                "session": 'session: "104th"',
            },
        )

        action, _ = ActionsMockDjango.objects.get_or_create(
            action_id=action_string,
            defaults={
                "description": "This is a mock action",
                "date": timezone.now(),
                "bill_id": bill,
            },
        )

        exists = UpdatesMockDjango.objects.filter(bill_id=bill)
        if not exists.exists():
            update = UpdatesMockDjango.objects.create(
                bill_id=bill,
                description="This is a mock update",
                date=timezone.now(),
                category=category,
                chamber="house",
                action_id=action,
            )

            print(f"Inserted mock update with ID: {update.id}")

        bill, _ = BillsMockDjango.objects.get_or_create(
            bill_id="ocd-bill/4ff0212a-8087-422f-b395-a9f3b707b059",
            defaults={
                "title": "CONGRATS-RONALD MCDONALD HOUSE",
                "number": "HR 191",
                "summary": "Congratulates Ronald McDonald House Charities on its 50th anniversary. Commends the organization for its commitment to Illinois families and children in their times of need. Thanks Ronald McDonald House Charities, its partners, its employees, and its volunteers for their dedication to providing a caring and compassionate environment where families can rest, find support, and heal together. Wishes the organization continued success in its mission.",
                "status": "Added Co-Sponsor Rep. Anne Stava-Murray",
                "state": "IL",
                "session": 'session: "104th"',
            },
        )

        action_string = get_random_string(length=10)

        action, _ = ActionsMockDjango.objects.get_or_create(
            action_id=action_string,
            defaults={
                "description": "This is a mock action",
                "date": timezone.now(),
                "bill_id": bill,
            },
        )

        exists = UpdatesMockDjango.objects.filter(bill_id=bill)

        if not exists.exists():
            update = UpdatesMockDjango.objects.create(
                bill_id=bill,
                description="This is a mock update",
                date=timezone.now(),
                category=category,
                chamber="house",
                action_id=action,
            )

            print(f"Inserted mock update with ID: {update.id}")
