import pytest
from django.urls import reverse
from apps.core.models import BillsTable
from apps.accounts.models import User

from datetime import datetime
from django.utils import timezone

# Home view tests
@pytest.fixture
def test_home(client):
    return client.get("/")


@pytest.mark.django_db
def test_home_status(test_home):
    assert test_home.status_code == 200


@pytest.mark.django_db
def test_home_content(test_home):
    bytes = [b"BILLinois", b"Get started by searching a custom bill topic", b"Education"]
    assert all(byte in test_home.content for byte in bytes)


# Search view tests: fake query
@pytest.fixture
def test_search_fake(client):
    return client.get("/search/", {"query": "This is a test query.", "state": "IL"})


@pytest.mark.django_db
def test_create_search(test_search_fake):
    assert test_search_fake.status_code == 200


@pytest.mark.django_db
def test_search_content(test_search_fake):
    bytes = [b"BILLinois", b"Menu"]
    assert all(byte in test_search_fake.content for byte in bytes)


# Search view tests: real query
@pytest.fixture
def test_bill():
    return BillsTable.objects.create(
        bill_id="hb123",
        number="hb123",
        title="Transportation Test Bill",
        state="illinois",
        session="104th",
        summary="This is a test bill.",
        status="Introduced",
    )

@pytest.fixture
def test_search_real(client, test_bill):
    return client.get("/search/", {"query": "Transportation"})


@pytest.mark.django_db
def test_create_search_real(test_search_real):
    assert test_search_real.status_code == 200


@pytest.mark.django_db
def test_search_content_real(test_search_real, test_bill):
    bytes = [b"BILLinois", b"Menu", b"123", b"Transportation Test Bill"]
    assert all(byte in test_search_real.content for byte in bytes)


# test user
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

# Bill page view tests: query by bill_id
@pytest.fixture
def test_bill_view_id(client, test_bill):
    print("Test bill_id:", test_bill.bill_id)
    url = reverse("bill_by_id", kwargs={"bill_id": test_bill.bill_id})
    print(url)
    response = client.get(url, follow=True)
    print("Status code:", response.status_code)
    if hasattr(response, "url"):
        print("Redirected to:", response.url)
    else:
        print("No redirect. Content:", response.content)
    return response

@pytest.mark.django_db
def test_create_bill_view_by_id(client, test_bill_view_id):
    # user = User.objects.create_user(username='test', password='testpass')
    # client.login(username='test', password='testpass')
    assert test_bill_view_id.status_code == 200


# Bill page view tests: query by state, session, and bill number
@pytest.fixture
def test_bill_view_info(client, test_bill):
    url = reverse("bill_by_info", kwargs={
        "state": test_bill.state,
        "session": test_bill.session,
        "bill_number": test_bill.number})
    response = client.get(url, follow=True)
    return response
    # return client.get("/bill/illinois/104th/123/", {"state": "illinois",
    #                              "session": "104th",
    #                              "number": "123"})

@pytest.mark.django_db
def test_create_bill_view(test_bill_view_info):
    assert test_bill_view_info.status_code == 200
