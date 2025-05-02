# Authorization Endpoints

## /signup/

Parameters:

* username: `str`
* email: `str`
* password: `str`
* phone number: `str`

Response: HTML sign-up page, success message upon successful registration, failure message upon failed registration

## /login/

Parameters: 

* username: `str`
* password: `str`

Response: HTML login page, redirect to home page `/` upon successful login, failure message upon failed login.