# Getting Set Up With Django

## Create an env file to put Django in debug mode
In the parent directory of the django project, create a .env file. Make sure that it gets picked up by .gitignore!

Contact the backend team for the text of this .env file, which includes database authentication credentials.

You'll see that what they give you contains this line:

```
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```
When we're ready to launch our production-level product, we will turn DEBUG off. This is for development purposes.

When Django starts, it checks for an .env file and sets its configuration based on the variables set in the .env file. 

## Create the _logs folder

You will also need to create an empty _logs folder, and a flat file within that:

```
mkdir _logs
touch _logs/flat.log
```

## Launch Django:
Once you have saved your .env file and created the logs folder, you should be able to launch Django with:

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