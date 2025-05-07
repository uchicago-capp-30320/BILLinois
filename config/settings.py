import sys
from pathlib import Path

import environ
import structlog


# Preamble -----
#
# This sets some global variables & reads in a `.env` file if present.
#
# Do not modify this section.

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
    DEBUG=(bool, False),
)


env.read_env(BASE_DIR / ".env")

# Environment Variable-Controlled Settings ------
#
# DEBUG is read first, and if DEBUG is true
# then certain settings (below) have defaults.
#
# It is recommended you do not change this block,
# instead opting to interact with these settings via the
# environ variables.
#
# The default settings in DEBUG are suitable for production
#  (a local SQLite DB, unsafe secret key, and console logged email)
# but in production all of these should be made explicit.
DEBUG = env.bool("DEBUG", False)

if DEBUG:
    SECRET_KEY = env.str("SECRET_KEY", "needs-to-be-set-in-prod")
    _DEFAULT_DB = env.db(default="sqlite:///" + str(BASE_DIR / "db.sqlite3"))
    EMAIL_CONFIG = env.email(default="consolemail://")
else:
    SECRET_KEY = env.str("SECRET_KEY")
    _DEFAULT_DB = env.db()
    EMAIL_CONFIG = env.email()
DATABASES = {"default": _DEFAULT_DB}
vars().update(EMAIL_CONFIG)


ALLOWED_HOSTS = []
INTERNAL_IPS = ["127.0.0.1"]

# Debug Toolbar
IS_TESTING = "test" in sys.argv or "pytest" in sys.argv


# Static Settings ------
#
# Settings below this point can be modified directly within the file.
# or, at your option, configured using `env`.

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "allauth",
    "allauth.account",
    # Uncomment for MFA/Webauthn
    # "allauth.mfa",
    "django_structlog",
    "django_typer",
    "apps.accounts",
    "apps.core",
    "django.contrib.postgres",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_structlog.middlewares.RequestMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

# Debug Toolbar needs to be configured after INSTALLED_APPS
#  recommend leaving this here.
if DEBUG and not IS_TESTING:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE.insert(
        2,
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    )

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
WSGI_APPLICATION = "config.wsgi.application"
ROOT_URLCONF = "config.urls"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Authentication -----

AUTH_USER_MODEL = "accounts.User"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# DJOK_USER_TYPE is a setting we introduce to pick between
#   a few common auth patterns.
#
# It is also used in accounts/models.py.
#
# WARNING: Changing this setting after initial setup can have
#          data-loss consequences.
#
# See documentation for explanation of options.
DJOK_USER_TYPE = "email"
# DJOK_PASSWORD_PROMPTS determines how many password prompts are shown.
#  0 - Email/Token based login.
#  1 - Single password box.
#  2 - Password box with confirmation.
DJOK_PASSWORD_PROMPTS = 1

_PASSWORDS = {0: [], 1: ["password1*"], 2: ["password1*", "password2*"]}[DJOK_PASSWORD_PROMPTS]

ACCOUNT_EMAIL_UNKNOWN_ACCOUNTS = False
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_LOGIN_BY_CODE_ENABLED = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_SIGNUP_FORM_HONEYPOT_FIELD = "user_name"  # underscore is fake one
ACCOUNT_USERNAME_BLACKLIST = ["admin"]
ACCOUNT_ADAPTER = "apps.accounts.adapters.CustomAccountAdapter"
ACCOUNT_UNIQUE_IDENTIFIER = "email"
LOGIN_REDIRECT_URL = "/"
# ACCOUNT_SIGNUP_FORM_CLASS = ""
# ACCOUNT_EMAIL_SUBJECT_PREFIX = "[Site] "
# ACCOUNT_LOGIN_BY_CODE_REQUIRED = False
# ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"


ACCOUNT_FORMS = {'signup': 'apps.accounts.forms.CustomSignupForm'}

if DJOK_USER_TYPE in ("email", "email+username"):
    ACCOUNT_LOGIN_METHODS = {"email"}
    ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
    ACCOUNT_EMAIL_VERIFICATION = "mandatory"
    ACCOUNT_EMAIL_VERIFICATION_BY_CODE_ENABLED = True
    if DJOK_USER_TYPE == "email":
        ACCOUNT_USER_MODEL_USERNAME_FIELD = None
        ACCOUNT_SIGNUP_FIELDS = ["email*", "phone*"] + _PASSWORDS
    else:
        ACCOUNT_USER_MODEL_USERNAME_FIELD = "username"
        ACCOUNT_SIGNUP_FIELDS = ["email*", "username"] + _PASSWORDS

# Email settings
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"

ANYMAIL = {
    "MAILGUN_API_KEY": env.str("MAILGUN_API_KEY"),
    "MAILGUN_SENDER_DOMAIN": env.str("MAILGUN_SENDER_DOMAIN"),
}

DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL")


# Uncomment for Webauthnn
# MFA_SUPPORTED_TYPES = ["webauthn"]
# MFA_PASSKEY_LOGIN_ENABLED = True
# MFA_PASSKEY_SIGNUP_ENABLED = True
# if DEBUG:
#     MFA_WEBAUTHN_ALLOW_INSECURE_ORIGIN = True


# Logging Config ---------

# default to not capturing data we don't know we need (re-enable as needed)
DJANGO_STRUCTLOG_IP_LOGGING_ENABLED = False
DJANGO_STRUCTLOG_USER_ID_FIELD = None

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        },
        "plain_console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
        },
        "key_value": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.KeyValueRenderer(
                key_order=["timestamp", "level", "event", "logger"]
            ),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "plain_console",
        },
        "json_file": {
            "class": "logging.handlers.WatchedFileHandler",
            "filename": "_logs/log.json",
            "formatter": "json_formatter",
        },
        "flat_line_file": {
            "class": "logging.handlers.WatchedFileHandler",
            "filename": "_logs/flat.log",
            "formatter": "key_value",
        },
    },
    "loggers": {
        "django_structlog": {
            "handlers": ["console", "flat_line_file", "json_file"],
            "level": "INFO",
        },
        # Modify this to match the name of your application.
        # to configure different logging for your app vs. Django's
        # internals.
        # "YOUR_APP": {
        #    "handlers": ["console", "flat_line_file", "json_file"],
        #    "level": "INFO",
        # },
    },
}

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)


# Static File Config (per whitenoise) -----

# TODO: make configurable
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

STATIC_ROOT = BASE_DIR / "_staticfiles"
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
# this directory is served at project root (for favicon.ico/robots.txt/etc.)
WHITENOISE_ROOT = BASE_DIR / "static" / "root"
