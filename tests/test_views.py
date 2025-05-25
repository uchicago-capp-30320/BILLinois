import pytest
from django.urls import reverse
from apps.core.models import BillsTable


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
        bill_id="123",
        number="123",
        title="Transportation Test Bill",
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


# Bill page view tests: real query
# Not implemented for now
# @pytest.fixture
# def test_bill_view(client, test_bill):
#     return client.get("/bill_page/", {"bill_number": "123"})

# @pytest.mark.django_db
# def test_create_bill_view(test_bill_view):
#     assert test_bill_view.status_code == 200
