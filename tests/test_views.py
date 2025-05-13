import pytest
from django.urls import reverse

@pytest.fixture
def test_home(client): 
    return client.get("/")

@pytest.mark.django_db
def test_home_status(test_home):
    # response = client.get("/")

    assert test_home.status_code == 200

@pytest.mark.django_db
def test_home_content(test_home):

    assert b"Billinois" in test_home.content
    # assert b"BILLinois" in response.content
    # assert b"Get started by searching a custom bill topic" in response.content
    # assert b"Education" in response.content

@pytest.fixture
def test_search_fake(client): 
    return client.get("/search/", {"query": "This is a test query."})

@pytest.mark.django_db
def test_create_search(test_search_fake):
    assert test_search_fake.status_code == 200

@pytest.mark.django_db
def test_search_content(test_search_fake):
    assert b"Billinois" in test_search_fake.content


@pytest.fixture
def test_search_real(client): 
    return client.get("/search/", {"query": "Transportation"})

@pytest.mark.django_db
def test_create_search_real(test_search_real):
    assert test_search_real.status_code == 200

@pytest.mark.django_db
def test_search_content_real(test_search_real):
    assert b"Billinois" in test_search_real.content