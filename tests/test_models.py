import pytest
from apps.core.models import BillsMockDjango, ActionsMockDjango, UsersMockDjango, FavoritesMockDjango
from apps.accounts.models import User
# import config.settings as settings
from datetime import datetime
from django.db import IntegrityError
from django.utils import timezone

# DJANGO_SETTINGS_MODULE=config.settings uv run python tests/test_search.py

# Bill model tests
@pytest.fixture
def test_bill():  
    return BillsMockDjango.objects.create(
            bill_id="123",
            number="AB 123",
            title="Test Bill",
            summary="This is a test bill.",
            status="Introduced"
    )

@pytest.mark.django_db
def test_mock_bill_created(test_bill):
    assert test_bill.bill_id == "123"

    assert test_bill._meta.db_table == "bills_mock"

@pytest.mark.django_db
def test_get_bill_from_number(test_bill):
    bill = BillsMockDjango.objects.get(number="AB 123")
    assert bill.bill_id == "123"


# Action model tests
@pytest.fixture
def test_action(test_bill):  
    return ActionsMockDjango.objects.create(
            bill_id=test_bill,
            action_id="Passed",
            description="Passed House",
            date=timezone.make_aware(datetime(2025, 5, 13, 8, 22, 0))
    )

@pytest.mark.django_db
def test_mock_action(test_action):
    assert test_action.action_id == "Passed"

    assert test_action._meta.db_table == "actions_mock"

@pytest.mark.django_db
def test_action_from_id(test_action):
    bill = ActionsMockDjango.objects.get(bill_id="123", action_id = "Passed")
    assert bill.description == "Passed House"

# User model from core tests
    # Will have to delete/change this after the PR that removes this
@pytest.fixture
def test_user():  
    return UsersMockDjango.objects.create(
            user_id="1",
            password="strong-password",
            phone="(555) 555-5555",
            zip="60615"
    )

@pytest.mark.django_db
def test_mock_user(test_user):
    assert test_user.user_id == "1"

    assert test_user._meta.db_table == "users_mock"

# Favorites model tests
@pytest.fixture
def test_favorite(test_bill, test_user):  
    return FavoritesMockDjango.objects.create(
            user_id=test_user,
            bill_id=test_bill
    )

@pytest.mark.django_db
def test_mock_favorite(test_favorite, test_user, test_bill):
    favorite = FavoritesMockDjango.objects.get(user_id=test_user.user_id, bill_id=test_bill.bill_id)

    print(f"favorite.user_id: {favorite.user_id}")
    print(f"test_user.user_id: {test_user.user_id}")

    assert favorite.user_id.user_id == test_user.user_id
    assert favorite._meta.db_table == "favorites_mock"


@pytest.mark.django_db
def test_unique_together(test_favorite, test_user, test_bill):
    FavoritesMockDjango.objects.create(
            user_id=test_user, bill_id=test_bill
    )

    # This should fail
    with pytest.raises(IntegrityError):
        FavoritesMockDjango.objects.create(user_id=test_user, bill_id=test_bill)


# User model from accounts tests
@pytest.fixture
def test_user_accounts(): 
    return User.objects.create(
    email = "test@gmail.COM",
    username = "david_test",
    full_name = "David Test",
    is_staff = False,
    is_active = True,
    date_joined = timezone.make_aware(datetime(2025, 5, 13, 8, 22, 0))
    )

@pytest.mark.django_db
def test_user_name(test_user_accounts):
    assert test_user_accounts.email == "test@gmail.COM"
    assert test_user_accounts.username == "david_test"

@pytest.mark.django_db
def test_get_full_name(test_user_accounts):
    assert test_user_accounts.get_full_name() == "David Test"

@pytest.mark.django_db
def test_get_short_name(test_user_accounts):
    assert test_user_accounts.get_short_name() == "david_test"

@pytest.mark.django_db
def test_clean_email(test_user_accounts):
    test_user_accounts.clean()
    assert test_user_accounts.email == "test@gmail.com"