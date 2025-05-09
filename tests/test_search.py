import pytest
from django.test import TestCase, Client
from apps.core.models import BillsMockDjango
import config.settings as settings
from django.core.management import call_command

@pytest.mark.django_db
def test_create_search(client):
    response = client.get("/search/", {"query": "This is a test query."})

    assert response.status_code == 200

@pytest.mark.django_db
def test_mock_bill():
    bill = BillsMockDjango.objects.create(
            bill_id="123",
            number="AB 123",
            title="Test Bill",
            summary="This is a test bill.",
            status="Introduced"
    )

    assert bill.bill_id == "123"

@pytest.mark.django_db
def test_bill_from_id():
    bill = BillsMockDjango.objects.create(
            bill_id="123",
            number="AB 123",
            title="Test Bill",
            summary="This is a test bill.",
            status="Introduced"
    )

    bill = BillsMockDjango.objects.get(number="AB 123")
    assert bill.bill_id == "123"

# from django.test import TestCase, Client
# from apps.core.models import BillsMockDjango

# class searchViewTest(TestCase):
#     """
#     Test the search view.
#     """

#     def setUp(self):
#         """
#         Set up the test client and create mock data.
#         """
#         self.client = Client()
#         self.bill = BillsMockDjango.objects.create(
#             bill_id="123",
#             number="AB 123",
#             title="Test Bill",
#             summary="This is a test bill.",
#             status="Introduced",
#         )

#     def test_search_view(self):
#         """
#         Test the search view with a valid query.
#         """
#         response = self.client.get("/search/", {"query": "This is a test query."})
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "This is a test query.")
#         self.assertContains(response, "Test Bill")