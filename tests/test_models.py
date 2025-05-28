import pytest
from django.contrib.auth import get_user_model

from apps.core.models import (
    BillsTable,
    ActionsTable,
    FavoritesTable,
    TopicsTable,
    UpdatesTable,
    UserNotificationQueue,
)
from apps.accounts.models import User

from datetime import datetime
from django.db import IntegrityError
from django.utils import timezone


# %% Bill model tests
@pytest.fixture
def test_bill():
    return BillsTable.objects.create(
        bill_id="123",
        number="AB 123",
        title="Test Bill",
        state="IL",
        session="104th",
        summary="This is a test bill.",
        status="Introduced",
    )


# Check that the bill has been created with the correct fields
@pytest.mark.django_db
def test_bill_created(test_bill):
    assert (test_bill.bill_id, test_bill.state, test_bill._meta.db_table) == (
        "123",
        "IL",
        "bills_table",
    )


# Check that a bill can be searched for by number
@pytest.mark.django_db
def test_get_bill_from_number(test_bill):
    bill = BillsTable.objects.get(number="AB 123", state="IL", session="104th")
    assert bill.bill_id == "123"


# %% Action model tests
@pytest.fixture
def test_action(test_bill):
    return ActionsTable.objects.create(
        action_id="123",
        bill_id=test_bill,
        description="Passed House",
        date=timezone.make_aware(datetime(2025, 5, 13, 8, 22, 0)),
        category="",
        chamber="House",
    )


# Test that the action has been created with the correct ID and fields
@pytest.mark.django_db
def test_action_created(test_action):
    assert (test_action.action_id, test_action._meta.db_table) == ("123", "actions_table")


# Pull an action from a bill ID and action ID
@pytest.mark.django_db
def test_action_from_id(test_action):
    bill = ActionsTable.objects.get(bill_id="123", action_id="123")
    assert bill.description == "Passed House"


# User model tests
@pytest.fixture
def test_user():
    return User.objects.create(
        email="test@gmail.COM",
        username="david_test",
        full_name="David Test",
        is_staff=False,
        is_active=True,
        date_joined=timezone.make_aware(datetime(2025, 5, 13, 8, 22, 0)),
    )


# Check that the user has been created with the correct fields
@pytest.mark.django_db
def test_user_name(test_user):
    assert (test_user.email, test_user.username) == ("test@gmail.COM", "david_test")


# Test that the user has the correct name
@pytest.mark.django_db
def test_get_full_name(test_user):
    assert test_user.get_full_name() == "David Test"


# Test that the user has the correct short name
@pytest.mark.django_db
def test_get_short_name(test_user):
    assert test_user.get_short_name() == "david_test"


# Test that the clean function correctly cleans the user email
@pytest.mark.django_db
def test_clean_email(test_user):
    test_user.clean()
    assert test_user.email == "test@gmail.com"


# %% Favorites model tests
@pytest.fixture
def test_favorite(test_bill, test_user):
    return FavoritesTable.objects.create(user_id=test_user, bill_id=test_bill)


# Test that a favorite can be pulled from a user ID and a bill ID
@pytest.mark.django_db
def test_get_favorite_from_user_and_bill(test_favorite, test_user, test_bill):
    favorite = FavoritesTable.objects.get(user_id=test_user, bill_id=test_bill.bill_id)

    assert (favorite.user_id, favorite._meta.db_table) == (
        test_user,
        "favorites_table",
    )


# Test the uniqueness constraint
@pytest.mark.django_db
def test_favorites_table_uniqueness(test_favorite, test_user, test_bill):
    # This should raise an error, the test will pass
    with pytest.raises(IntegrityError):
        FavoritesTable.objects.create(user_id=test_user, bill_id=test_bill)


# Topics table tests
@pytest.fixture
def test_topics(test_bill):
    educ = TopicsTable.objects.create(bill_id=test_bill, topic="Education")
    health = TopicsTable.objects.create(bill_id=test_bill, topic="Health")
    return educ, health


# Test that the two topics have both been assigned to the bill
@pytest.mark.django_db
def test_topics_created(test_topics):
    educ, health = test_topics
    assert (educ.topic, educ._meta.db_table, health.topic, health._meta.db_table) == (
        "Education",
        "topics_table",
        "Health",
        "topics_table",
    )


# Test getting a specific topic from the topics table
@pytest.mark.django_db
def test_get_specific_topic_from_id(test_topics, test_bill):
    topics = TopicsTable.objects.filter(bill_id=test_bill)
    assert any(topic.topic == "Education" for topic in topics)


# Test getting all the topics from the table: they should all have that bill ID
@pytest.mark.django_db
def test_get_all_topic_from_id(test_topics, test_bill):
    topics = TopicsTable.objects.filter(bill_id=test_bill)
    assert all(topic.bill_id == test_bill for topic in topics)


# Updates table tests
@pytest.fixture
def test_update(test_bill, test_action):
    return UpdatesTable.objects.create(
        action_id=test_action,
        bill_id=test_bill,
        description="Passed House",
        date=timezone.make_aware(datetime(2025, 5, 13, 8, 22, 0)),
        category="",
        chamber="House",
    )


# Test that the update is created as expected
@pytest.mark.django_db
def test_update_created(test_update, test_bill, test_action):
    assert (test_update.bill_id, test_update.action_id) == (test_bill, test_action)


# Test that the correct update can be searched for by bill and action IDs
@pytest.mark.django_db
def test_get_update_from_id(test_update, test_bill, test_action):
    updates = UpdatesTable.objects.filter(bill_id=test_bill, action_id=test_action)
    assert any(update.description == "Passed House" for update in updates)


# Test uniqueness constraint
@pytest.mark.django_db
def test_updates_table_uniqueness(test_update, test_bill, test_action):
    # This should raise an error, the test will pass
    with pytest.raises(IntegrityError):
        UpdatesTable.objects.create(
            bill_id=test_bill,
            action_id=test_action,
            description="Passed House",
            date=timezone.make_aware(datetime(2025, 5, 18, 8, 22, 0)),
            category="",
            chamber="House",
        )
