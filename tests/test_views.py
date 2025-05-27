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


# Test that the home page loads
@pytest.mark.django_db
def test_home_status(test_home):
    assert test_home.status_code == 200


# Test that the home page has the expected content
@pytest.mark.django_db
def test_home_content(test_home):
    bytes = [b"BILLinois", b"Get started by searching a custom bill topic", b"Education"]
    assert all(byte in test_home.content for byte in bytes)


# Search view tests: fake query
@pytest.fixture
def test_search_fake(client):
    return client.get("/search/", {"query": "This is a test query.", "state": "IL"})


# Test that the search works
@pytest.mark.django_db
def test_create_search(test_search_fake):
    assert test_search_fake.status_code == 200


# Test that the result returns nothing as expected
@pytest.mark.django_db
def test_search_content(test_search_fake):
    bytes = [b"BILLinois", b"Menu", b"No results found."]
    assert all(byte in test_search_fake.content for byte in bytes)


# Create test bills
@pytest.fixture
def test_bill():
    bill_il = BillsTable.objects.create(
        bill_id="hb123_il",
        number="HB 123",
        title="Transportation Test Bill (Illinois)",
        state="Illinois",
        session="104th",
        summary="This is a test bill.",
        status="Introduced",
    )
    bill_in = BillsTable.objects.create(
        bill_id="hb123_in",
        number="HB 123",
        title="Transportation Test Bill (Indiana)",
        state="Indiana",
        session="104th",
        summary="This is a test bill.",
        status="Introduced",
    )
    return bill_il, bill_in


# Search view tests: real query
@pytest.fixture
def test_search_real(client, test_bill):
    return client.get("/search/", {"query": "Transportation"})


# Test that the search worked
@pytest.mark.django_db
def test_create_search_real(test_search_real):
    assert test_search_real.status_code == 200


# Test that the bills are both returned when no state is filtered for
@pytest.mark.django_db
def test_search_content_real(test_search_real, test_bill):
    bytes = [
        b"BILLinois",
        b"Menu",
        b"123",
        b"Transportation Test Bill (Illinois)",
        b"Transportation Test Bill (Indiana",
    ]
    assert all(byte in test_search_real.content for byte in bytes)


# Test search specifically by state
@pytest.fixture
def test_search_by_state(client, test_bill):
    return client.get("/search/", {"query": "Transportation", "state": "Illinois"})


# Test that search by state worked
@pytest.mark.django_db
def test_create_search_by_state(test_search_by_state):
    assert test_search_by_state.status_code == 200


# Test that the filtering works - Illinois bill is returned and Indiana bill is not
@pytest.mark.django_db
def test_search_content_by_state_real(test_search_by_state, test_bill):
    bytes = [b"BILLinois", b"Menu", b"123", b"Transportation Test Bill (Illinois)"]
    no_bytes = [b"Transportation Test Bill (Indiana)"]
    assert all(byte in test_search_by_state.content for byte in bytes) and not all(
        byte in test_search_by_state.content for byte in no_bytes
    )


# Bill page view tests: query by bill_id
@pytest.fixture
def test_bill_view_id(client, test_bill):
    test_bill_il, _ = test_bill
    print("Test bill_id:", test_bill_il.bill_id)
    url = reverse("bill_by_id", kwargs={"bill_id": test_bill_il.bill_id})
    response = client.get(url, follow=True)
    return response


# Test that the bill page is created
@pytest.mark.django_db
def test_create_bill_view_by_id(client, test_bill_view_id):
    assert test_bill_view_id.status_code == 200


# Test that the bill page has the correct information
@pytest.mark.django_db
def test_bill_view_by_id_content(test_bill_view_id):
    bytes = [b"Transportation Test Bill (Illinois)"]
    no_bytes = [b"Transportation Test Bill (Indiana)"]
    assert all(byte in test_bill_view_id.content for byte in bytes) and not all(
        byte in test_bill_view_id.content for byte in no_bytes
    )


# Bill page view tests: query by state, session, and bill number
@pytest.fixture
def test_bill_view_info(client, test_bill):
    response = client.get("/bill/illinois/104th/hb123/", follow=True)
    print("Status code:", response.status_code)
    return response


# Test that the bill page is returned
@pytest.mark.django_db
def test_create_bill_view_by_info(test_bill_view_info):
    assert test_bill_view_info.status_code == 200


# Test that the bill page has the correct information
@pytest.mark.django_db
def test_bill_view_by_info_content(test_bill_view_info):
    bytes = [b"Transportation Test Bill (Illinois)"]
    no_bytes = [b"Transportation Test Bill (Indiana)"]
    assert all(byte in test_bill_view_info.content for byte in bytes) and not all(
        byte in test_bill_view_info.content for byte in no_bytes
    )


# Test privacy policy call
@pytest.fixture
def test_privacy_policy(client):
    return client.get("/privacy_policy/")


# Test the privacy policy works
@pytest.mark.django_db
def test_privacy_policy_works(test_privacy_policy):
    assert test_privacy_policy.status_code == 200
