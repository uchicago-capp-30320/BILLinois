# Authorization Endpoints

## /accounts/signup/

<!-- ::: apps.accounts.views.make_account_page -->

::: apps.accounts.views.CustomUserManager.create_user

## /accounts/confirm-email/

Parameters:

- code: `str` a confirmation code sent to the user's email to confirm signup

Response: HTML confirmation page

## /accounts/login/

Parameters:

- email: `str`
- remember_me: `bool`

Response: HTML login page, redirect to confirmation page, failure message upon failed login.

## /accounts/login/code/confirm/

Parameters:

- code: `str`

Response: Redirect to home page `/` after successful confirmation, failure message upon failed confirmation.

## /accounts/logout

Parameters:

Response: Redirect to home page `/` after successful logout.

## /accounts/password/reset/

Parameters:

- email: `str`

Response: HTML password reset page, sends an email to the user upon form submit.

## /accounts/delete_account

::: apps.accounts.views.delete_account

## /accounts/account_goodbye

::: apps.accounts.views.account_goodbye

## /accounts/unsubscribe/

::: apps.accounts.views.unsubscribe
