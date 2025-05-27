import re

from django.contrib.auth.decorators import login_required
from django.contrib.postgres.aggregates import ArrayAgg
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.paginator import Paginator
from django.db.models import Exists, OuterRef, Subquery, Value, BooleanField
from django.contrib.postgres.aggregates import ArrayAgg
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from .models import ActionsTable, BillsTable, FavoritesTable
from .utils import bill_number_for_url, normalize_bill_number
from .states import STATES, STATE_NAME_TO_ABBR, STATE_LINKS


def home(request: HttpRequest) -> HttpResponse:
    """
    Render the home page.

    Args:
        request (HttpRequest): An HTTP request object.

    Returns:
        HttpResponse:
            The rendered HTML home page, redirect to `/search/` page
            upon search submission.
    """
    return render(request, "home.html", {"states": STATES})


def search(request: HttpRequest) -> HttpResponse:
    """
    Handle search requests. Includes options for:
        search on keyword
        search on topic
        search for keywords on a specified topic

    Args:
        request (HttpRequest): 
            An HTTP request object containing GET parameters:

            - query (str): Search query string.
            - state (str): 
                State abbreviation (e.g., 'il' for Illinois) for the state in which legislation was introduced.

    Returns:
        HttpResponse: The rendered search results page listing all bills matching a search query.
        Results:
            An array of JSON objects from the Postgres database, containing
            bill information about searched bills.
            The fields correspond to the columns in the database's bills table:

            - bill_id: The unique identifier for the bill
            - number: The bill number
            - title: The bill title
            - summary: The bill summary
            - status: The bill status
            - topics: TO BE IMPLEMENTED
            - favorite: TO BE IMPLEMENTED

    Example:

    `http://billinois.unnamed.computer/search/?query=environment`

    ```json
    [
        {
            "bill_id": '123',
            "number": "HB-001",
            "title": "Test Bill",
            "summary": "Tests a bill.",
            "status": "Submitted",
            "topics": ['Environment', 'Education'],
            "sponsors": ['Rep. Patel', 'Rep. Wilks']
        },
        ...
    ]
    ```
    """

    query = request.GET.get("query", "")
    topic = request.GET.get("topic", None)
    state = request.GET.get("state", None)
    session = request.GET.get("session", None)

    results = BillsTable.objects

    # when topic provided we start by filtering results on it
    if topic:
        results = results.filter(topicstable__topic__iexact=topic)

    # likewise with state and session
    if state:
        results = results.filter(state__iexact=state)

    if session:
        results = results.filter(session__iexact=session)

    # if query provided we look for keyword on filtered (if topic) or unfiltered table
    if query:
        bill_number_pattern = r"^(HB|HR|SJR|HJR|HJRCA|SR|SJRCA|SB|AM|EO|JSR)\s*\d+"
        
        # If the user has searched by bill number, only search the number field
        # This is to avoid returning unrelated results for bill numbers
        if re.fullmatch(bill_number_pattern, query.upper()):
            search_vector = SearchVector("number", config="english")
        else:
            search_vector = SearchVector("title", "summary", "number", config="english")

        search_query = SearchQuery(query, config="english")
        results = results.annotate(search=search_vector).filter(search=search_query)
        results = results.annotate(rank=SearchRank(search_vector, search_query)).order_by("-rank")

    results = results.annotate(topics=ArrayAgg("topicstable__topic", distinct=True))

    # include "favorited" status if the user is logged in
    if request.user.is_authenticated:
        user_id = request.user.id
        favorites_query = FavoritesTable.objects.filter(
            user_id=user_id, bill_id=OuterRef("bill_id")
        )
        results = results.annotate(favorite=Exists(favorites_query))

    # Paginate the results
    paginator = Paginator(results, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "search.html",
        {"query": query, "results": page_obj, "states": STATES, "state": state},
    )


@login_required
def toggle_favorite(request, bill_id):
    """
    Toggle the favorite status of a bill for the current user. If the bill is already favorited, it will be removed from favorites.

    Args:
        request (HttpRequest): An HTTP request object.
        bill_id (str): The unique identifier for the bill (e.g., ocd-bill/12bcc69d-cfa4-4021-974a-5f562297ea34).

    Returns:
        HttpResponse: Rendered partial template containing the updated favorite button HTML.
    """

    if request.method == "POST":
        # Django expects an object to be passed to a ForeignKey field, not a string
        user = request.user
        bill = get_object_or_404(BillsTable, bill_id=bill_id)

        # Use get_or_create with the related objects
        favorite, created = FavoritesTable.objects.get_or_create(user_id=user, bill_id=bill)
        if not created:
            favorite.delete()
            is_favorite = False
        else:
            is_favorite = True

        # Render the partial template of updated button HTML
        button_html = render_to_string(
            "partials/favorite_button.html",
            {"bill": bill, "is_favorite": is_favorite},
            request=request,
        )

        return HttpResponse(button_html)

    else:
        raise Http404("Unable to update favorites.")


