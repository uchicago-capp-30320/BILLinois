# Core App Endpoints

## /

::: apps.core.views.home

## /search?query='{query}'&state='{state}'

::: apps.core.views.search

## /bill/{bill_number}

::: apps.core.views.bill_page

## /favorites/

<!-- ::: apps.core.views.favorites -->

A list of favorited bills for the logged in user.

Parameters:

- None

Response:

- HTML for favorited bills if the user is logged in, otherwise a message directing the user to log in at the `/login/` end point

- An array of JSON objects from the Postgres database, containing bill information about favorited bills:

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
  }
]
```

## /privacy_policy/

::: apps.core.views.privacy_policy
