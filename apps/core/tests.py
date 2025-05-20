from django.test import TestCase, Client
from .models import BillsMockDjango


class SearchViewTest(TestCase):
    """
    Test the search view.
    """

    def setUp(self):
        """
        Set up the test client and create mock data.
        """
        self.client = Client()
        self.bill = BillsMockDjango.objects.create(
            bill_id="123",
            number="AB 123",
            title="Test Bill",
            summary="This is a test bill.",
            status="Introduced",
        )

    def test_search_view(self):
        """
        Test the search view with a valid query.
        """
        response = self.client.get("/search/", {"query": "This is a test query."})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is a test query.")
        self.assertContains(response, "Test Bill")
