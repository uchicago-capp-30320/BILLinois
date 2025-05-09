from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .models import BillsTable


def home(request: HttpRequest) -> HttpResponse:
    """
    Render the home page.

    Args:
        request (HttpRequest): An HTTP request object:

    Returns:
        HttpResponse: The rendered home page.
    """
    return render(request, "home.html")


def search(request: HttpRequest) -> HttpResponse:
    """
    Handle search requests.

    Args:
        request (HttpRequest): An HTTP request object.

    Returns:
        HttpResponse: The rendered search results page.
        Results: Search results returned by the database.
            This is an object containing the following fields, corresponding
            to the columns in the database's bills table:
                bill_id: The unique identifier for the bill
                number: The bill number
                title: The bill title
                summary: The bill summary
                status: The bill status
                topics: TO BE IMPLEMENTED
                favorite: TO BE IMPLEMENTED
    """
    query = request.GET.get("query", "")

    results = []

    if query:
        search_vector = SearchVector("title", "summary", config="english")
        search_query = SearchQuery(query, search_type="websearch", config="english")
        results = (
            BillsTable.objects.annotate(search=search_vector)
            .filter(search=search_query)
            .annotate(rank=SearchRank(search_vector, search_query))
            .order_by("-rank")
        )

    return render(
        request,
        "search.html",
        {"query": request.GET.get("query", ""), "results": results},
    )
