from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .models import BillsMock


def home(request):
    """
    Render the home page.
    """
    return render(request, "home.html")

def search(request):
    """
    Handle search requests.
    """
    query = request.GET.get("query", "")

    results = []

    if query:
        search_vector = SearchVector("title", "summary", config="english")
        search_query = SearchQuery(query, search_type="websearch", config="english")
        results = BillsMock.objects.annotate(search=search_vector)\
            .filter(search=search_query)\
                .annotate(rank=SearchRank(search_vector, search_query))\
                    .order_by("-rank")
    

    return render(request, "search.html", {"query": request.GET.get("query", ""), "results": results})