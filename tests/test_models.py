import pytest
from django.contrib.auth import get_user_model

from apps.core.models import BillsTable, ActionsTable, FavoritesTable, TopicsTable, UpdatesTable, UserNotificationQueue
from apps.accounts.models import User

from datetime import datetime
from django.db import IntegrityError
from django.utils import timezone

# User = get_user_model()

# uv venv
# source .venv/bin/activate
# uv run python manage.py runserver
# DJANGO_SETTINGS_MODULE=config.settings pytest tests/test_models.py -v

# unset EMAIL_URL
# export EMAIL_URL="consolemail://"
# unset DATABASE_URL
# export DATABASE_URL="postgres://billinois:orange-49280-shrimp-coordination@138.201.16.221:5432/billinois"


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


@pytest.mark.django_db
def test_bill_created(test_bill):
    assert (test_bill.bill_id, test_bill.state, test_bill._meta.db_table) == ("123", "IL", "bills_table")


@pytest.mark.django_db
def test_get_bill_from_number(test_bill):
    bill = BillsTable.objects.get(number="AB 123", state = "IL", session = "104th")
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
        chamber="House"
    )


@pytest.mark.django_db
def test_action_created(test_action):
    assert (test_action.action_id, test_action._meta.db_table) == ("123", "actions_table")


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


@pytest.mark.django_db
def test_user_name(test_user):
    assert (test_user.email, test_user.username) == ("test@gmail.COM", "david_test")


@pytest.mark.django_db
def test_get_full_name(test_user):
    assert test_user.get_full_name() == "David Test"


@pytest.mark.django_db
def test_get_short_name(test_user):
    assert test_user.get_short_name() == "david_test"


@pytest.mark.django_db
def test_clean_email(test_user):
    test_user.clean()
    assert test_user.email == "test@gmail.com"


# %% Favorites model tests
@pytest.fixture
def test_favorite(test_bill, test_user):
    return FavoritesTable.objects.create(
        user_id=test_user, 
        bill_id=test_bill)


@pytest.mark.django_db
def test_get_favorite_from_user_and_bill(test_favorite, test_user, test_bill):
    favorite = FavoritesTable.objects.get(user_id=test_user, bill_id=test_bill.bill_id)

    assert (favorite.user_id, favorite._meta.db_table) == (
        test_user,
        "favorites_table",
    )


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


@pytest.mark.django_db
def test_topics_created(test_topics):
    educ, health = test_topics
    assert (educ.topic, educ._meta.db_table, \
            health.topic, health._meta.db_table) == \
            ("Education", "topics_table", \
                "Health", "topics_table")


@pytest.mark.django_db
def test_get_topics_from_id(test_topics, test_bill):
    topics = TopicsTable.objects.filter(bill_id=test_bill)
    assert any(topic.topic == "Education" for topic in topics)
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


@pytest.mark.django_db
def test_update_created(test_update, test_bill, test_action):
    assert (test_update.bill_id, test_update.action_id) == (test_bill, test_action)


@pytest.mark.django_db
def test_get_update_from_id(test_update, test_bill, test_action):
    updates = UpdatesTable.objects.filter(bill_id=test_bill, action_id=test_action)
    assert any(update.description == "Passed House" for update in updates)


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


# User Notification Queue
@pytest.fixture
def test_queue(test_user):
    return UserNotificationQueue.objects.create(
        user_id=test_user,
        number_of_notifications = 2,
        bills_to_notify = {},
        is_notified = True
    )


@pytest.mark.django_db
def test_queue_created(test_queue, test_user):
    assert (test_queue.user_id, test_queue.number_of_notifications) == (test_user, 2)

@pytest.mark.django_db
def test_get_queue_from_id(test_queue, test_user):
    queues = UserNotificationQueue.objects.filter(user_id=test_user)
    assert any((queue.number_of_notifications, queue.is_notified) == (2, True) for queue in queues)