import re

from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.paginator import Paginator
from django.http import Http404, HttpRequest, HttpResponse
from .models import BillsTable
from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404, redirect, render

from .models import FavoritesTable


def home(request: HttpRequest) -> HttpResponse:
    """
    Render the home page.

    Args:
        request (HttpRequest): An HTTP request object:

    Returns:
        HttpResponse:
            The rendered HTML home page, redirect to `/search/` page
            upon search submission.
    """
    return render(request, "home.html")


def search(request: HttpRequest) -> HttpResponse:
    """
    Handle search requests.

    Args:
        request (HttpRequest): An HTTP request object.

    Returns:
        HttpResponse: The rendered search results page listing all bills matching a search query.
        Results:
            An array of JSON objects from the Postgres database, containing
            bill information about searched bills.
            The fields correspond to the columns in the database's bills table:

            - bill_id: The unique identifier for the bill<br />
            - number: The bill number\n
            - title: The bill title
            - summary: The bill summary
            - status: The bill status
            - topics: TO BE IMPLEMENTED
            - favorite: TO BE IMPLEMENTED

    Example:

    `http://127.0.0.1:8000/search/?query=environment`

    ```json
    [{
        "bill_id": '123',
        "number": "HB-001",
        "title": "Test Bill",
        "summary": "Tests a bill.",
        "status": "Submitted",
        "topics": ['Environment', 'Education'],
        "sponsors": ['Rep. Patel', 'Rep. Wilks']
    }]
    ```
    """
    query = request.GET.get("query", "")
    state = request.GET.get("state", None)
    # topic = request.GET.get("topic", None)

    results = []

    bill_number_pattern = r'^(HB|HR|SJR|HJR|HJRCA|SR|SJRCA|SB|AM|EO|JSR)\s*\d+'

    # If the user has searched by bill number, only search the number field
    # This is to avoid returning unrelated results for bill numbers
    if re.fullmatch(bill_number_pattern, query.strip().upper()):
        search_vector = SearchVector("number", config="english")
        search_query = SearchQuery(query, config="english")
        results = BillsTable.objects.annotate(search=search_vector).filter(search=search_query)

    else:
        search_vector = SearchVector("title", "summary", "number", config="english")
        search_query = SearchQuery(query, config="english")
        results = BillsTable.objects.annotate(search=search_vector).filter(search=search_query)
        results = results.annotate(rank=SearchRank(search_vector, search_query)).order_by("-rank")

    if state:
        results = results.filter(state=state)    

    if request.user.is_authenticated:
        user_id = request.user.id

        favorites_query = FavoritesTable.objects.filter(
            user_id=user_id, bill_id=OuterRef("bill_id")
        )

        results = results.annotate(favorite=Exists(favorites_query))

    # Paginate the results to avoid overwhelming the frontend
    paginator = Paginator(results, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "search.html",
        {
            "query": query,
            "results": page_obj,
        },
    )


@login_required
def toggle_favorite(request, bill_id):
    """
    Toggle a bill as favorite for the logged-in user via a form submission.
    """
    if request.method == "POST":
        # Django expects an object to be passed to a ForeignKey field, not a string
        user = request.user
        bill = get_object_or_404(BillsTable, bill_id=bill_id)

        # Use get_or_create with the related objects
        favorite, created = FavoritesTable.objects.get_or_create(user_id=user, bill_id=bill)

        if not created:
            favorite.delete()

    return redirect(request.META.get("HTTP_REFERER", "search"))


def bill_page(request: HttpRequest, bill_number: str) -> HttpResponse:
    """
    Return data from a single bill, including the status, sponsors, name and tagged topic

    Args:
        request (HttpRequest): An HTTP request object.
        bill_number (str):
            The `bill_id` from the Postgres bills model for the bill you want to view
            (i.e. SB 2253)

    Returns:
        HttpResponse: A Django context variable with the data from the query.
        Renders HTML bill page if bill exists, otherwise, an error
        Results: A JSON object containing the following columns from database's table:

            - bill_id: The unique identifier for the bill
            number: The bill number
            - title: The bill title
            summary: The bill summary
            - status: The bill status
                - includes: current and all previous statuses
                    - dates: date of change of status
                    - description: a description of the change of status
            - topics: A tagged topic from the summary
            - sponsors: any registered sponsor for the bill
                - includes: name of sponsor
                    - party: the political party they represent
                    position: their role in the legislature
                    - sponsor_id: unique number for sponsor

    Example:
    ```json
    {
        "bill_id": '123',
        "number": "HB-001",
        "title": "Test Bill",
        "summary": "Tests a bill.",
        "status": "Submitted",
        "topics": ['Environment', 'Education'],
        "sponsors": ['Rep. Patel', 'Rep. Wilks']
    }
    ```
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

    return render(request, "bill_page.html", {"bill_data": data})