def bill_page(
    request: HttpRequest,
    bill_id: str = None,
    state: str = None,
    session: str = None,
    bill_number: str = None,
) -> HttpResponse:
    """
    Return detailed bill data. At least one of the following must be provided:
    
    - `bill_id`, or
    - All of: `state`, `session`, and `bill_number`.

    Args:
        request (HttpRequest): An HTTP request object.
        bill_id (str): The unique identifier for the bill.
        state (str): The name of the U.S. state where the bill was introduced.
        session (str): The legislative session.
        bill_number (str): The assigned bill number.


    Returns:
        HttpResponse: A Django context variable with the data from the query.
        Results: Contains the following columns from database's table:

            - bill_id: The unique identifier for the bill.
            - number: The bill number assigned by the legislative chamber where it was introduced.
            - title: The bill title.
            - summary: The bill summary.
            - status: The bill status, including current and all previous statuses.
                - dates: Date of the change of status.
                - description: Description of the change of status.
            - topics: Pre-determined topics extracted from the summary using keyword match.
            sponsors: Any registered sponsor for the bill.
                - sponsor_id: unique identification number for sponsor
                - party: the political party the sponsor represents
                - position: sponsor's role in the legislature

    Example:

    `http://billinois.unnamed.computer/bill/illinois/104th/hb3657/`
    `http://billinois.unnamed.computer/bill/ocd-bill/12bcc69d-cfa4-4021-974a-5f562297ea34`

    ```json
    [
        {
            "bill_id": '123',
            "number": "HB-001",
            "title": "Test Bill",
            "summary": "Tests a bill.",
            "status": "Submitted",
            "topics": ['Environment', 'Education'],
            "sponsors": ['Rep. Patel', 'Rep. Wilks']
        },
        ...
    ]
    ```
    """
    if bill_id:
        try:
            bill = BillsTable.objects.get(bill_id=bill_id)
        except BillsTable.DoesNotExist as err:
            raise Http404("Bill not found with given ID.") from err

        url_bill_number = bill_number_for_url(bill.number)
        return redirect(
            "bill_by_info",
            state=bill.state.lower(),
            session=bill.session,
            bill_number=url_bill_number,
        )

    elif state and session and bill_number:
        try:
            normalized_number = normalize_bill_number(bill_number)
            bill = BillsTable.objects.get(
                state=state.capitalize(),
                session=session,
                number=normalized_number,
            )
        except BillsTable.DoesNotExist as err:
            raise Http404("Bill not found with given state/session/number.") from err
    else:
        raise Http404("Insufficient information to find bill.")

    data = {
        "bill_id": bill.bill_id,
        "number": bill.number,
        "title": bill.title,
        "summary": bill.summary,
        "state": bill.state,
        "state_abbr": STATE_NAME_TO_ABBR[bill.state],
        "state_link": STATE_LINKS[bill.state],
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
                "date": a.date,
                "status": a.category,
                "status_desc": a.description,
            }
            for a in bill.actionstable_set.exclude(category=None).order_by("date")
        ],
    }

    return render(request, "bill_page.html", {"bill_data": data, "states": STATES})


@login_required
def favorites_page(request):
    """
    Return a list of bills favorited by the current user, with optional sorting.

    If "?sort=action_date" GET parameter is provided the favorited bills will be sorted
    by the most recent relevant (has a non-null `category`) action taken on each bill.
    Otherwise, the list is sorted by `favorite_id` (order in which user favorited each bill).

    Args:
        request (HttpRequest): The HTTP request object containing user-optional GET parameters:

            - sort (str): "action_date" or "favorite_id". Defaults to "favorite_id".

    Returns:
        HttpResponse: A Django context variable with the data from the query. If the user is not logged in, redirect to the `/login/` endpoint.
        
            - favorited_bills (QuerySet): Bills favorited by the user.
            - sort_option (str): The current sort option in use ("action_date" or "favorite_id").

    An array of JSON objects from the Postgres database, containing bill information about favorited bills:

    ```json
    [
        {
            "bill_id": "123",
            "number": "HB-001",
            "title": "Test Bill",
            "summary": "Tests a bill.",
            "status": "Submitted",
            "topics": ["Environment", "Education"],
            "sponsors": ["Rep. Patel", "Rep. Wilks"]
        },
        ...
    ]
    ```
    """

    user_id = request.user.id
    sort_option = request.GET.get("sort", "favorited")  # default sort

    # queryset of bills the user favorited
    favorite_qs = FavoritesTable.objects.filter(user_id=user_id)
    favorite_bill_ids = favorite_qs.values("bill_id")

    bills_qs = BillsTable.objects.filter(bill_id__in=Subquery(favorite_bill_ids)).prefetch_related(
        "topicstable_set"
    )

    # Annote bills with a favorite status = true for use with htmx
    bills_qs = bills_qs.annotate(favorite=Value(True, output_field=BooleanField()))

    if sort_option == "action_date":
        # get most recent relevant action (i.e. with a category) for bills
        latest_action_date = (
            ActionsTable.objects.filter(bill_id=OuterRef("bill_id"))
            .exclude(category=None)
            .order_by("-date")
            .values("date")[:1]
        )

        # sort bills by latest categorized action date
        bills_qs = bills_qs.annotate(latest_action=Subquery(latest_action_date)).order_by(
            "-latest_action"
        )
    else:
        # sort by when user favorited
        bills_qs = bills_qs.annotate(
            favorite_id=Subquery(favorite_qs.filter(bill_id=OuterRef("bill_id")).values("id")[:1])
        ).order_by("-favorite_id")

    return render(
        request,
        "favorites.html",
        {"favorited_bills": bills_qs, "sort_option": sort_option},
    )


def privacy_policy(request: HttpRequest) -> HttpResponse:
    """
    Render the privacy policy page.

    Args:
        request (HttpRequest): An HTTP request object.
    Returns:
        HttpResponse: The rendered HTML privacy policy page.
    """
    return render(request, "privacy_policy.html")
