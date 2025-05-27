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

    Connects to:

    - Bills (on bill_id ForeignKey)

    Attributes:
        action_id (Varchar, PrimaryKey, unique):
            Unique identifier for the action.
        bill_id (ForeignKey):
            `bill_id` from the bills table for the bill associated with this action.
        description (Varchar): Description of the action, e.g., ("First Reading").
        date (Timestamp): Date of the action.
        category (Varchar, nullable):
            Category of the action. Used to group actions into broader types for
            tracking bill status.
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
    as the search view and individual bill pages.

    Has connections from:

    - Actions
    - Favorites
    - Sponsors
    - Topics

    Attributes:
        bill_id (Varchar, PrimaryKey, unique):
            Unique identifier for the bill, sourced from OpenStates.
        number (Varchar): Bill number used by the legislature.
        title (Varchar): Official title of the bill.
        state (Varchar): State where the bill is introduced.
        session (Varchar): Legislative session in which the bill is introduced.
        summary (Varchar): Bill summary as sourced from OpenStates API.
        status (Varchar): The latest action taken on the bill.
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

    Connects to:

    - Bills (on bill_id ForeignKey)
    - Users (on user_id ForeignKey)

    Attributes:
        id (Bigint, PrimaryKey): Internal ID for a favorite.
        bill_id (Varchar, ForeignKey):
            `bill_id` from the bills table for the bill favorited.
        user_id (Varchar, ForeignKey):
            `user_id` from the users table for the user favoriting the bill.
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

    Connects to:

    - Bills (on bill_id ForeignKey)

    Attributes:
        id (Varchar, PrimaryKey, unique):
            Internal id of the sponsor. Separate from sponsor_id
            as sponsor_id comes from OpenStates and may be null.
        sponsor_id (Varchar): sponsor_id from OpenStates.
        sponsor_name (Varchar): Name of the bill sponsor.
        bill_id (Varchar, ForeignKey):
            `bill_id` from the bills table, the bill that the sponsor has sponsored.
        position (Varchar, nullable):
            The position (e.g., Member of the State House, Member
            of the State Senate) that the sponsor occupies.
        party (Varchar, nullable): The political party of the sponsor.
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

    Connects to:

    - Bills (on bill_id ForeignKey)

    Attributes:
        id (Bigint, PrimaryKey): ID of the topic.
        topic (Varchar): Topic name.
        bill_id (Varchar, ForeignKey):
            `bill_id` from the bills table, the bill the topic is associated with.
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

    This table is included in addition to the ActionsTable to provide a simple way to
    to use the most recent action for notifications.

    Connects to:

    - Actions (on action_id ForeignKey)
    - Bills (on bill_id ForeignKey)

    Attributes:
        action_id (Varchar, ForeignKey):
            `action_id` from the actions table, the bill the update is associated with.
        topic (Varchar): Topic name.
        bill_id (Varchar, ForeignKey):
            `bill_id` from the bills table, the bill the update is associated with.
        description (Varchar): Description of the update.
        date (DateTime): Date of the update.
        category (Varchar, nullable): Category of the update.
        chamber (Varchar): Chamber (House or Senate) associated with the update.
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

    Has connections from:

    - Favorites

    Attributes:
        user_id (Bigint, PrimaryKey, unique):
            Internal user id, used for authentication and user management.
            This doubles as the username and email.
        password (Varchar): Hashed user password.
        phone (Varchar): User's phone number, used for notifications and dual authentication.
        zip (Varchar):
            User's zip code, used for location-based features. (Currently not implemented)
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

    Connects to:

    - Users (on user_id)

    Attributes:
        id (Bigint, PrimaryKey): ID of the queue entry.
        user_id (ForeignKey): The user_id of the user to be notified.
        number_of_notifications (Int): Number of notifications for a user on a given day.
        bills_to_notify (Array): A list of the bill ids that the user needs to be updated on.
        is_notified (Boolean): Whether or not a notification email has been sent to the user.
    """

    user_id = models.OneToOneField(User, on_delete=models.CASCADE, db_column="user_id")
    number_of_notifications = models.IntegerField()
    bills_to_notify = models.JSONField()
    is_notified = models.BooleanField(default=False)

    class Meta:
        db_table = "user_notification_queue"


class MostRecentUpload(models.Model):
    """
    A table that stores the most recent date that bills data were uploaded.

    Used to determine whether or not a notification email should be sent, or
    if there was an error uploading the bills.

    Connects to:

    - None

    Attributes:
        id (Bigint, PrimaryKey): ID of the upload.
        last_upload_date (Date): Date of the last successful bill upload.
    """

    last_upload_date = models.DateField()

    class Meta:
        db_table = "most_recent_upload"
