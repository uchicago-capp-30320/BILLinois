# Launching Django

## Create an env file to put Django in debug mode
In the parent directory of the django project, create a .env file. Make sure that it gets picked up by .gitignore!

In the .env file, put the following:

```
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

When Django starts, it checks for an .env file and sets its configuration based on the variables set in the .env file. 

When we're ready to launch our production-level product, we will turn DEBUG off. This is for development purposes.

## Launch Django:
`uv run python manage.py runserver`

You should get a message that says something like this:

```
Performing system checks...

System check identified no issues (0 silenced).
April 25, 2025 - 22:01:41
Django version 5.2, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

If you put in http://127.0.0.1:8000/, or the location the message on your terminal gives you into your web browser, you will be able to access the site.