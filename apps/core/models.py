from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class ActionsMockDjango(models.Model):
    """
    A mock model for the actions table.
    Used for testing mock data for actions taken on legislation. Deprecated.
    """

    bill_id = models.ForeignKey("BillsMockDjango", on_delete=models.CASCADE, db_column="bill_id")
    action_id = models.CharField(unique=True, primary_key=True)
    description = models.CharField()
    date = models.DateTimeField()

    class Meta:
        db_table = "actions_mock"  # Specify table name


class ActionsTable(models.Model):
    """
    Stores each distinct action taken on a bill, e.g., ("First Reading").
    Represented by a one-to-many relationship between bill and actions.

    This table is queried by frontend views that show bill information, such
    as most recent action. Additionally, it will be queried by the
    notification system, which updates users about favorited bills that have
    had a significant action associated with them in the past 24 hours.
    """

    action_id = models.CharField(unique=True, primary_key=True, db_column="action_id")
    bill_id = models.ForeignKey("BillsTable", on_delete=models.CASCADE, db_column="bill_id")
    description = models.CharField()
    date = models.DateTimeField()
    category = models.CharField(null=True)
    chamber = models.CharField(null=True, default=None)

    class Meta:
        db_table = "actions_table"
        unique_together = ("action_id", "bill_id")


class BillsMockDjango(models.Model):
    """
    A mock model for the bills table.
    Used for testing mock data. Deprecated.
    """

    bill_id = models.CharField(unique=True, primary_key=True)
    number = models.CharField()
    title = models.CharField()
    state = models.CharField()
    session = models.CharField()
    summary = models.CharField()
    status = models.CharField()

    class Meta:
        db_table = "bills_mock"


class BillsTable(models.Model):
    """
    Stores data for each bill.

    This table is queried by frontend views that show bill information, such
    as the search view, and individual bill pages.
    """

    bill_id = models.CharField(unique=True, primary_key=True)
    number = models.CharField()
    title = models.CharField()
    state = models.CharField()
    session = models.CharField()
    summary = models.CharField()
    status = models.CharField()

    class Meta:
        db_table = "bills_table"


class FavoritesMockDjango(models.Model):
    """
    A mock model for the favorites table.
    Used for testing mock data for user favorites. Deprecated.
    """

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    bill_id = models.ForeignKey("BillsMockDjango", on_delete=models.CASCADE, db_column="bill_id")

    class Meta:
        db_table = "favorites_mock"
        unique_together = ("user_id", "bill_id")


class FavoritesTable(models.Model):
    """
    Stores data for user favorites of bills. Represents a many-to-many
    relationship: one user can like many bills, one bill can be associated
    with many users.

    This table will be queried by frontend views that show users which bills
    they have favorited. Additionally, this table will be used for the
    automatic notification system that notifies users about updates from
    bills they have favorited.
    """

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    bill_id = models.ForeignKey("BillsTable", on_delete=models.CASCADE, db_column="bill_id")

    class Meta:
        db_table = "favorites_table"
        unique_together = ("user_id", "bill_id")


class SponsorsMockDjango(models.Model):
    """
    A mock model for the sponsors table.
    Used for testing mock data for sponsors of legislation. Deprecated.
    """

    id = models.CharField(unique=True, primary_key=True)
    bill_id = models.ForeignKey("BillsMockDjango", on_delete=models.CASCADE, db_column="bill_id")
    sponsor_id = models.CharField()
    sponsor_name = models.CharField()

    class Meta:
        db_table = "sponsors_mock"


class SponsorsTable(models.Model):
    """
    Stores data for sponsors of bills. Represents a one-to-many relationship:
    one bill may have many sponsors.

    This table is queried by frontend views that show bill information,
    including sponsor information.
    """

    id = models.CharField(unique=True, primary_key=True)
    bill_id = models.ForeignKey("BillsTable", on_delete=models.CASCADE, db_column="bill_id")
    sponsor_id = models.CharField(null=True)
    sponsor_name = models.CharField()
    position = models.CharField(null=True)
    party = models.CharField(null=True)

    class Meta:
        db_table = "sponsors_table"


class TopicsMockDjango(models.Model):
    """
    A mock model for the topics table.
    Used for testing mock data for topics of legislation. Deprecated.
    """

    bill_id = models.ForeignKey("BillsMockDjango", on_delete=models.CASCADE, db_column="bill_id")
    topic = models.CharField()

    class Meta:
        db_table = "topics_mock"


class TopicsTable(models.Model):
    """
    Stores data for topics associated with each bill. Represents a many-to-many relationship:
    one bill may have many topics, one topic may have many bills associated with it.

    This table is queried by frontend views that show bill information,
    including topic information.
    """

    bill_id = models.ForeignKey("BillsTable", on_delete=models.CASCADE, db_column="bill_id")
    topic = models.CharField()

    class Meta:
        db_table = "topics_table"


class UpdatesMockDjango(models.Model):
    """
    A mock model for the updates table.
    Used for testing mock data for periodic updates on legislation. Deprecated.
    """

    action_id = models.ForeignKey(
        "ActionsMockDjango", on_delete=models.CASCADE, db_column="action_id"
    )
    bill_id = models.ForeignKey("BillsMockDjango", on_delete=models.CASCADE, db_column="bill_id")
    description = models.CharField()
    date = models.DateTimeField()
    category = models.CharField(null=True)
    chamber = models.CharField()

    class Meta:
        db_table = "updates_mock"
        unique_together = ("action_id", "bill_id")


class UpdatesTable(models.Model):
    """
    A table storing periodic updates for bills.
    """

    action_id = models.ForeignKey("ActionsTable", on_delete=models.CASCADE, db_column="action_id")
    bill_id = models.ForeignKey("BillsTable", on_delete=models.CASCADE, db_column="bill_id")
    description = models.CharField()
    date = models.DateTimeField()
    category = models.CharField(null=True)
    chamber = models.CharField()

    class Meta:
        db_table = "updates_table"
        unique_together = ("action_id", "bill_id")


class UsersMockDjango(models.Model):
    """
    A mock model for the users table.
    Used for testing mock data. Deprecated.
    """

    user_id = models.CharField(unique=True, primary_key=True, null=False)
    password = models.CharField()
    phone = models.CharField()
    zip = models.CharField()

    class Meta:
        db_table = "users_mock"


class UsersTable(models.Model):
    """
    Stores all app users.

    This table is used in authentication views, as well as the bill updates notification system.
    """

    user_id = models.CharField(unique=True, primary_key=True, null=False)
    password = models.CharField()
    phone = models.CharField()
    zip = models.CharField()

    class Meta:
        db_table = "users_table"


class UserNotificationQueue(models.Model):
    """
    A table to store user notifications.
    """

    user_id = models.OneToOneField(User, on_delete=models.CASCADE, db_column="user_id")
    number_of_notifications = models.IntegerField()
    bills_to_notify = models.JSONField()
    is_notified = models.BooleanField(default=False)

    class Meta:
        db_table = "user_notification_queue"


class MostRecentUpload(models.Model):
    """
    A table that stores the most recent bill upload date.
    Used to determine whether or not a notification email should be sent, or
    if there was an error uploading the bills.
    """

    last_upload_date = models.DateField()

    class Meta:
        db_table = "most_recent_upload"
