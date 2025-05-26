import re

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Exists, OuterRef, Subquery
from django.contrib.postgres.aggregates import ArrayAgg
from django.http import Http404, HttpRequest, HttpResponse
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from .models import ActionsTable, BillsTable, FavoritesTable
from .utils import bill_number_for_url, normalize_bill_number
from .states import STATES


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
    return render(request, "home.html", {"states": STATES})


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

    bill_number_pattern = r"^(HB|HR|SJR|HJR|HJRCA|SR|SJRCA|SB|AM|EO|JSR)\s*\d+"

    # If the user has searched by bill number, only search the number field
    # This is to avoid returning unrelated results for bill numbers
    if re.fullmatch(bill_number_pattern, query.strip().upper()):
        search_vector = SearchVector("number", config="english")

    else:
        search_vector = SearchVector("title", "summary", "number", config="english")

    search_query = SearchQuery(query, config="english")
    results = BillsTable.objects.annotate(search=search_vector).filter(search=search_query)

    if state:
        results = results.filter(state=state)

    results = results.annotate(rank=SearchRank(search_vector, search_query)).order_by("-rank")
    results = results.annotate(topics=ArrayAgg("topicstable__topic", distinct=True))

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
        {"query": query, "results": page_obj, "states": STATES, "state": state},
    )


@login_required
def toggle_favorite(request, bill_id):
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
    Return detailed bill data using either the bill ID or a combination of
        state, year, and bill number.


    Args:
        request (HttpRequest): An HTTP request object.
        bill_id (str): The unique identifier for the bill
                (e.g., ocd-bill/12bcc69d-cfa4-4021-974a-5f562297ea34).
        state (str): The U.S. state abbreviation or name
                (e.g., 'il' for Illinois).
        year (str): The legislative session year
                (e.g., '2025').
        bill_number (str): The official bill number
                (e.g., 'HB1234').

        At least one of the following must be provided:
        - `bill_id`, or
        - All of: `state`, `year`, and `bill_number`.

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
            raise Http404("Bill not found with given state/year/number.") from err
    else:
        raise Http404("Insufficient information to find bill.")

    if request.user.is_authenticated:
        user_id = request.user.id

        favorites_query = FavoritesTable.objects.filter(
            user_id=user_id, bill_id=bill.bill_id
        )

        bill.favorite = favorites_query.exists()
    else:
        bill.favorite = False

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
                "date": a.date,
                "status": a.category,
                "status_desc": a.description,
            }
            for a in bill.actionstable_set.exclude(category=None).order_by("date")
        ],
        "favorite": bill.favorite
    }

    return render(request, "bill_page.html", {"bill_data": data,
                                              "states": STATES,
                                              "state": state})


@login_required
def favorites_page(request):
    """
    Return a list of bills favorited by the current user, with optional sorting.

    If "?sort=action_date" GET parameter is provided the favorited bills will be sorted
    by the most recent relevant (has a non null category) action taken on each bill.
    Otherwise, the list is sorted by favorite_id (order user favorited each bill).

    Args:
        request (HttpRequest): The HTTP request object containing user
                               optional GET parameters (with ?sort=action_date).

    Returns:
        HttpResponse: A Django context variable with the data from the query.
            - favorited_bills (QuerySet): Bills favorited by the user.
            - sort_option (str): The current sort option in use ("action_date" or "favorite_date").
    """
    user_id = request.user.id
    sort_option = request.GET.get("sort", "favorited")  # default sort

    # queryset of bills the user favorited
    favorite_qs = FavoritesTable.objects.filter(user_id=user_id)
    favorite_bill_ids = favorite_qs.values("bill_id")

    bills_qs = BillsTable.objects.filter(bill_id__in=Subquery(favorite_bill_ids))

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
