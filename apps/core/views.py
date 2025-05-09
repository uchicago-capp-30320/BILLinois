from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from .models import BillsMockDjango, BillsTable
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


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


def bill_page(request: HttpRequest, bill_number: str) -> HttpResponse:
    """
    Return data from bill, including the status, sponsors, name and tagged topic

    Args:
        request (HttpRequest): An HTTP request object.
        bill_number (str): The number of the bill you want to view (i.e. SB 2253)

    Returns:
    HttpResponse: A Django context variable with the data from the query.
    Results: contains the following columns from database's table:
            bill_id: The unique identifier for the bill
            number: The bill number
            title: The bill title
            summary: The bill summary
            status: The bill status
                includes: current and all previous statuses
                          dates: date of change of status
                          description: a description of the change of status
            topics: A tagged topic from the summary
            sponsors: any registered sponsor for the bill
                includes: name of sponsor
                          party: the political party they represent
                          position: their role in the legislature
                          sponsor_id: unique number for sponsor
    """
    try:
        bill = BillsTable.objects.get(number=bill_number)
    except BillsTable.DoesNotExist as err:
        raise Http404("Bill not found.") from err

    data = {
        "bill_id": bill.bill_id,
        "number": bill.number,
        "title": bill.title,
        "summary": bill.summary,
        "sponsors": [
            {
                "sponsor_id": s.sponsor_id,
                "sponsor_name": s.sponsor_name,
                "party": s.party,
                "position": s.position,
            }
            for s in bill.sponsorstable_set.exclude(sponsor_id=None)
        ],
        "topics": [{"topic": t.topic} for t in bill.topicstable_set.all()],
        "status": [
            {
                "date": a.date.isoformat(),
                "status": a.category,
                "status_desc": a.description,
            }
            for a in bill.actionstable_set.exclude(category=None).order_by("date")
        ],
    }

    return render(request, "bill.html", {"bill_data": data})
