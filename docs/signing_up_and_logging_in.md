# Signing Up and Logging In

## To start the server:
`uv run python manage.py runserver`

## Currently In Progress:
We are currently awaiting our Twilio campaign to be approved in order to send text messages without running into spam filters.
In the meantime, authentication codes for phone authorization will be sent to `_logs/phone_verification.log`

## Signing Up
To sign up, you will need to provide three things:

* Email Address
* Phone Number
* Password

After entering this, you will be instructed to authorize the phone number. Enter the authorization code sent to your phone, or to `_logs/phone_verification.log`.

You will then be instructed to authorize your email address. Enter the authorization code sent to your email address. If you can't find it, check your spam folder.

## Logging In
BILLinois uses two-factor authentication. After entering your username and password, you will be instructed to enter a verification code sent to your phone, or to `_logs/phone_verification.log`.