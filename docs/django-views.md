# Django Views

## Overview
`apps/core/views.py` is the file containing the Django views for our app.

Django views are the functions in Django that render the webpages, as well as access and transform the data in the database.

## How to Use this Doc
Whenever a Django view is created or updated, the documentation for that view should be updated in this doc. 

## Current Views and Functions:

### Home: `/`
Renders `templates/home.html` at the default endpoint – `""`

### Search: `/search/`
Search does two things:

1. Renders `templates/search.html` at the `/search/` endpoint.
2. Handles search requests from search form submissions. Queries the database, and then returns the `results` object.

#### The Results Array:
Search results returned by the database. 

Results is an array, containing objects with the following fields, corresponding to the columns in the database's bills table:

`bill_id`: The unique identifier for the bill
`number`: The bill number
`title`: The bill title
`summary`: The bill summary
`status`: The bill status
`topics`: TO BE IMPLEMENTED
`favorite`: If the bill has been favorited by the user

### Favorites: `toggle_favorite/<path:bill_id>/`
Hitting this endpoint with a `POST` request will trigger a toggle function that either creates a favorite for a user in the favorites table, or deletes that favorite if the user has already favorited the bill.
