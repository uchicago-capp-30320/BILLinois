from django.db import models


class ActionsMockDjango(models.Model):
    """
    A mock model for the actions table.
    Meant to store mock data for actions taken on legislation.
    """

    bill_id = models.ForeignKey("BillsMockDjango", on_delete=models.CASCADE, db_column="bill_id")
    action_id = models.CharField(unique=True, primary_key=True)
    description = models.CharField()
    date = models.DateTimeField()

    class Meta:
        db_table = "actions_mock"  # Specify table name

class ActionsTable(models.Model):
    """
    The full actions table.
    """
    action_id = models.CharField(unique=True, primary_key=True)
    bill_id = models.ForeignKey("BillsTable", on_delete=models.CASCADE, db_column="bill_id")
    description = models.CharField()
    date = models.DateTimeField()
    category = models.CharField()

    class Meta:
        db_table = "actions_table"

class BillsMockDjango(models.Model):
    """
    A mock model for the bills table.
    Meant to store mock data for bills.
    """

    bill_id = models.CharField(unique=True, primary_key=True)
    number = models.CharField()
    title = models.CharField()
    summary = models.CharField()
    status = models.CharField()

    class Meta:
        db_table = "bills_mock"

class BillsTable(models.Model):
    """"
    The full bills table.
    """

    bill_id = models.CharField(unique=True, primary_key=True)
    number = models.CharField()
    title = models.CharField()
    summary = models.CharField()
    status = models.CharField()

    class Meta:
        db_table = "bills_table"

class FavoritesMockDjango(models.Model):
    """
    A mock model for the favorites table.
    Meant to store mock data for user favorites.
    """

    user_id = models.ForeignKey("UsersMockDjango", on_delete=models.CASCADE, db_column="user_id")
    bill_id = models.ForeignKey("BillsMockDjango", on_delete=models.CASCADE, db_column="bill_id")

    class Meta:
        db_table = "favorites_mock"
        unique_together = ("user_id", "bill_id")

class FavoritesTable(models.Model):
    """
    The full favorites table.
    """

    user_id = models.ForeignKey("UsersTable", on_delete=models.CASCADE, db_column="user_id")
    bill_id = models.ForeignKey("BillsTable", on_delete=models.CASCADE, db_column="bill_id")

    class Meta:
        db_table = "favorites_table"
        unique_together = ("user_id", "bill_id")

class SponsorsMockDjango(models.Model):
    """
    A mock model for the sponsors table.
    Meant to store mock data for bill sponsors.
    """

    id = models.CharField(unique=True, primary_key=True)
    bill_id = models.ForeignKey("BillsMockDjango", on_delete=models.CASCADE, db_column="bill_id")
    sponsor_id = models.CharField()
    sponsor_name = models.CharField()

    class Meta:
        db_table = "sponsors_mock"

class SponsorsTable(models.Model):
    """"
    The full sponsors table.
    """

    id = models.CharField(unique=True, primary_key=True)
    bill_id = models.ForeignKey("BillsTable", on_delete=models.CASCADE, db_column="bill_id")
    sponsor_id = models.CharField()
    sponsor_name = models.CharField()

    class Meta:
        db_table = "sponsors_table"

class TopicsMockDjango(models.Model):
    """
    A mock model for the topics table.
    Meant to store mock data for bill topics.
    """

    bill_id = models.ForeignKey("BillsMockDjango", on_delete=models.CASCADE, db_column="bill_id")
    topic = models.CharField()

    class Meta:
        db_table = "topics_mock"

class TopicsTable(models.Model):
    """
    The full topics table.
    """

    bill_id = models.ForeignKey("BillsTable", on_delete=models.CASCADE, db_column="bill_id")
    topic = models.CharField()

    class Meta:
        db_table = "topics_table"

class UsersMockDjango(models.Model):
    """
    A mock model for the users table.
    Meant to store mock data for users.
    """

    user_id = models.CharField(unique=True, primary_key=True, null=False)
    password = models.CharField()
    phone = models.CharField()
    zip = models.CharField()

    class Meta:
        db_table = "users_mock"

class UsersTable(models.Model):
    """
    The full users table.
    """

    user_id = models.CharField(unique=True, primary_key=True, null=False)
    password = models.CharField()
    phone = models.CharField()
    zip = models.CharField()

    class Meta:
        db_table = "users_table"