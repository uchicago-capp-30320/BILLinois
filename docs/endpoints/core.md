# Core App Endpoints

## /

The home page.

Parameters:

* query: `str`

Response: HTML home page, redirect to `/search/` page upon search submission.

## /search?query='{query}'

A search page listing all bills matching a search query.

Parameters

* query: `str`

Response: 

* HTML search page

* An array of JSON objects from the Postgres database, containing bill information about searched bills:

  ```json
  [
  {"bill_id": '123', "number": "HB-001", "title": "Test Bill", "summary": "Tests a bill.", "status": "Submitted", "topics": ['Environment', 'Education'], "sponsors": ['Rep. Patel', 'Rep. Wilks']}
  ]
  ```

* Results upon successful search query

Example:

`http://127.0.0.1:8000/search/?query=environment`

## /bill/{bill_id}

A detail page for a single bill.

Parameters:

* bill_id: `str`: The `bill_id` from the Postgres bills model.

Response: 

* HTML bill page if bill exists, otherwise, an error
* A JSON object containing bill information:

```json
{"bill_id": '123', "number": "HB-001", "title": "Test Bill", "summary": "Tests a bill.", "status": "Submitted", "topics": ['Environment', 'Education'], "sponsors": ['Rep. Patel', 'Rep. Wilks']}
```

## /favorites/

A list of favorited bills for the logged in user.

Parameters:

* None

Response: 

* HTML for favorited bills if the user is logged in, otherwise a message directing the user to log in at the `/login/` end point

* An array of JSON objects from the Postgres database, containing bill information about favorited bills:

  ```json
  [
  {"bill_id": '123', "number": "HB-001", "title": "Test Bill", "summary": "Tests a bill.", "status": "Submitted", "topics": ['Environment', 'Education'], "sponsors": ['Rep. Patel', 'Rep. Wilks']}
  ]
  ```